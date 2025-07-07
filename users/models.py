from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('EMP', 'Employee'),
        ('MGR', 'Manager')
    ]
    role = models.CharField(max_length=3, choices=ROLE_CHOICES, default='EMP')
