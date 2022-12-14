# Generated by Django 2.2.9 on 2022-01-31 16:07

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0031_delete_meetinglocation'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReferenceNumStyles',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('ref_style_format', models.CharField(blank=True, max_length=500, null=True)),
                ('re_style_sample', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
    ]
