from django import forms

from recipes_app.models import Recipe

class PostForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = (
            'chef',
            'title',
            'recipe_url',
            'prep_time',
            'cook_time',
            'ingredients',
            'directions',
            'tags'
        )
