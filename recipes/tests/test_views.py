from django.test import TestCase, Client
from django.urls import reverse
from recipes.models import Ingredient, Recipe, RecipeIngredient, RecipeStep


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.recipes_url = reverse('recipes:recipes')
        self.recipe_detail_url = reverse('recipes:recipe_detail', args=[1])
        self.recipe = Recipe.objects.create(id=1, title='some test recipe')

    def test_recipes_GET(self):
        response = self.client.get(self.recipes_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipes.html')

    def test_recipe_detail_GET(self):
        response = self.client.get(self.recipe_detail_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe_detail.html')



