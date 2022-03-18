from asyncore import write
import string
import pickle
import time
import random

letters = list(string.ascii_lowercase)
empty_dictionary_string = '{}'

path1 = 'day2/results.txt'
path2 = 'day2/results_with_dict.txt'

def load_in_pickle(data):
    with open(f'pickled_dictionaries/{data}.pkl', 'rb') as f:
        return pickle.load(f)

def remove_dict_of_words_from_remaining(from_dict,target_dict):
    for key in from_dict:
        if key in target_dict:
            del target_dict[f'{key}']
    return target_dict

def get_intersection_between_two_dict(from_dict,target_dict):
    return len(from_dict.keys() & target_dict.keys())

for letter in letters:
    for number in range(0,5):
        exec(f"""{letter}{number} = load_in_pickle('{letter}{number}')""")

def save_as_pickle(data,data_as_string):
    with open(f'cached_dict/{data_as_string}.pkl', 'wb') as f:
        pickle.dump(data, f)

def write_to_txt(line):
    with open(path1, 'a') as f:
        try:
            f.write(line)
            f.write('\n')
        except:
            pass
    with open(path2, 'a') as f:
        f.write(str(line))
        f.write('\n')

all_wordle_words_dict = load_in_pickle('all_wordle_words_dict')

class new_feedback:
    def __init__(self,input_word,input_feedback,input_remaining_wordle_words):
        self.word = input_word
        self.feedback = input_feedback
        # print(self.feedback)
        self.remaining_wordle_words = input_remaining_wordle_words
        self.running_dict = {}
        # print(f'before trim: {len(self.remaining_wordle_words)}')

    def trim_eliminated_words(self):
        self.running_dict.clear()
        for index in range(0,len(self.feedback)):
            letter_result = self.feedback[index]
            if letter_result == '0':
                for number in range(0,5):
                    exec(f'self.running_dict.update({self.word[index]}{number})')
            if letter_result == '2':
                for letter in letters:
                    if letter != self.word[index]:
                        exec(f'self.running_dict.update({letter}{index})')

            if letter_result == '1':
                exec(f'self.running_dict.update({self.word[index]}{index})')
        return get_intersection_between_two_dict(self.running_dict,self.remaining_wordle_words)

    def get_number_of_remaining_words(self):
        # print(f'after trim: {len(self.remaining_wordle_words)}')
        return self.trim_eliminated_words()

class new_branch:
    def __init__(self,input_word,input_remaining_wordle_words):
        self.remaining_wordle_words_branch = input_remaining_wordle_words.copy()
        self.word = input_word
        # print(self.word)
    
    def get_max_for_all_feedback(self):
        all_possibilities_after_feedback = []
        # start_time = time.time()
        for place_1 in range(0,3):
            for place_2 in range(0,3):
                for place_3 in range(0,3):
                    for place_4 in range(0,3):
                        for place_5 in range(0,3):
                            feedback_this_branch = f'{place_1}{place_2}{place_3}{place_4}{place_5}'
                            # print(len(self.remaining_wordle_words_branch))
                            feedback = new_feedback(self.word,feedback_this_branch,self.remaining_wordle_words_branch)
                            all_possibilities_after_feedback.append(feedback.get_number_of_remaining_words())
                            # print(all_possibilities_after_feedback)
        # end_time = time.time()
        # print(f'for 1 word: time = {end_time-start_time}s')
        max_for_this_word = min(all_possibilities_after_feedback)
        # print(all_possibilities_after_feedback)
        # print(max_for_this_word)
        return max_for_this_word

class guesser:
    def __init__(self):
        #load in pickled dictionaries
        self.branches_all_wordle_words_dict = all_wordle_words_dict.copy()
        self.remaining_possible_wordle_words = all_wordle_words_dict.copy()
        self.how_many_guesses_so_far = 1
        self.guess = 'sauce'
        self.feedback = ''
        self.word_found = False
        self.correct_word = list(all_wordle_words_dict)[random.randint(0,len(list(all_wordle_words_dict))-1)]
        print(f'correct word: {self.correct_word}')
        write_to_txt(f'correct word: {self.correct_word}')
    
    def modify_dict_of_remaining_words(self,feedback):
        for index in range(0,len(feedback)):
            result = feedback[index]
            if result == '0':
                for number in range(0,5):
                    exec(f'self.remaining_possible_wordle_words = remove_dict_of_words_from_remaining({self.guess[index]}{number},self.remaining_possible_wordle_words)')
            if result == '2':
                for letter in letters:
                    if letter != self.guess[index]:
                        exec(f'self.remaining_possible_wordle_words = remove_dict_of_words_from_remaining({letter}{index},self.remaining_possible_wordle_words)')
            if result == '1':
                exec(f'self.remaining_possible_wordle_words = remove_dict_of_words_from_remaining({self.guess[index]}{index},self.remaining_possible_wordle_words)')
        if len(self.remaining_possible_wordle_words) == 1:
            self.word_found = True
            self.how_many_guesses_so_far += 1
            self.guess = list(self.remaining_possible_wordle_words.keys())[0]
            # print(f'word found! word: {self.guess}')

    def update_branch(self):
        index = 0
        percent_complete = 0
        for key in list(all_wordle_words_dict):
            branch = new_branch(key,self.remaining_possible_wordle_words)
            self.branches_all_wordle_words_dict[key] = branch.get_max_for_all_feedback()
            index += 1
            if index%230 == 0:
                percent_complete += 10
                print(f'search {percent_complete}% complete')
        
    
    def rearrange_all_wordle_words_dict(self):
        self.branches_all_wordle_words_dict = dict(sorted(self.branches_all_wordle_words_dict.items(), key=lambda item: item[1]))
    
    def generate_guess(self):
        self.rearrange_all_wordle_words_dict()
        print(self.branches_all_wordle_words_dict)
        write_to_txt(self.branches_all_wordle_words_dict)
        print(self.remaining_possible_wordle_words)
        write_to_txt(self.remaining_possible_wordle_words)
        print(f'# of remaining words: {len(self.remaining_possible_wordle_words)}!')
        write_to_txt(f'# of remaining words: {len(self.remaining_possible_wordle_words)}!')
        self.guess = list(self.branches_all_wordle_words_dict.keys())[-1]
        best_outcome = list(self.branches_all_wordle_words_dict.values())[-1]
        for word in list(self.remaining_possible_wordle_words):
            if self.branches_all_wordle_words_dict[word] == best_outcome:
                self.guess = word
        self.how_many_guesses_so_far += 1
        print(f'guess #{self.how_many_guesses_so_far}: {self.guess}!')
        write_to_txt(f'guess #{self.how_many_guesses_so_far}: {self.guess}!')
    
    def manually_get_feedback(self):
        print("0=grey,1=yellow,2=green")
        self.feedback = input()
        return self.feedback
    
    def automatically_get_feedback(self):
        self.feedback = ''
        for index in range(0,len(self.guess)):
            if self.guess[index] == self.correct_word[index]:
                self.feedback += '2'
            elif self.guess[index] in self.correct_word:
                self.feedback += '1'
            else:
                self.feedback += '0'
        print(self.feedback)
        write_to_txt(self.feedback)
        return self.feedback

n = 1000
total_guesses = 0

for number_of_simulated_games_so_far in range(1,n+1):
    g = guesser();
    print('guess #1: sauce!')
    write_to_txt('guess #1: sauce!')
    while (not g.word_found) and g.how_many_guesses_so_far < 11:
        g.modify_dict_of_remaining_words(g.automatically_get_feedback())
        if g.word_found:
            total_guesses += g.how_many_guesses_so_far
            print(f'word found! word: {g.guess}')
            write_to_txt(f'word found! word: {g.guess}')
            print(f'word found in {g.how_many_guesses_so_far} guesses!')
            write_to_txt(f'word found in {g.how_many_guesses_so_far} guesses!')
            print(f'average accuracy so far: {total_guesses/number_of_simulated_games_so_far}')
            write_to_txt(f'average accuracy so far: {total_guesses/number_of_simulated_games_so_far}')
            print(f'number of games simulated so far: {number_of_simulated_games_so_far}!')
            write_to_txt(f'number of games simulated so far: {number_of_simulated_games_so_far}!')
            with open(path1, 'a') as f:
                f.write('\n')
            with open(path2, 'a') as f:
                f.write('\n')
        if not g.word_found:
            g.update_branch()
            g.generate_guess()
        if g.how_many_guesses_so_far > 9:
            print(f'{g.correct_word} took 10 guesses! abort!')
            write_to_txt(f'{g.correct_word} took 10 guesses! abort!')
            write_to_txt('\n')
        # save_as_pickle(g.branches_all_wordle_words_dict,f'{g.guess}{g.feedback}')