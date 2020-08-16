from django.urls import path
from .views import index, order_list, order_detail

app_name="market"

urlpatterns=[
    path('', index, name='index'),
    path('orders', order_list, name='order_list'),
    path('orders/<int:pk>/', order_detail, name='order_detail'),
]
