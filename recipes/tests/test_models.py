from django.test import TestCase
from recipes.models import Ingredient, Recipe, RecipeIngredient, RecipeStep

#
# class TestModels(TestCase):
#
#     def setUp(self):
#         self.recipe1 = Recipe.objects.create(
#             title='Test Recipe',
#             description='This is a recipe for test purposes',
#             source_url='This is the source URL',
#             img_url='This is the image URL',
#         )
#
#         self.ingredient1 = Ingredient.objects.create(
#             name='Onions'
#         )
#
#         self.recipeingredient1 = RecipeIngredient.objects.create(
#             recipe=self.recipe1,
#             ingredient=self.ingredient1,
#             ingredient_quantity='3 Large ones, sliced'
#         )
#
#
#     def attempt_duplicate_ingredient_creation(self):
#         ingredients = Ingredient.objects.all()
#         print(ingredients.length)
