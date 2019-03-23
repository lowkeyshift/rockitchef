from django.contrib import admin
from .models import Recipes, Chefs, Directions, Ingredients

admin.site.register(Recipes)
admin.site.register(Chefs)
admin.site.register(Directions)
admin.site.register(Ingredients)
