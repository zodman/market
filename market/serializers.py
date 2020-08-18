from rest_framework import serializers
from .models import Food, Order, CartRow, Cart


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = "__all__"


class CartRowSerializer(serializers.ModelSerializer):
    food = FoodSerializer()

    class Meta:
        model = CartRow
        fields = ["id", "food", "quantity", "price"]


class CartSerializer(serializers.ModelSerializer):
    cart_rows = CartRowSerializer(many=True)

    class Meta:
        model = Cart
        fields = ["id", "cart_rows"]


class OrderSerializer(serializers.ModelSerializer):
    cart = CartSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ["id", "cart", "status", "total", "user"]
        read_only_fields = ("id", "cart", "total", "user")


class CustomRow(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)
    food = serializers.PrimaryKeyRelatedField(queryset=Food.objects.all())
