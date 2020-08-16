from rest_framework.views import APIView
from rest_framework.response import Response
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



class OrderList(APIView):

    def get(self, response):
        orders = Order.objects.all()
        data = OrderSerializer(orders, many=True).data
        return Response(data)


order_list = OrderList.as_view()
