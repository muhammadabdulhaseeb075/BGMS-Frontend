# Generated by Django 2.1 on 2019-05-17 13:05

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('geometriespublic', '0003_auto_20190517_0904'),
    ]

    operations = [
        migrations.CreateModel(
            name='DefaultSurveyTemplateField',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('optional', models.BooleanField(default=True)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geometriespublic.FieldType')),
            ],
        ),
    ]