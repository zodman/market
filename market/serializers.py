from rest_framework import serializers

from .models import Food, Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["cart","total", "user"]


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ["id", "name", "type", "price"]
