from django.views.generic import ListView, CreateView
from .models import Task
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from users.mixins import ManagerRequiredMixin

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'tasks/task_list.html'
    
    def get_queryset(self):
        Task.objects.filter(
            user=self.request.user,
            status__in=['NS','P'],
            created_at__date=timezone.now().date() - timedelta(days=1)
        ).update(is_carryover=True)
        
        return Task.objects.filter(user=self.request.user)

from django.urls import reverse_lazy

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'due_date']
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task-list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class UpdateTaskStatusView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk, user=request.user)
        task.status = request.POST.get('status')
        task.save()
        return redirect('dashboard')

class AdminTaskListView(ManagerRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'tasks/admin_task_list.html'

    def get_queryset(self):
        return Task.objects.all()

def generate_report(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="task_report.pdf"'
    
    p = canvas.Canvas(response)
    p.drawString(100, 750, "Task Completion Report")
    p.showPage()
    p.save()
    return response