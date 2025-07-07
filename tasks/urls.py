from django.urls import path
from .views import TaskListView, TaskCreateView, UpdateTaskStatusView, AdminTaskListView

urlpatterns = [
    path('', TaskListView.as_view(), name='task-list'),
    path('new/', TaskCreateView.as_view(), name='task-create'),
    path('<int:pk>/update_status/', UpdateTaskStatusView.as_view(), name='update_task_status'),
    path('admin_pannel/', AdminTaskListView.as_view(), name='admin_pannel'),
]