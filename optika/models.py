from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=200)
    unit = models.CharField(max_length=20)
    stock = models.PositiveIntegerField()
    price = models.PositiveIntegerField()

    user = models.ForeignKey(User, related_name='products_by_user', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} - {self.stock}'


class Customer(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=16)
    email = models.EmailField(max_length=100)
    address = models.TextField()

    user = models.ForeignKey(User, related_name='customers_by_user', on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    order_number = models.CharField(max_length=10, unique=True)
    date = models.DateField()
    customer = models.ForeignKey(Customer, related_name='orders_by_customer', on_delete=models.CASCADE)
    total = models.PositiveIntegerField()
    paid_amount = models.PositiveIntegerField()
    change_amount = models.PositiveIntegerField()

    user = models.ForeignKey(User, related_name='orders_by_user', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_number


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items_by_order', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items_by_product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.order.order_number} ({self.product.name})'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['order', 'product'],
                name='unique_order_item_order_product'
            )
        ]


class Purchase(models.Model):
    purchase_number = models.CharField(max_length=10, unique=True)
    date = models.DateField()

    user = models.ForeignKey(User, related_name='purchases_by_user', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.purchase_number


class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, related_name='purchase_items_by_order', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='purchase_items_by_product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.purchase.purchase_number} ({self.product.name})'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['purchase', 'product'],
                name='unique_purchase_item_purchase_product'
            )
        ]


class StockMovement(models.Model):
    INIT = 'INIT'
    IN = 'IN'
    OUT = 'OUT'
    ADJUSTMENT = 'ADJUSTMENT'

    MOVEMENT_CHOICES = (
        (INIT, 'Initial Stock'),
        (IN, 'Stock In'),
        (OUT, 'Stock Out'),
        (ADJUSTMENT, 'Stock Adjustment'),
    )

    product = models.ForeignKey(Product, related_name='stock_movements_by_product', on_delete=models.CASCADE)
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_CHOICES, default=IN)
    quantity = models.IntegerField()
    source_doc = models.CharField(max_length=100)
    note = models.TextField()
    date = models.DateTimeField()

    user = models.ForeignKey(User, related_name='stock_movements_by_user', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name


class StockAdjustment(models.Model):
    product = models.ForeignKey(Product, related_name='stock_adjustments_by_product', on_delete=models.CASCADE)
    quantity_difference = models.IntegerField()

    user = models.ForeignKey(User, related_name='stock_adjustments_by_user', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name