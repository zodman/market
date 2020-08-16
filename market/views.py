from django.shortcuts import render
from inertia.views import render_inertia
from .models import Food
from .serializers import FoodSerializer

def index(request):
    foods = Food.objects.all()
    context = {
        'foods': FoodSerializer(foods, many=True).data
    }
    return render_inertia(request, "Index", context)


