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

class RecipeView(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = RecipeSerializer
    def post_save(self, recipes, *args, **kwargs):
        if type(recipes.tags) is list:
            # If tags were provided in the request
            saved_recipes = Recipes.objects.get(pk=recipes.pk)
            for tag in recipes.tags:
                saved_recipes.tags.add(tag)

class ChefView(viewsets.ModelViewSet):
    queryset = Chefs.objects.all()
    serializer_class = ChefSerializer

class DirectionView(viewsets.ModelViewSet):
    queryset = Directions.objects.all()
    serializer_class = DirectionSerializer

class IngredientView(viewsets.ModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientSerializer
