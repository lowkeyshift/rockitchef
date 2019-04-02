from django.urls import path, include
from . import views
from rest_framework import routers

urlpatterns = [
    path('lookup_author/', views.helloWorld)
]
