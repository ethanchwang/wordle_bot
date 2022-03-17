import string
import pickle
import time

letters = list(string.ascii_lowercase)
empty_dictionary_string = '{}'

def load_in_pickle(data):
    with open(f'pickled_dictionaries/{data}.pkl', 'rb') as f:
        return pickle.load(f)

def remove_dict_of_words_from_remaining(from_dict,target_dict):
    for key in from_dict:
        if key in target_dict:
            del target_dict[f'{key}']
    return target_dict

for letter in letters:
    for number in range(0,5):
        exec(f"""{letter}{number} = load_in_pickle('{letter}{number}')""")

def save_as_pickle(data,data_as_string):
    with open(f'cached_dict/{data_as_string}.pkl', 'wb') as f:
        pickle.dump(data, f)

all_wordle_words_dict = load_in_pickle('all_wordle_words_dict')

class new_feedback:
    def __init__(self,input_word,input_feedback,input_remaining_wordle_words):
        self.word = input_word
        self.feedback = input_feedback
        # print(self.feedback)
        self.remaining_wordle_words = input_remaining_wordle_words.copy()
        # print(f'before trim: {len(self.remaining_wordle_words)}')

    def trim_eliminated_words(self):
        for index in range(0,len(self.feedback)):
            letter_result = self.feedback[index]
            if letter_result == '0':
                for number in range(0,5):
                    exec(f'self.remaining_wordle_words = remove_dict_of_words_from_remaining({self.word[index]}{number},self.remaining_wordle_words)')
            if letter_result == '2':
                for letter in letters:
                    if letter != self.word[index]:
                        exec(f'self.remaining_wordle_words = remove_dict_of_words_from_remaining({letter}{index},self.remaining_wordle_words)')

            if letter_result == '1':
                exec(f'self.remaining_wordle_words = remove_dict_of_words_from_remaining({self.word[index]}{index},self.remaining_wordle_words)')

    def get_number_of_remaining_words(self):
        self.trim_eliminated_words()
        # print(f'after trim: {len(self.remaining_wordle_words)}')
        return len(self.remaining_wordle_words)

class new_branch:
    def __init__(self,input_word,input_remaining_wordle_words):
        self.remaining_wordle_words_branch = input_remaining_wordle_words.copy()
        self.word = input_word
        # print(self.word)
    
    def get_max_for_all_feedback(self):
        all_possibilities_after_feedback = []
        start_time = time.time()
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
        end_time = time.time()
        print(f'for 1 word: time = {end_time-start_time}s')
        max_for_this_word = max(all_possibilities_after_feedback)
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

    def update_branch(self):
        index = 0
        percent_complete = 0
        for key in list(all_wordle_words_dict):
            branch = new_branch(key,self.remaining_possible_wordle_words)
            self.branches_all_wordle_words_dict[key] = branch.get_max_for_all_feedback()
            index += 1
            if index%23 == 0:
                percent_complete += 1
                print(f'search {percent_complete}% complete')
        
    
    def rearrange_all_wordle_words_dict(self):
        self.branches_all_wordle_words_dict = dict(sorted(self.branches_all_wordle_words_dict.items(), key=lambda item: item[1]))
    
    def generate_guess(self):
        self.rearrange_all_wordle_words_dict()
        self.guess = next(iter(self.branches_all_wordle_words_dict))
        self.how_many_guesses_so_far += 1
        print(f'guess #{self.how_many_guesses_so_far}: {self.guess}!')
    
    def manually_get_feedback(self):
        print("0=grey,1=yellow,2=green")
        self.feedback = input()
        return self.feedback

print('guess #1: sauce!')
g = guesser();

while True:
    g.modify_dict_of_remaining_words(g.manually_get_feedback())
    g.update_branch()
    g.generate_guess()
    print(g.branches_all_wordle_words_dict)
    save_as_pickle(g.branches_all_wordle_words_dict,f'{g.guess}{g.feedback}')