from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Doctor, Department
from .serializers import DoctorSerializer, DepartmentSerializer
from accounts.permissions import IsAdmin, IsDoctor
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import DoctorFilter, DepartmentFilter


class DepartmentViewSet(viewsets.ModelViewSet):
    serializer_class = DepartmentSerializer
    filterset_class = DepartmentFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']

    def get_queryset(self):
        return Department.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAdmin()]


class DoctorViewSet(viewsets.ModelViewSet):
    serializer_class = DoctorSerializer
    filterset_class = DoctorFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['user__first_name', 'user__last_name', 'specialization']
    ordering_fields = ['user__first_name', 'specialization']
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'doctor':
            return Doctor.objects.select_related('user', 'department').filter(user=user)
        return Doctor.objects.select_related('user', 'department').all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        if self.action in ['update', 'partial_update']:
            return [IsAuthenticated(), IsDoctor()]
        if self.action in ['create', 'destroy']:
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated(), IsAdmin()]