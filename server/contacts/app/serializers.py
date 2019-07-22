# serializers/user.py
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
from .models import Contact

User = get_user_model()


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ("id", "user", "name", "codename", "phone")
        read_only_fields = ("id",)


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    password = serializers.CharField(
        required=True, min_length=8, max_length=128, write_only=True
    )

    class Meta:
        model = User
        fields = ("id", "username", "password")
        write_only_fields = ("password",)
        read_only_fields = ("id",)

    def create(self, data):
        user = User.objects.create(username=data["username"])
        user.set_password(data["password"])
        user.save()
        return user
