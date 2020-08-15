from django.contrib import admin
from .models import Cart, CartRow, Food, Order


class RowInline(admin.TabularInline):
    model = CartRow
    raw_id_fields = ("food",)


class CartAdmin(admin.ModelAdmin):
    inlines = [
       RowInline 
    ]


class FoodAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "price")

admin.site.register(Cart, CartAdmin)
admin.site.register(Food, FoodAdmin)
admin.site.register(Order)
