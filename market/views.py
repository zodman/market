from rest_framework import generics
from django.shortcuts import render
from inertia.views import render_inertia
from inertia.share import share_flash
from .models import Food, Order
from .serializers import FoodSerializer, OrderSerializer


def index(request):
    foods = Food.objects.all()
    context = {"foods": FoodSerializer(foods, many=True).data}
    share_flash(request, "error", error=True)
    return render_inertia(request, "Index", context)

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
