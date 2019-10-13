from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.forms import modelformset_factory, inlineformset_factory

from .models import Recipe, RecipeSteps
from .forms import RecipeForm, RecipeStepsForm

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
    # Question for Ernesto: Is it better to do the inlineformset stuff here or in the forms code?
    recipe_form = RecipeForm()
    recipesteps_formset = inlineformset_factory(Recipe, RecipeSteps, fields=('step_text', ), can_delete=False)

    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST)

        if recipe_form.is_valid():
            recipe = recipe_form.save()

        formset = recipesteps_formset(request.POST, instance=recipe)
        if formset.is_valid():
            recipesteps = formset.save(commit=False)
            i = 1
            for step in recipesteps:
                step.recipe = recipe
                step.step_number = i
                i += 1
                step.save()

            return HttpResponseRedirect(reverse('recipes:recipes'))

    context = {'recipe_form': recipe_form, 'recipesteps_formset': recipesteps_formset}
    return render(request, 'recipes/new_recipe.html', context)


def recipe_detail(request, recipe_id):
    """View a specific recipe on this page"""
    recipe = Recipe.objects.get(id=recipe_id)

    context = {'recipe': recipe}
    return render(request, 'recipes/recipe_detail.html', context)