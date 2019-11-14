from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
  # Home Page (Directs to recipes page)
  path('', views.recipes, name='index'),

  # Recipes Page
  path('recipes/', views.recipes, name='recipes'),

  # Add New Recipe Page (Ingredients form Test)
  path('new_recipe/', views.NewRecipeView.as_view(), name='new_recipe'),

  # Recipe Detail Page
  path('recipes/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),

  # Recipes API
  path('api/recipes/', views.api_recipe_list, name='api_recipe_list'),

  # Recipe Detail API
  path('api/recipes/<int:pk>/', views.api_recipe_detail, name='api_recipe_detail')

]

urlpatterns = format_suffix_patterns(urlpatterns)