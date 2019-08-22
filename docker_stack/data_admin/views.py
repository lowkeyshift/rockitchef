from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from recipes_app import models
import re

from .forms import PostForm
from django.urls import reverse
from django.contrib import messages

def home(request):
    recipes_list = models.Recipe.objects.all()
    if recipes_list.exists():
        paginator = Paginator(recipes_list, 10)
        page = request.GET.get('page')
        recipes = paginator.get_page(page)
    return render(request, 'admin_page/recipe_editor.html', {'recipes': recipes})

def dashboard(request):
    #profile_data_list = models.Profile.objects.all()
    return render(request, 'dashboard/dashboard.html')

def edit_recipe(request, pk):
    template = 'admin_page/edit_form.html'
    recipe = get_object_or_404(models.Recipe, pk=pk)
    url = request.get_full_path
    print(url)
    next = re.search(r'(?<=full_path=)[^.\s]*',str(url))
    print(next)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=recipe)

        try:
            if recipe.exists():
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Recipe details updated.')
                    return HttpResponseRedirect(next)
        except Exception as e:
            messages.warning(request, 'Your update failed. Error: {}'.format(e))
    else:
        form = PostForm(instance=recipe)

    context = {
        'form': form,
        'recipe': recipe,
    }
    return render(request, template, context)

def delete_recipe(request, pk):
    template = 'admin_page/recipe_editor.html'
    recipe = get_object_or_404(models.Recipe, pk=pk)
    next = request.POST.get('full_path')
    try:
        if request.method == 'POST':
            recipe.delete()
            messages.success(request, "You have deleted recipe with ID: {}".format(pk))
            return HttpResponseRedirect(next)
    except Exception as e:
        messages.warning(request, 'Your deletion failed. Error: {}'.format(e))
        return HttpResponseRedirect(next)
    #instance = models.Recipe.objects.filter(id__in=[ 1,2,3,4,5,6]).delete()
