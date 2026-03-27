from django.db import models
import uuid
from patients.models import Patient
from doctors.models import Doctor


class Appointment(models.Model):
    STATUS = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    )
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=15, choices=STATUS, default='pending')
    is_available = models.BooleanField(default=True)
    reason = models.TextField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [
            ['doctor', 'date', 'time'],
            ['patient', 'date', 'time'],
        ]

    def __str__(self):
        return f"{self.patient} - Dr.{self.doctor} on {self.date}"