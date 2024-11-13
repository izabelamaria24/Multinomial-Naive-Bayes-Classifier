import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def word_statistics(plots, categories_dict, vocab, word_to_index):
    word_plot_count = {category: {} for category in categories_dict}
    
    genre_colors = {
        "Drama": "blue",
        "Horror": "red",
        "Comedy": "green",
        "Action": "orange"
    }

    for category, category_plots in plots.items():
        for plot in category_plots:
            unique_words = set(plot)
            for word in unique_words:
                word_index = word_to_index.get(word, None)
                if word_index is not None:
                    if word_index not in word_plot_count[category]:
                        word_plot_count[category][word_index] = 0
                    word_plot_count[category][word_index] += 1

    num_categories = len(word_plot_count)
    fig, axes = plt.subplots(1, num_categories, figsize=(16, 6), sharey=True)

    if num_categories == 1:
        axes = [axes]

    for ax, (category, words) in zip(axes, word_plot_count.items()):
        top_words = sorted(words.items(), key=lambda x: x[1], reverse=True)[:5]
        word_labels = [vocab[word_index] for word_index, _ in top_words]
        counts = [count for _, count in top_words]

        color = genre_colors.get(category, "gray") 

        ax.bar(word_labels, counts, color=color)
        ax.set_title(f"Top 5 Words in {category}", color=color)
        ax.set_ylabel('Number of Plots')
        ax.set_xlabel('Words')
        ax.set_xticks(range(len(word_labels)))
        ax.set_xticklabels(word_labels, rotation=45, ha='right')

    plt.tight_layout()
    plt.savefig('top_words_per_genre.png')
    plt.close(fig) 


def plot_accuracy_vs_genres():
    genres = ['5 genres', '4 genres', '3 genres', '2 genres']
    accuracy = [0.50, 0.63, 0.72, 0.80]
    colors = ['purple', 'blue', 'green', 'orange']

    plt.figure(figsize=(8, 5))
    plt.bar(genres, accuracy, color=colors)
    plt.title('Accuracy vs Number of Genres')
    plt.xlabel('Number of Genres')
    plt.ylabel('Accuracy')
    plt.ylim(0, 1)
    plt.grid(axis='y', linestyle='--')

    # Annotate bars with accuracy percentages
    for i, acc in enumerate(accuracy):
        plt.text(i, acc + 0.02, f'{int(acc * 100)}%', ha='center')

    plt.tight_layout()
    plt.savefig('accuracy_vs_genres.png')
    plt.close()
