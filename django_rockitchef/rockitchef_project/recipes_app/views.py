from django.shortcuts import render
from rest_framework import viewsets
from .models import Recipes
from .models import Chefs
from .models import Directions
from .models import Ingredients
from .serializers import RecipeSerializer
from .serializers import ChefSerializer
from .serializers import DirectionSerializer
from .serializers import IngredientSerializer
from django.http import JsonResponse

class RecipeView(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = RecipeSerializer

class ChefView(viewsets.ModelViewSet):
    queryset = Chefs.objects.all()
    serializer_class = ChefSerializer

def getChef(request):
    arg = request.GET.get('q','')
    response = {}
    try:
        chef = Chefs.objects.filter(chef_url=arg)
        response = chef.to_json()
    except Chefs.DoesNotExist:
        return {}
    finally:
        return JsonResponse({'hello':resp})

    
class DirectionView(viewsets.ModelViewSet):
    queryset = Directions.objects.all()
    serializer_class = DirectionSerializer

class IngredientView(viewsets.ModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientSerializer
