from django.db import models


class Recipe(models.Model):
    """The recipe model"""
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """The ingredient model related to the recipe"""
    name = models.CharField(max_length=255)
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="ingredients"
    )

    def __str__(self):
        return self.name
