from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from time_tracker.models import Attendance, WorkSession

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        if self.request.user.role == 'MGR':
            return reverse_lazy('manager_dashboard')
        return reverse_lazy('dashboard')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        today = timezone.now().date()
        if not Attendance.objects.filter(user=self.request.user, date=today).exists():
            Attendance.objects.create(user=self.request.user)
        return response

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                latest_session = WorkSession.objects.filter(user=request.user, end_time__isnull=True).latest('start_time')
                latest_session.end_time = timezone.now()
                latest_session.save()
            except WorkSession.DoesNotExist:
                pass
        return super().dispatch(request, *args, **kwargs)