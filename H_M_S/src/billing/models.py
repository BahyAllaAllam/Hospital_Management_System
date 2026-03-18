from django.db import models
from patients.models import Patient
from appointments.models import Appointment
from accounts.models import User


class Invoice(models.Model):
    STATUS = (
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid'),
        ('refunded', 'Refunded'),
    )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS, default='unpaid')
    refunded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='refunds')
    refund_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Invoice - {self.patient} - {self.total}"


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.description} - {self.amount}"