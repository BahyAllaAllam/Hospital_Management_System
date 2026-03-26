from rest_framework import serializers
from .models import Appointment


class AppointmentSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'doctor', 'date', 'time', 'is_available']


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        exclude = ['created_at']