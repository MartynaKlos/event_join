# Generated by Django 3.2.8 on 2021-10-31 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events_app', '0002_alter_event_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='is_private',
            field=models.BooleanField(default=False, verbose_name='Private'),
        ),
    ]
