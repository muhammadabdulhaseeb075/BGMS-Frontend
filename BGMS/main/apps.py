from django.apps import AppConfig

class MainConfig(AppConfig):
    name = 'main'
    verbose_name = "Burial Ground Site"

    def ready(self):
        import main.signals
