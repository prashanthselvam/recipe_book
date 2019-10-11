from django.db import models

# Create your models here.


class Ingredient(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """A recipe that a user can create"""
    title = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    steps = models.TextField()
    source_url = models.URLField()
    img_url = models.URLField()

    class Meta:
        ordering = ('-date_added',)
        verbose_name_plural = 'recipes'

    def __str__(self):
        return self.title
