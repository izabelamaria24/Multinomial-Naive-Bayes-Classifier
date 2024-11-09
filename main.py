import csv
import re

# Constants
MAX_COUNTER = 1950

# Regex pattern to match words containing only letters
pattern = re.compile(r'[a-zA-Z]+')

# Dictionaries to store word counts by category
categories = {"drama": {}, "comedy": {}, "horror": {}, "romance": {}, "adventure": {}}
lengths = {"drama": 0, "comedy": 0, "horror": 0, "romance": 0, "adventure": 0}
categories_count = {"drama": 0, "comedy": 0, "horror": 0, "romance": 0, "adventure": 0}

# Dictionary to store all words found across all categories
dict_all_words_from_our_planet = {}

# Initialize counters
total_words_count = 0
plot_avg = 0

# Open and read the CSV file
with open('filtered_movies.csv', mode='r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    
    # Skip header row
    next(csv_reader)
    
    # Process each row in the CSV
    for row in csv_reader:
        # Ensure the row has enough columns
        if len(row) < 2:
            continue
        
        # Extract movie title and category
        title, category = row[0], row[1]
        
        # Check if the category is one of the predefined ones
        if category not in categories:
            continue
        
        # Get the dictionary for the current category
        current_category_dict = categories[category]
        
        # Update the count of movies in the current category
        categories_count[category] += 1
        
        # Skip if the count exceeds the maximum limit
        if categories_count[category] > MAX_COUNTER:
            continue
        
        # Extract words from the movie title
        words = pattern.findall(title)
        plot_avg += len(words)
        
        # Process each word in the title
        for word in words:
            # Skip words that start with an uppercase letter (assuming they're proper nouns)
            if word[0].isupper():
                continue
            
            # Update global word count dictionary
            dict_all_words_from_our_planet[word] = [dict_all_words_from_our_planet.get(word, (0, 0))[0] + 1, 0]
            
            # Update word count in the current category
            current_category_dict[word] = [current_category_dict.get(word, (0, 0))[0] + 1, 0]
            
            # Update lengths and total word count
            lengths[category] += 1
            total_words_count += 1

# Debugging output for word counts
print("\n--- Debugging Counts ---")
print(f"Total words count: {total_words_count}")
print(f"Lengths by category: {lengths}")
print(f"Words count by category: {categories}")

# Calculate probabilities for each word in each category
for category, words_dict in categories.items():
    total_words_in_category = lengths[category]
    print(f"\nCategory: {category}, Total Words: {total_words_in_category}")  # Debugging line
    if total_words_in_category > 0:
        for word, counts in words_dict.items():
            # Probability within the category
            words_dict[word][1] = float(counts[0]) / total_words_in_category
            print(f"  Word: {word}, Count: {counts[0]}, Probability: {words_dict[word][1]}")  # Debugging line

# Calculate global probabilities
print("\n--- Global Words ---")
for word, counts in dict_all_words_from_our_planet.items():
    # Probability across all categories
    if total_words_count > 0:
        counts[1] = float(counts[0]) / total_words_count
    print(f"Word: {word}, Count: {counts[0]}, Global Probability: {counts[1]}")  # Debugging line

# Optional: Calculate average plot length (if needed)
average_plot_length = plot_avg / sum(categories_count.values()) if sum(categories_count.values()) > 0 else 0
print(f"\nAverage plot length: {average_plot_length:.2f}")
