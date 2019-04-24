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

class IngredientSerializer(serializers.ModelSerializer):
    #recipe = serializers.IntegerField()
    #order = serializers.IntegerField()
    #ingredient = serializers.CharField()
    #quantity = serializers.CharField()

    class Meta:
        model = Ingredient
        fields = '__all__'

class RecipeSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    ingredient = IngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = (
            'chef',
            'title',
            'recipe_url',
            'prep_time',
            'cook_time',
            'tags',
            'ingredient'
        )

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredient')
        recipe = Recipe.objects.create(**validated_data)

        for ingredient in ingredients_data:
            ingredient, created = Ingredient.objects.get_or_create(name=ingredient['item'])
            ingredient, created = Ingredient.objects.get_or_create(name=ingredient['quantity'])
            recipe.ingredients.add(ingredient)
        return recipe
