from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """A recipe that a user can create"""
    title = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    ingredients = models.ManyToManyField(Ingredient)
    source_url = models.URLField()
    img_url = models.URLField()

    class Meta:
        ordering = ('-date_added',)
        verbose_name_plural = 'recipes'

    def __str__(self):
        return self.title


class RecipeSteps(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    step_number = models.IntegerField()
    step_text = models.TextField()

    class Meta:
        ordering = ('recipe', 'step_number')
        verbose_name_plural = 'recipe steps'

    def __str__(self):
        return str(self.recipe.title) + '_' + 'step_' + str(self.step_number)