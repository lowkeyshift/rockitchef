from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase

class Inventory(models.Model):
    user_item = models.CharField(max_length=200)
    qty = models.CharField(max_length=200)

class Profile(models.Model):
    connected_user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, help_text='User bio of themselves.')
    diet = models.CharField(max_length=100, blank=True)
    inventory = models.ManyToManyField(Inventory, blank=True)
    saved_recipes = models.IntegerField(blank=True, null=True)
    subscribed_chefs = models.IntegerField(blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

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
    tags = TaggableManager(through=TaggedFood, help_text="A comma-separated list of tags.")
    # https://django-taggit.readthedocs.io/en/latest/getting_started.html
    # Explained: https://medium.com/sthzg/a-short-exploration-of-django-taggit-bb869ea5051f

    def __str__(self):
        return self.title
