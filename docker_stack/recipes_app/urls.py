from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('recipes', views.RecipeView)
router.register('chefs', views.ChefView)
router.register('directions', views.DirectionView)
router.register('users', views.ProfileView)

urlpatterns = [
    path('', include(router.urls))
]
