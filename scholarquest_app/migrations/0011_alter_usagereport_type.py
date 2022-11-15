# Generated by Django 4.1.1 on 2022-11-14 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scholarquest_app', '0010_usagereport_graphimage_usagereport_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usagereport',
            name='type',
            field=models.CharField(choices=[('daily', 'Daily'), ('monthly', 'Monthly'), ('institution', 'Institution'), ('weekly', 'Weekly')], max_length=100),
        ),
    ]
