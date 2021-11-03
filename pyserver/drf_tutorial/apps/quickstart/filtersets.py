from django_filters import rest_framework as filters
from apps.quickstart import models


class CoursePriceFilterSet(filters.FilterSet):
    # price <= max_price
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
    # max_price = filters.NumberFilter(method='lte_min_price')

    def lte_min_price(self, queryset, name, value):
        return self.queryset.filter(price__lte=value)

    class Meta:
        model = models.Course
        fields = '__all__'
