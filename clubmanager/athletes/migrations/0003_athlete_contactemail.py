# Generated by Django 4.1 on 2023-05-31 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('athletes', '0002_alter_athlete_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='athlete',
            name='contactemail',
            field=models.CharField(default='alla@gmail.com', max_length=250),
            preserve_default=False,
        ),
    ]