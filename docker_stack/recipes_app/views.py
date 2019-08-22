from django.shortcuts import render
from django_filters import rest_framework as filters
from django.contrib.auth import get_user_model
from django.db.models import Q, Count
from functools import reduce

from .models import Recipe
from .models import Chef
from .models import Direction
from .models import Ingredient
from .models import Profile
from .models import Inventory

from .serializers import RecipeSerializer
from .serializers import ProfileSerializer
from .serializers import InventorySerializer
from .serializers import ChefSerializer
from .serializers import DirectionSerializer
from .serializers import IngredientSerializer
from .serializers import AuthCustomTokenSerializer

from rest_framework.generics import CreateAPIView
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status

from rest_framework.parsers import JSONParser
from rest_framework.parsers import FormParser
from rest_framework.parsers import MultiPartParser
from rest_framework.renderers import JSONRenderer

from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import BasePermission
#from cosine_sim import CosineSimilarity

class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (
        FormParser,
        MultiPartParser,
        JSONParser,
    )

    renderer_classes = (JSONRenderer,)

    def post(self, request, *args, **kwargs):
        serializer = AuthCustomTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        token_data = {"token": token.key}

        return Response(
            {**serializer.data, **token_data},
            status=status.HTTP_201_CREATED,
        )

class CustomUpdatePermission(BasePermission):
    """
    Permission class to check that a user can update his own resource only
    """

    def has_permission(self, request, view):
        # check that its an update request and user is modifying his resource only
        if view.action == 'update' and view.kwargs['id']!=request.user.id:
            return False # not grant access
        return True # grant access otherwise

class ProfileView(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    model = Profile
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        return Profile.objects.filter(email=self.request.user)

    def put(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def pre_save(self, obj):
        obj.user = self.request.user

class LogoutUserAPIView(APIView):
    queryset = get_user_model().objects.all()

    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(
        {"message": "Successfully Logged Out"},
        status=status.HTTP_200_OK
        )

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

class RecommendationsEngine(ListAPIView):
    """
    Cosine Similarity of ingredients in user Profile
    compared to recipes ingredients in Database.
    Output should be All Recipes that match the most ingredients
    from the users inventory.

    Ranking:
        0     | no matches between ingredients & inventory
    1 > n > 0 | at least 1 or more matching ingredients
        1     | inventory & ingredients match 100%

    Exclusions:
      Using users profile diet options as main recipe exclude param
    """
    queryset = Recipe.objects.all()
    serializer_class =  RecipeSerializer

    def get_queryset(self):
        """
        devicesubnet = Profile.objects.filter(ingredients__=device_id)
        sitesubnet = Subnets.objects.filter(sitesubnets__site_id=site_id)
        common_subnets = list(set(devicesubnet) & set(sitesubnet))"""
# Update code to use sets or return most matches.
# Currently only returns %LIKE% matches between User Inventory & Recipe Ingredients.
# It returns an all matching or nothing.
# Need match all, some and rest of recipe database
        user_id = self.request.user
        user_inventory_set = Inventory.objects.filter(
        profile__id__exact=user_id.id).values('inventory')
        if not user_inventory_set:
            return Recipe.objects.all()
        else:

            inv_set = [item['inventory'] \
            for item in user_inventory_set.iterator() \
            if user_inventory_set.exists()]

            recipes = Recipe.objects.filter(\
            reduce(lambda x, y: x | y,\
            [Q(ingredients__item__icontains=item['inventory']) \
            for item in user_inventory_set.iterator() \
            if user_inventory_set.exists()])) \
            .annotate(num_ingredients=Count('ingredients')) \
            .filter(num_ingredients=len(inv_set))
            print(recipes)
            return recipes

class RecipeFilter(filters.FilterSet):
    """
    Generic Django Filter matching:
    Urls: Recipe Url origin
    Title: Recipe title
    Tags: Tags from recipe title & ingredients
    """
    recipe_url = filters.CharFilter(lookup_expr='icontains')
    title = filters.CharFilter(lookup_expr='icontains')
    tags = TagsFilter()

    class Meta:
        model = Recipe
        fields = ('title','recipe_url', 'chef', 'id', 'ingredients')

class RecipeView(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filterset_class = RecipeFilter
