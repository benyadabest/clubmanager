# Generated by Django 4.1 on 2023-05-27 21:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('athletes', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='eventsignup',
            unique_together={('athlete', 'event')},
        ),
    ]
