import string
import pickle

def txtToList(path):
    file = open(path).read()
    return file.split()

def save_as_pickle(data,data_as_string):
    with open(f'pickled_dictionaries/{data_as_string}.pkl', 'wb') as f:
        pickle.dump(data, f)

word_value = 0
letter_frequency = {'a':7.8,'b':2,'c':4,'d':5.8,'e':11,'f':1.4,'g':3,'h':2.3,'i':8.2,'j':.003,'k':2.5,'l':5.3,'m':3.2,'n':7.2,'o':6.1,'p':2.8,'q':.24,'r':7.3,'s':8.7,'t':6.7,'u':3.3,'v':1,'w':.91,'x':.26,'y':1.6,'z':.44}

all_wordle_words_list = txtToList('/Users/ethanhwang/Documents/wordle/wordle-nyt-answers-alphabetical.txt')
all_wordle_words_dict = {}
for word in all_wordle_words_list:
    letters_so_far_in_word = []
    for each_letter in word:
        if each_letter not in letters_so_far_in_word:
            word_value += letter_frequency[f'{each_letter}']
            letters_so_far_in_word.append(each_letter)
    all_wordle_words_dict[f'{word}'] = word_value
    word_value = 0

all_wordle_words_dict = dict(sorted(all_wordle_words_dict.items(), key=lambda item: item[1]))

letters = list(string.ascii_lowercase)

#initialize empty dictionaries
empty_dictionary_string = '{}'
for letter in letters:
    for number in range(0,5):
        exec(f'{letter}{number} = {empty_dictionary_string}')

#populate a1 to z5

for letter in letters:
    for number in range(0,5):
        for word in all_wordle_words_list:
            letters_so_far_in_word = []
            for each_letter in word:
                if each_letter not in letters_so_far_in_word:
                    word_value += letter_frequency[f'{each_letter}']
                    letters_so_far_in_word.append(each_letter)
            if word[number] == letter:
                exec(f"""{letter}{number}['{word}']={word_value}""")
            word_value = 0

print(all_wordle_words_dict)

#pickle a1 to z5
for letter in letters:
    for number in range(0,5):
        data_as_string = f'{letter}{number}'
        exec(f"""save_as_pickle({letter}{number},'{data_as_string}')""")
        # with open(f'pickled_dictionaries/{letter}{number}.pkl', 'wb') as f:
        #     exec(f"""pickle.dump({letter}{number}, f)""")

#pickle all_wordle_words_list and all_wordle_words_dict
save_as_pickle(all_wordle_words_dict,'all_wordle_words_dict')
save_as_pickle(all_wordle_words_list,'all_wordle_words_list')
# with open('pickled_dictionaries/all_wordle_words_list.pkl', 'wb') as f:
#     pickle.dump(all_wordle_words_list, f)