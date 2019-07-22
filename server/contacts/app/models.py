from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contacts")
    name = models.CharField(max_length=100, blank=True)
    codename = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100, blank=True)
