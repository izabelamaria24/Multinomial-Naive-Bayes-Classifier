import re
import random
import json
import math
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
from stop_words import stop_words
from word_statistics import word_statistics, plot_accuracy_vs_genres

DRAMA = "Drama"
HORROR = "Horror"
COMEDY = "Comedy"
THRILLER = "Thriller"
ACTION = "Action"

pattern = re.compile(r'[a-zA-Z]+')

categories_dict = {DRAMA: {}, HORROR: {}, COMEDY: {}, ACTION: {}}
plots = {DRAMA: [], HORROR: [], COMEDY: [], ACTION: []}
test_plots = {DRAMA: [], HORROR: [], COMEDY: [], ACTION: []}
bayes_category_dict = {}

vocab = []
word_to_index = {}

def manual_stem(word):
    if word.endswith("ing") and len(word) > 4:
        return word[:-3]
    elif word.endswith("ed") and len(word) > 3:
        return word[:-2]
    elif word.endswith("es") and len(word) > 3:
        return word[:-2]
    elif word.endswith("s") and len(word) > 3:
        return word[:-1]
    return word


def preprocess_plot(plot):
    tokens = [
        manual_stem(word.lower()) 
        for word in pattern.findall(plot) 
        if word.lower() not in stop_words
    ]
    return set(tokens)


def balance_dataset():
    min_count = min(len(plots[category]) for category in plots)
    for category in plots:
        if len(plots[category]) > min_count:
            plots[category] = random.sample(plots[category], min_count)


def open_func():
    with open('balanced_filtered_movies.json', mode='r', encoding='utf-8') as file:
        movie_data = json.load(file)
    
    allowed_genres = [DRAMA, COMEDY, HORROR, ACTION]
    plots_list, genres_list = [], []
    
    for movie in movie_data:
        if movie['Genre'] in allowed_genres:
            plots_list.append(movie['Plot'])
            genres_list.append(movie['Genre'])

    train_plots, test_plots_data, train_genres, test_genres = train_test_split(
        plots_list, genres_list, test_size=0.2
    )

    for plot, genre in zip(train_plots, train_genres):
        tokens = preprocess_plot(plot)
        plots[genre].append(tokens)

    for plot, genre in zip(test_plots_data, test_genres):
        tokens = preprocess_plot(plot)
        test_plots[genre].append(tokens)

    balance_dataset()


def train_test_split(data, labels, test_size=0.2):
    data_size = len(data)
    indices = list(range(data_size))
    random.shuffle(indices)
    split_idx = int(data_size * (1 - test_size))
    
    train_indices = indices[:split_idx]
    test_indices = indices[split_idx:]
    
    train_data = [data[i] for i in train_indices]
    train_labels = [labels[i] for i in train_indices]
    test_data = [data[i] for i in test_indices]
    test_labels = [labels[i] for i in test_indices]
    
    return train_data, test_data, train_labels, test_labels


def update_vocab():
    global vocab, word_to_index
    word_set = set()
    for category, category_plots in plots.items():
        for plot in category_plots:
            word_set.update(plot)
    
    vocab = sorted(list(word_set))
    word_to_index = {word: i for i, word in enumerate(vocab)}


def category_tokens():
    for category, category_plots in plots.items():
        for plot in category_plots:
            for word in plot:
                word_index = word_to_index[word]
                if word_index not in categories_dict[category]:
                    categories_dict[category][word_index] = 0
                categories_dict[category][word_index] += 1


def test_bayes(plot):
    bayes_category_dict.clear()
    plot_indices = [word_to_index.get(word, -1) for word in plot if word in word_to_index]

    for category in categories_dict:
        log_prob = math.log(len(plots[category]) / total_plots)
        total_words_in_category = sum(categories_dict[category].values())
        vocab_size = len(categories_dict[category])

        log_prob_words = np.zeros(len(vocab))

        for index in plot_indices:
            if index >= 0:
                word_count = categories_dict[category].get(index, 0)
                smoothed_prob = (word_count + 0.5) / (total_words_in_category + vocab_size)
                log_prob_words[index] = np.log(smoothed_prob)

        log_prob += np.sum(log_prob_words[plot_indices])

        bayes_category_dict[category] = log_prob

    return max(bayes_category_dict, key=bayes_category_dict.get)


def evaluate():
    y_true, y_pred = [], []
    for category in test_plots:
        for plot in test_plots[category]:
            y_true.append(category)
            y_pred.append(test_bayes(plot))
    
    accuracy = sum(1 for true, pred in zip(y_true, y_pred) if true == pred) / len(y_true)
    print("Classification Report:\n", classification_report(y_true, y_pred))
    print("Confusion Matrix:\n", confusion_matrix(y_true, y_pred))


def test():
    total_test_plots = sum(len(test_plots[category]) for category in test_plots)
    accuracy = sum(1 for category in test_plots for plot in test_plots[category] if test_bayes(plot) == category)
    return accuracy / total_test_plots


def main():
    open_func()
    global total_plots
    total_plots = sum(len(plots[category]) for category in plots)
    update_vocab()
    category_tokens()

    print("Training Set Sizes:")
    [print(f"{category}: {len(plots[category])}") for category in plots]
    print("\nTesting Set Sizes:")
    [print(f"{category}: {len(test_plots[category])}") for category in test_plots]
    
    print("\nAccuracy:", test())
    evaluate()
    
    word_statistics(plots,categories_dict, vocab, word_to_index)

if __name__ == "__main__":
    main()
