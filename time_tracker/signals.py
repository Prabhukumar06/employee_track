from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Attendance, WorkSession

@receiver(post_save, sender=Attendance)
def start_work_timer(sender, instance, created, **kwargs):
    if created:
        WorkSession.objects.create(
            user=instance.user,
            start_time=timezone.now()
        )

@receiver(post_save, sender=WorkSession)
def save_work_session_duration(sender, instance, **kwargs):
    if instance.end_time and not instance.duration:
        instance.duration = instance.end_time - instance.start_time
        instance.save(update_fields=['duration'])

@receiver(post_save, sender=WorkSession)
def save_work_session_duration(sender, instance, **kwargs):
    if instance.end_time and not instance.duration:
        instance.duration = instance.end_time - instance.start_time
        instance.save(update_fields=['duration'])