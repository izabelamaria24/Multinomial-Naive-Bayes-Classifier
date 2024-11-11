import csv
import re
import random
from sklearn.metrics import classification_report, confusion_matrix

length_all_words_from_our_planet = 0
MAX_COUNTER = 10**7
DRAMA = "drama"
HORROR = "horror"
ROMANCE = "romance"
ADVENTURE = "adventure"
COMEDY = "comedy"

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

categories_dict = {DRAMA: {}, HORROR: {}, ROMANCE: {}, ADVENTURE: {}, COMEDY: {}}
plots = {DRAMA: [], HORROR: [], ROMANCE: [], ADVENTURE: [], COMEDY: []}
test_plots = {DRAMA: [], HORROR: [], ROMANCE: [], ADVENTURE: [], COMEDY: []}
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
    plot = re.sub(r'[^\w\s?!]', '', plot)
    tokens = [
        manual_stem(word.lower())
        for word in plot.split()
        if word.lower() not in stop_words and len(word) > 1
    ]
    return set(tokens)

def balance_dataset():
    min_count = min(len(plots[category]) for category in plots)
    for category in plots:
        if len(plots[category]) > min_count:
            plots[category] = random.sample(plots[category], min_count)

def open_func():
    with open('filtered_movies.csv', mode='r', encoding='utf-8') as file:
        csv_reader = list(csv.reader(file))[1:]
    plots_list = [row[0] for row in csv_reader]
    genres_list = [row[1] for row in csv_reader]

    combined = list(zip(plots_list, genres_list))
    random.shuffle(combined)
    plots_list, genres_list = zip(*combined)

    split_index = int(0.8 * len(plots_list))
    train_plots = plots_list[:split_index]
    test_plots_data = plots_list[split_index:]
    train_genres = genres_list[:split_index]
    test_genres = genres_list[split_index:]

    for plot, genre in zip(train_plots, train_genres):
        if genre in plots and len(plots[genre]) <= MAX_COUNTER:
            tokens = preprocess_plot(plot)
            plots[genre].append(tokens)
    
    for plot, genre in zip(test_plots_data, test_genres):
        if genre in test_plots:
            tokens = preprocess_plot(plot)
            test_plots[genre].append(tokens)
    
    balance_dataset()

def category_tokens():
    for category, category_plots in plots.items():
        for plot in category_plots:
            for word in plot:
                categories_dict[category][word] = categories_dict[category].get(word, 0) + 1

def test_bayes(plot):
    bayes_category_dict.clear()
    for category in categories_dict:
        prod = len(plots[category]) / total_plots
        total_words_in_category = sum(categories_dict[category].values())
        vocab_size = len(categories_dict[category])

        for word in plot:
            word_count = categories_dict[category].get(word, 0)
            smoothed_prob = (word_count + 1) / (total_words_in_category + vocab_size)
            prod *= smoothed_prob
        
        bayes_category_dict[category] = prod
    
    return max(bayes_category_dict, key=bayes_category_dict.get)

def test_bayes_laplace_smoothing(plot, alpha=0.5):
    bayes_category_dict.clear()
    
    for category in categories_dict:
        prod = len(plots[category]) / total_plots
        total_words_in_category = sum(categories_dict[category].values())
        vocab_size = len(categories_dict)
        
        for word in plot:
            word_count = categories_dict[category].get(word, 0)
            smoothed_prob = (word_count + alpha) / (total_words_in_category + alpha * vocab_size)
            prod *= smoothed_prob
        
        bayes_category_dict[category] = prod
    
    return max(bayes_category_dict, key=bayes_category_dict.get)

def evaluate():
    y_true, y_pred = [], []
    for category in test_plots:
        for plot in test_plots[category]:
            y_true.append(category)
            y_pred.append(test_bayes(plot))
    
    print("Classification Report:\n", classification_report(y_true, y_pred))
    print("Confusion Matrix:\n", confusion_matrix(y_true, y_pred))

def test():
    total_test_plots = sum([len(test_plots[category]) for category in test_plots])
    accuracy = sum(1 for category in test_plots for plot in test_plots[category] if test_bayes_laplace_smoothing(plot) == category)
    return accuracy / total_test_plots

def main():
    open_func()
    global total_plots
    total_plots = sum([len(plots[category]) for category in plots])
    category_tokens()

    print("Training Set Sizes:")
    [print(f"{category}: {len(plots[category])}") for category in plots]
    print("\nTesting Set Sizes:")
    [print(f"{category}: {len(test_plots[category])}") for category in test_plots]
    print("\nAccuracy:", test())
    evaluate()

if __name__ == "__main__":
    main()
