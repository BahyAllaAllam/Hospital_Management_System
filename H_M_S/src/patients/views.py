from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Patient
from .serializers import PatientSerializer
from accounts.permissions import IsAdmin, IsDoctor, IsNurse, IsReceptionist, IsPatient

class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer

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