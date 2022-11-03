from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models

# Create your models here.
class Report(models.Model):
    name = models.CharField(max_length=100)
    table_schema = JSONField()# ArrayField(models.CharField(max_length=100))
    creation_date = models.DateTimeField(auto_now_add=True)
