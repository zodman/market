from rest_framework import serializers

from .models import Food, Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "cart", "status", "total", "user"]
        read_only_fields = ("cart", "total", "user")



class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ["id", "name", "type", "price"]
