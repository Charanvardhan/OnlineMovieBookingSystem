# Generated by Django 4.2.10 on 2024-03-24 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='subscribe_to_promotions',
            field=models.BooleanField(default=False),
        ),
    ]