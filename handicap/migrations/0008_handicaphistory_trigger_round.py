# Generated by Django 2.2.18 on 2021-06-21 14:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('handicap', '0007_auto_20210621_0754'),
    ]

    operations = [
        migrations.AddField(
            model_name='handicaphistory',
            name='trigger_round',
            field=models.ForeignKey(default=7, on_delete=django.db.models.deletion.CASCADE, to='handicap.Round'),
            preserve_default=False,
        ),
    ]