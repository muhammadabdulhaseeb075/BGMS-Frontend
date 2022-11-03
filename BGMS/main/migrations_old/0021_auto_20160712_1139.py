# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models, connection

def update_burial_officials(apps, schema_editor):
    # BurialOfficialType = apps.get_model("main", "BurialOfficialType")
    # Burial_Official = apps.get_model("bgsite", "Burial_Official") 
    # BurialGroundSite = apps.get_model("main", "BurialGroundSite")
    # if connection.schema_name == 'public':
    #     if BurialOfficialType.objects.filter(official_type="Ceremony Performed By").exists():
    #         performed_by = BurialOfficialType.objects.get(official_type="Ceremony performed by")
    #         issued_by = BurialOfficialType.objects.get_or_create(official_type="Certificate issued by")[0]
    #         for site in BurialGroundSite.objects.all():
    #             if site.schema_name != 'public':
    #                 connection.schema_name = site.schema_name
    #                 for burial_official in Burial_Official.objects.all():
    #                     if burial_official.burial_official_type:
    #                         type_str = burial_official.burial_official_type.official_type
    #                         if type_str=="Ceremony Performed By" or type_str=="Ceremony Performed by":
    #                             burial_official.burial_official_type = performed_by
    #                             burial_official.official_type = "Ceremony performed by"
    #                             burial_official.save()
    #                         elif type_str=="Certificate Given By" or type_str=="certificate issued by":
    #                             burial_official.burial_official_type = issued_by
    #                             burial_official.official_type = "Certificate issued by"
    #                             burial_official.save()
    #         connection.schema_name ='public'

#     Traceback (most recent call last):
# File "C:\Users\mauricio\Documents\Mauricio\virtualenv\BGMS_DEV\lib\site-packages\django\apps\registry.py", line 148, in get_app_config
#   return self.app_configs[app_label]
# KeyError: 'bgsite'

# During handling of the above exception, another exception occurred:

# Traceback (most recent call last):
# File "C:\Users\mauricio\Documents\Mauricio\GitHub\bgms_anu\BGMS_Anu\BGMS\manage.py", line 10, in <module>
#   execute_from_command_line(sys.argv)
# File "C:\Users\mauricio\Documents\Mauricio\virtualenv\BGMS_DEV\lib\site-packages\django\core\management\__init__.py", line 354, in execute_from_command_line
#   utility.execute()
# File "C:\Users\mauricio\Documents\Mauricio\virtualenv\BGMS_DEV\lib\site-packages\django\core\management\__init__.py", line 346, in execute
#   self.fetch_command(subcommand).run_from_argv(self.argv)
# File "C:\Users\mauricio\Documents\Mauricio\virtualenv\BGMS_DEV\lib\site-packages\django\core\management\commands\test.py", line 30, in run_from_argv
#   super(Command, self).run_from_argv(argv)
# File "C:\Users\mauricio\Documents\Mauricio\virtualenv\BGMS_DEV\lib\site-packages\django\core\management\base.py", line 394, in run_from_argv
#   self.execute(*args, **cmd_options)
# File "C:\Users\mauricio\Documents\Mauricio\virtualenv\BGMS_DEV\lib\site-packages\django\core\management\commands\test.py", line 74, in execute
#   super(Command, self).execute(*args, **options)
# File "C:\Users\mauricio\Documents\Mauricio\virtualenv\BGMS_DEV\lib\site-packages\django\core\management\base.py", line 445, in execute
#   output = self.handle(*args, **options)
# File "C:\Users\mauricio\Documents\Mauricio\virtualenv\BGMS_DEV\lib\site-packages\django\core\management\commands\test.py", line 90, in handle
#   failures = test_runner.run_tests(test_labels)
# File "C:\Users\mauricio\Documents\Mauricio\virtualenv\BGMS_DEV\lib\site-packages\django\test\runner.py", line 210, in run_tests
#   old_config = self.setup_databases()
# File "C:\Users\mauricio\Documents\Mauricio\virtualenv\BGMS_DEV\lib\site-packages\django\test\runner.py", line 166, in setup_databases
#   **kwargs
# File "C:\Users\mauricio\Documents\Mauricio\virtualenv\BGMS_DEV\lib\site-packages\django\test\runner.py", line 370, in setup_databases
#   serialize=connection.settings_dict.get("TEST", {}).get("SERIALIZE", True),
# File "C:\Users\mauricio\Documents\Mauricio\virtualenv\BGMS_DEV\lib\site-packages\django\db\backends\base\creation.py", line 368, in create_test_db
#   test_flush=not keepdb,
# File "C:\Users\mauricio\Documents\Mauricio\virtualenv\BGMS_DEV\lib\site-packages\django\core\management\__init__.py", line 120, in call_command
#   return command.execute(*args, **defaults)
# File "C:\Users\mauricio\Documents\Mauricio\virtualenv\BGMS_DEV\lib\site-packages\django\core\management\base.py", line 445, in execute
#   output = self.handle(*args, **options)
# File "C:\Users\mauricio\Documents\Mauricio\virtualenv\BGMS_DEV\lib\site-packages\tenant_schemas\management\commands\migrate_schemas.py", line 40, in handle
#   self.run_migrations(self.schema_name, settings.SHARED_APPS)
# File "C:\Users\mauricio\Documents\Mauricio\virtualenv\BGMS_DEV\lib\site-packages\tenant_schemas\management\commands\migrate_schemas.py", line 58, in run_migrations
#   command.execute(*self.args, **self.options)
# File "C:\Users\mauricio\Documents\Mauricio\virtualenv\BGMS_DEV\lib\site-packages\django\core\management\base.py", line 445, in execute
#   output = self.handle(*args, **options)
# File "C:\Users\mauricio\Documents\Mauricio\virtualenv\BGMS_DEV\lib\site-packages\django\core\management\commands\migrate.py", line 222, in handle
#   executor.migrate(targets, plan, fake=fake, fake_initial=fake_initial)
# File "C:\Users\mauricio\Documents\Mauricio\virtualenv\BGMS_DEV\lib\site-packages\django\db\migrations\executor.py", line 110, in migrate
#   self.apply_migration(states[migration], migration, fake=fake, fake_initial=fake_initial)
# File "C:\Users\mauricio\Documents\Mauricio\virtualenv\BGMS_DEV\lib\site-packages\django\db\migrations\executor.py", line 148, in apply_migration
#   state = migration.apply(state, schema_editor)
# File "C:\Users\mauricio\Documents\Mauricio\virtualenv\BGMS_DEV\lib\site-packages\django\db\migrations\migration.py", line 115, in apply
#   operation.database_forwards(self.app_label, schema_editor, old_state, project_state)
# File "C:\Users\mauricio\Documents\Mauricio\virtualenv\BGMS_DEV\lib\site-packages\django\db\migrations\operations\special.py", line 183, in database_forwards
#   self.code(from_state.apps, schema_editor)
# File "C:\Users\mauricio\Documents\Mauricio\GitHub\bgms_anu\BGMS_Anu\BGMS\main\migrations\0021_auto_20160712_1139.py", line 8, in update_burial_officials
#   Burial_Official = apps.get_model("bgsite", "Burial_Official")
# File "C:\Users\mauricio\Documents\Mauricio\virtualenv\BGMS_DEV\lib\site-packages\django\apps\registry.py", line 202, in get_model
#   return self.get_app_config(app_label).get_model(model_name.lower())
# File "C:\Users\mauricio\Documents\Mauricio\virtualenv\BGMS_DEV\lib\site-packages\django\apps\registry.py", line 150, in get_app_config
#   raise LookupError("No installed app with label '%s'." % app_label)
# LookupError: No installed app with label 'bgsite'.
    pass
                                   
        
def undo_update_burial_officials(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_burialofficialtype'),
    ]

    operations = [
        migrations.RunPython(
            code=update_burial_officials,
            reverse_code=undo_update_burial_officials,
            atomic=True,
        ),
    ]
