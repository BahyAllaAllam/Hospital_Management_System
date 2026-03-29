import django_filters
from .models import Appointment


class AppointmentFilter(django_filters.FilterSet):
    date_from = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name='date', lookup_expr='lte')
    doctor = django_filters.UUIDFilter(field_name='doctor__uuid')
    patient = django_filters.UUIDFilter(field_name='patient__uuid')
    is_available = django_filters.BooleanFilter(field_name='is_available')

    class Meta:
        model = Appointment
        fields = ['status', 'is_available']