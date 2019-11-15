from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.forms import formset_factory
from django.db import transaction
from django.views import View
from django.views.decorators.csrf import csrf_exempt


from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from .models import Recipe, Ingredient, RecipeStep, RecipeIngredient
from .forms import RecipeForm, IngredientsForm, RecipeStepForm
from .serializers import ListRecipeSerializer, IngredientSerializer
from .controllers import process_recipe_form, process_ingredients_formset, process_recipesteps_formset


def index(request):
    """The Home Page for Recipe Book"""
    return render(request, 'recipes/index.html')


def recipes(request):
    """The recipes page which lists out all the recipes"""
    recipe_list = Recipe.objects.order_by('-date_added')
    context = {'recipes': recipe_list}
    return render(request, 'recipes/recipes.html', context)


@api_view(['GET', 'POST'])
def api_ingredient(request, format=None):
    if request.method == 'GET':
        ingredients = Ingredient.objects.all()
        serializer = IngredientSerializer(ingredients, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data
        serializer = IngredientSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)



@api_view(['GET', 'POST'])
def api_recipe(request, format=None):
    """List all recipes in the app via API"""
    if request.method == 'GET':
        recipes = Recipe.objects.all()
        serializer = ListRecipeSerializer(recipes, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        pass

        # TODO: really having trouble with this

        # serializer = CreateRecipeSerializer()
        # if serializer.is_valid():
        #     serializer.save()
        #     return JsonResponse(serializer.data, status=201)
        # print(serializer.errors)
        # return JsonResponse(serializer.errors, status=400)
        # serializer = RecipeSerializer(data=data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return JsonResponse(serializer.data, status=201)
        # print(serializer.errors)
        # return JsonResponse(serializer.errors, status=400)


def recipe_detail(request, recipe_id):
    """View a specific recipe on this page"""
    recipe = Recipe.objects.get(id=recipe_id)
    steps = RecipeStep.objects.filter(recipe=recipe)
    ingredients = RecipeIngredient.objects.filter(recipe=recipe)

    context = {'recipe': recipe, 'steps': steps, 'ingredients': ingredients}
    return render(request, 'recipes/recipe_detail.html', context)


@api_view(['GET'])
def api_recipe_detail(request, pk, format=None):
    """Get details on a particular recipe ID"""
    try:
        recipe = Recipe.objects.get(pk=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ListRecipeSerializer(recipe)
        return Response(serializer.data)


class NewRecipeView(View):
    IngredientsFormSet = formset_factory(IngredientsForm)
    RecipeStepFormSet = formset_factory(RecipeStepForm)

    def get(self, request):
        recipe_form = RecipeForm()
        ingredients_formset = self.IngredientsFormSet(prefix='ingredient_form')
        recipestep_formset = self.RecipeStepFormSet(prefix='recipestep_form')
        ingredientslist = [ingredient.name for ingredient in Ingredient.objects.all()]

        context = {
            'recipe_form': recipe_form,
            'ingredients_formset': ingredients_formset,
            'recipestep_formset': recipestep_formset,
            'ingredientslist': ingredientslist
        }

        return render(request, 'recipes/new_recipe.html', context)

    @transaction.atomic
    def post(self, request):
        recipe_form = RecipeForm(data=request.POST)
        ingredients_formset = self.IngredientsFormSet(data=request.POST, prefix='ingredient_form')
        recipestep_formset = self.RecipeStepFormSet(data=request.POST, prefix='recipestep_form')

        # Process the input into the recipe form and save the recipe
        recipe = process_recipe_form(recipe_form)

        # Process the ingredients formset and save to the RecipeIngredients model
        process_ingredients_formset(ingredients_formset, recipe)

        # Process recipe steps formset and save to the RecipeSteps model
        process_recipesteps_formset(recipestep_formset, recipe)

        return HttpResponseRedirect(reverse('recipes:recipes'))

