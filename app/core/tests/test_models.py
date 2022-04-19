from django.test import TestCase

from core import models


def sample_recipe():
    return models.Recipe.objects.create(
        name='Test name',
        description='Some description')


class TestModel (TestCase):
    """Class to test all the models"""

    def test_recipe_str(self):
        recipe = models.Recipe.objects.create(
            name='Test recipe',
            description='Lorem ipsum dolor sit amet, consectetur adipiscing '
                        'elit.',
        )

        self.assertEqual(str(recipe), recipe.name)

    def test_ingredient_str(self):
        """Test the ingredient model"""
        ingredient = models.Ingredient.objects.create(
            name='Test Ingredient',
            recipe=sample_recipe()
        )

        self.assertEqual(str(ingredient), ingredient.name)
