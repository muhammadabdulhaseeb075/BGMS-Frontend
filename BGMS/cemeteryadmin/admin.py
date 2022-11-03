from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget
from cemeteryadmin.models import Settings


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    formfield_overrides = {
        #fields.JSONField: {'widget': JSONEditorWidget}, # if django < 3.1
        #models.JSONField: {'widget': JSONEditorWidget},
    }

