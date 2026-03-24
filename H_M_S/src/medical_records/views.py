from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import MedicalRecord, DoctorNote, NurseNote, LabResult
from .serializers import MedicalRecordSerializer, DoctorNoteSerializer, NurseNoteSerializer, LabResultSerializer
from accounts.permissions import IsAdmin, IsDoctor, IsNurse, IsLab, IsRadiology, IsPatient

class MedicalRecordViewSet(viewsets.ModelViewSet):
    serializer_class = MedicalRecordSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'patient':
            return MedicalRecord.objects.select_related(
                'patient__user'
            ).prefetch_related(
                'doctor_notes', 'nurse_notes', 'lab_results'
            ).filter(patient__user=user)
        return MedicalRecord.objects.select_related(
            'patient__user'
        ).prefetch_related(
            'doctor_notes', 'nurse_notes', 'lab_results'
        ).all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        if self.action == 'create':
            return [IsAuthenticated(), IsAdmin()]
        if self.action == 'destroy':
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated(), IsAdmin()]


class DoctorNoteViewSet(viewsets.ModelViewSet):
    serializer_class = DoctorNoteSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'doctor':
            return DoctorNote.objects.select_related(
                'record', 'doctor__user'
            ).filter(doctor__user=user)
        return DoctorNote.objects.select_related('record', 'doctor__user').all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated(), IsDoctor()]
        if self.action in ['create', 'update', 'partial_update']:
            return [IsAuthenticated(), IsDoctor()]
        if self.action == 'destroy':
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated(), IsAdmin()]


class NurseNoteViewSet(viewsets.ModelViewSet):
    serializer_class = NurseNoteSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'nurse':
            return NurseNote.objects.select_related(
                'record', 'nurse'
            ).filter(nurse=user)
        return NurseNote.objects.select_related('record', 'nurse').all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated(), IsNurse()]
        if self.action == 'create':
            return [IsAuthenticated(), IsNurse()]
        if self.action in ['update', 'partial_update']:
            return [IsAuthenticated(), IsNurse()]
        if self.action == 'destroy':
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated(), IsAdmin()]

    def update(self, request, *args, **kwargs):
        nurse_note = self.get_object()
        # nurse can only edit her own notes
        if nurse_note.nurse != request.user:
            return Response(
                {'error': 'You can only edit your own notes'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)


class LabResultViewSet(viewsets.ModelViewSet):
    serializer_class = LabResultSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role in ['lab', 'radiology']:
            return LabResult.objects.select_related(
                'record', 'technician'
            ).filter(technician=user)
        return LabResult.objects.select_related('record', 'technician').all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        if self.action in ['create', 'update', 'partial_update']:
            from accounts.permissions import IsLab, IsRadiology
            return [IsAuthenticated(), IsLab() if request.user.role == 'lab' else IsRadiology()]
        if self.action == 'destroy':
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated(), IsAdmin()]

    def update(self, request, *args, **kwargs):
        lab_result = self.get_object()
        # technician can only edit their own results
        if lab_result.technician != request.user:
            return Response(
                {'error': 'You can only edit your own results'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)