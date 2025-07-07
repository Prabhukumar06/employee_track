from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from tasks.models import Task
from time_tracker.models import WorkSession, Attendance
from datetime import timedelta
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

class HomePageView(TemplateView):
    template_name = 'home.html'

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.role == 'MGR':
            return redirect(reverse_lazy('manager_dashboard'))
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        
        today_sessions = WorkSession.objects.filter(
            user=self.request.user,
            start_time__date=today
        )
        total_duration = sum(
            ((s.duration if s.duration else timezone.now() - s.start_time) 
            for s in today_sessions), timedelta()
        )
        
        context.update({
            'tasks': Task.objects.filter(user=self.request.user),
            'total_duration': total_duration,
            'attendance': Attendance.objects.filter(user=self.request.user, date=today).first()
        })
        return context

def page_not_found(request, exception):
    return render(request, '404.html', status=404)
