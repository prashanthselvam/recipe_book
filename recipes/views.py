from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.forms import formset_factory
from django.db import transaction

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Recipe, Ingredient, RecipeStep, RecipeIngredient
from .forms import RecipeForm, IngredientsForm, RecipeStepForm
from .serializers import RecipeSerializer
from .controllers import process_recipe_form, process_ingredients_formset, process_recipesteps_formset


def index(request):
    """The Home Page for Recipe Book"""
    return render(request, 'recipes/index.html')


def recipes(request):
    """The recipes page which lists out all the recipes"""
    recipe_list = Recipe.objects.order_by('-date_added')
    context = {'recipes': recipe_list}
    return render(request, 'recipes/recipes.html', context)


@api_view(['GET'])
def api_recipe_list(request, format=None):
    """List all recipes in the app via API"""
    if request.method == 'GET':
        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)



def recipe_detail(request, recipe_id):
    """View a specific recipe on this page"""
    recipe = Recipe.objects.get(id=recipe_id)
    steps = RecipeStep.objects.filter(recipe=recipe)
    ingredients = RecipeIngredient.objects.filter(recipe=recipe)

    context = {'recipe': recipe, 'steps': steps, 'ingredients': ingredients}
    return render(request, 'recipes/recipe_detail.html', context)


@transaction.atomic
def new_recipe(request):
    """Create a new recipe on this page"""
    # We're using formsets here to display multiple forms (since we can have multiple steps/ingredients

    IngredientsFormSet = formset_factory(IngredientsForm)
    RecipeStepFormSet = formset_factory(RecipeStepForm)

    if request.method == 'POST':

        recipe_form = RecipeForm(data=request.POST)
        ingredients_formset = IngredientsFormSet(data=request.POST, prefix='ingredient_form')
        recipestep_formset = RecipeStepFormSet(data=request.POST, prefix='recipestep_form')

        # Process the input into the recipe form and save the recipe
        recipe = process_recipe_form(recipe_form)

        # Process the ingredients formset and save to the RecipeIngredients model
        process_ingredients_formset(ingredients_formset, recipe)

        # Process recipe steps formset and save to the RecipeSteps model
        process_recipesteps_formset(recipestep_formset, recipe)

        return HttpResponseRedirect(reverse('recipes:recipes'))

    else:
        recipe_form = RecipeForm()
        ingredients_formset = IngredientsFormSet(prefix='ingredient_form')
        recipestep_formset = RecipeStepFormSet(prefix='recipestep_form')
        ingredientslist = [ingredient.name for ingredient in Ingredient.objects.all()]

    context = {
        'recipe_form': recipe_form,
        'ingredients_formset': ingredients_formset,
        'recipestep_formset': recipestep_formset,
        'ingredientslist': ingredientslist
    }

    return render(request, 'recipes/new_recipe.html', context)


@api_view(['GET'])
def api_recipe_detail(request, pk, format=None):
    """Get details on a particular recipe ID"""
    try:
        recipe = Recipe.objects.get(pk=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RecipeSerializer(recipe)
        return Response(serializer.data)