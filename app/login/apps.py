from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = 'login'

    def ready(self):
        import login.signals