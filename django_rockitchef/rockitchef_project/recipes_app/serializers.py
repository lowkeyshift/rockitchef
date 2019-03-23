from .models import Recipes
from .models import Chefs
from .models import Directions
from .models import Ingredients
from rest_framework import serializers
from rest_framework.exceptions import ParseError

class ChefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chefs
        fields = ('name', 'chef_url')

class RecipeSerializer(serializers.ModelSerializer):
    tags = TagListSerializer(blank=True)
    class Meta:
        model = Recipes
        fields = ('chef','title', 'recipe_url', 'prep_time', 'cook_time', 'tags')

class TagListSerializer(serializers.Field):

    def from_native(self, data):
        if type(data) is not list:
            raise ParseError("expected a list of data")
        return data

    def to_native(self, obj):
        if type(obj) is not list:
            return [tag.name for tag in obj.all()]
        return obj

class DirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Directions
        fields = ('directions_json')

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = ('ingredient_qty')
