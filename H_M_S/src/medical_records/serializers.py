from rest_framework import serializers
from .models import MedicalRecord, MedicalRecordAttachment

class MedicalRecordAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecordAttachment
        fields = '__all__'

class MedicalRecordSerializer(serializers.ModelSerializer):
    attachments = MedicalRecordAttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = MedicalRecord
        fields = '__all__'