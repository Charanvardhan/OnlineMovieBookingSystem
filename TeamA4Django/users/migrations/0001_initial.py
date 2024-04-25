# Generated by Django 5.0.3 on 2024-04-23 21:16

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Admin",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user_id", models.CharField(max_length=100)),
                ("password", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Bookings",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("booking_number", models.IntegerField(unique=True)),
                ("ticket_number", models.IntegerField()),
                ("availability", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Movie",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100, unique=True)),
                ("description", models.TextField(default="None", max_length=200)),
                ("cast", models.TextField(default="None", max_length=100)),
                ("producer", models.TextField(default="None", max_length=100)),
                ("director", models.TextField(default="None", max_length=100)),
                ("review", models.TextField(default="None", max_length=200)),
                ("release_date", models.DateField()),
                ("duration", models.IntegerField()),
                ("trailer_url", models.URLField(blank=True)),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="static/assets/img/gallery"
                    ),
                ),
                (
                    "genre",
                    models.CharField(
                        choices=[
                            ("none", "None"),
                            ("action", "Action"),
                            ("comedy", "Comedy"),
                            ("drama", "Drama"),
                            ("horror", "Horror"),
                            ("romance", "Romance"),
                            ("sci-fi", "Science Fiction"),
                        ],
                        default="none",
                        max_length=100,
                    ),
                ),
                (
                    "rating",
                    models.CharField(
                        choices=[
                            ("none", "None"),
                            ("g", "G"),
                            ("pg", "PG"),
                            ("pg13", "PG13"),
                            ("r", "R"),
                        ],
                        default="none",
                        max_length=100,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("nowPlaying", "Now Playing"),
                            ("comingSoon", "Coming Soon"),
                        ],
                        default="nowPlaying",
                        max_length=100,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Promotions",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code", models.CharField(max_length=100, unique=True)),
                ("percentage", models.IntegerField()),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("show", models.CharField(max_length=100)),
                ("is_available", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Showroom",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("seats", models.IntegerField()),
                ("showroom_number", models.IntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Ticket",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("ticket_number", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="TicketPrices",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("adult_tickets", models.IntegerField()),
                ("senior_tickets", models.IntegerField()),
                ("child_tickets", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Customer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                ("password", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254, unique=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Active", "Active"),
                            ("Inactive", "Inactive"),
                            ("Suspended", "Suspended"),
                        ],
                        default="Active",
                        max_length=10,
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CreditCard",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name_on_card", models.CharField(blank=True, max_length=100)),
                ("card_number", models.CharField(blank=True, max_length=16)),
                ("cvv", models.CharField(blank=True, max_length=4)),
                ("expiration", models.CharField(blank=True, max_length=5)),
                ("address_line_1", models.CharField(blank=True, max_length=255)),
                ("address_line_2", models.CharField(blank=True, max_length=255)),
                ("apartment_suite", models.CharField(blank=True, max_length=255)),
                ("city", models.CharField(blank=True, max_length=100)),
                ("state_province", models.CharField(blank=True, max_length=100)),
                ("country", models.CharField(blank=True, max_length=50)),
                ("zip_postal_code", models.CharField(blank=True, max_length=12)),
                (
                    "customer",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="users.customer",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Showtimes",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField(default=django.utils.timezone.now)),
                (
                    "time_slot",
                    models.CharField(
                        choices=[
                            ("Morning", "09:00-12:00"),
                            ("Afternoon", "12:00-15:00"),
                            ("Evening", "15:00-18:00"),
                            ("Night", "18:00-21:00"),
                        ],
                        default="Morning",
                        max_length=15,
                    ),
                ),
                (
                    "showroom",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="users.showroom",
                    ),
                ),
            ],
            options={
                "unique_together": {("date", "time_slot", "showroom")},
            },
        ),
        migrations.CreateModel(
            name="Show",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("show_id", models.IntegerField(unique=True)),
                (
                    "movie",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="users.movie",
                    ),
                ),
                (
                    "showroom",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="users.showroom",
                    ),
                ),
                (
                    "showtime",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="users.showtimes",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254)),
                ("password", models.CharField(blank=True, max_length=100, null=True)),
                ("address_line_1", models.CharField(blank=True, max_length=255)),
                ("address_line_2", models.CharField(blank=True, max_length=255)),
                ("apartment_suite", models.CharField(blank=True, max_length=255)),
                ("city", models.CharField(blank=True, max_length=100)),
                ("state_province", models.CharField(blank=True, max_length=100)),
                ("country", models.CharField(blank=True, max_length=50)),
                ("zip_postal_code", models.CharField(blank=True, max_length=12)),
                ("name_on_card", models.CharField(blank=True, max_length=100)),
                ("card_number", models.CharField(blank=True, max_length=16)),
                ("expiration", models.CharField(blank=True, max_length=5)),
                ("cvv", models.CharField(blank=True, max_length=4)),
                (
                    "billing_zip_postal_code",
                    models.CharField(blank=True, max_length=12),
                ),
                ("subscribe_to_promotions", models.BooleanField(default=False)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
