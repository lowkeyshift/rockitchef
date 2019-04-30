from django.contrib import admin
from .models import Recipe, Chef, Direction, Ingredient

admin.site.register(Recipe)
admin.site.register(Chef)
admin.site.register(Direction)
admin.site.register(Ingredient)
