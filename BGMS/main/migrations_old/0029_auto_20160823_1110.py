# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0028_auto_20160809_0830'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bguser',
            options={'verbose_name': 'User', 'verbose_name_plural': 'Users'},
        ),
        migrations.AlterModelOptions(
            name='tenantuser',
            options={'verbose_name': 'Site User', 'verbose_name_plural': 'Site Users'},
        ),
        migrations.AlterField(
            model_name='bguser',
            name='email',
            field=models.EmailField(help_text='Required.', unique=True, verbose_name='email address', error_messages={'unique': 'User with this email already exists.'}, max_length=254),
        ),
        migrations.AlterField(
            model_name='bguser',
            name='site_groups',
            field=models.ManyToManyField(blank=True, to='main.SiteGroup'),
        ),
        migrations.AlterField(
            model_name='bguser',
            name='username',
            field=models.CharField(null=True, unique=True, verbose_name='username', error_messages={'unique': 'User with this username already exists.'}, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')], max_length=30),
        ),
    ]
