from rest_framework import viewsets

from core.models import Recipe

from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer

    def get_queryset(self):
        """Retrieving recipes by name"""
        queryset = self.queryset
        name = self.request.query_params.get("name")

        if name is not None:
            queryset = queryset.filter(name__icontains=name)

        return queryset
