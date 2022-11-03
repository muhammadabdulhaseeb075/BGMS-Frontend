from django.db import migrations, models, connection
import django.db.models.deletion

def migrate_event_type(apps, schema_editor):
    if connection.schema_name != 'public':
        EventType = apps.get_model("cemeteryadmin", "EventType")
        EventCategory = apps.get_model("cemeteryadmin", "EventCategory")
        Funeral = EventCategory.objects.get(name="Funeral")
        Digging = EventCategory.objects.get(name="Digging")
        BurialData = EventType.objects.create(name="Burial data", event_category=Funeral, default_duration=60,
                                             event_earliest_time_mon="10:00:00", event_latest_time_mon="16:00:00",
                                             event_earliest_time_tue="10:00:00", event_latest_time_tue="16:00:00",
                                             event_earliest_time_wed="10:00:00", event_latest_time_wed="16:00:00",
                                             event_earliest_time_thu="10:00:00", event_latest_time_thu="16:00:00",
                                             event_earliest_time_fri="10:00:00", event_latest_time_fri="16:00:00",
                                             event_earliest_time_sat="10:00:00", event_latest_time_sat="16:00:00",
                                             event_earliest_time_sun="10:00:00", event_latest_time_sun="16:00:00",
                                             )
        BurialData.save()
        Celebration = EventType.objects.create(name="Celebration", event_category=Digging, default_duration=60,
                                             event_earliest_time_mon="10:00:00", event_latest_time_mon="16:00:00",
                                             event_earliest_time_tue="10:00:00", event_latest_time_tue="16:00:00",
                                             event_earliest_time_wed="10:00:00", event_latest_time_wed="16:00:00",
                                             event_earliest_time_thu="10:00:00", event_latest_time_thu="16:00:00",
                                             event_earliest_time_fri="10:00:00", event_latest_time_fri="16:00:00",
                                             event_earliest_time_sat="10:00:00", event_latest_time_sat="16:00:00",
                                             event_earliest_time_sun="10:00:00", event_latest_time_sun="16:00:00",
                                             )
        Celebration.save()

def reverse_migrate_event_type(apps, schema_editor):
    if connection.schema_name != 'public':
        EventType = apps.get_model("bgsite", "EventType")
        EventType.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('cemeteryadmin', '0013_funeralevent_authority_for_interment'),
    ]

    operations = [
        migrations.RunPython(
            code=migrate_event_type,
            reverse_code=reverse_migrate_event_type,
        ),
    ]
