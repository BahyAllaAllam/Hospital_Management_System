import django_filters
from .models import Patient


class PatientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='user__first_name', lookup_expr='icontains')
    blood_type = django_filters.CharFilter(field_name='blood_type', lookup_expr='exact')

    class Meta:
        model = Patient
        fields = ['blood_type']