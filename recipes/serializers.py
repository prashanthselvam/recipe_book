from rest_framework import serializers
from .models import Recipe, RecipeSteps, Ingredient


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'date_added', 'description', 'ingredients', 'ingredient_quantity', 'source_url', 'img_url']





