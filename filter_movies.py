import json
from collections import Counter

def filter_genre(movie, top_genres):
    genres = movie['Genre'].split(', ') 
    valid_genres = [genre for genre in genres if genre in top_genres]
    
    if valid_genres:
        return valid_genres[0]
    else:
        return None  

with open("movies.json", "r", encoding="utf-8") as file:
    movie_data = json.load(file)

all_genres = []
for movie in movie_data:
    genres = movie['Genre'].split(', ') 
    all_genres.extend(genres)

genre_counts = Counter(all_genres)
top_genres = [genre for genre, _ in genre_counts.most_common(5)]

filtered_movies = []

for movie in movie_data:
    filtered_genre = filter_genre(movie, top_genres)
    if filtered_genre:
        filtered_movies.append({
            "Plot": movie["Plot"],
            "Genre": filtered_genre
        })


filtered_counts = Counter([movie["Genre"] for movie in filtered_movies])
for genre, count in filtered_counts.items():
    print(f"{genre}: {count}")


with open("balanced_filtered_movies.json", "w", encoding="utf-8") as outfile:
    json.dump(filtered_movies, outfile, indent=4, ensure_ascii=False)

