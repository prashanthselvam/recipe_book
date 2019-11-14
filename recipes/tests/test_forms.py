from django.test import TestCase
from recipes.forms import RecipeForm, RecipeStepForm, IngredientsForm


class RecipeFormTest(TestCase):

    def recipe_form_data(self, title, description, source_url, img_url):
        return RecipeForm(
            data={
                'title': title,
                'description': description,
                'source_url': source_url,
                'img_url': img_url
            }
        )

    def test_recipe_form(self):
        form = self.recipe_form_data(
            title='This is a recipe name',
            description='This is a recipe description',
            source_url='https://www.thekitchn.com/recipe-greek-pasta-salad-258330',
            img_url='https://cdn.apartmenttherapy.info/image/fetch/f_auto,q_auto:eco,c_fit,w_1460/https%3A%2F%2Fstorage.googleapis.com%2Fgen-atmedia%2F3%2F2018%2F06%2F8577e9ba119d0ffad190b467d5476f0e874d6b90.jpeg'
        )
        self.assertTrue(form.is_valid())

    def test_recipe_form_missing_data(self):
        form = self.recipe_form_data(
            title='This is a recipe name',
            description='',
            source_url='https://www.thekitchn.com/recipe-greek-pasta-salad-258330',
            img_url='https://cdn.apartmenttherapy.info/image/fetch/f_auto,q_auto:eco,c_fit,w_1460/https%3A%2F%2Fstorage.googleapis.com%2Fgen-atmedia%2F3%2F2018%2F06%2F8577e9ba119d0ffad190b467d5476f0e874d6b90.jpeg'
        )
        errors = form['description'].errors.as_data()
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].code, 'required')

    def test_recipe_form_invalid_url(self):
        form = self.recipe_form_data(
            title='This is a recipe name',
            description='This is a recipe description',
            source_url='not a url',
            img_url='https://cdn.apartmenttherapy.info/image/fetch/f_auto,q_auto:eco,c_fit,w_1460/https%3A%2F%2Fstorage.googleapis.com%2Fgen-atmedia%2F3%2F2018%2F06%2F8577e9ba119d0ffad190b467d5476f0e874d6b90.jpeg'
        )
        errors = form['source_url'].errors.as_data()
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].code, 'invalid')


class IngredientsFormTest(TestCase):

    def ingredients_form_data(self, ingredient, quantity):
        return IngredientsForm(
            data={
                'ingredient': ingredient,
                'quantity': quantity
            }
        )

    def test_ingredients_form_data(self):
        form = self.ingredients_form_data(
            ingredient='Onions',
            quantity='3 big ones'
        )
        self.assertTrue(form.is_valid())

    def test_ingredients_form_missing_data(self):
        form = self.ingredients_form_data(
            ingredient='Onions',
            quantity=''
        )
        errors = form['quantity'].errors.as_data()
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].code, 'required')