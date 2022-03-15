import string
import pickle

letters = list(string.ascii_lowercase)
frequency_dictionary = dict.fromkeys(letters,0)
number_of_letters_indexed = 0

def load_in_pickle(data):
    with open(f'pickled_dictionaries/{data}.pkl', 'rb') as f:
        return pickle.load(f)

all_wordle_words_list = load_in_pickle('all_wordle_words_list')

for word in all_wordle_words_list:
    for letter in word:
        frequency_dictionary[letter] += 1
        number_of_letters_indexed += 1


for letter in frequency_dictionary:
    frequency_dictionary[letter] = frequency_dictionary[letter]/number_of_letters_indexed

print(frequency_dictionary)