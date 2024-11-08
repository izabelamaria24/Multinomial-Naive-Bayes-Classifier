import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from collections import defaultdict
from math import log
from itertools import chain
from multiprocessing import Pool, cpu_count

nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words('english'))

stemmer = PorterStemmer()

df = pd.read_csv("movies_dataset.csv")
df = df.dropna(subset=['Plot', 'Genre'])

selected_genres = ["action", "comedy", "drama", "horror", "science fiction"]
df = df[df['Genre'].isin(selected_genres)].reset_index(drop=True)

def preprocess_plot(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text) 
    words = text.split()
    filtered_words = [stemmer.stem(word) for word in words if word not in stop_words] 
    return filtered_words 


def create_ngrams(words, n=2):
    ngrams = zip(*[words[i:] for i in range(n)])
    return [' '.join(ngram) for ngram in ngrams]


df['Processed_Plot'] = df['Plot'].apply(preprocess_plot)


plots = df['Processed_Plot'].tolist()
genres = df['Genre'].tolist()


all_ngrams = []
for plot in plots:
    all_ngrams.extend(create_ngrams(plot, n=1))
    all_ngrams.extend(create_ngrams(plot, n=2))  

ngram_freq = defaultdict(int)
for ngram in all_ngrams:
    ngram_freq[ngram] += 1

vocabulary = set(sorted(ngram_freq, key=ngram_freq.get, reverse=True)[:5000])
vocab_size = len(vocabulary)

genre_counts = defaultdict(int)
genre_word_counts = defaultdict(lambda: defaultdict(int))

for plot, genre in zip(plots, genres):
    genre_counts[genre] += 1
    ngrams = create_ngrams(plot, n=1) + create_ngrams(plot, n=2)  
    for ngram in ngrams:
        if ngram in vocabulary:  
            genre_word_counts[ngram][genre] += 1

likelihood_cache = {}

genre_denominators = {genre: genre_counts[genre] + vocab_size for genre in genre_counts}

def calculate_likelihood(word, genre):
    if (word, genre) in likelihood_cache:
        return likelihood_cache[(word, genre)]
    
    count = genre_word_counts[word][genre]
    total_count = genre_denominators[genre]
    likelihood = (count + 1) / total_count  
    likelihood_cache[(word, genre)] = likelihood
    return likelihood

def calculate_posterior(plot, genre):
    words = create_ngrams(plot, n=1) + create_ngrams(plot, n=2) 
    posterior = 0 
    for word in words:
        if word in genre_word_counts: 
            likelihood = calculate_likelihood(word, genre)
            posterior += log(likelihood)
 
    genre_prior = log(genre_counts[genre] / sum(genre_counts.values()))
    posterior += genre_prior
    return posterior

def classify_plot(plot):
    max_posterior = -float('inf') 
    max_genre = None
    for genre in genre_counts:
        posterior = calculate_posterior(plot, genre)
        if posterior > max_posterior:
            max_posterior = posterior
            max_genre = genre
    return max_genre

def classify_plot_parallel(plot):
    return classify_plot(plot)

def classify_in_parallel():
    with Pool(processes=min(cpu_count(), 4)) as pool: 
        classifications = pool.map(classify_plot_parallel, df['Processed_Plot'])

    df['Classification'] = classifications

    correct_predictions = sum(df['Genre'] == df['Classification'])
    total_predictions = len(df)
    accuracy = correct_predictions / total_predictions
    return accuracy

if __name__ == '__main__':
    accuracy = classify_in_parallel()
    print(f"Accuracy: {accuracy * 100:.2f}%")
