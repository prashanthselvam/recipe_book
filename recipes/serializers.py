from rest_framework import serializers
from .models import Recipe, RecipeStep, Ingredient, RecipeIngredient


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'date_added']


class RecipeStepSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecipeStep
        fields = ['step_number', 'step_text']


class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = serializers.CharField(source='ingredient.name')

    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'ingredient_quantity']


class ListRecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(source='recipeingredient_set', many=True)
    recipe_steps = RecipeStepSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'date_added', 'description', 'source_url', 'img_url', 'ingredients', 'recipe_steps']








