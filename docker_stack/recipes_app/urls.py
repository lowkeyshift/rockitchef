from django.urls import path, include
from django.conf.urls import url
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('recipes', views.RecipeView)
router.register('chefs', views.ChefView)
router.register('directions', views.DirectionView)
router.register('users', views.ProfileView)
#router.register('recommendations', views.RecommendationsEngine, basename='Recipe')

urlpatterns = [
    path('', include(router.urls)),
    url('^recommendations/$', views.RecommendationsEngine.as_view(), name='recommendations engine'),
]
