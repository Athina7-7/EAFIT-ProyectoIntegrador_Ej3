from django.core.management.base import BaseCommand
from movie.models import Movie
from openai import OpenAI
import numpy as np
import os
from dotenv import load_dotenv

class Command(BaseCommand):
    help = 'Genera embeddings de OpenAI para todas las películas'

    def handle(self, *args, **kwargs):
        # Ruta absoluta al .env
        dotenv_path = r"C:\Users\cliente\Downloads\Taller3P1\TallerIA_PI\openAI.env"
        load_dotenv(dotenv_path)

        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            self.stdout.write(self.style.ERROR(
                f"No se pudo cargar la API Key de OpenAI desde: {dotenv_path}"
            ))
            return

        self.stdout.write(f'API Key cargada correctamente: {api_key[:5]}***')

        client = OpenAI(api_key=api_key)

        movies = Movie.objects.all()
        total = movies.count()
        self.stdout.write(f'Procesando {total} películas...')

        for i, movie in enumerate(movies, start=1):
            try:
                response = client.embeddings.create(
                    input=[movie.description],  # usar description es mejor
                    model="text-embedding-3-small"
                )
                emb_vector = np.array(response.data[0].embedding, dtype=np.float32)
                movie.emb = emb_vector.tobytes()
                movie.save()
                self.stdout.write(f'{i}/{total} - Embedding generado para: {movie.title}')
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error generando embedding para {movie.title}: {e}'))

        self.stdout.write(self.style.SUCCESS('Embeddings generados correctamente.'))
