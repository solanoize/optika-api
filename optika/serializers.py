from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers

from optika.models import Product, Customer, StockMovement, OrderItem, Order, StockAdjustment, PurchaseItem, Purchase
from optika.services import move_out_stock_by_order, initialize_stock_by_product, move_in_stock_by_purchasing


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UserPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_active']


class ProductPreviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)

    class Meta:
        model = Product
        fields = ['id', 'name', 'unit', 'stock', 'price', 'user', 'created_at', 'updated_at']


class ProductDetailSerializer(serializers.ModelSerializer):
    user = UserPreviewSerializer(many=False)

    class Meta:
        model = Product
        fields = ['id', 'name', 'unit', 'stock', 'price', 'user', 'created_at', 'updated_at']


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'unit', 'stock', 'price']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('Ensure this value is greater than to 0')

        return value

    def validate_stock(self, value):
        if value <= 0:
            raise serializers.ValidationError('Ensure this value is greater than to 0')

        return value

    def create(self, validated_data):
        product = super().create(validated_data)
        initialize_stock_by_product(product)

        return product


class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'unit', 'price']


class CustomerPreviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)

    class Meta:
        model = Customer
        fields = ['id', 'name', 'phone', 'email', 'address', 'user', 'created_at', 'updated_at']


class CustomerDetailSerializer(serializers.ModelSerializer):
    user = UserPreviewSerializer(many=False)

    class Meta:
        model = Customer
        fields = ['id', 'name', 'phone', 'email', 'address', 'user', 'created_at', 'updated_at']


class CustomerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'email', 'address']


class CustomerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'email', 'address']


class OrderItemCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price', 'subtotal']

    def validate(self, attrs):
        errors = {}

        product = attrs['product']
        quantity = attrs['quantity']
        price = attrs['price']
        subtotal = attrs['subtotal']

        # quantity
        if quantity <= 0:
            errors.setdefault('quantity', []).append(
                "Quantity must be greater than 0."
            )

        if product.stock < quantity:
            errors.setdefault('quantity', []).append(
                f"Quantity {quantity} larger than product stock {product.stock}."
            )

        # price
        if product.price != price:
            errors.setdefault('price', []).append(
                f"Invalid price {price}."
            )

        # subtotal
        if product.price * quantity != subtotal:
            errors.setdefault('subtotal', []).append(
                f"Invalid subtotal {subtotal}."
            )

        # kalau ada error, raise semuanya sekaligus
        if errors:
            raise serializers.ValidationError(errors)

        return attrs


class OrderItemPreviewSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price', 'subtotal', 'created_at', 'updated_at']


class OrderPreviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    customer = serializers.StringRelatedField(many=False)

    class Meta:
        model = Order
        fields = ['order_number', 'date', 'customer', 'total', 'paid_amount', 'change_amount', 'user', 'created_at',
                  'updated_at']


class OrderCreateSerializer(serializers.ModelSerializer):
    order_items = OrderItemCreateSerializer(many=True)

    class Meta:
        model = Order
        fields = ['order_number', 'date', 'customer', 'total', 'paid_amount', 'change_amount', 'order_items']

    def validate(self, attrs):
        errors = {}

        order_items = attrs['order_items']
        total = int(attrs['total'])
        paid_amount = int(attrs['paid_amount'])
        change_amount = int(attrs['change_amount'])

        if not order_items:
            errors.setdefault('order_items', []).append(
                f"Order items must be set."
            )

        # --- Cek duplicate product ---
        seen = set()
        for item in order_items:
            product = item['product']
            if product.id in seen:
                errors.setdefault('order_items', []).append(
                    f"Duplicate product: {product.name}"
                )
            else:
                seen.add(product.id)

        # --- Cek total ---
        calculated_total = sum(order_item['subtotal'] for order_item in order_items)
        if calculated_total != total:
            errors.setdefault('total', []).append(
                f"Invalid total {total}, should be {calculated_total}."
            )

        # --- Cek paid amount ---
        if paid_amount < total:
            errors.setdefault('paid_amount', []).append(
                f"Paid amount {paid_amount} is less than total {total}."
            )

        # --- Cek change amount ---
        calculated_change = paid_amount - total
        if calculated_change != change_amount:
            errors.setdefault('change_amount', []).append(
                f"Invalid change amount {change_amount}, should be {calculated_change}."
            )

        # Jika ada error, lempar semuanya
        if errors:
            raise serializers.ValidationError(errors)

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        order_items = validated_data.pop('order_items')
        order = Order.objects.create(**validated_data)

        items = [OrderItem(order=order, **item) for item in order_items]

        order_items = OrderItem.objects.bulk_create(items)

        move_out_stock_by_order(order, order_items)

        return order


class OrderDetailingSerializer(serializers.ModelSerializer):
    order_items = OrderItemPreviewSerializer(many=True, source='order_items_by_order')
    user = serializers.StringRelatedField(many=False, source='user.email')
    customer = CustomerPreviewSerializer(many=False)

    class Meta:
        model = Order
        fields = ['order_number', 'date', 'customer', 'total', 'paid_amount', 'change_amount', 'user', 'created_at',
                  'updated_at', 'order_items']


class PurchaseItemCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = PurchaseItem
        fields = ['product', 'quantity',]

    def validate(self, attrs):
        quantity = attrs['quantity']

        if quantity <= 0:
            raise serializers.ValidationError({"quantity": [f"Quantity {quantity} must be large then 0."]})

        return attrs


class PurchaseItemPreviewSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()

    class Meta:
        model = PurchaseItem
        fields = ['product', 'quantity', 'created_at', 'updated_at']


class PurchasePreviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)

    class Meta:
        model = Purchase
        fields = ['purchase_number', 'date', 'user', 'created_at', 'updated_at']


class PurchaseCreateSerializer(serializers.ModelSerializer):
    purchase_items = PurchaseItemCreateSerializer(many=True)

    class Meta:
        model = Purchase
        fields = ['purchase_number', 'date', 'purchase_items']

    def validate(self, attrs):
        purchase_items = attrs['purchase_items']

        if not purchase_items:
            raise serializers.ValidationError({"purchase_items": ["Purchase item is empty."]})

        seen = set()
        for item in purchase_items:
            product = item['product']
            if product.id in seen:
                raise serializers.ValidationError({"product": [f"Duplicate {product.name} product in purchase."]})
            seen.add(product.id)

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        purchase_items = validated_data.pop('purchase_items')
        purchase = Purchase.objects.create(**validated_data)

        items = [PurchaseItem(purchase=purchase, **item) for item in purchase_items]

        purchase_items = PurchaseItem.objects.bulk_create(items)

        move_in_stock_by_purchasing(purchase, purchase_items)

        return purchase


class PurchaseDetailSerializer(serializers.ModelSerializer):
    purchase_items = PurchaseItemPreviewSerializer(many=True, source='purchase_items_by_purchase')
    user = serializers.StringRelatedField(many=False, source='user.email')

    class Meta:
        model = Purchase
        fields = ['purchase_number', 'date', 'user', 'purchase_items', 'created_at', 'updated_at']


class StockMovementPreviewSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

    class Meta:
        model = StockMovement
        fields = ['id', 'product', 'movement_type', 'quantity', 'source_doc', 'note', 'date', 'user', 'created_at',
                  'updated_at']


class StockMovementDetailSerializer(serializers.ModelSerializer):
    product = ProductPreviewSerializer(many=False)
    user = UserPreviewSerializer(many=False)

    class Meta:
        model = StockMovement
        fields = ['id', 'product', 'movement_type', 'quantity', 'source_doc', 'note', 'date', 'user', 'created_at',
                  'updated_at']


class StockAdjustmentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockAdjustment
        fields = ['product', 'quantity_difference']


class StockAdjustmentDetailSerializer(serializers.ModelSerializer):
    product = ProductPreviewSerializer()
    user = UserPreviewSerializer()

    class Meta:
        model = StockAdjustment
        fields = ['product', 'quantity_difference']

    @transaction.atomic
    def create(self, validated_data):
        stock_adjustment = super().create(validated_data)

        # initialize_stock_by_product(product)
        return stock_adjustment

