from django.views.generic import TemplateView, CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.hashers import make_password
from users.mixins import ManagerRequiredMixin
from users.models import CustomUser
from tasks.models import Task
from time_tracker.models import WorkSession, Attendance
from .forms import TaskAssignmentForm, UserCreationForm
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from datetime import timedelta

class ManagerLoginView(LoginView):
    template_name = 'manager/login.html'

    def get_success_url(self):
        return reverse_lazy('manager_dashboard')

class ManagerDashboardView(ManagerRequiredMixin, TemplateView):
    template_name = "manager/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employees = CustomUser.objects.filter(role='EMP')
        employee_data = {}
        for employee in employees:
            tasks = Task.objects.filter(user=employee)
            work_sessions = WorkSession.objects.filter(user=employee).order_by('-start_time')
            attendance_records = Attendance.objects.filter(user=employee).order_by('-date')

            total_duration = timedelta()
            for session in work_sessions:
                if session.duration:
                    total_duration += session.duration
                elif session.end_time is None and session.start_time.date() == timezone.now().date():
                    total_duration += (timezone.now() - session.start_time)

            employee_data[employee] = {
                'tasks': tasks,
                'work_sessions': work_sessions,
                'attendance_records': attendance_records,
                'total_work_duration': total_duration,
            }
        context['employee_data'] = employee_data
        context['task_assignment_form'] = TaskAssignmentForm()
        return context

    def post(self, request, *args, **kwargs):
        form = TaskAssignmentForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = form.cleaned_data['employee']
            task.save()
            return redirect('manager_dashboard')
        return self.get(request, *args, **kwargs)

class CreateUserView(ManagerRequiredMixin, CreateView):
    model = CustomUser
    form_class = UserCreationForm
    template_name = 'manager/create_user.html'
    success_url = reverse_lazy('manager_dashboard')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.password = make_password(form.cleaned_data['password'])
        user.save()
        return super().form_valid(form)
