from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import MedicalRecord, DoctorNote, NurseNote, LabResult
from .serializers import MedicalRecordSerializer, DoctorNoteSerializer, NurseNoteSerializer, LabResultSerializer


class MedicalRecordViewSet(viewsets.ModelViewSet):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated]

class DoctorNoteViewSet(viewsets.ModelViewSet):
    queryset = DoctorNote.objects.all()
    serializer_class = DoctorNoteSerializer
    permission_classes = [IsAuthenticated]

class NurseNoteViewSet(viewsets.ModelViewSet):
    queryset = NurseNote.objects.all()
    serializer_class = NurseNoteSerializer
    permission_classes = [IsAuthenticated]

class LabResultViewSet(viewsets.ModelViewSet):
    queryset = LabResult.objects.all()
    serializer_class = LabResultSerializer
    permission_classes = [IsAuthenticated]