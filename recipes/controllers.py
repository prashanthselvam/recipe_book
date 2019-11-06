from .models import Ingredient, RecipeIngredient, RecipeStep


def process_recipe_form(recipe_form):
    if recipe_form.is_valid():
        return recipe_form.save()


def process_ingredients_formset(ingredients_formset, recipe):

    existing_ingredients = [ingredient.name for ingredient in Ingredient.objects.all()]

    if ingredients_formset.is_valid():

        for ingredient_form in ingredients_formset:
            if ingredient_form.cleaned_data.get('ingredient') is not None:
                ingredient = ingredient_form.cleaned_data.get('ingredient').title()
                quantity = ingredient_form.cleaned_data.get('quantity').title()

                if ingredient not in existing_ingredients:
                    ingredient = Ingredient.objects.create(name=ingredient)
                else:
                    ingredient = Ingredient.objects.get(name=ingredient)

                RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient, ingredient_quantity=quantity)


def process_recipesteps_formset(recipestep_formset, recipe):

    if recipestep_formset.is_valid():

        for step_number, step in enumerate(recipestep_formset, start=1):
            step_text = step.cleaned_data.get('step_text')
            RecipeStep.objects.create(recipe=recipe, step_number=step_number, step_text=step_text)