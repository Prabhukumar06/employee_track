from django.db import models
from users.models import CustomUser

class Task(models.Model):
    STATUS_CHOICES = [
        ('NS', 'Not Started'),
        ('P', 'Pending'),
        ('C', 'Complete')
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='NS')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateField(null=True, blank=True)
    is_carryover = models.BooleanField(default=False)
