# Generated by Django 2.0.1 on 2018-02-16 06:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PlanningBoard', '0021_comment_planning'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='planning',
            new_name='detail',
        ),
    ]
