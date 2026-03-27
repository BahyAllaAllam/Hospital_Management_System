from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'groups', 'user_permissions', 'is_superuser',
                   'is_staff', 'last_login', 'id']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        exclude = ['groups', 'user_permissions', 'is_superuser', 'is_staff',
                   'last_login', 'id']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user