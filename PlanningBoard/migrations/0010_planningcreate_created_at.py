# Generated by Django 2.0.1 on 2018-02-06 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PlanningBoard', '0009_auto_20180207_0358'),
    ]

    operations = [
        migrations.AddField(
            model_name='planningcreate',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
