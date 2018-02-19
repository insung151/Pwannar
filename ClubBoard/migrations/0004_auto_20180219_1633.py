# Generated by Django 2.0.1 on 2018-02-19 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ClubBoard', '0003_auto_20180219_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='create_post',
            name='recruiting_number',
            field=models.IntegerField(max_length=30, verbose_name='모집 인원'),
        ),
        migrations.AlterField(
            model_name='create_post',
            name='recruiting_period',
            field=models.DateField(verbose_name='모집 마감일 #YYYY-MM-DD 형식으로 입력하세요.'),
        ),
    ]
