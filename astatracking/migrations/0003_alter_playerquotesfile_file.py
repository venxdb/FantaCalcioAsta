# Generated by Django 3.2.5 on 2024-08-11 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('astatracking', '0002_playerquotesfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playerquotesfile',
            name='file',
            field=models.FileField(upload_to='static/player_quotes/'),
        ),
    ]
