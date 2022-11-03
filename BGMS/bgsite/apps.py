from django.apps import AppConfig

class BgsiteConfig(AppConfig):
    name = 'bgsite'
    verbose_name = "Burial Ground Site"

    def ready(self):
        import bgsite.handlers
        import bgsite.signals
