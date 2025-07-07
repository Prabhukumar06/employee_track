from django.apps import AppConfig

class TimeTrackerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'time_tracker'

    def ready(self):
        import time_tracker.signals

    def ready(self):
        import time_tracker.signals
