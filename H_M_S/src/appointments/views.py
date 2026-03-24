from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Appointment
from .serializers import AppointmentSerializer
from accounts.permissions import IsAdmin, IsReceptionist, IsPatient, IsDoctor, IsNurse

class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer

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
            # receptionist can only assign or remove a patient
            if 'patient' in request.data:
                patient = request.data.get('patient')
                if patient is None:
                    # remove patient from slot
                    appointment.patient = None
                    appointment.is_available = True
                    appointment.status = 'pending'
                    appointment.save()
                    return Response(AppointmentSerializer(appointment).data)
                elif appointment.is_available:
                    # assign patient to slot
                    appointment.patient_id = patient
                    appointment.is_available = False
                    appointment.status = 'confirmed'
                    appointment.save()
                    return Response(AppointmentSerializer(appointment).data)
                else:
                    return Response(
                        {'error': 'This slot is not available'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            return Response(
                {'error': 'Receptionist can only assign or remove a patient'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().partial_update(request, *args, **kwargs)