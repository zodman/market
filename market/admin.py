from django.contrib import admin
from .models import Cart, CartRow, Food, Order
from django.urls import reverse_lazy
from django.utils.html import format_html


class RowInline(admin.TabularInline):
    model = CartRow
    raw_id_fields = ("food",)
    readonly_fields = ("price", "row_price")
    extra = 1

    def row_price(self, obj):
        return obj.quantity*obj.price
    row_price.short_description = "price"


class CartAdmin(admin.ModelAdmin):
    inlines = [
       RowInline
    ]
    list_display = ("id", "get_order", "order_status")

    def get_order(self, obj):
        order = obj.order
        url = reverse_lazy("admin:market_order_change", args=(obj.order.id,))
        return format_html("<a href='{}'>{}</a>", url, order)
    get_order.short_description = "Order"
    get_order.admin_order_field = "order"

    def order_status(self, obj):
        status = dict(obj.order.STATUS)
        return status.get(obj.order.status)
    order_status.admin_order_field = "order__status"

class FoodAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "price")
    search_fields = ("name", "type")
    list_filter = ("type",)

class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "get_cart", "total", "status", "user")
    list_filter = ("status",)
    readonly_fields = ("total",)


    def get_cart(self, obj):
        url = reverse_lazy("admin:market_cart_change", args=(obj.cart.id,))
        return format_html("<a href='{}'>{}</a>", url, obj.cart)
    get_cart.short_description = "Cart"
    get_cart.admin_order_field = "cart__id"
 
admin.site.register(Cart, CartAdmin)
admin.site.register(Food, FoodAdmin)
admin.site.register(Order, OrderAdmin)
