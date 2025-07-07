from django.utils import timezone
from datetime import timedelta
from tasks.models import Task

def handle_carryover():
    yesterday = timezone.now() - timedelta(days=1)
    unfinished_tasks = Task.objects.filter(
        due_date=yesterday.date(),
        status__in=['NS','P']
    )
    for task in unfinished_tasks:
        Task.objects.create(
            title=task.title + " (Carryover)",
            description=task.description,
            user=task.user,
            is_carryover=True,
            due_date=timezone.now().date()
        )
