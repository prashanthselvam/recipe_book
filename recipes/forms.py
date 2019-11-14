from django import forms
from .models import Recipe, RecipeStep, Ingredient


class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'source_url', 'img_url']


class RecipeStepForm(forms.Form):

    step_text = forms.CharField(
        max_length=1000,
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 80})
    )


class IngredientsForm(forms.Form):

    ingredient = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'awesomplete',
            'list': 'ingredientslist',
            'autocomplete': 'false'
        })
    )

    quantity = forms.CharField(
        max_length=200,
        widget=forms.TextInput()
    )