from .models import Recipe
from .models import Chef
from .models import Direction
from .models import Ingredient
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.exceptions import ParseError
from django.http import HttpResponse, JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)


class ChefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chef
        fields = ('name', 'chef_url')

class DirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direction
        fields = '__all__'

class IngredientManySerializer(serializers.DictField):
    ingredient = serializers.CharField()
    quantity = serializers.CharField() #ingredient = serializers.CharField(max_length=200)

class IngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientManySerializer(child=serializers.CharField())

    """serializers.SerializerMethodField()
    def get_ingredient(self, obj):
        return dict(
            ingredient1=obj.address1, # As long as the fields are auto serializable to JSON
            some_field=SomeSerializer(obj.some_field).data,
        )"""
    class Meta:
        model = Ingredient
        fields = '__all__'

class RecipeSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Recipe
        fields = ('chef','title', 'recipe_url', 'prep_time', 'cook_time', 'tags')
