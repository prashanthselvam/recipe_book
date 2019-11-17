from django.test import SimpleTestCase
from django.urls import reverse, resolve
from recipes.views import index, recipes, recipe_detail, NewRecipeView, api_recipe_list, api_recipe_detail


class TestUrls(SimpleTestCase):



    def test_index_is_resolved(self):
        url = reverse('recipes:index')
        self.assertEquals(resolve(url).func, recipes)

    def test_recipes_is_resolved(self):
        url = reverse('recipes:recipes')
        self.assertEquals(resolve(url).func, recipes)

    def test_new_recipe_is_resolved(self):
        url = reverse('recipes:new_recipe')
        self.assertEquals(resolve(url).func.view_class, NewRecipeView)

    def test_recipe_detail_is_resolved(self):
        url = reverse('recipes:recipe_detail', args=[1])
        self.assertEquals(resolve(url).func, recipe_detail)

    def test_api_recipes_is_resolved(self):
        url = reverse('recipes:api_recipe_list')
        self.assertEquals(resolve(url).func, api_recipe_list)

    def test_api_recipe_detail_is_resolved(self):
        url = reverse('recipes:api_recipe_detail', args=[1])
        self.assertEquals(resolve(url).func, api_recipe_detail)
