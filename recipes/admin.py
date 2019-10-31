from django.contrib import admin

# Register your models here.

from recipes.models import Recipe, Ingredient, RecipeStep, RecipeIngredient

admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(RecipeStep)
admin.site.register(RecipeIngredient)