from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    ROLES = (
        ('admin', 'Admin'),
        ('supervisor', 'Supervisor'),
        ('doctor', 'Doctor'),
        ('nurse', 'Nurse'),
        ('receptionist', 'Receptionist'),
        ('patient', 'Patient'),
        ('lab', 'Lab Technician'),
        ('radiology', 'Radiology Technician'),
        ('accountant', 'Accountant'),
    )
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    role = models.CharField(max_length=20, choices=ROLES)
    phone = models.CharField(max_length=15, blank=True)