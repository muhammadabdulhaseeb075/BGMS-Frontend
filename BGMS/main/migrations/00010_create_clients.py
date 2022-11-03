from django.db import migrations, models

def create_clients(apps, schema_editor):
    """ Create a default client for each existing site """
    BurialGroundSite = apps.get_model('main', 'BurialGroundSite')
    Client = apps.get_model('main', 'Client')
    for site in BurialGroundSite.objects.all():
        client = Client.objects.create(name=site.name)
        site.client = client
        site.save()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20190321_1239'),
    ]

    operations = [
        migrations.RunPython(create_clients),
    ]