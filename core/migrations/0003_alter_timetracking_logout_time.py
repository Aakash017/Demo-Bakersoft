# Generated by Django 3.2.12 on 2022-08-02 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_project_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timetracking',
            name='logout_time',
            field=models.DateTimeField(null=True),
        ),
    ]
