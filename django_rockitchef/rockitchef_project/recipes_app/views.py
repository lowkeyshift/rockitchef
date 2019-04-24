from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from django_filters import rest_framework as filters
from .models import Recipe
from .models import Chef
from .models import Direction
from .models import Ingredient
#from .models import TaggedFood
from .serializers import RecipeSerializer
from .serializers import ChefSerializer
from .serializers import DirectionSerializer
from .serializers import IngredientSerializer
from django.http import HttpResponse, JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

class ChefView(viewsets.ModelViewSet):
    queryset = Chef.objects.all()
    serializer_class = ChefSerializer

class DirectionView(viewsets.ModelViewSet):
    queryset = Direction.objects.all()
    serializer_class = DirectionSerializer

class TagsFilter(filters.CharFilter):
    def filter(self, qs, value):
        if value:
            tags = [tag.strip() for tag in value.split(',')]
            qs = qs.filter(tags__name__in=tags).distinct()

        return qs

class RecipeFilter(filters.FilterSet):
    recipe_url = filters.CharFilter(lookup_expr='icontains')
    title = filters.CharFilter(lookup_expr='icontains')
    tags = TagsFilter()

    class Meta:
        model = Recipe
        fields = ('title','recipe_url')

class RecipeView(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filterset_class = RecipeFilter
