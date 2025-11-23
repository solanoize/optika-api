from django.contrib import admin

from optika.models import (
    Customer,
    Order,
    OrderItem,
    Purchase,
    PurchaseItem, Product
)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'stock', 'unit', 'price')
    search_fields = ('name',)
    list_filter = ('unit',)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone", "email", "user", "created_at")
    search_fields = ("name", "phone", "email")
    list_filter = ("user",)
    ordering = ("-created_at",)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 2
    autocomplete_fields = ["product"]
    fields = ["product", "quantity", "price", "subtotal"]

    class Media:
        js = ["js/order_item_autocalc.js"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]


class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    extra = 0
    fields = ("product", "quantity")


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = (
        "purchase_number",
        "date",
        "user",
        "created_at",
    )

    search_fields = ("purchase_number",)
    list_filter = ("date", "user")
    ordering = ("-date",)

    inlines = [PurchaseItemInline]

    readonly_fields = ("created_at", "updated_at")
