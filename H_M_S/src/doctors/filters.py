import django_filters
from .models import Doctor, Department


class DepartmentFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Department
        fields = ['name']


class DoctorFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='user__first_name', lookup_expr='icontains')
    department = django_filters.UUIDFilter(field_name='department__uuid')
    specialization = django_filters.CharFilter(field_name='specialization', lookup_expr='icontains')

    class Meta:
        model = Doctor
        fields = ['specialization']