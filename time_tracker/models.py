from django.db import models
from users.models import CustomUser

class WorkSession(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)

class Attendance(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    login_time = models.DateTimeField(auto_now_add=True)
