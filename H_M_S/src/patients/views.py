from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Patient
from .serializers import PatientSerializer
from .filters import PatientFilter
from accounts.permissions import IsAdmin, IsDoctor, IsNurse, IsReceptionist, IsPatient

class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    filterset_class = PatientFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['user__first_name', 'user__last_name', 'user__email']
    ordering_fields = ['user__first_name', 'user__last_name']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'patient':
            return Patient.objects.select_related('user').filter(user=user)
        return Patient.objects.select_related('user').all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        if self.action in ['update', 'partial_update']:
            return [IsAuthenticated(), IsDoctor()]
        if self.action in ['create', 'destroy']:
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated(), IsAdmin()]