# Generated by Django 4.2.10 on 2024-02-28 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('release_date', models.DateField()),
                ('duration', models.IntegerField()),
                ('trailer_url', models.URLField(blank=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='movie_images/')),
                ('genre', models.CharField(choices=[('none', 'None'), ('action', 'Action'), ('comedy', 'Comedy'), ('drama', 'Drama'), ('horror', 'Horror'), ('romance', 'Romance'), ('sci-fi', 'Science Fiction')], default='none', max_length=100)),
            ],
        ),
    ]
