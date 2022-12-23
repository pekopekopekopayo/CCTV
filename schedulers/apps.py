from django.apps import AppConfig
from django.conf import settings


class SchedulersConfig(AppConfig):
    name = "schedulers"

    def ready(self):
        if settings.SCHEDULER_DEFAULT:
            from schedulers import operator

            operator.start()
