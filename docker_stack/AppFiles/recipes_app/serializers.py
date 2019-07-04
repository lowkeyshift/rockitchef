from .models import Recipe
from .models import Chef
from .models import Direction
from .models import Ingredient
from .models import Profile
from .models import Inventory

from django.contrib.auth import get_user_model
from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)

class CreateUserSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True,
                                     style={'input_type': 'password'})

    class Meta:
        model = get_user_model()
        fields = ('email', 'password')
        write_only_fields = ('password')
        read_only_fields = ('is_staff', 'is_superuser', 'is_active',)

    def create(self, validated_data):
        user = super(CreateUserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class InventorySerializer(WritableNestedModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__' 

class ProfileSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    inventory = InventorySerializer(many=True)
    class Meta:
        model = Profile
        fields = '__all__'

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
    ##Uncomment when react native app can successfully GET/POST from API
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

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
