from django.contrib import admin
from .models import WorkSession

class WorkSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_time', 'duration')
    list_filter = ('user',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

admin.site.register(WorkSession, WorkSessionAdmin)
