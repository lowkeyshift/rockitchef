from .models import Recipes
from .models import Chefs
from .models import Directions
from .models import Ingredients
from rest_framework import serializers
from rest_framework.exceptions import ParseError
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)


class ChefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chefs
        fields = ('name', 'chef_url')

class RecipeSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Recipes
        fields = ('chef','title', 'recipe_url', 'prep_time', 'cook_time', 'tags')

class DirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Directions
        fields = ('directions_json')

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = ('ingredient_qty')
