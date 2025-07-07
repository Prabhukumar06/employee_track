from django.contrib import admin
from django.urls import path, include, re_path
from users.views import CustomLoginView, CustomLogoutView
from core.views import DashboardView, HomePageView, page_not_found
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('tasks/', include('tasks.urls')),
    path('time/', include('time_tracker.urls')),
    path('manager/', include('manager.urls')),
]

handler404 = 'core.views.page_not_found'

if not settings.DEBUG:
    urlpatterns += [re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT})]