
import re
import random
from collections import Counter
from sklearn.metrics import classification_report, confusion_matrix
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.model_selection import train_test_split
import json

length_all_words_from_our_planet = 0
DRAMA = "Drama"
HORROR = "Horror"
COMEDY = "Comedy"
THRILLER = "Thriller"
ACTION = "Action"

pattern = re.compile(r'[a-zA-Z]+')
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

categories_dict = {
    DRAMA: {}, 
    HORROR: {},
    COMEDY: {},
    #THRILLER: {},
    ACTION: {}
}

plots = {
    DRAMA: [], 
    HORROR: [],
    COMEDY: [],
    #THRILLER: [],
    ACTION: []
}

test_plots = {
    DRAMA: [], 
    HORROR: [],
    COMEDY: [],
    #THRILLER: [],
    ACTION: []
}

bayes_category_dict = {} 

def preprocess_plot(plot):
    tokens = [
        stemmer.stem(word.lower()) 
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
    
    plots_list = []
    genres_list = []
    
    for movie in movie_data:
        if movie['Genre'] in allowed_genres:
            plots_list.append(movie['Plot'])
            genres_list.append(movie['Genre'])

    train_plots, test_plots_data, train_genres, test_genres = train_test_split(
        plots_list, genres_list, test_size=0.2, random_state=42
    )

    for plot, genre in zip(train_plots, train_genres):
        tokens = preprocess_plot(plot)  
        plots[genre].append(tokens) 

    for plot, genre in zip(test_plots_data, test_genres):
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
    accuracy = 0
    for category in test_plots:
        for plot in test_plots[category]:
            if test_bayes(plot) == category:
                accuracy += 1
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
