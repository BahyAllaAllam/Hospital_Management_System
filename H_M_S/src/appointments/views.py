from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .models import Appointment
from rest_framework.response import Response
from .serializers import AppointmentSerializer, AppointmentSlotSerializer
from accounts.permissions import IsAdmin, IsReceptionist, IsPatient, IsDoctor, IsNurse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import AppointmentFilter


class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    filterset_class = AppointmentFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['patient__user__first_name', 'patient__user__last_name', 'doctor__user__first_name']
    ordering_fields = ['date', 'time', 'status']

    def get_serializer_class(self):
        if self.action == 'create':
            return AppointmentSlotSerializer
        return AppointmentSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'patient':
            return Appointment.objects.select_related(
                'patient__user', 'doctor__user'
            ).filter(patient__user=user)
        if user.role == 'doctor':
            return Appointment.objects.select_related(
                'patient__user', 'doctor__user'
            ).filter(doctor__user=user)
        return Appointment.objects.select_related(
            'patient__user', 'doctor__user'
        ).all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        if self.action in ['update', 'partial_update']:
            return [IsAuthenticated(), IsReceptionist()]
        if self.action in ['create', 'destroy']:
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated(), IsAdmin()]

    def partial_update(self, request, *args, **kwargs):
        appointment = self.get_object()
        user = request.user

        if user.role == 'receptionist':
            allowed_fields = {'patient', 'reason', 'notes'}
            if set(request.data.keys()) - allowed_fields:
                return Response(
                    {'error': 'Receptionist can only assign a patient, reason and notes'},
                    status=status.HTTP_403_FORBIDDEN
                )
            if 'patient' in request.data:
                patient = request.data.get('patient')
                if patient is None:
                    appointment.patient = None
                    appointment.is_available = True
                    appointment.status = 'pending'
                    appointment.reason = ''
                    appointment.notes = ''
                    appointment.save()
                    return Response(AppointmentSerializer(appointment).data)
                elif appointment.is_available:
                    appointment.patient_id = patient
                    appointment.is_available = False
                    appointment.status = 'confirmed'
                    appointment.reason = request.data.get('reason', '')
                    appointment.notes = request.data.get('notes', '')
                    appointment.save()
                    return Response(AppointmentSerializer(appointment).data)
                else:
                    return Response(
                        {'error': 'This slot is not available'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
        return super().partial_update(request, *args, **kwargs)