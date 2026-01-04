from typing import TextIO
import random

training_file = open('adele.txt')


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
    """ Helper function for generate_text. Concatenates together the currently
    generated text and next_word chosen to be added.
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
    

def generate_random_output(training_file: TextIO,
                           context_length: int,
                           num_words: int) -> str:
    """Return randomly generated output with num_words words based on a context
    of context_length words from the training text in open file training_file.
    >>> generate_random_output(training_file, 2, 20)
    """
    word_list = training_file.read().split()
    
    dct = context_dictionary(word_list, context_length)
    
    text = generate_text(dct, num_words)
    
    return text
