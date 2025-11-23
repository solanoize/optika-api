from django.db.models import Sum, Case, When, IntegerField, F
from django.utils import timezone

from optika.models import StockMovement, Product


def calculate_current_stock(product):
    queryset = StockMovement.objects.filter(product=product)

    aggregation = queryset.aggregate(
        stock=(
            Sum(
                Case(
                    When(movement_type=StockMovement.INIT, then='quantity'),
                    When(movement_type=StockMovement.IN, then='quantity'),
                    When(movement_type=StockMovement.OUT, then=-1 * F('quantity')),
                    When(movement_type=StockMovement.ADJUSTMENT, then='quantity'),
                    output_field=IntegerField()
                )
            )
        )
    )

    return aggregation['stock'] or 0


def initialize_stock_by_product(product):
    movement_type = StockMovement.INIT
    quantity = product.stock
    source_doc = 'Initial Stock'
    date = timezone.now()
    user = product.user
    note = f'Initial stock of product {product.name}'

    StockMovement.objects.create(product=product, movement_type=movement_type, quantity=quantity, source_doc=source_doc,
                                 date=date, note=note, user=user)


def move_out_stock_by_order(order, order_items):
    stock_movement_list = []
    products_to_update = []
    date = timezone.now()
    source_doc = order.order_number
    note = f'Order Number #{source_doc}'
    user = order.user
    movement_type = StockMovement.OUT

    for order_item in order_items:
        product = order_item.product
        quantity = order_item.quantity

        stock_movement_list.append(StockMovement(product=product, movement_type=movement_type, source_doc=source_doc,
                                                 date=date, note=note, user=user, quantity=quantity))

        product.stock = product.stock - quantity
        products_to_update.append(product)

    StockMovement.objects.bulk_create(stock_movement_list)
    Product.objects.bulk_update(products_to_update, ['stock'])


def move_in_stock_by_purchasing(purchase, purchase_items):
    stock_movement_list = []
    products_to_update = []
    date = timezone.now()
    source_doc = purchase.purchase_number
    note = f'Purchase Number #{source_doc}'
    user = purchase.user
    movement_type = StockMovement.IN

    for purchase_item in purchase_items:
        product = purchase_item.product
        quantity = purchase_item.quantity

        stock_movement_list.append(StockMovement(product=product, movement_type=movement_type, source_doc=source_doc,
                                                 date=date, note=note, user=user, quantity=quantity))

        product.stock = product.stock + quantity
        products_to_update.append(product)

    StockMovement.objects.bulk_create(stock_movement_list)
    Product.objects.bulk_update(products_to_update, ['stock'])


def create_stock_adjustment(product):
    pass


def create_stock_in_by(order_item):
    product = order_item.product
    movement_type = StockMovement.OUT
    quantity = order_item.quantity
    source_doc = order_item.order.order_number
    date = timezone.now()
    note = f'Order Number #{source_doc}'
    user = order_item.order.user

    stock_movement = StockMovement.objects.create(product=product, movement_type=movement_type, source_doc=source_doc,
                                                  date=date, note=note, user=user, quantity=quantity)

    product.stock = calculate_current_stock(product)
    product.save()

    return stock_movement



