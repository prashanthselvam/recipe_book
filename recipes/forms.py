from django import forms
from .models import Recipe, RecipeSteps, Ingredient


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'source_url', 'img_url']


class RecipeStepsForm(forms.ModelForm):
    class Meta:
        model = RecipeSteps
        fields = ['step_text']
        widgets = {'step_text': forms.Textarea(attrs={'rows': 1, 'cols': 40})}


class IngredientsForm(forms.Form):

    ingredient = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'awesomplete',
            'list': 'ingredientslist'
        })
    )

    quantity = forms.CharField(
        max_length=200,
        widget=forms.TextInput()
    )