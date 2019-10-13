from django.contrib import admin

# Register your models here.

from recipes.models import Recipe, Ingredient, RecipeSteps

admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(RecipeSteps)