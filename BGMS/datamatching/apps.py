from django.apps import AppConfig


class Config(AppConfig):
    name = 'datamatching'
 
    def ready(self):
        import datamatching.signals
