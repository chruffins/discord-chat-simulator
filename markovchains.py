import random
import os

fileOverride = True

if not fileOverride:
    file = input("Enter the file you want to process into random sentences: ")
else:
    file = "Official Team Facepalm/chatroom.txt"

def get_tokens_from_file(path):
    if os.path.exists(path):
        return open(path, encoding='utf-8', errors='ignore').read().split()
    else:
        print("This path doesn't exist.")

test_dict = {"bruh": 3, "what": 2, "kill": 4}

def build_successors_table(tokens):
        """Takes in a list of words or tokens. Return a dictionary: keys are words; values are lists of successor words. By default, we set the first word in tokens to be a successor to "."
        """
        table = {}
        prev = '.'
        for word in tokens:
            if prev not in table:
                table[prev] = []
            table[prev] += [word]
            prev = word
        return table

def build_successors_table_with_likelihoods(tokens):
    """Takes in a list of words or tokens. Return a dictionary: keys are words; values are lists of dictionaries of successor words and their chance of appearance. By default, we set the first word in tokens to be a successor to "."
    """
    table = {}
    prev = '.'
    for word in tokens:
        if prev not in table:
            table[prev] = {}
        if word not in table[prev]:
            table[prev].update({word: 1})
        else:
            table[prev][word] = table[prev][word] + 1
        prev = word
    return table

def get_word_likelihoods(dictionary):
    tbl = [item for subl in [[key] * value for key, value in dictionary.items()] for item in subl]
    return tbl + (['.'] * (1 + (len(tbl) // 10)))

def construct_sentence_using_likelihoods(word, table):
    """Returns a string that is a random sentence starting with word, and choosing successors from table.
    """

    result = ' '
    while word not in ['.', '!', '?']:
        result += word + ' '
        word = random.choice(get_word_likelihoods(table[word]))
    return result + word
    
def construct_sentence(word, table):
    """Returns a string that is a random sentence starting with word, and choosing successors from table.
    """

    result = ' '
    while word not in ['.', '!', '?']:
        result += word + ' '
        word = random.choice(table[word])
    return result + word

def random_sentence(table):
    text = construct_sentence(random.choice(table['.']), table)
    if text == " .":
        return ".fm"
    else:
        return text[1:-2]

def improved_random_sentence(table):
    text = construct_sentence_using_likelihoods(random.choice(list(table['.'].keys())), table)
    if text == " .":
        return ".fm"
    else:
        return text[1:-2]

tokens = get_tokens_from_file(file)
usetokens = build_successors_table(tokens)
newtokens = build_successors_table_with_likelihoods(tokens)

#print(get_word_likelihoods(test_dict))

for i in range(20):
    print(random_sentence(usetokens))

print('\n')

for i in range(20):
    print(improved_random_sentence(newtokens))

