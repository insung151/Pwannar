# Generated by Django 2.0.1 on 2018-02-15 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PlanningBoard', '0019_auto_20180213_1551'),
    ]

    operations = [
        migrations.AddField(
            model_name='planning',
            name='invite_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='planning',
            name='is_invite',
            field=models.BooleanField(default=True),
        ),
    ]
