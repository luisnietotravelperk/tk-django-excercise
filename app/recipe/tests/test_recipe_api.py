from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.reverse import reverse

from core.models import Recipe, Ingredient

from recipe.serializers import RecipeSerializer


RECIPE_URL = reverse('recipe:recipe-list')


def recipe_detail_url(recipe_id):
    """Return the url for and recipe"""
    return reverse('recipe:recipe-detail', args=[recipe_id])


def sample_recipe(**params):
    """Create a sample recipe"""
    default = {
        'name': 'Test name',
        'description': 'Test description'
    }
    default.update(params)

    return Recipe.objects.create(**default)


def sample_ingredient(recipe, **params):
    """Create a sample ingredient"""
    default = {
        'name': 'Test ingredient'
    }
    default.update(params)

    return Ingredient.objects.create(recipe=recipe, **default)


class TestRecipeApi(TestCase):
    """Class to test the recipe API"""

    def setUp(self):
        self.client = APIClient()

    def test_recipe_list(self):
        """Test the retrieving values on the list"""
        sample_recipe(name='Recipe one')
        sample_recipe(name='Recipe two')

        res = self.client.get(RECIPE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_recipe_filtering_list(self):
        """Test tje retrieving values filtering by name"""
        recipe_01 = sample_recipe(name='Recipe one')
        recipe_02 = sample_recipe(name='Number two recipe')
        recipe_03 = sample_recipe(name="Another one")

        res = self.client.get(RECIPE_URL, {'name': 'rec'})

        serialized_data_01 = RecipeSerializer(recipe_01)
        serialized_data_02 = RecipeSerializer(recipe_02)
        serialized_data_03 = RecipeSerializer(recipe_03)

        self.assertIn(serialized_data_01.data, res.data)
        self.assertIn(serialized_data_02.data, res.data)
        self.assertNotIn(serialized_data_03.data, res.data)

    def test_recipe_detail(self):
        """Test the retrieving values of one recipe"""
        recipe = sample_recipe()

        url = recipe_detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeSerializer(recipe)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data)

    def test_recipe_valid_creation_without_ingredients(self):
        """Test the valid creation of a recipe without ingredients"""
        payload = {
            'name': 'Scrambled eggs',
            'description': 'Delicious and easy'
        }

        res = self.client.post(RECIPE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(recipe, key))

    def test_recipe_valid_creation_with_ingredient(self):
        """Test the valid creation adding ingredients since the beginning"""
        payload = {
            'name': 'Chicken over rice',
            'description': 'Delicious plate',
            'ingredients': [
                {'name': 'chicken'},
                {'name': 'rice'},
                {'name': 'salt'}
            ]
        }

        res = self.client.post(RECIPE_URL, payload, format='json')

        recipe = Recipe.objects.get(id=res.data['id'])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(recipe.ingredients.all().count(), 3)

    def test_recipe_invalid_creation(self):
        """Test the invalid creation of the recipe"""
        payload = {'name': ''}
        res = self.client.post(RECIPE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_recipe_partial_update(self):
        """Test the partial update of a recipe"""
        recipe = sample_recipe()
        current_description = recipe.description
        payload = {
            'name': 'Best recipe in the world'
        }

        url = recipe_detail_url(recipe.id)
        self.client.patch(url, payload)

        recipe.refresh_from_db()
        self.assertEqual(recipe.name, payload['name'])
        self.assertEqual(recipe.description, current_description)

    def test_recipe_full_update_without_ingredients(self):
        """Test the full update of a recipe without ingredients"""
        recipe = sample_recipe()
        sample_ingredient(recipe)
        payload = {
            'name': 'New recipe',
            'description': 'New description'
        }

        url = recipe_detail_url(recipe.id)
        self.client.put(url, payload)

        recipe.refresh_from_db()
        self.assertEqual(recipe.name, payload['name'])
        self.assertEqual(recipe.description, payload['description'])
        self.assertEqual(recipe.ingredients.count(), 0)

    def test_recipe_full_update_with_ingredients(self):
        """Test the full update of a recipe with ingredients"""
        recipe = sample_recipe()
        sample_ingredient(recipe)
        payload = {
            'name': 'New recipe',
            'description': 'New description',
            'ingredients': [
                {'name': 'new ingredient'}
            ]
        }

        url = recipe_detail_url(recipe.id)
        self.client.put(url, payload, format='json')

        recipe.refresh_from_db()
        self.assertEqual(recipe.name, payload['name'])
        self.assertEqual(recipe.description, payload['description'])
        self.assertEqual(recipe.ingredients.count(), 1)

    def test_recipe_invalid_update(self):
        """Test the invalid update of a recipe"""
        recipe = sample_recipe()
        payload = {'name': ''}

        url = recipe_detail_url(recipe.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_recipe_valid_elimination(self):
        """Test the valid elimination of a recipe"""
        recipe = sample_recipe()
        sample_ingredient(recipe)
        sample_ingredient(recipe)

        url = recipe_detail_url(recipe.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Recipe.objects.all().count(), 0)
        self.assertEqual(Ingredient.objects.all().count(), 0)
