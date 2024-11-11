import re
import random
import json
import math
from sklearn.metrics import classification_report, confusion_matrix

DRAMA = "Drama"
HORROR = "Horror"
COMEDY = "Comedy"
THRILLER = "Thriller"
ACTION = "Action"

pattern = re.compile(r'[a-zA-Z]+')
stop_words = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as", "at",
    "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't", "cannot", "could",
    "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", "each", "few", "for",
    "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's",
    "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm",
    "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't",
    "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours",
    "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't",
    "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there",
    "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too",
    "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't",
    "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's",
    "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself",
    "yourselves"
}

categories_dict = {DRAMA: {}, HORROR: {}, COMEDY: {}, ACTION: {}}
plots = {DRAMA: [], HORROR: [], COMEDY: [], ACTION: []}
test_plots = {DRAMA: [], HORROR: [], COMEDY: [], ACTION: []}
bayes_category_dict = {}


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


def category_tokens():
    for category, category_plots in plots.items():
        for plot in category_plots:
            for word in plot:
                categories_dict[category][word] = categories_dict[category].get(word, 0) + 1
                

def test_bayes(plot):
    bayes_category_dict.clear()
    
    for category in categories_dict:
        log_prob = math.log(len(plots[category]) / total_plots)
        total_words_in_category = sum(categories_dict[category].values())
        vocab_size = len(categories_dict[category])
        
        for word in plot:
            word_count = categories_dict[category].get(word, 0)
            smoothed_prob = (word_count + 0.5) / (total_words_in_category + vocab_size)
            log_prob += math.log(smoothed_prob)
        
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
    category_tokens()

    print("Training Set Sizes:")
    [print(f"{category}: {len(plots[category])}") for category in plots]
    print("\nTesting Set Sizes:")
    [print(f"{category}: {len(test_plots[category])}") for category in test_plots]
    
    print("\nAccuracy:", test())
    evaluate()

if __name__ == "__main__":
    main()
