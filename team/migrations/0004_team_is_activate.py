# Generated by Django 2.0.1 on 2018-02-22 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0003_project_project_end'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='is_activate',
            field=models.BooleanField(default=True),
        ),
    ]
