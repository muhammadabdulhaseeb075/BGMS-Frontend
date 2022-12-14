# Generated by Django 2.1 on 2021-04-15 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cemeteryadmin', '0016_auto_20210412_0138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preburialcheck',
            name='burial_certificate',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='preburialcheck',
            name='burial_grant_noi',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='preburialcheck',
            name='grave_details',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='preburialcheck',
            name='grave_on_ground',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='preburialcheck',
            name='gravedigger',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='preburialcheck',
            name='indemnity',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='preburialcheck',
            name='invoice',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='preburialcheck',
            name='noi_details',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='preburialcheck',
            name='notice_of_interment',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='preburialcheck',
            name='signed_off',
            field=models.DateTimeField(null=True),
        ),
    ]
