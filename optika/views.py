from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from optika.models import Product, Customer, Order, StockMovement, Purchase
from optika.paginations import CustomPagination
from optika.serializers import ProductPreviewSerializer, CustomerPreviewSerializer, ProductCreateSerializer, \
    ProductDetailSerializer, ProductUpdateSerializer, CustomerCreateSerializer, CustomerDetailSerializer, \
    CustomerUpdateSerializer, OrderPreviewSerializer, OrderCreateSerializer, OrderDetailingSerializer, \
    StockMovementPreviewSerializer, StockMovementDetailSerializer, PurchasePreviewSerializer, PurchaseCreateSerializer, \
    PurchaseDetailSerializer


@api_view(['GET', 'POST'])
def product_list_view(request):
    if request.method == 'GET':
        products = Product.objects.all().order_by('-updated_at')
        search = request.GET.get('search')

        if search:
            products = products.filter(name__icontains=search)

        paginator = CustomPagination()
        paginated_qs = paginator.paginate_queryset(products, request)

        serializer_output = ProductPreviewSerializer(paginated_qs, many=True)

        return paginator.get_paginated_response(serializer_output.data)

    if request.method == 'POST':
        # The transaction.atomic decorator is necessary because we have signals triggered during the creation of a
        # new product. The stock movement in the inventory module is also created as part of this process. Without
        # transaction.atomic, if the product is successfully created but the stock movement fails, data inconsistency
        # would occur. In other words, the transaction here encompasses the signals, even if they reside in a separate
        # module (inventory module). This means the inventory signals are still part of the same transaction initiated
        # in this service method. This behavior has been tested and verified... :p hehe.

        serializer_input = ProductCreateSerializer(data=request.data)

        if serializer_input.is_valid():
            instance = serializer_input.save(user=request.user)
            serializer_output = ProductPreviewSerializer(instance)

            return Response(serializer_output.data, status=status.HTTP_201_CREATED)

        return Response(serializer_input.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'GET':
        serializer_output = ProductDetailSerializer(product)
        return Response(serializer_output.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer_input = ProductUpdateSerializer(product, data=request.data)

        if serializer_input.is_valid():
            instance = serializer_input.save()
            serializer_output = ProductDetailSerializer(instance)

            return Response(serializer_output.data, status=status.HTTP_200_OK)

        return Response(serializer_input.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def customer_list_view(request):
    if request.method == 'GET':
        customers = Customer.objects.all().order_by('-updated_at')
        search = request.GET.get('search')

        if search:
            customers = customers.filter(name__contains=search)

        paginator = CustomPagination()
        paginate_qs = paginator.paginate_queryset(customers, request)

        serializer_output = CustomerPreviewSerializer(paginate_qs, many=True)

        return paginator.get_paginated_response(serializer_output.data)

    elif request.method == 'POST':
        serializer_input = CustomerCreateSerializer(data=request.data)

        if serializer_input.is_valid():
            instance = serializer_input.save(user=request.user)
            serializer_output = CustomerPreviewSerializer(instance)

            return Response(serializer_output.data, status=status.HTTP_201_CREATED)

        return Response(serializer_input.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def customer_detail_view(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == 'GET':
        serializer_output = CustomerDetailSerializer(customer)
        return Response(serializer_output.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer_input = CustomerUpdateSerializer(customer, data=request.data)

        if serializer_input.is_valid():
            instance = serializer_input.save()
            serializer_output = CustomerPreviewSerializer(instance)

            return Response(serializer_output.data, status=status.HTTP_200_OK)

        return Response(serializer_input.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def order_list_view(request):
    if request.method == 'GET':
        orders = Order.objects.all().order_by('-updated_at')
        search = request.GET.get('search')

        if search:
            orders = orders.filter(order_number__contains=search)

        paginator = CustomPagination()
        paginated_qs = paginator.paginate_queryset(orders, request)

        serializer_output = OrderPreviewSerializer(paginated_qs, many=True)

        return paginator.get_paginated_response(serializer_output.data)

    if request.method == 'POST':
        serializer_input = OrderCreateSerializer(data=request.data)

        if serializer_input.is_valid():
            instance = serializer_input.save(user=request.user)
            serializer_output = OrderDetailingSerializer(instance)

            return Response(serializer_output.data, status=status.HTTP_201_CREATED)

        return Response(serializer_input.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def order_detail_view(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    serializer_output = OrderDetailingSerializer(order)
    return Response(serializer_output.data, status=status.HTTP_200_OK)


# purchase

@api_view(['GET', 'POST'])
def purchase_list_view(request):
    if request.method == 'GET':
        purchases = Purchase.objects.all().order_by('-updated_at')
        search = request.GET.get('search')

        if search:
            orders = purchases.filter(order_number__contains=search)

        paginator = CustomPagination()
        paginated_qs = paginator.paginate_queryset(purchases, request)

        serializer_output = PurchasePreviewSerializer(paginated_qs, many=True)

        return paginator.get_paginated_response(serializer_output.data)

    if request.method == 'POST':
        serializer_input = PurchaseCreateSerializer(data=request.data)

        if serializer_input.is_valid():
            instance = serializer_input.save(user=request.user)
            serializer_output = PurchaseDetailSerializer(instance)

            return Response(serializer_output.data, status=status.HTTP_201_CREATED)

        return Response(serializer_input.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def purchase_detail_view(request, purchase_number):
    purchase = get_object_or_404(Order, purchase_number=purchase_number)

    serializer_output = PurchaseDetailSerializer(purchase)
    return Response(serializer_output.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def stock_movement_list_view(request):
    stock_movements = StockMovement.objects.all().order_by('-updated_at')
    search = request.GET.get('search')

    if search:
        stock_movements = stock_movements.filter(product__name__contains=search)

    paginator = CustomPagination()
    paginated_qs = paginator.paginate_queryset(stock_movements, request)

    serializer_output = StockMovementPreviewSerializer(paginated_qs, many=True)

    return paginator.get_paginated_response(serializer_output.data)


@api_view(['GET'])
def stock_movement_detail_view(request, pk):
    stock_movement = get_object_or_404(StockMovement, pk=pk)
    serializer_output = StockMovementDetailSerializer(stock_movement)
    return Response(serializer_output.data, status=status.HTTP_200_OK)

# #############################################################################

