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


class OrderDetail(generics.RetrieveDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


# TODO: Delete order
# TODO: update order
order_detail = OrderDetail.as_view()
order_list = OrderList.as_view()



