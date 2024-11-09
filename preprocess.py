import pandas as pd

df = pd.read_csv("movies_dataset.csv")

selected_genres = ["comedy", "drama", "horror", "romance", "adventure"]
df = df[df['Genre'].isin(selected_genres)]

df = df[['Plot', 'Genre']]

df.to_csv("filtered_movies.csv", index=False)

print(df)
