# Generated by Django 2.2.18 on 2021-06-23 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('handicap', '0009_auto_20210621_2213'),
    ]

    operations = [
        migrations.AddField(
            model_name='round',
            name='nine_holes',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='round',
            name='differential',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='round',
            name='score1',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='round',
            name='score10',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='round',
            name='score11',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='round',
            name='score12',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='round',
            name='score13',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='round',
            name='score14',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='round',
            name='score15',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='round',
            name='score16',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='round',
            name='score17',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='round',
            name='score18',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='round',
            name='score2',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='round',
            name='score3',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='round',
            name='score4',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='round',
            name='score5',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='round',
            name='score6',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='round',
            name='score7',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='round',
            name='score8',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='round',
            name='score9',
            field=models.IntegerField(null=True),
        ),
    ]