from django.db import models
import uuid
from patients.models import Patient
from doctors.models import Doctor
from accounts.models import User


class MedicalRecord(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_records')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Medical Record - {self.patient}"


class DoctorNote(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='doctor_notes')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    prescription = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Doctor Note - {self.doctor} - {self.record}"


class NurseNote(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='nurse_notes')
    nurse = models.ForeignKey(User, on_delete=models.CASCADE)
    blood_pressure = models.CharField(max_length=20, blank=True)
    sugar_level = models.CharField(max_length=20, blank=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Nurse Note - {self.nurse} - {self.record}"


class LabResult(models.Model):
    TYPES = (
        ('xray', 'X-Ray'),
        ('mri', 'MRI'),
        ('sonar', 'Sonar'),
        ('ct', 'CT Scan'),
        ('blood_test', 'Blood Test'),
        ('urine_test', 'Urine Test'),
        ('other', 'Other'),
    )
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='lab_results')
    technician = models.ForeignKey(User, on_delete=models.CASCADE)
    result_type = models.CharField(max_length=20, choices=TYPES)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='lab_results/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Lab Result - {self.result_type} - {self.record}"
