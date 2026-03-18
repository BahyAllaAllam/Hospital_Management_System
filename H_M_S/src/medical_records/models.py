from django.db import models
from django.db import models
from patients.models import Patient
from doctors.models import Doctor


class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_records')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='medical_records')
    diagnosis = models.TextField()
    prescription = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient} - {self.diagnosis[:50]}"


class MedicalRecordAttachment(models.Model):
    ATTACHMENT_TYPES = (
        ('xray', 'X-Ray'),
        ('mri', 'MRI'),
        ('sonar', 'Sonar'),
        ('ct', 'CT Scan'),
        ('report', 'Report'),
        ('other', 'Other'),
    )
    record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='attachments')
    attachment_type = models.CharField(max_length=10, choices=ATTACHMENT_TYPES)
    file = models.FileField(upload_to='medical_records/')
    description = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.record} - {self.attachment_type}"