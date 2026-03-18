from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import MedicalRecord, MedicalRecordAttachment
from .serializers import MedicalRecordSerializer, MedicalRecordAttachmentSerializer


class MedicalRecordViewSet(viewsets.ModelViewSet):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated]


class MedicalRecordAttachmentViewSet(viewsets.ModelViewSet):
    queryset = MedicalRecordAttachment.objects.all()
    serializer_class = MedicalRecordAttachmentSerializer
    permission_classes = [IsAuthenticated]