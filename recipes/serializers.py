from rest_framework import serializers
from .models import Recipe, RecipeStep, Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'date_added']


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'date_added', 'description', 'ingredients', 'source_url', 'img_url']





