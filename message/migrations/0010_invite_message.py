# Generated by Django 2.0.1 on 2018-02-20 06:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0009_invite_is_apply'),
    ]

    operations = [
        migrations.AddField(
            model_name='invite',
            name='message',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='message.Message'),
        ),
    ]
