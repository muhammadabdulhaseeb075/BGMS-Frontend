from django.apps import AppConfig

class GeometriesConfig(AppConfig):
    name = 'geometries'
    verbose_name = "Geometries"

    def ready(self):
        import geometries.signals
