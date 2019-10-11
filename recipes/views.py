from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Recipe
from .forms import RecipeForm

# Create your views here.


def index(request):
    """The Home Page for Recipe Book"""
    return render(request, 'recipes/index.html')


def recipes(request):
    """The recipes page which lists out all the recipes"""
    recipe_list = Recipe.objects.order_by('-date_added')
    context = {'recipes': recipe_list}
    return render(request, 'recipes/recipes.html', context)


def new_recipe(request):
    """You can add a new recipe on this page"""
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.steps = recipe.steps.split('\r\n\r\n')
            recipe.save()
            return HttpResponseRedirect(reverse('recipes:recipes'))

    else:
        form = RecipeForm()

    context = {'form': form}
    return render(request, 'recipes/new_recipe.html', context)


def recipe_detail(request, recipe_id):
    """View a specific recipe on this page"""
    recipe = Recipe.objects.get(id=recipe_id)
    steps = recipe.steps.split('\r\n\r\n')
    recipe.steps = steps

    context = {'recipe': recipe}
    return render(request, 'recipes/recipe_detail.html', context)