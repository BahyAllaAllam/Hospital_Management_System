from rest_framework import serializers
from .models import MedicalRecord, DoctorNote, NurseNote, LabResult


class DoctorNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorNote
        exclude = ['id']

class NurseNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = NurseNote
        exclude = ['id']

class LabResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabResult
        exclude = ['id']

class MedicalRecordSerializer(serializers.ModelSerializer):
    doctor_notes = DoctorNoteSerializer(many=True, read_only=True)
    nurse_notes = NurseNoteSerializer(many=True, read_only=True)
    lab_results = LabResultSerializer(many=True, read_only=True)

    class Meta:
        model = MedicalRecord
        exclude = ['id']