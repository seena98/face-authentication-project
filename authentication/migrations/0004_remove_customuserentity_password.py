# Generated by Django 2.2 on 2020-11-05 19:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_auto_20201105_1904'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuserentity',
            name='password',
        ),
    ]
