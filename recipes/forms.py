from django import forms
from .models import Recipe, RecipeSteps


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'source_url', 'img_url']


class RecipeStepsForm(forms.ModelForm):
    class Meta:
        model = RecipeSteps
        fields = ['step_text']


class IngredientsForm(forms.Form):

    ingredient = forms.CharField(
        max_length=200,
        widget=forms.TextInput()
    )

    quantity = forms.CharField(
        max_length=200,
        widget=forms.TextInput()
    )