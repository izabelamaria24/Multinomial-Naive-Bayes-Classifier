import csv
import re
import random

length_all_words_from_our_planet = 0

MAX_COUNTER = 1000000
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
plots = {
    DRAMA: [], 
    HORROR: [],
    ROMANCE: [],
    ADVENTURE: [],
    COMEDY: []
}

test_plots = {
    DRAMA: [], 
    HORROR: [],
    ROMANCE: [],
    ADVENTURE: [],
    COMEDY: []
}


def preprocess_plot(plot):
    # TODO -> preprocess given plot
    # return a list of words (tokens)'
    tokens = set([word for word in pattern.findall(plot) if not word[0].isupper()])
    return tokens

def open_func():
    with open('filtered_movies.csv', mode='r', encoding='utf-8') as file:
        csv_reader = list(csv.reader(file))[1:]
        #random.shuffle(csv_reader)
        num_rows = int(len(csv_reader) * 0.8)

        # for every row (plot), preprocess it, and keep only the preprocessed words from the plot (tokens) 
        # keep a list with all of the data (a list of tuples (preprocessed plot (string), genre (string)))
        # we can use a dict too, but then we will need to filter based on the genre when we need it

        for row in csv_reader[:num_rows]:
            plot = row[0]
            genre = row[1]
            if len(plots[genre]) > MAX_COUNTER:
                continue
            tokens = preprocess_plot(plot)
            plots[genre].append(tokens)

        for row in csv_reader[num_rows:]:
            plot = row[0]
            genre = row[1]
            tokens = preprocess_plot(plot)
            test_plots[genre].append(tokens)

total_plots = 0
# for every category, iterate through its plots 
# for each word, increment the counter 
def category_tokens():
    # TODO -> populate the categories_dict
    for category, category_plots in plots.items():
        for plot in category_plots:
            for word in plot:
                categories_dict[category][word] = categories_dict[category].get(word, 0) + 1



bayes_category_dict = {} # dict for keeping probabilities
def test_bayes(plot):
    # TODO -> test the bayes on a given plot
    # return the category with the highest probability
    for category in categories_dict:
        prod = len(plots[category]) / total_plots
        for word in plot:
            if categories_dict[category].get(word, 0) == 0:
                continue
            prod *= categories_dict[category][word]/len(plots[category])
        bayes_category_dict[category] = prod
    return max(bayes_category_dict, key=bayes_category_dict.get)

def test():
    total_test_plots = sum([len(test_plots[category]) for category in test_plots])
    accuracy = 0
    for category in test_plots:
        for plot in test_plots[category]:
            #print(f"{test_bayes(plot)}\t{category}")
            if test_bayes(plot) == category:
                accuracy += 1
    return accuracy / total_test_plots


def main():
    open_func()
    global total_plots
    total_plots = sum([len(plots[category]) for category in plots])
    length_all_words_from_our_planet = sum([len(plot) for plot in plots.values()])
    category_tokens()

    [print(len(x)) for x in plots.values()]
    print()
    [print(len(x)) for x in test_plots.values()]
    print(test())

if __name__ == "__main__":
    main()