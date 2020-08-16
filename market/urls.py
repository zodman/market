from django.urls import path
from .views import index, order_list

app_name="market"

urlpatterns=[
    path('', index, name='index'),
    path('orders', order_list, name='order_list'),
]
