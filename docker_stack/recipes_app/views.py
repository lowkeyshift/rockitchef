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
from .serializers import AuthCustomTokenSerializer

from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.parsers import JSONParser
from rest_framework.parsers import FormParser
from rest_framework.parsers import MultiPartParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class CreateUserAPIView(CreateAPIView):
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]

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
class ProfileView(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    model = Profile
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return Profile.objects.filter(email=self.request.user)

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
