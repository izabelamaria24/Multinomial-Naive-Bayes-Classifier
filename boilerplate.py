import csv
import re

# MAX_COUNTER = 1950
DRAMA = "drama"
HORROR = "horror"
ROMANCE = "romance"
ADVENTURE = "adventure"
COMEDY = "comedy"

pattern = re.compile(r'[a-zA-Z]+')

categories_dict = {
    # dict of words (the key will be the word and the value, how many plots from the category it appears)
    DRAMA: {}, 
    HORROR: {},
    ROMANCE: {},
    ADVENTURE: {},
    COMEDY: {}
}

# container for ALL of the plots described below
plots = []

def split_train_test_dataset():
    # TODO -> split the dataset into training and test set (80%, 20%)


def preprocess_plot(plot):
    # TODO -> preprocess given plot
    # return a list of words (tokens)


with open('filtered_movies.csv', mode='r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)

    # for every row (plot), preprocess it, and keep only the preprocessed words from the plot (tokens) 
    # keep a list with all of the data (a list of tuples (preprocessed plot (string), genre (string)))
    # we can use a dict too, but then we will need to filter based on the genre when we need it


# for every category, iterate through its plots 
# for each word, increment the counter 
def category_tokens():
    # TODO -> populate the categories_dict


bayes = {} # dict for keeping probabilities
def bayes_category(category):
    # TODO -> calculate bayes for category

# bayes -> for every category compute the probability to contain each word from its list
def bayes():
    # TODO -> iterate through the categories and compute bayes
    # return the maximum value found

