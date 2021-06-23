# Generated by Django 2.2.18 on 2021-06-21 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('handicap', '0004_auto_20210620_1842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='round',
            name='differential',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='round',
            name='gross',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='round',
            name='score_in',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='round',
            name='score_out',
            field=models.IntegerField(blank=True),
        ),
    ]
