# Generated by Django 4.1.1 on 2022-11-02 01:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scholarquest_app', '0005_course_grade_evaluation_grade_evaluation_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='grade',
            new_name='finalGrade',
        ),
        migrations.AddField(
            model_name='course',
            name='completionProgress',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AddField(
            model_name='course',
            name='currentGrade',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
    ]
