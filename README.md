# Movie Genre Classification using Naive Bayes

## Overview

This project implements a **Naive Bayes classifier** to classify movie plots into one of four genres: **Drama**, **Horror**, **Comedy**, and **Action**. The model uses text preprocessing, manual stemming, and a Naive Bayes approach based on word frequencies to predict the genre of a given plot.

## Mathematical Model

The classification model follows the **Naive Bayes** algorithm. The core idea is to compute the posterior probability of each category (genre) given a set of features (words in the plot) and choose the genre with the highest probability.

### Formula:
The posterior probability for a genre \( C \) given a set of words \( W = w_1, w_2, \dots, w_n \) is:

$ P(C \mid W) \propto P(C) \prod_{i=1}^{n} P(w_i \mid C) $

Where:
- \( P(C) \) is the prior probability of a genre.
- \( P(w_i \mid C) \) is the likelihood of word \( w_i \) appearing in genre \( C \), calculated using a smoothed version of word frequencies.

The word likelihood is estimated using the formula:

\[
P(w_i \mid C) = \frac{\text{count}(w_i, C) + 0.5}{\text{total words in C} + \text{vocabulary size}}
\]

Where:
- \( \text{count}(w_i, C) \) is the count of word \( w_i \) in the training data for genre \( C \).
- The smoothing factor of 0.5 is used to prevent zero probabilities.

The genre with the highest posterior probability is selected as the predicted genre for the plot.

## Code Structure

The project is structured as follows:

1. **`manual_stem(word)`**: A function to manually stem words (remove common suffixes like 'ing', 'ed', 's').
2. **`preprocess_plot(plot)`**: Preprocesses a movie plot by tokenizing, converting to lowercase, and removing stopwords.
3. **`balance_dataset()`**: Balances the dataset across genres by ensuring that all genres have the same number of movie plots.
4. **`open_func()`**: Loads and processes the dataset, splits it into training and testing sets, and pre-processes the plots.
5. **`train_test_split(data, labels, test_size=0.2)`**: Splits data and labels into training and testing sets.
6. **`update_vocab()`**: Builds the vocabulary from the training data.
7. **`category_tokens()`**: Generates word frequency counts for each genre.
8. **`test_bayes(plot)`**: Classifies a plot using Naive Bayes.
9. **`evaluate()`**: Evaluates the model's performance using metrics like accuracy, classification report, and confusion matrix.
10. **`test()`**: Computes the accuracy of the model on the test set.

## Example Usage
**Make Predictions**: You can use the trained model to predict the genre of new movie plots by using the `test_bayes(plot)` function.

**How to Use**: After the model is trained, you can classify a movie plot (a string of text) by calling the test_bayes() function with the plot as an argument.
```bash
genre = test_bayes("A mysterious phone call will change the life of the writer Valentino Lombardi and his family.")
print("Predicted Genre:", genre)
```
This will output the predicted genre for the provided movie plot. For example, it might print:


```
Predicted Genre: Horror
```
## Improvements
- **Tokenization and Preprocessing** - the `preprocess_plot` function uses a regular expression `(re.compile(r'[a-zA-Z]+') )` to clean the text (remove punctuation) and tokenizes the plot into lowercase words, further processing them by stemming and filtering out stopwords.
- We removed **stopwords** to eliminate common, meaningless words, allowing the model to focus on more important terms.
- We implemented a **stemmer** from scratch to reduce words to their root form by removing suffixes, which helps standardize variations of the same word and reduces the vocabulary size, improving model accuracy and efficiency.
- The **logarithmic function** improvement makes the model more stable by turning the multiplication of probabilities into addition, avoiding very small numbers. It makes calculations easier, helps the model work more reliably, and leads to better predictions.
- **Balancing the dataset** ensures that each category (genre) has an equal number of training samples, which helps prevent the model from being biased toward categories with more samples and improves generalization.
- **Shuffling and Splitting Data** - the `open_func` function loads movie plot data, shuffles it, and splits it into training and test sets. This helps ensure the model is trained on diverse and unbiased data.
- We implemented **Laplace smoothing** (also called additive smoothing), which handles the issue of zero probabilities for unseen words in the test data. The smoothing parameter alpha is used to ensure that words not seen in the training set still have a non-zero probability (0.5 in our case).

## Example Command:

```bash
python bayes.py
```

## Bibliografie
- https://github.com/scikit-learn/scikit-learn/blob/a71860add/sklearn/naive_bayes.py#L778
- https://scikit-learn.org/dev/modules/naive_bayes.html#multinomial-naive-bayes
- https://en.wikipedia.org/wiki/Naive_Bayes_classifier
- https://www.analyticsvidhya.com/blog/2021/04/improve-naive-bayes-text-classifier-using-laplace-smoothing/
- Dataset: https://www.themoviedb.org/
