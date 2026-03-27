from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import Patient

class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)


    class Meta:
        model = Patient
        exclude = ['id']