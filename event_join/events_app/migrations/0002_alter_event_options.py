# Generated by Django 3.2.8 on 2021-10-23 11:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['start_date']},
        ),
    ]
