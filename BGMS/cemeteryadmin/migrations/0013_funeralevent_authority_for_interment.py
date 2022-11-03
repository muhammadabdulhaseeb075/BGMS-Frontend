from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bgsite', '0046_authorityforinterment'),
        ('cemeteryadmin', '0012_funeralevent_meeting_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='funeralevent',
            name='authority_for_interment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='authority_for_interment', to='bgsite.AuthorityForInterment'),
        ),
    ]
