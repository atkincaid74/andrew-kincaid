# Generated by Django 2.2.4 on 2019-08-11 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ValidEmails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('paid', models.BooleanField()),
                ('date_added', models.DateTimeField()),
                ('date_paid', models.DateTimeField()),
            ],
        ),
    ]
