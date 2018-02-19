# Generated by Django 2.0.1 on 2018-02-09 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0004_message_read_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='message',
            name='read_time',
            field=models.DateField(auto_now=True),
        ),
    ]
