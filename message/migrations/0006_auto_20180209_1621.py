# Generated by Django 2.0.1 on 2018-02-09 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0005_auto_20180209_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='read_time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='send_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]