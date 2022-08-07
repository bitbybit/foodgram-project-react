from rest_framework import serializers

from .models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "color",
            "id",
            "name",
            "slug",
        )

        model = Tag
