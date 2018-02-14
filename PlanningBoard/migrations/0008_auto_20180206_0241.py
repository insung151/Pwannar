# Generated by Django 2.0.1 on 2018-02-05 17:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('PlanningBoard', '0007_auto_20180205_2204'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag_Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=20, null=True)),
                ('user', models.ManyToManyField(related_name='tag_language', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag_Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=20, null=True)),
                ('user', models.ManyToManyField(related_name='tag_project', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag_Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=20, null=True)),
                ('user', models.ManyToManyField(related_name='tag_region', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='tag',
            name='user',
        ),
        migrations.RemoveField(
            model_name='planningcreate',
            name='tag',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
        migrations.AddField(
            model_name='planningcreate',
            name='language',
            field=models.ManyToManyField(to='PlanningBoard.Tag_Language'),
        ),
        migrations.AddField(
            model_name='planningcreate',
            name='project',
            field=models.ManyToManyField(to='PlanningBoard.Tag_Project'),
        ),
        migrations.AddField(
            model_name='planningcreate',
            name='region',
            field=models.ManyToManyField(to='PlanningBoard.Tag_Region'),
        ),
    ]
