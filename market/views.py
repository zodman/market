from rest_framework import generics
from django.shortcuts import render
from inertia.views import render_inertia
from .models import Food, Order
from .serializers import FoodSerializer, OrderSerializer

def index(request):
    foods = Food.objects.all()
    context = {
        'foods': FoodSerializer(foods, many=True).data
    }
    return render_inertia(request, "Index", context)


class OrderList(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


order_list = OrderList.as_view()
