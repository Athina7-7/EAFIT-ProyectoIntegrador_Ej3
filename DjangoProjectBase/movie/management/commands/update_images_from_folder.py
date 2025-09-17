import os
from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = "Assign images from folder to movies in the database"

    def handle(self, *args, **kwargs):
        images_folder = 'media/movie/images/'
        updated_count = 0

        for movie in Movie.objects.all():
            image_filename = f"m_{movie.title}.png"
            image_path_full = os.path.join(images_folder, image_filename)

            if os.path.exists(image_path_full):
                movie.image = os.path.join('movie/images', image_filename)
                movie.save()
                updated_count += 1
                self.stdout.write(self.style.SUCCESS(f"Updated image for: {movie.title}"))
            else:
                self.stderr.write(f"Image not found for: {movie.title}")

        self.stdout.write(self.style.SUCCESS(f"Finished updating {updated_count} movies with images."))
