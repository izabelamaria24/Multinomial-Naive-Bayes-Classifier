import pandas as pd
import re

df = pd.read_csv("movies_dataset.csv")
df = df.dropna(subset=['Plot'])


def preprocess_plot(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    
    return text


df['Processed_Plot'] = df['Plot'].apply(preprocess_plot)

print(df[['Title', 'Processed_Plot']].head())

# Here we have the preprocessed plot (lower case and without any special characters)