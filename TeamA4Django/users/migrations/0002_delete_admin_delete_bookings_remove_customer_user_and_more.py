# Generated by Django 5.0.3 on 2024-04-24 15:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Admin",
        ),
        migrations.DeleteModel(
            name="Bookings",
        ),
        migrations.RemoveField(
            model_name="customer",
            name="user",
        ),
        migrations.RemoveField(
            model_name="creditcard",
            name="customer",
        ),
        migrations.DeleteModel(
            name="Promotions",
        ),
        migrations.RemoveField(
            model_name="show",
            name="movie",
        ),
        migrations.RemoveField(
            model_name="show",
            name="showroom",
        ),
        migrations.RemoveField(
            model_name="show",
            name="showtime",
        ),
        migrations.RemoveField(
            model_name="showtimes",
            name="showroom",
        ),
        migrations.AlterUniqueTogether(
            name="showtimes",
            unique_together=None,
        ),
        migrations.DeleteModel(
            name="Ticket",
        ),
        migrations.DeleteModel(
            name="TicketPrices",
        ),
        migrations.AddField(
            model_name="creditcard",
            name="user_profile",
            field=models.ForeignKey(
                default=1111111111111,
                on_delete=django.db.models.deletion.CASCADE,
                to="users.userprofile",
            ),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name="Customer",
        ),
        migrations.DeleteModel(
            name="Show",
        ),
        migrations.DeleteModel(
            name="Showroom",
        ),
        migrations.DeleteModel(
            name="Showtimes",
        ),
    ]