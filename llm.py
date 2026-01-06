from typing import TextIO
import random



def get_file_decision() -> str:
    """Prompts the user for which type of text they want generated.
    """
    file = input("""What type of text would you like?:  (1-2)
1. Adele Song Lyrics
2. News Headlines
3. Trump Tweets
>>> """)
    while not file.isalnum() or int(file) not in [1, 2, 3]:
        print("Invalid, please pick a number 1-3.")
        file = input("""What type of text would you like?:  (1-3)
1. Adele Song Lyrics
2. New Headlines
3. Trump Tweets
>>> """)    
        
    if int(file) == 1:
        return open('adele.txt', 'r')
    if int(file) == 2:
        return open('news.txt', 'r')
    else:
        return open('trump.txt', 'r')
    

def get_numwords_and_clength() -> tuple[int, int]:
    """Gets num_words and context_lenghts as inputs.
    Re-prompting if context_length > num_words, or invalid inputs given.
    """
    
    num_words = input('Numbers Of Words: ')
    while not num_words.isalnum() or int(num_words) <= 0:
        print('Invalid. Must be a positive number.')
        num_words = input('Numbers Of Words: ')
    num_words = int(num_words)
    
    
    clength = input('Length Of Contexts: ')
    while not clength.isalnum() or int(clength) <= 0 or int(clength) > num_words:
        print('Invalid. Must be a positive number smaller then \
                number of words')
        context_length = input('Length Of Contexts: ')
        
    return num_words, int(clength)    
    

def context_dictionary(words_list: list[str], 
                     context_length: int) -> dict[tuple, list[str]]:
    """Create a dictionary of all the words in our training file, mapping
    contexts to what words come after, including duplicates from our read list.
    >>> context_dictionary(training_file.read().split(), 2)
    """
    dct = {}
    
    for i in range(len(words_list) - context_length - 1):
        context = tuple(words_list[i : i + context_length])
        
        if context not in dct:
            dct[context] = []
        dct[context].append(words_list[i + context_length])
        
    return dct

    
def join_lst(text_lst: [str]) -> str:
    """ Helper function for generate_text and clean_text. 
    Concatenates together the currently generated text and next_word 
    chosen to be added.
    >>> join_strs(['hello', 'hello'])
    'hello hello'
    """
    
    s = ''
    for word in text_lst:
        s = s + ' ' + word
    return s.strip()


def generate_text(context_dict: dict[tuple[str], list[str]], 
                     num_words: int) -> str:
    """ From our context ditionnary, keep chaining current context to a random
    next work that procedes it according to however many words we want.
    """
    
    context_list = list(context_dict.keys())
    context = random.choice(context_list)
    
    text = list(context)
    num_words -= len(context)
    
    while num_words != 0:
 
        next_word = random.choice(context_dict[context])
    
        if context_dict[context] == []:
            context = random.choice(context_list)
            next_word = random.choice(context_dict[context])
        else:
            context = context[1:] + (next_word,)
        
        text.append(next_word)
        num_words -= 1
        
    return join_lst(text)


def clean_text(raw_text: str) -> str:
    """ Digests the raw generated text to be more grammatically correct
    Better punctuation, capitalization, no weird symbols, run on sentences
    and overall sensenicality.
    """
    
    text_list = raw_text.split()
    for i in range(len(text_list)):
        if i == 0:
            text_list[i] = text_list[i].capitalize()
        elif text_list[i].istitle() and text_list[i - 1][-1] != '.':
            text_list[i - 1] = text_list[i - 1][:-1] + '.'
        
        if i == len(text_list) - 1 and text_list[i][-1] != '.':
            text_list[i] = text_list[i] + '.'
            
        for char in text_list[i]:
            if char in '@#$%^&*()"\'[]':
                i_char = text_list[i].index(char)
                text_list[i] = text_list[i][:i_char] + text_list[i][i_char + 1:]
            
    return join_lst(text_list)
        

def generate_random_output(training_file: TextIO) -> str:
    """Return randomly generated output with num_words words based on a context
    of context_length words from the training text in open file training_file.
    >>> generate_random_output(training_file)
    """
    
    num_words, context_length = get_numwords_and_clength()
    
    word_list = training_file.read().split()
    
    dct = context_dictionary(word_list, context_length)
    
    raw_text = generate_text(dct, num_words)
    
    text = clean_text(raw_text)
    
    return text

training_file = get_file_decision()
print(generate_random_output(training_file))
