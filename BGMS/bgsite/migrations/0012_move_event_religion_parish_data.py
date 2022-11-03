# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models, connection
import main.validators


def move_religion(apps, schema_editor):

    if connection.schema_name != 'public':
        
        Death = apps.get_model("bgsite", "Death")
        NewReligion = apps.get_model("bgsite", "NewReligion")
        
        persons_with_religion = Death.objects.filter(religion__isnull=False)
        
        for person in persons_with_religion:
            try:
                religion = person.religion.religion
                
                existing_religion = NewReligion.objects.filter(religion=religion)
                
                if existing_religion:
                    person.newreligion=existing_religion[0]
                else:
                    new_religion = NewReligion.objects.create(religion=religion)
                    person.newreligion=new_religion
                    
                person.save()
            except:
                continue

def move_parish(apps, schema_editor):

    if connection.schema_name != 'public':
        
        Death = apps.get_model("bgsite", "Death")
        NewParish = apps.get_model("bgsite", "NewParish")
        
        persons_with_parish = Death.objects.filter(parish__isnull=False)
        
        for person in persons_with_parish:
            try:
                parish = person.parish.parish
                
                existing_parish = NewParish.objects.filter(parish=parish)
                
                if existing_parish:
                    person.newparish=existing_parish[0]
                else:
                    new_parish = NewParish.objects.create(parish=parish)
                    person.newparish=new_parish
                    
                person.save()
            except:
                continue

def move_event(apps, schema_editor):

    if connection.schema_name != 'public':
        
        Death = apps.get_model("bgsite", "Death")
        NewEvent = apps.get_model("bgsite", "NewEvent")
        
        persons_with_event = Death.objects.filter(event__isnull=False)
        
        for person in persons_with_event:
            try:
                event_name = person.event.name
                event_description = None
                
                existing_event = NewEvent.objects.filter(name=event_name, description=event_description)
                
                if existing_event:
                    person.newevent=existing_event[0]
                else:
                    new_event = NewEvent.objects.create(name=event_name, description=event_description)
                    person.newevent=new_event
                
                if person.event.description:
                    if person.death_cause:
                        person.death_cause = person.death_cause + ' ' + person.event.description
                    else:
                        person.death_cause = person.event.description
                
                person.save()
            except:
                continue

class Migration(migrations.Migration):

    dependencies = [
        ('bgsite', '0011_auto_20181026_0918'),
    ]

    operations = [
        migrations.RunPython(
            code=move_religion,
            reverse_code=None,
            atomic=True,
        ),
        migrations.RunPython(
            code=move_parish,
            reverse_code=None,
            atomic=True,
        ),
        migrations.RunPython(
            code=move_event,
            reverse_code=None,
            atomic=True,
        ),
    ]
