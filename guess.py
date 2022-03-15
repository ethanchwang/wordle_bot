import string
import pickle

letters = list(string.ascii_lowercase)
empty_dictionary_string = '{}'

def load_in_pickle(data):
    with open(f'pickled_dictionaries/{data}.pkl', 'rb') as f:
        return pickle.load(f)

def remove_dict_of_words_from_remaining(from_dict):
    global remaining_possible_wordle_words
    for word in from_dict:
        try:
            del remaining_possible_wordle_words[f'{word}']
        except KeyError:
            pass

#load in pickled dictionaries
all_wordle_words_list = load_in_pickle('all_wordle_words_list')
all_wordle_words_dict = load_in_pickle('all_wordle_words_dict')
remaining_possible_wordle_words = all_wordle_words_dict
for letter in letters:
    for number in range(0,5):
        exec(f"""{letter}{number} = load_in_pickle('{letter}{number}')""")

#guess
how_many_guesses_so_far = 0
while True:
    guess = [*remaining_possible_wordle_words.keys()][-1]
    how_many_guesses_so_far += 1
    print(f'guess #{how_many_guesses_so_far}: {guess}! 0=grey,1=yellow,2=green')
    feedback = input()

    #check if word found
    if feedback == "11111":
        print(f"yay! the word was: {guess}! found in {how_many_guesses_so_far} guesses!")
        break

    for index in range(0,len(feedback)):
        result = feedback[index]
        if result == '0':
            #remove letter from all places
            for number in range(0,5):
                exec(f'remove_dict_of_words_from_remaining({guess[index]}{number})')
                print(f'removed: {guess[index]}{number}')
        if result == '2':
            # for number in range(0,5):
            #     if number != index:
            #         exec(f'remove_dict_of_words_from_remaining({guess[index]}{number})')
            #         print(f'removed: {guess[index]}{number}')
            for letter in letters:
                if letter != guess[index]:
                    exec(f'remove_dict_of_words_from_remaining({letter}{index})')
                    print(f'removed: {letter}{index}')
        if result == '1':
            exec(f'remove_dict_of_words_from_remaining({guess[index]}{index})')
            print(f'removed: {guess[index]}{index}')