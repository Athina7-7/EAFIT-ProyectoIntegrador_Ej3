import os
import numpy as np
from django.core.management.base import BaseCommand
from movie.models import Movie
from openai import OpenAI
from dotenv import load_dotenv

class Command(BaseCommand):
    help = "Compare two movies and optionally a prompt using OpenAI embeddings safely"

    def handle(self, *args, **kwargs):
        # ✅ Cargar API Key de OpenAI
        load_dotenv('../openAI.env')
        client = OpenAI(api_key=os.environ.get('openai_apikey'))

        # ✅ Configura aquí los títulos de las películas y el prompt
        titles = ["A Trip to the Moon", "Cinderella"]  # Títulos que sí existen en tu DB
        prompt = "película sobre fantasía y aventuras" # Prompt para comparar

        # ✅ Buscar películas en la base de datos
        movies = []
        for t in titles:
            movie = Movie.objects.filter(title=t).first()
            if movie:
                movies.append(movie)
            else:
                self.stdout.write(f"❌ La película '{t}' no existe en la base de datos")

        if len(movies) < 2:
            self.stdout.write("⚠️ No hay suficientes películas para comparar. Terminado.")
            return

        movie1, movie2 = movies[0], movies[1]

        # ✅ Función para obtener embedding de un texto
        def get_embedding(text):
            response = client.embeddings.create(
                input=[text],
                model="text-embedding-3-small"
            )
            return np.array(response.data[0].embedding, dtype=np.float32)

        # ✅ Función para calcular similitud de coseno
        def cosine_similarity(a, b):
            return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

        # ✅ Generar embeddings de las películas
        emb1 = get_embedding(movie1.description)
        emb2 = get_embedding(movie2.description)

        # ✅ Similitud entre películas
        similarity = cosine_similarity(emb1, emb2)
        self.stdout.write(f"\U0001F3AC Similaridad entre '{movie1.title}' y '{movie2.title}': {similarity:.4f}")

        # ✅ Comparación con el prompt
        prompt_emb = get_embedding(prompt)
        sim_prompt_movie1 = cosine_similarity(prompt_emb, emb1)
        sim_prompt_movie2 = cosine_similarity(prompt_emb, emb2)

        self.stdout.write(f"\U0001F4DD Similitud prompt vs '{movie1.title}': {sim_prompt_movie1:.4f}")
        self.stdout.write(f"\U0001F4DD Similitud prompt vs '{movie2.title}': {sim_prompt_movie2:.4f}")
