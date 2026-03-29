import django_filters
from .models import MedicalRecord, DoctorNote, NurseNote, LabResult


class MedicalRecordFilter(django_filters.FilterSet):
    date_from = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')
    patient = django_filters.UUIDFilter(field_name='patient__uuid')

    class Meta:
        model = MedicalRecord
        fields = []

class DoctorNoteFilter(django_filters.FilterSet):
    doctor = django_filters.UUIDFilter(field_name='doctor__uuid')
    record = django_filters.UUIDFilter(field_name='record__uuid')
    date_from = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = DoctorNote
        fields = []

class NurseNoteFilter(django_filters.FilterSet):
    nurse = django_filters.UUIDFilter(field_name='nurse__uuid')
    record = django_filters.UUIDFilter(field_name='record__uuid')
    date_from = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = NurseNote
        fields = []

class LabResultFilter(django_filters.FilterSet):
    technician = django_filters.UUIDFilter(field_name='technician__uuid')
    record = django_filters.UUIDFilter(field_name='record__uuid')
    date_from = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = LabResult
        fields = ['result_type']