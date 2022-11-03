from django.apps import AppConfig


class Config(AppConfig):
    name = 'dataentry'
 
    def ready(self):
        import dataentry.signals
