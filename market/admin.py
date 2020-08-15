from django.contrib import admin
from .models import Cart, CartRow, Food, Order
from django.urls import reverse_lazy
from django.utils.html import format_html

from adminsortable.admin import NonSortableParentAdmin, SortableTabularInline


class RowInline(SortableTabularInline):
    model = CartRow
    raw_id_fields = ("food",)
    readonly_fields = ("price", "row_price")
    extra = 0

    def row_price(self, obj):
        return obj.quantity*obj.price
    row_price.short_description = "price"


class CartAdmin(NonSortableParentAdmin):
    inlines = [
       RowInline
    ]
    list_display = ("__str__", "get_order", "order_status")

    def get_order(self, obj):
        order = obj.order
        url = reverse_lazy("admin:market_order_change", args=(obj.order.id,))
        return format_html("<a href='{}'>{}</a>", url, order)
    get_order.short_description = "Order"

    def order_status(self, obj):
        status = dict(obj.order.STATUS)
        return status.get(obj.order.status)

class FoodAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "price")
    search_fields = ("name", "type")
    list_filter = ("type",)

class OrderAdmin(admin.ModelAdmin):
    list_display = ("__str__", "cart", "status", "user")
    list_filter = ("status",)
    list_select_related = ("cart", "user")

admin.site.register(Cart, CartAdmin)
admin.site.register(Food, FoodAdmin)
admin.site.register(Order, OrderAdmin)
