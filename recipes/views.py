import json

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.forms import inlineformset_factory, formset_factory

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view


from .models import Recipe, RecipeSteps, Ingredient
from .forms import RecipeForm, IngredientsForm, RecipeStepsForm
from .serializers import RecipeSerializer


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
    # We're using formsets here to display multiple forms (since we can have multiple steps/ingredients

    IngredientsFormSet = formset_factory(IngredientsForm)
    RecipeStepsFormSet = inlineformset_factory(Recipe, RecipeSteps, form=RecipeStepsForm, fields=('step_text',), can_delete=False)

    if request.method == 'POST':
        ingredients_formset = IngredientsFormSet(request.POST)
        recipe_form = RecipeForm(request.POST)

        if recipe_form.is_valid():

            recipe = recipe_form.save()

            if ingredients_formset.is_valid():

                ingredient_quantity_pairs = []
                existing_ingredients = [ingredient.name for ingredient in Ingredient.objects.all()]

                for ingredient_form in ingredients_formset:
                    if ingredient_form.cleaned_data.get('ingredient') is not None:
                        ingredient = ingredient_form.cleaned_data.get('ingredient').title()
                        quantity = ingredient_form.cleaned_data.get('quantity').title()

                        if ingredient in existing_ingredients:
                            ingredient_model = Ingredient.objects.get(name=ingredient)
                        else:
                            ingredient_model = Ingredient(name=ingredient)
                            ingredient_model.save()

                        recipe.ingredients.add(ingredient_model)

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

        ingredientslist = [ingredient.name for ingredient in Ingredient.objects.all()]

    context = {
        'recipe_form': recipe_form,
        'ingredients_formset': ingredients_formset,
        'recipesteps_formset': recipesteps_formset,
        'ingredientslist': ingredientslist
    }

    return render(request, 'recipes/new_recipe.html', context)


@api_view(['GET'])
def api_recipe_list(request, format=None):
    """List all recipes in the app via API"""
    if request.method == 'GET':
        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)


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