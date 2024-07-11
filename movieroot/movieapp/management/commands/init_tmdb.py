from datetime import datetime
from time import sleep

import requests
from django.core.management.base import BaseCommand
from movieapp.models import Movie, Genre
from tqdm import tqdm


class Command(BaseCommand):
    help = 'init DB'

    def handle(self, *args, **kwargs):
        # genre
        url = "https://api.themoviedb.org/3/genre/movie/list?api_key=0591f00cf0e88bb94a9bf75ac29051dd&language=ko-KR"
        try:
            response = requests.get(url)
            response.raise_for_status()
            datas = response.json()
            for data in datas["genres"]:
                genre = Genre()
                genre.genre_id = data["id"]
                genre.name = data["name"]
                genre.save()

        except requests.exceptions.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # HTTP 에러 발생 시 출력
        except Exception as err:
            print(f'Other error occurred: {err}')  # 기타 오류 발생 시 출력

        for i in tqdm(range(1, 51)):
            url = (
                f"https://api.themoviedb.org/3/discover/movie?api_key=0591f00cf0e88bb94a9bf75ac29051dd&language=ko-KR"
                f"&sort_by=popularity.desc&include_adult=false&include_video=false&page={i}"
            )
            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                for j in range(20):
                    movie = Movie()
                    movie.adult = data["results"][j]["adult"]
                    movie.backdrop_path = data["results"][j]["backdrop_path"]
                    movie.movie_id = data["results"][j]["id"]
                    movie.original_language = data["results"][j]["original_language"]
                    movie.original_title = data["results"][j]["original_title"]
                    movie.overview = data["results"][j]["overview"]
                    movie.popularity = data["results"][j]["popularity"]
                    movie.poster_path = data["results"][j]["poster_path"]
                    movie.release_date = data["results"][j]["release_date"]
                    if movie.release_date:
                        try:
                            movie.release_date = datetime.strptime(movie.release_date, '%Y-%m-%d').date()
                        except ValueError:
                            movie.release_date = None
                    movie.title = data["results"][j]["title"]
                    movie.vote_average = data["results"][j]["vote_average"]
                    movie.vote_count = data["results"][j]["vote_count"]
                    movie.save()
                    for genre_id in data["results"][j]["genre_ids"]:
                        genre = Genre.objects.get(genre_id=genre_id)
                        movie.genre_ids.add(genre)
            except requests.exceptions.HTTPError as http_err:
                print(f'HTTP error occurred: {http_err}')  # HTTP 에러 발생 시 출력
            except:
                pass
            sleep(0.5)

        self.stdout.write(self.style.SUCCESS('Successfully added data to the database'))
