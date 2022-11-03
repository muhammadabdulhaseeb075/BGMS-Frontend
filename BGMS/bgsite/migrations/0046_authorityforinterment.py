from django.db import migrations, models
import main.validators
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('bgsite', '0045_gravedeed_tenure'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthorityForInterment',
            fields=[
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('first_names', models.CharField(blank=True, max_length=200, null=True, validators=[main.validators.bleach_validator], verbose_name='First names')),
                ('last_name', models.CharField(blank=True, max_length=50, null=True, validators=[main.validators.bleach_validator], verbose_name='Last name')),
                ('title', models.CharField(blank=True, max_length=50, null=True, validators=[main.validators.bleach_validator], verbose_name='Title')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
