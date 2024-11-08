import csv
import re

MAX_COUNTER = 1950

pattern = re.compile(r'[a-zA-Z]+')
categories = {"drama": {}, "comedy":{}, "horror":{}, "romance":{}, "adventure":{}}
lengths = {"drama": 0, "comedy":0, "horror":0, "romance":0, "adventure":0}
categories_count = {"drama": 0, "comedy":0, "horror":0, "romance":0, "adventure":0}
dict_all_words_from_our_planet = {}


total_words_count = 0
plot_avg = 0
i = 0


with open('filtered_movies.csv', mode='r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        if i == 0:
            i+=1
            continue
        i += 1
        current_category_dict = categories[row[1]]
        categories_count[row[1]]+=1
        if categories_count[row[1]]>MAX_COUNTER:
            continue
        words = pattern.findall(row[0])
        plot_avg += len(words)
        for word in words:
            #w = word.strip('.,!?()[]\{\}-;:"/')
            if word[0] >= 'A' and word[0] <= 'Z':
                continue
            dict_all_words_from_our_planet[word] = [dict_all_words_from_our_planet.get(word, (0,0))[0] + 1, 0]
            current_category_dict[word] = [current_category_dict.get(word, (0,0))[0] + 1, 0]
            lengths[row[1]] += 1
            total_words_count += 1

        # if i == 50:
        #     break

# print(total_words_count)

# print(dict_all_words_from_our_planet["the"][0]*100/total_words_count)
# print(categories["horror"]["the"][0]*100/lengths["horror"])

# print(plot_avg/i)  
# print(lengths)
# exit(0) 

def bayes(word, categ):
    prob_categ = 1 * 100/len(categories)
    prob_word = dict_all_words_from_our_planet[word][0]*100/total_words_count
    prob_word_cond_categ = categories[categ][word][0]*100/lengths[categ]
    result = prob_categ * prob_word_cond_categ / prob_word
    return round(result,2)

for key, dict_for_categ in categories.items():

    for word, ct in dict_for_categ.items():
        probability = bayes(word, key)
        dict_for_categ[word][1] = probability


    # filtered_dict = {key: value for key, value in values.items() if value > 20}
    # print(filtered_dict)


    top_50_items = dict(sorted(dict_for_categ.items(), key=lambda item: item[1][1], reverse=True)[:50])
    print(len(top_50_items))
    print(top_50_items)
    
    #print(categories[key])    

        