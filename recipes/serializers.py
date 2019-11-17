from rest_framework import serializers
from .models import Recipe, RecipeStep, Ingredient, RecipeIngredient
from django.db import transaction


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

    @transaction.atomic
    def create(self, validated_data):
        """ This serializer requires a custom create method because it uses nested models """
        recipe_steps = validated_data.pop('recipe_steps')
        recipe_ingredients = validated_data.pop('recipeingredient_set')

        existing_ingredients = [ingredient.name for ingredient in Ingredient.objects.all()]

        recipe = Recipe.objects.create(**validated_data)

        for step in recipe_steps:
            RecipeStep.objects.create(recipe=recipe, step_number=step['step_number'], step_text=step['step_text'])

        for ingredient in recipe_ingredients:
            name = ingredient['ingredient']['name'].title()
            quantity = ingredient['ingredient_quantity']

            if name in existing_ingredients:
                r_ingredient = Ingredient.objects.get(name=name)
            else:
                r_ingredient = Ingredient.objects.create(name=name)

            RecipeIngredient.objects.create(recipe=recipe, ingredient=r_ingredient, ingredient_quantity=quantity)

        return recipe




