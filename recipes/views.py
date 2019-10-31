import json

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.forms import inlineformset_factory, formset_factory

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view


from .models import Recipe, Ingredient, RecipeStep, RecipeIngredient
from .forms import RecipeForm, IngredientsForm, RecipeStepForm
from .serializers import RecipeSerializer


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


def new_recipe(request):
    """Create a new recipe on this page"""
    # We're using formsets here to display multiple forms (since we can have multiple steps/ingredients

    IngredientsFormSet = formset_factory(IngredientsForm)
    RecipeStepFormSet = formset_factory(RecipeStepForm)

    if request.method == 'POST':

        ingredients_formset = IngredientsFormSet(data=request.POST, prefix='ingredient_form')
        recipe_form = RecipeForm(data=request.POST)

        if recipe_form.is_valid():

            recipe = recipe_form.save()

            if ingredients_formset.is_valid():

                existing_ingredients = [ingredient.name for ingredient in Ingredient.objects.all()]

                for ingredient_form in ingredients_formset:
                    if ingredient_form.cleaned_data.get('ingredient') is not None:
                        ingredient = ingredient_form.cleaned_data.get('ingredient').title()
                        quantity = ingredient_form.cleaned_data.get('quantity').title()

                        if ingredient not in existing_ingredients:
                            ingredient = Ingredient.objects.create(name=ingredient)
                        else:
                            ingredient = Ingredient.objects.get(name=ingredient)

                        RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient, ingredient_quantity=quantity)

                recipestep_formset = RecipeStepFormSet(data=request.POST, prefix='recipestep_form')

                if recipestep_formset.is_valid():

                    for step_number, step in enumerate(recipestep_formset, start=1):
                        step_text = step.cleaned_data.get('step_text')
                        RecipeStep.objects.create(recipe=recipe, step_number=step_number, step_text=step_text)

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