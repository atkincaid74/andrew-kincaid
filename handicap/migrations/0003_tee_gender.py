# Generated by Django 2.2.18 on 2021-06-19 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('handicap', '0002_auto_20210618_2033'),
    ]

    operations = [
        migrations.AddField(
            model_name='tee',
            name='gender',
            field=models.CharField(choices=[('M', 'Men'), ('W', 'Women'), ('B', 'Both')], default='M', max_length=1),
            preserve_default=False,
        ),
    ]
