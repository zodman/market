from django.urls import path
from .views import index, order_list, order_detail
from .views import create_cart, login, logout

app_name = "market"

urlpatterns = [
    path("", index, name="index"),
    path("login", login, name="login"),
    path("logout", logout, name="logout"),
    path('create', create_cart, name='create_cart'),
    path("orders", order_list, name="order_list"),
    path("orders/<int:pk>/", order_detail, name="order_detail"),
]
