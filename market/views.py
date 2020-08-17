from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from inertia.views import render_inertia
from inertia.share import share_flash
from django.shortcuts import redirect
from .models import Food, Order, Cart, CartRow
from .serializers import FoodSerializer, OrderSerializer
from .serializers import CustomRow


def login(request):
    return render_inertia(request, "Login", {})


def index(request):
    foods = Food.objects.all()
    context = {
        "foods": FoodSerializer(foods, many=True).data
    }
    if request.user.is_authenticated:
        context["user"] = request.user.username
    return render_inertia(request, "Index", context)


class CreateCart(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        rows = CustomRow(data=request.data, many=True)
        if not request.user.is_authenticated:
            share_flash(request, error="User not auth")
            return redirect("market:index")
        if not rows.is_valid():
            share_flash(request, error=f"Failed to create and order")
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
            msg = (f"Orden with id: {cart.order.id} was created with"
                 f"{cart.rows.count()} elements with total as {cart.order.total}")
            share_flash(request, msg) 
        return redirect("market:index")
            #return Response(OrderSerializer(cart.order).data)


class OrderList(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', "cart__rows__name", "cart__rows__type"]

    def get_queryset(self):
        if self.request.user.is_superuser:
            qs = Order.objects.all()
        else:
            qs = Order.objects.filter(user=self.request.user)

        status_param = self.request.query_params.get("status", None)
        if status_param:
            qs = qs.filter(status=status_param)
        user = self.request.query_params.get("user", False)
        if user is not False:
            qs = qs.filter(user__username=user)
        return qs


class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)


create_cart = CreateCart.as_view()
order_detail = OrderDetail.as_view()
order_list = OrderList.as_view()
