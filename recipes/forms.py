from django import forms
from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'steps', 'source_url', 'img_url']


    # title = forms.CharField(label='Recipe Name', max_length=100)
    # description = forms.CharField(widget=forms.Textarea)
    # steps = forms.CharField(widget=forms.Textarea)
    # source_url = forms.URLField()
    # img_url = forms.URLField()