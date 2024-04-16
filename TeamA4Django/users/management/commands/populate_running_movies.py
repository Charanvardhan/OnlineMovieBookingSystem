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
                'cast': 'Matthew McConaughey as Joseph "Coop" Cooper. Anne Hathaway as Dr. Amelia Brand, Jessica Chastain as Murphy "Murph" Cooper (adult), Mackenzie Foy as Murphy "Murph" Cooper (young), Michael Caine as Professor John Brand, Casey Affleck as Tom Cooper, Timothée Chalamet as Tom Cooper (15 years old)',
                'producer': 'Christopher Nolan',
                'director': 'Christopher Nolan',
                'review': 'Critics praised its ambitious storytelling, visuals, performances, and Hans Zimmers musical score. However, some criticized its lengthy runtime and complex plot. ',
                'release_date': '2024-01-01',
                'duration': 180,
                'trailer_url': 'https://www.youtube.com/embed/4T4wxDnTYLg',
                'genre': 'sci-fi',
                'image': 'static/assets/img/gallery/interstellar.png',  # Path to the image file
                'rating': 'pg13',
                'status': 'nowPlaying',
                # 'isPlaying': True
            },
            {
                'title': 'Fast and Furious X',
                'description': 'Over many missions and against impossible odds, Dom Toretto and his family have outsmarted and outdriven every foe in their path. Now, they must confront the most lethal opponent they haveve ever faced. Over many missions and against impossible odds, Dom Toretto and his family have outsmarted and outdriven every foe in their path. Now, they must confront the most lethal opponent they have ever faced.',
                'cast': 'Matthew McConaughey as Joseph "Coop" Cooper. Anne Hathaway as Dr. Amelia Brand, Jessica Chastain as Murphy "Murph" Cooper (adult), Mackenzie Foy as Murphy "Murph" Cooper (young), Michael Caine as Professor John Brand, Casey Affleck as Tom Cooper, Timothée Chalamet as Tom Cooper (15 years old)',
                'producer': 'Christopher Nolan',
                'director': 'Christopher Nolan',
                'review': 'Critics praised its ambitious storytelling, visuals, performances, and Hans Zimmers musical score. However, some criticized its lengthy runtime and complex plot. ',
                'release_date': '2024-01-05',
                'duration': 180,
                'trailer_url': 'https://www.youtube  .com/embed/32RAq6JzY-w',
                'genre': 'sci-fi',
                'image': 'static/assets/img/gallery/fastx.png',
                'rating': 'pg13',
                'status': 'nowPlaying',
                # isPlaying :True
            },
            {
                'title': 'Avatar: The Way of the Water',
                'description': 'Jake Sully lives with his newfound family formed on the extrasolar moon Pandora. Once a familiar threat returns to finish what was previously started, Jake must work with Neytiri and the army of the Navi race to protect their home.',
                'cast': 'Sam Worthington as Jake Sully, Zoe Saldana as Neytiri, Sigourney Weaver as Dr. Grace Augustine, Stephen Lang as Colonel Miles Quaritch, and others',
                'producer': 'James Cameron',
                'director': 'James Cameron',
                'review': 'Critics praised its groundbreaking visual effects and immersive world-building. However, opinions on the film\'s story and characters have been more mixed.',
                'release_date': '2024-01-09',
                'duration': 195,
                'trailer_url': 'https://www.youtube.com/embed/d9MyW72ELq0',
                'genre': 'Action, Adventure, Sci-Fi',
                'image': 'static/assets/img/gallery/avatar.png',
                'rating': 'PG-13',
                'status': 'nowPlaying',
            }
        ]

        for movie_data in populate_running_movies:
            title = movie_data.pop('title')  # Remove 'title' key from movie_data
            movie, created = Movie.objects.get_or_create(title=title, defaults=movie_data)
            ###movie = form.save() when the admin adds stuff on the site (html way), how do i get the title to be the
            

            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully added movie: {title}'))
            else:
                self.stdout.write(self.style.WARNING(f'Movie already exists: {title}'))

        return populate_running_movies

    #return movies 
