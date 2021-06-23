# Generated by Django 2.2.18 on 2021-06-22 03:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('handicap', '0008_handicaphistory_trigger_round'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tee',
            name='slope',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(55), django.core.validators.MaxValueValidator(155)]),
        ),
    ]
