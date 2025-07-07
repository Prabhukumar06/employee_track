from django.urls import path
from .views import ManagerDashboardView, CreateUserView, ManagerLoginView

urlpatterns = [
    path('login/', ManagerLoginView.as_view(), name='manager_login'),
    path('dashboard/', ManagerDashboardView.as_view(), name='manager_dashboard'),
    path('create-user/', CreateUserView.as_view(), name='create_user'),
]
