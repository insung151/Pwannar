# Generated by Django 2.0.1 on 2018-02-09 03:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PlanningBoard', '0012_auto_20180209_1234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag_region',
            name='province',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='PlanningBoard.Tag_Province'),
        ),
    ]