import requests
import json
import os
from dotenv import load_dotenv

def fetch_tmdb_movie_data(api_key, page=1):
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}&page={page}"
    response = requests.get(url)
    data = response.json()
    return data['results']


def fetch_movie_details(api_key, movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
    response = requests.get(url)
    movie_data = response.json()
    return movie_data


def save_to_json(movies, filename="movies.json"):
    with open(filename, mode="w", encoding="utf-8") as file:
        json.dump(movies, file, ensure_ascii=False, indent=4)


api_key = os.getenv('API_KEY') 
if not api_key:
    raise ValueError("API key not found in .env file!")

all_movies = []

for page in range(1, 501):  
    movies = fetch_tmdb_movie_data(api_key, page)
    all_movies.extend(movies)
    print(page)

processed_movies = []
for movie in all_movies:
    plot = movie.get("overview", "No description available")
    movie_id = movie.get("id")
    print(movie_id)
    
    detailed_movie = fetch_movie_details(api_key, movie_id)
    
    genres = ', '.join([genre['name'] for genre in detailed_movie.get("genres", [])]) if "genres" in detailed_movie else "No genre available"
    
    processed_movies.append({"Plot": plot, "Genre": genres})

save_to_json(processed_movies, "movies.json")

print("Data has been saved to 'movies.json'.")
