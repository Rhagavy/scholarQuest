# Generated by Django 4.1.1 on 2022-10-29 16:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scholarquest_app', '0004_alter_course_totalmidterms_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='grade',
            field=models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='grade',
            field=models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='status',
            field=models.CharField(choices=[('assignment', 'Assignment'), ('midterm', 'MidTerm'), ('finalexam', 'FinalExam')], default='in-progress', max_length=50),
        ),
    ]
