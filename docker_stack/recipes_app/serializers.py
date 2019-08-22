from .models import Recipe
from .models import Chef
from .models import Direction
from .models import Ingredient
from .models import Profile
from .models import Inventory

from rest_framework.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from django.utils.translation import gettext as _
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from drf_writable_nested import WritableNestedModelSerializer
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)


class AuthCustomTokenSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True,
                                     style={'input_type': 'password'})
    class Meta:
        model = get_user_model()
        fields = ('email', 'password')
        write_only_fields = ('password')
        read_only_fields = ('is_staff', 'is_superuser', 'is_active',)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            # Check if user sent email
            if validate_email(email):
                user_request = get_object_or_404(
                    User,
                    email=email,
                )

                email = user_request.username

            user = authenticate(username=email, password=password)

            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise ValidationError(msg)
            else:
                msg = _('Unable to log in with provided credentials.')
                raise ValidationError(msg)
        else:
            msg = _('Must include "email or username" and "password"')
            raise ValidationError(msg)

        attrs['user'] = user
        return attrs

class InventorySerializer(WritableNestedModelSerializer):
    class Meta:
        model = Inventory
        fields = ('inventory', 'qty')

class ProfileSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    inventory = InventorySerializer(many=True)


    class Meta:
        model = Profile
        fields = (
            'id',
            'bio',
            'atkins',
            'zone',
            'ketogenic',
            'vegetarian',
            'vegan',
            'weight_watchers',
            'south_beach',
            'raw',
            'mediterranean',
            'inventory',
            'saved_recipes',
            'subscribed_chefs',
            'first_name',
            'last_name',
            'city',
            'state',
            'country',
        )

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
