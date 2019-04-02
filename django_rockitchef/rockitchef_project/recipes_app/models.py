from django.db import models

from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase

class TaggedFood(TaggedItemBase):
    content_object = models.ForeignKey('Recipes', on_delete=models.CASCADE)

class Crawled(models.Model):
    crawled_url = models.URLField(max_length=500, blank=True, default='')
    source = models.CharField(max_length=80)


class Chefs(models.Model):
    chef_url = models.URLField(max_length=500, blank=True, default='')
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
        
    def to_json(self):
        return {
            'id': self.id,
            'chef_url': self.chef_url,
            'name': self.name
        }

class Recipes(models.Model):
    chef = models.ForeignKey(Chefs, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    recipe_url = models.URLField(max_length=500, blank=True, default='')
    prep_time = models.CharField(max_length=10)
    cook_time = models.CharField(max_length=10)
    tags = TaggableManager(through=TaggedFood)
    # https://django-taggit.readthedocs.io/en/latest/getting_started.html
    # Explained: https://medium.com/sthzg/a-short-exploration-of-django-taggit-bb869ea5051f

    def __str__(self):
        return self.title

class Directions(models.Model):
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    directions_json = models.CharField(max_length=5000)


class Ingredients(models.Model):
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    ingredient_qty = models.CharField(max_length=50)
