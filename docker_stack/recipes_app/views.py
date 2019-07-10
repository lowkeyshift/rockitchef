from django.shortcuts import render
from rest_framework import viewsets
from django_filters import rest_framework as filters

from .models import Recipe
from .models import Chef
from .models import Direction
from .models import Ingredient
from .models import Profile

from .serializers import RecipeSerializer
from .serializers import ProfileSerializer
from .serializers import ChefSerializer
from .serializers import DirectionSerializer
from .serializers import IngredientSerializer
from .serializers import CreateUserSerializer

from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.views import APIView



class CreateUserAPIView(CreateAPIView):
    serializer_class = CreateUserSerializer
    #permission_classes = [AllowAny]
    """
    post:
    Create a new user instance.
    Returns user and auth token.
    """
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # We create a token than will be used for future auth
        token = Token.objects.create(user=serializer.instance)
        token_data = {"token": token.key}
        return Response(
            {**serializer.data, **token_data},
            status=status.HTTP_201_CREATED,
            headers=headers
        )

class ProfileView(viewsets.ModelViewSet):
    """
    get:
    Returns user profiles.
    Use specific 'pk' to return indivual user.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class LogoutUserAPIView(APIView):
    """
    post:
    Individual user logout.
    Deletes auth token.
    """
    queryset = get_user_model().objects.all()

    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

class ChefView(viewsets.ModelViewSet):
    """
    get:
    Returns recipe's chef and url backlink.
    post:
    Create new chef entry.
    {"name":"Paula Dean","chef_url": "https://iloveheartdisease.com"}
    """
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
        fields = ('title','recipe_url', 'chef', 'id', 'ingredients')

class RecipeView(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filterset_class = RecipeFilter

# Future use to have staff and user api access
# to different fields
#    def get_serializer_class(self):
#    if self.request.user.is_staff:
#        return FullAccountSerializer
#    return BasicAccountSerializer
