from rest_framework import generics
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from inertia.views import render_inertia
from inertia.share import share_flash
from .models import Food, Order, Cart, CartRow
from .serializers import FoodSerializer, OrderSerializer
from .serializers import CustomRow
from django.views.decorators.http import require_http_methods
from rest_framework.parsers import JSONParser



def index(request):
    foods = Food.objects.all()
    context = {"foods": FoodSerializer(foods, many=True).data}
    share_flash(request, "error", error=True)
    return render_inertia(request, "Index", context)

class CreateCart(APIView):
    def post(self, request, format=None):
        rows = CustomRow(data=request.data, many=True)
        if not rows.is_valid():
            return Response(rows.errors, status=status.HTTP_400_BAD_REQUEST) 
        else:
            cart = Cart.objects.create()
            for entry in rows.data:
                food = Food.objects.get(id=entry["food"])
                row = CartRow(food=food, cart=cart,

                        quantity=entry["quantity"])
                row.save()
            cart.order.update_total()
            cart.order.user = request.user
            cart.order.save()
            return Response(OrderSerializer(cart.order).data)

create_cart = CreateCart.as_view()

class OrderList(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        qs = Order.objects.all()
        status = self.request.query_params.get("status", None)
        if status:
            qs = qs.filter(status=status)
        user = self.request.query_params.get("user", False)
        if user is not False:
            qs = qs.filter(user__username=user)
        return qs


class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


# TODO: Delete order
# TODO: update order
order_detail = OrderDetail.as_view()
order_list = OrderList.as_view()
