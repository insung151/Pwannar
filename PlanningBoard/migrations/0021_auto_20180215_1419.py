# Generated by Django 2.0.1 on 2018-02-15 05:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PlanningBoard', '0020_auto_20180215_1416'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='planning',
            name='invite_url',
        ),
        migrations.RemoveField(
            model_name='planning',
            name='is_invite',
        ),
    ]
