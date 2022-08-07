from django.db.models import IntegerField, Value
from django_filters import CharFilter, FilterSet

from .models import Ingredient


class IngredientFilter(FilterSet):
    def filter_name(queryset, name, value):
        startswith = queryset.filter(
            **{f"{name}__istartswith": value}
        ).annotate(order=Value(0, IntegerField()))

        contains = (
            queryset.filter(**{f"{name}__icontains": value})
            .exclude(id__in=startswith.values("id"))
            .annotate(order=Value(1, IntegerField()))
        )

        return startswith.union(contains).order_by("order")

    name = CharFilter(field_name="name", method=filter_name)

    class Meta:
        model = Ingredient
        fields = ("name",)
