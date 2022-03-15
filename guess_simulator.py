import string
import pickle
import random

letters = list(string.ascii_lowercase)
empty_dictionary_string = '{}'

def load_in_pickle(data):
        with open(f'pickled_dictionaries/{data}.pkl', 'rb') as f:
            return pickle.load(f)

def remove_dict_of_words_from_remaining(from_dict,target_dict):
        for word in from_dict:
            try:
                del target_dict[f'{word}']
            except KeyError:
                pass

for letter in letters:
    for number in range(0,5):
        exec(f"""{letter}{number} = load_in_pickle('{letter}{number}')""")

class game_simulator:

    def __init__(game):
        #load in pickled dictionaries
        game.all_wordle_words_list = load_in_pickle('all_wordle_words_list')
        game.all_wordle_words_dict = load_in_pickle('all_wordle_words_dict')
        game.remaining_possible_wordle_words = game.all_wordle_words_dict
        game.how_many_guesses_so_far = 0
        game.guess = ''
        game.correct_word = game.all_wordle_words_list[random.randint(0,len(game.all_wordle_words_list)-1)]
        print(f'correct word: {game.correct_word}')
        game.word_found = False

    #guess
    def generate_guess(game):
        game.guess = [*game.remaining_possible_wordle_words.keys()][-1]
        game.how_many_guesses_so_far += 1
        print(f'guess #{game.how_many_guesses_so_far}: {game.guess}!')
    
    def get_feedback(game):
        feedback = ''
        for index in range(0,len(game.guess)):
            if game.guess[index] == game.correct_word[index]:
                feedback += '2'
            elif game.guess[index] in game.correct_word:
                feedback += '1'
            else:
                feedback += '0'
        print(f'feedback: {feedback}')
        return feedback


    def modify_based_on_feedback(game,feedback):
        #check if word found
        if feedback == "22222":
            print(f"yay! the word was: {game.guess}! found in {game.how_many_guesses_so_far} guesses!")
            game.word_found = True
            return

        for index in range(0,len(feedback)):
            result = feedback[index]
            if result == '0':
                #remove letter from all places
                for number in range(0,5):
                    exec(f'remove_dict_of_words_from_remaining({game.guess[index]}{number},game.remaining_possible_wordle_words)')
                    # print(f'removed: {game.guess[index]}{number}')
            if result == '2':
                for letter in letters:
                    if letter != game.guess[index]:
                        exec(f'remove_dict_of_words_from_remaining({letter}{index},game.remaining_possible_wordle_words)')
                        # print(f'removed: {letter}{index}')
            if result == '1':
                exec(f'remove_dict_of_words_from_remaining({game.guess[index]}{index},game.remaining_possible_wordle_words)')
                # print(f'removed: {game.guess[index]}{index}')

total_guesses = 0

for _ in range(0,1000):
    g = game_simulator();
    while not g.word_found:
        g.generate_guess()
        g.modify_based_on_feedback(g.get_feedback())
    total_guesses += g.how_many_guesses_so_far

print(f'avg # of guesses: {total_guesses/1000}')