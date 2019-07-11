from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

class Inventory(models.Model):
    user_item = models.CharField(max_length=200)
    qty = models.CharField(max_length=200)

class Profile(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    objects = UserManager()
    active = models.BooleanField(default=True, help_text="True/False user active/inactive")
    staff = models.BooleanField(default=False, help_text="True/False staff account permissions") # a admin user; non super-user
    admin = models.BooleanField(default=False, help_text="True/False admin account permissions") # a superuser
    bio = models.TextField(max_length=500, blank=True, null=True, help_text='User bio of themselves.')
    atkins = models.BooleanField(default=False, help_text="True/False search filter diet option")
    zone = models.BooleanField(default=False, help_text="True/False search filter diet option")
    ketogenic = models.BooleanField(default=False, help_text="True/False search filter diet option")
    vegetarian = models.BooleanField(default=False, help_text="True/False search filter diet option")
    vegan = models.BooleanField(default=False, help_text="True/False search filter diet option")
    weight_watchers = models.BooleanField(default=False, help_text="True/False search filter diet option")
    south_beach = models.BooleanField(default=False, help_text="True/False search filter diet option")
    raw = models.BooleanField(default=False, help_text="True/False search filter diet option")
    mediterranean = models.BooleanField(default=False, help_text="True/False search filter diet option")
    inventory = models.ManyToManyField(Inventory, blank=True, help_text="User's personal inventory")
    saved_recipes = models.IntegerField(blank=True, null=True, help_text="recipes saved by pk(id)")
    subscribed_chefs = models.IntegerField(blank=True, null=True, help_text="Chefs subscribed by pk(id)")
    first_name = models.CharField(max_length=255, blank=True, null=True, help_text="User's first name")
    last_name = models.CharField(max_length=255, blank=True, null=True, help_text="User's last name")
    city = models.CharField(max_length=255, blank=True, null=True, help_text="User City in Country")
    state = models.CharField(max_length=255, blank=True, null=True, help_text="User State in Country")
    country = models.CharField(max_length=255, blank=True, null=True, help_text="User Country of origin")
    joined_at = models.DateTimeField('Joined at', default=timezone.now, help_text="User registration date")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active


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
    title = models.CharField(max_length=100, help_text="recipes title")
    recipe_url = models.URLField(max_length=500, blank=True, default='', unique=True, help_text="unique recipe origin url")
    prep_time = models.CharField(max_length=10, help_text="charfield preparation time 'example: 10 mins'")
    cook_time = models.CharField(max_length=10, help_text="charfield cook time 'example: 10 mins'")
    ingredients = models.ManyToManyField(Ingredient, help_text="List of dictionaries")
    directions = models.ManyToManyField(Direction)
    tags = TaggableManager(through=TaggedFood, help_text="A comma-separated list of tags.")
    # https://django-taggit.readthedocs.io/en/latest/getting_started.html
    # Explained: https://medium.com/sthzg/a-short-exploration-of-django-taggit-bb869ea5051f

    def __str__(self):
        return self.title
