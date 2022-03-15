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

    def __init__(self):
        #load in pickled dictionaries
        self.all_wordle_words_list = load_in_pickle('all_wordle_words_list')
        self.all_wordle_words_dict = load_in_pickle('all_wordle_words_dict')
        self.remaining_possible_wordle_words = self.all_wordle_words_dict
        self.how_many_guesses_so_far = 0
        self.guess = ''
        self.correct_word = self.all_wordle_words_list[random.randint(0,len(self.all_wordle_words_list)-1)]
        print(f'correct word: {self.correct_word}')
        self.word_found = False

    #guess
    def generate_guess(self):
        self.guess = [*self.remaining_possible_wordle_words.keys()][-1]
        self.how_many_guesses_so_far += 1
        print(f'guess #{self.how_many_guesses_so_far}: {self.guess}!')
    
    def get_feedback(self):
        feedback = ''
        for index in range(0,len(self.guess)):
            if self.guess[index] == self.correct_word[index]:
                feedback += '2'
            elif self.guess[index] in self.correct_word:
                feedback += '1'
            else:
                feedback += '0'
        print(f'feedback: {feedback}')
        return feedback


    def modify_based_on_feedback(self,feedback):
        #check if word found
        if feedback == "22222":
            print(f"yay! the word was: {self.guess}! found in {self.how_many_guesses_so_far} guesses!")
            self.word_found = True
            return

        for index in range(0,len(feedback)):
            result = feedback[index]
            if result == '0':
                #remove letter from all places
                for number in range(0,5):
                    exec(f'remove_dict_of_words_from_remaining({self.guess[index]}{number},game.remaining_possible_wordle_words)')
                    # print(f'removed: {game.guess[index]}{number}')
            if result == '2':
                for letter in letters:
                    if letter != self.guess[index]:
                        exec(f'remove_dict_of_words_from_remaining({letter}{index},game.remaining_possible_wordle_words)')
                        # print(f'removed: {letter}{index}')
            if result == '1':
                exec(f'remove_dict_of_words_from_remaining({self.guess[index]}{index},game.remaining_possible_wordle_words)')
                # print(f'removed: {game.guess[index]}{index}')

total_guesses = 0
n = 100

for _ in range(0,n):
    g = game_simulator();
    while not g.word_found:
        g.generate_guess()
        g.modify_based_on_feedback(g.get_feedback())
    total_guesses += g.how_many_guesses_so_far

print(f'avg # of guesses: {total_guesses/n}')