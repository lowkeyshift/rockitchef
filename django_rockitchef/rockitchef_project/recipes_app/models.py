from django.db import models

from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase

class TaggedFood(TaggedItemBase):
    content_object = models.ForeignKey('Recipe', on_delete=models.CASCADE)

class Crawled(models.Model):
    crawled_url = models.URLField(max_length=500, blank=True, default='')
    source = models.CharField(max_length=80)

class Chef(models.Model):
    chef_url = models.URLField(max_length=500, blank=True, default='')
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    item = models.CharField(max_length=200)
    quantity = models.CharField(max_length=200)
    def __str__(self):
        return self.item

class Direction(models.Model):
    # recipe = models.OneToOneField(Recipe, on_delete=models.CASCADE)
    direction_text = models.CharField(max_length=1000, blank=True, default='')

    def __str__(self):
        return self.direction_text

class Recipe(models.Model):
    chef = models.ForeignKey(Chef, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    recipe_url = models.URLField(max_length=500, blank=True, default='', unique=True)
    prep_time = models.CharField(max_length=10)
    cook_time = models.CharField(max_length=10)
    ingredients = models.ManyToManyField(Ingredient)
    directions = models.ManyToManyField(Direction)
    tags = TaggableManager(through=TaggedFood)
    # https://django-taggit.readthedocs.io/en/latest/getting_started.html
    # Explained: https://medium.com/sthzg/a-short-exploration-of-django-taggit-bb869ea5051f

    def __str__(self):
        return self.title
