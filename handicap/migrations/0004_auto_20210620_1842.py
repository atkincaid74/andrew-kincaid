# Generated by Django 2.2.18 on 2021-06-20 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('handicap', '0003_tee_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='round',
            name='differential',
            field=models.FloatField(default=-1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='round',
            name='gross',
            field=models.IntegerField(default=-1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='round',
            name='score_in',
            field=models.IntegerField(default=-1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='round',
            name='score_out',
            field=models.IntegerField(default=-1),
            preserve_default=False,
        ),
    ]
