# Generated by Django 2.0.1 on 2018-02-08 03:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0003_auto_20180202_1701'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(blank=True, max_length=20, null=True)),
                ('leader', models.BooleanField(default=False)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=20)),
                ('project_name', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('end_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='member',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='team.Team'),
        ),
    ]