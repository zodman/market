from rest_framework import serializers

from .models import Food, Order, CartRow, Cart


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "cart", "status", "total", "user"]
        read_only_fields = ("cart", "total", "user")


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ["id", "name", "type", "price"]

class CustomRow(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)
    food = serializers.PrimaryKeyRelatedField(queryset=Food.objects.all())

