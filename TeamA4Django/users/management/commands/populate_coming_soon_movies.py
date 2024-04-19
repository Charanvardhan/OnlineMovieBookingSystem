from django.core.management.base import BaseCommand
from users.models import Movie

class Command(BaseCommand):
    help = 'Populate the Movie model with sample data'

    def handle(self, *args, **kwargs):
        # Create Movie objects
        populate_coming_soon_movies = [
            {
                
                'title': 'Barbie',
                'description': 'Join Barbie, portrayed by Margot Robbie, on a thrilling adventure as she embarks on a quest to save her kingdom from an evil sorcerer.',
                'cast': 'Margot Robbie as Barbie, Ryan Gosling as Ken',
                'producer': 'Warner Bros. Pictures',
                'director': 'Greta Gerwig',
                'review': 'Critics are praising Margot Robbie\'s performance as Barbie and the film\'s captivating storyline. It\'s a delightful family-friendly movie that everyone will enjoy!',
                'release_date': '2024-07-01',
                'duration': 130,
                'trailer_url': 'https://www.youtube.com/embed/your-trailer-url',
                'genre': 'Adventure, Fantasy',
                'image': 'static/assets/img/gallery/barbie_margot_robbie.png',
                'rating': 'pg13',
                'status': 'comingSoon',
            },
            {
                'title': 'Oppenheimer',
                'description': 'Discover the fascinating story of J. Robert Oppenheimer, the brilliant physicist who led the Manhattan Project, the research and development project that produced the first atomic bombs during World War II.',
                'cast': 'Cillian Murphy, Florence Pugh',
                'producer': 'Paramount Pictures',
                'director': 'Christopher Nolan',
                'review': 'Critics are hailing "Oppenheimer" as a masterpiece, praising Christopher Nolan\'s direction and the stellar performances of the cast. It offers a gripping portrayal of one of the most significant events in modern history.',
                'release_date': '2024-10-15',
                'duration': 160,
                'trailer_url': 'https://www.youtube.com/embed/your-trailer-url',
                'genre': 'Biography, Drama, History',
                'image': 'assets/img/gallery/oppenheimer.png',
                'rating': 'R',
                'status': 'comingSoon',
            },
          
        ]

        for movie_data in populate_coming_soon_movies:
            title = movie_data.pop('title')  # Remove 'title' key from movie_data
            movie, created = Movie.objects.get_or_create(title=title, defaults=movie_data)
            ###movie = form.save() when the admin adds stuff on the site (html way), how do i get the title to be the
            

            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully added movie: {title}'))
            else:
                self.stdout.write(self.style.WARNING(f'Movie already exists: {title}'))

        return populate_coming_soon_movies

    #return movies 
