# Generated by Django 5.0.3 on 2024-03-25 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_userprofile_email_userprofile_first_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="register_for_promotions",
            field=models.BooleanField(default=False),
        ),
    ]
