from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import MedicalRecord, DoctorNote, NurseNote, LabResult
from .serializers import MedicalRecordSerializer, DoctorNoteSerializer, NurseNoteSerializer, LabResultSerializer
from accounts.permissions import IsAdmin, IsDoctor, IsNurse, IsLab, IsRadiology, IsPatient
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import MedicalRecordFilter, DoctorNoteFilter, NurseNoteFilter, LabResultFilter


class MedicalRecordViewSet(viewsets.ModelViewSet):
    serializer_class = MedicalRecordSerializer
    filterset_class = MedicalRecordFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['patient__user__first_name', 'patient__user__last_name']
    ordering_fields = ['created_at']

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
    filterset_class = DoctorNoteFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['diagnosis', 'prescription']
    ordering_fields = ['created_at']

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
    filterset_class = NurseNoteFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = ['created_at']

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
    filterset_class = LabResultFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['description']
    ordering_fields = ['created_at', 'result_type']

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