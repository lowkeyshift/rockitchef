from .models import Recipe
from .models import Chef
from .models import Direction
from .models import Ingredient
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.exceptions import ParseError
from drf_writable_nested import WritableNestedModelSerializer
from django.http import HttpResponse, JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)


class ChefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chef
        fields = ('id','name', 'chef_url')

class DirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direction
        fields = '__all__'

class IngredientSerializer(WritableNestedModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'

class RecipeSerializer(WritableNestedModelSerializer, TaggitSerializer, serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)
    directions = DirectionSerializer(many=True)
    tags = TagListSerializerField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'chef',
            'title',
            'recipe_url',
            'prep_time',
            'cook_time',
            'tags',
            'ingredients',
            'directions'
        )
