from django.core.management.base import BaseCommand
from users.models import Show, Showtimes, Movie, Showroom

class Command(BaseCommand):
    help = 'Populate the Show model with sample data'

    def handle(self, *args, **kwargs):
        # Create Show objects
        populate_shows = [
            {
                'movie_title': 'Interstellar',
                'showtime_date': '2024-05-01',
                'showtime_slot': 'Morning 09:00-12:00',
                'showroom_number': 1,
            },
            {
                'movie_title': 'Fast and Furious X',
                'showtime_date': '2024-05-02',
                'showtime_slot': 'Afternoon 12:00-15:00',
                'showroom_number': 2,
            },
            # Add more show data as needed
        ]

        # for movie_data in populate_running_movies:
        #     title = movie_data.pop('title')  # Remove 'title' key from movie_data
        #     movie, created = Movie.objects.get_or_create(title=title, defaults=movie_data)
        #     ###movie = form.save() when the admin adds stuff on the site (html way), how do i get the title to be the
            

        #     if created:
        #         success_message = f'Successfully added movie: {title}'
        #         self.stdout.write(self.style.SUCCESS(success_message))
        #     else:
        #         warning_message = f'Movie already exists: {title}'
        #         self.stdout.write(self.style.WARNING(warning_message))

        for show_data in populate_shows:
            # Get movie object
            movie_title = show_data.pop('movie_title')
            movie = Movie.objects.get(title=movie_title)

            # Get showroom object
            showroom_number = show_data.pop('showroom_number')
            showroom = Showroom.objects.get(showroom_number=showroom_number)

            # Get or create showtime object
            showtime_date = show_data.pop('showtime_date')
            showtime_slot = show_data.pop('showtime_slot')
            showtime, _ = Showtimes.objects.get_or_create(date=showtime_date, time_slot=showtime_slot, showroom=showroom)

            show = Show.objects.create(movie=movie, showroom=showroom, showtime=showtime)
            self.stdout.write(self.style.SUCCESS(f'Successfully added show for movie: {movie_title}'))

