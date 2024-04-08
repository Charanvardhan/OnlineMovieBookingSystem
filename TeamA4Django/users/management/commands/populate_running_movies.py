from django.core.management.base import BaseCommand
from users.models import Movie

class Command(BaseCommand):
    help = 'Populate the Movie model with sample data'

    def handle(self, *args, **kwargs):
        # Create Movie objects
        populate_running_movies = [
            {
                'title': 'Interstellar',
                'description': 'When Earth becomes uninhabitable in the future, a farmer and ex-NASA pilot, Joseph Cooper, is tasked to pilot a spacecraft, along with a team of researchers, to find a new planet for humans.',
                'release_date': '2024-01-01',
                'duration': 180,
                'trailer_url': 'https://www.youtube.com/embed/4T4wxDnTYLg',
                'genre': 'sci-fi',
                'image': 'static/assets/img/gallery/interstellar.png',  # Path to the image file
            },
            {
                'title': 'Fast and Furious X',
                'description': 'Over many missions and against impossible odds, Dom Toretto and his family have outsmarted and outdriven every foe in their path. Now, they must confront the most lethal opponent they haveve ever faced. Over many missions and against impossible odds, Dom Toretto and his family have outsmarted and outdriven every foe in their path. Now, they must confront the most lethal opponent they have ever faced.',
                'release_date': '2024-01-05',
                'duration': 180,
                'trailer_url': 'https://www.youtube  .com/embed/32RAq6JzY-w',
                'genre': 'sci-fi',
                'image': 'static/assets/img/gallery/fastx.png',
            },
            {
                'title': 'Avatar: the Way of the Water',
                'description': 'Jake Sully lives with his newfound family formed on the extrasolar moon Pandora. Once a familiar threat returns to finish what was previously started, Jake must work with Neytiri and the army of the Navi race to protect their home.',
                'release_date': '2024-01-09',
                'duration': 195,
                'trailer_url': 'https://www.youtube.com/embed/d9MyW72ELq0',
                'genre': 'sci-fi',
                'image': 'static/assets/img/gallery/avatar.png',
            }
            # Add more movie data as needed
        ]

        for movie_data in populate_running_movies:
            title= movie_data.pop('title')  # Remove 'title' key from movie_data
            movie, created = Movie.objects.get_or_create(title=title, defaults=movie_data)
            ###movie = form.save() when the admin adds stuff on the site (html way), how do i get the title to be the
            

            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully added movie: {movie.title}'))
            else:
                self.stdout.write(self.style.WARNING(f'Movie already exists: {movie.title}'))
