# Generated by Django 2.1 on 2019-10-03 09:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import main.validators
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_auto_20190613_1353'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPasswordRequests',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_update', models.DateTimeField(auto_now=True, null=True)),
                ('count', models.IntegerField(blank=True, default=0, null=True)),
                ('status', models.TextField(default='Open', max_length=20, validators=[main.validators.bleach_validator])),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='burialgroundsite',
            name='name',
            field=models.CharField(max_length=100, verbose_name='burial ground site name'),
        ),
        migrations.AlterField(
            model_name='sitegroup',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.Group'),
        ),
    ]