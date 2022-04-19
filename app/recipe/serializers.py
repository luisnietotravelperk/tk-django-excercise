from rest_framework import serializers

from core.models import Recipe, Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for the Ingredient object"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', )
        read_only_fields = ('id', )


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for the Recipe object"""
    ingredients = IngredientSerializer(
        many=True,
        required=False
    )

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'description', 'ingredients']
        read_only_fields = ('id', )

    def create(self, validated_data):
        """Create recipe related with the ingredients"""
        ingredients = validated_data.pop('ingredients', [])
        recipe = Recipe.objects.create(**validated_data)

        for ingredient in ingredients:
            Ingredient.objects.create(
                name=ingredient['name'],
                recipe=recipe
            )

        return recipe

    def update(self, instance, validated_data):
        """Update recipe related with the ingredients"""
        ingredients = validated_data.pop('ingredients', [])
        instance.ingredients.all().delete()

        for ingredient in ingredients:
            instance.ingredients.create(
                name=ingredient['name'],
                recipe=instance
            )

        super().update(instance, validated_data)
        return instance
