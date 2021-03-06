# Generated by Django 2.2.4 on 2019-10-30 23:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0003_privilege'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrivilegeLookup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('privilege', models.TextField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='UserPrivilege',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('privilege', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.PrivilegeLookup')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Privilege',
        ),
    ]
