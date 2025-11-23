from django.urls import path

from optika import views

app_name = 'optika'

urlpatterns = [
    path("products/", views.product_list_view, name='product_list_view'),
    path("products/<int:pk>/", views.product_detail_view, name='product_detail_view'),
    path("customers/", views.customer_list_view, name='customer_list_view'),
    path("customers/<int:pk>/", views.customer_detail_view, name='customer_detail_view'),
    path("orders/", views.order_list_view, name='order_list_view'),
    path("orders/<str:order_number>/", views.order_detail_view, name='order_detail_view'),
    path("purchases/", views.purchase_list_view, name='purchase_list_view'),
    path("purchases/<str:purchase_number>/", views.purchase_detail_view, name='purchase_detail_view'),
    path("stock-movements/", views.stock_movement_list_view, name='stock_movement_list_view'),
    path("stock-movements/<int:pk>/", views.stock_movement_detail_view, name='stock_movement_detail_view'),
]