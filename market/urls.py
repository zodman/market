from django.urls import path
from .views import index

app_name="market"

urlpatterns=[
    path('', index, name='index'),
]
