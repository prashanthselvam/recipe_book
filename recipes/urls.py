from django.urls import path

from . import views

urlpatterns = [
  # Home Page
  path('', views.index, name='index'),

  # Recipes Page
  path('recipes/', views.recipes, name='recipes'),

  # Add New Recipe Page
  path('new_recipe/', views.new_recipe, name='new_recipe'),

  # Recipe Detail Page
  path('recipes/<recipe_id>', views.recipe_detail, name='recipe_detail')

]