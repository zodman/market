from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from inertia.views import render_inertia
from inertia.share import share_flash
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout as django_logout
from django.contrib.auth import login as django_login
from django.urls import reverse
from .models import Food, Order, Cart, CartRow
from .serializers import FoodSerializer, OrderSerializer
from .serializers import CustomRow
import json


def logout(request):
    django_logout(request)
    return redirect(reverse("market:login"))


def login(request):
    if request.user.is_authenticated:
        return redirect(reverse("market:index"))
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("email")
        password = data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            django_login(request, user)
            return redirect(reverse("market:index"))
        else:
            share_flash(request, error="username wrongly")
    return render_inertia(request, "Login")


@login_required
def index(request):
    foods = Food.objects.all()
    context = {
        "foods": FoodSerializer(foods, many=True).data,
        "user": request.user.username
    }
    return render_inertia(request, "Index", context)


class CreateCart(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        rows = CustomRow(data=request.data, many=True)
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
            msg = (f"Orden with id: {cart.order.id} was created with "
                   f"{cart.rows.count()} elements with total as "
                   f"{cart.order.total}")
            share_flash(request, msg)
        return redirect("market:index")


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
