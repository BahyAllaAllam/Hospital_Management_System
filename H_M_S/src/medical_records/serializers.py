from rest_framework import serializers
from .models import MedicalRecord, DoctorNote, NurseNote, LabResult


class DoctorNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorNote
        fields = '__all__'

class NurseNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = NurseNote
        fields = '__all__'

class LabResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabResult
        fields = '__all__'

class MedicalRecordSerializer(serializers.ModelSerializer):
    doctor_notes = DoctorNoteSerializer(many=True, read_only=True)
    nurse_notes = NurseNoteSerializer(many=True, read_only=True)
    lab_results = LabResultSerializer(many=True, read_only=True)

    class Meta:
        model = MedicalRecord
        fields = '__all__'