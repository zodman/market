from django.contrib import admin
from .models import Cart, CartRow, Food, Order


class RowInline(admin.TabularInline):
    model = CartRow
    raw_id_fields = ("food",)
    readonly_fields = ("price", "row_price")

    def row_price(self, obj):
        return obj.quantity*obj.price
    row_price.short_description = "price"


class CartAdmin(admin.ModelAdmin):
    inlines = [
       RowInline
    ]


class FoodAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "price")


admin.site.register(Cart, CartAdmin)
admin.site.register(Food, FoodAdmin)
admin.site.register(Order)
