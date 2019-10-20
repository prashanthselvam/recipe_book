import json

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.forms import modelformset_factory, inlineformset_factory, formset_factory

from .models import Recipe, RecipeSteps, Ingredient
from .forms import RecipeForm, IngredientsForm


def index(request):
    """The Home Page for Recipe Book"""
    return render(request, 'recipes/index.html')


def recipes(request):
    """The recipes page which lists out all the recipes"""
    recipe_list = Recipe.objects.order_by('-date_added')
    context = {'recipes': recipe_list}
    return render(request, 'recipes/recipes.html', context)


def recipe_detail(request, recipe_id):
    """View a specific recipe on this page"""
    recipe = Recipe.objects.get(id=recipe_id)
    steps = RecipeSteps.objects.filter(recipe__pk=recipe.id)

    context = {'recipe': recipe, 'steps': steps}
    return render(request, 'recipes/recipe_detail.html', context)


def new_recipe(request):
    """Create a new recipe on this page"""
    IngredientsFormSet = formset_factory(IngredientsForm)
    RecipeStepsFormSet = inlineformset_factory(Recipe, RecipeSteps, fields=('step_text',), can_delete=False)

    if request.method == 'POST':
        ingredients_formset = IngredientsFormSet(request.POST)
        recipe_form = RecipeForm(request.POST)

        if recipe_form.is_valid():

            recipe = recipe_form.save(commit=False)

            if ingredients_formset.is_valid():

                ingredient_quantity_pairs = []

                for ingredient_form in ingredients_formset:
                    ingredient = ingredient_form.cleaned_data.get('ingredient')
                    quantity = ingredient_form.cleaned_data.get('quantity')

                    ingredient_quantity_pairs.append({'ingredient': ingredient, 'quantity': quantity})

                recipe.ingredient_quantity = json.dumps(ingredient_quantity_pairs)
                recipe.save()

                recipesteps_formset = RecipeStepsFormSet(request.POST, instance=recipe)

                if recipesteps_formset.is_valid():

                    recipesteps = recipesteps_formset.save(commit=False)
                    i = 1

                    for step in recipesteps:
                        step.recipe = recipe
                        step.step_number = i
                        i += 1
                        step.save()

                    return HttpResponseRedirect(reverse('recipes:recipes'))

    else:
        recipe_form = RecipeForm()
        ingredients_formset = IngredientsFormSet()
        recipesteps_formset = RecipeStepsFormSet()

    context = {
        'recipe_form': recipe_form,
        'ingredients_formset': ingredients_formset,
        'recipesteps_formset': recipesteps_formset
    }

    return render(request, 'recipes/new_recipe.html', context)
