import re
import random

CSW = {}



def related(word, lexicon='csw'):
    my_result = []
    if lexicon == 'csw':
        for w in CSW:
            x = CSW[w][0].upper()
            if re.search("[^a-zA-Z]" + word + "[^a-zA-Z]", x) \
                    or re.search("[^a-zA-Z]" + word + "S[^a-zA-Z]", x) \
                    or re.search("[^a-zA-Z]" + word + ",[^a-zA-Z]", x):
                my_result.append(w)
    elif lexicon == 'twl':
        for w in TWL:
            x = TWL[w][0].upper()
            if re.search("[^a-zA-Z]" + word + "[^a-zA-Z]", x) \
                    or re.search("[^a-zA-Z]" + word + "S[^a-zA-Z]", x) \
                    or re.search("^" + word + "[^a-zA-Z]", x):
                my_result.append(w)

    num_results = len(my_result)
    p = -1
    msg = ''
    for x in my_result:
        p += 1
        if p < 30:
            msg += my_result[p] + "   "
        else:
            msg += '\nLimited to first 30 results'
            break
    return num_results, msg


def starts_with(word, lexicon='csw'):
    my_result = []
    if lexicon == 'csw':
        for w in CSW:
            if re.search("^" + word, w):
                my_result.append(w)
    elif lexicon == 'twl':
        for w in TWL:
            if re.search("^" + word, w):
                my_result.append(w)
    num_results = len(my_result)
    p = -1
    msg = ''
    for x in range(0, len(my_result)):
        p += 1
        if p < 30:
            msg += my_result[p] + "   "
        else:
            msg += '\nLimited to first 30 results'
            break
    return num_results, msg


def contains(word, lexicon='csw'):
    global cache_count
    global cache
    word = word.replace('?', '.').upper()
    my_result = []
    if lexicon == 'csw':
        for w in CSW:
            if re.search(word, w):
                my_result.append(w)
    elif lexicon == 'twl':
        for w in TWL:
            if re.search(word, w):
                my_result.append(w)
    num_results = len(my_result)
    p = -1
    msg = ''
    for x in my_result:
        p += 1
        if p < 30:
            msg += my_result[p] + "   "
        else:
            msg += '\nLimited to first 30 results'
            break
    return num_results, msg


def hidden(word, length, lexicon='csw'):
    phrase = word.replace(" ", "")
    msg = 'No hidden words'
    if lexicon == 'twl':
        for x in range(0, len(phrase) - length + 1):
            if phrase[x:x + length] in TWL:
                msg = msg + phrase[x:x + length] + " "
    if lexicon == 'csw':
        for x in range(0, len(phrase) - length + 1):
            if phrase[x:x + length] in CSW:
                msg = msg + phrase[x:x + length] + " "
    return msg


def pattern(word, lexicon='csw'):
    global cache_count
    global cache
    word = ('^' + word + '$').upper()
    my_result = []
    if lexicon == 'csw':
        for w in CSW:
            if re.search(word, w):
                my_result.append(w)
    elif lexicon == 'twl':
        for w in TWL:
            if re.search(word, w):
                my_result.append(w)
    num_results = len(my_result)
    p = -1
    msg = ''
    for x in my_result:
        p += 1
        if p < 30:
            msg += my_result[p] + "   "
        else:
            msg += '\nLimited to first 30 results'
            break
    return num_results, msg


def ends_with(word, lexicon='csw'):
    global cache_count
    global cache
    word = word.replace('?', '.').upper()
    my_result = []
    if lexicon == 'csw':
        for w in CSW:
            if re.search(word + "$", w):
                my_result.append(w)
    elif lexicon == 'twl':
        for w in TWL:
            if re.search(word + "$", w):
                my_result.append(w)
    num_results = len(my_result)
    p = -1
    msg = ''
    for x in my_result:
        p += 1
        if p < 30:
            msg += my_result[p] + "   "
        else:
            msg += '\nLimited to first 30 results'
            break
    return num_results, msg

def define(word, lexicon='csw'):
    my_result = ''
    num_results = 1
    if lexicon == 'csw':
        try:
            my_result = CSW[word][0]
        except KeyError:
            my_result = 'not found'
    elif lexicon == 'twl':
        try:
            my_result = TWL[word][0]
        except KeyError:
            my_result = 'not found'

    msg = word.upper() + " - " + my_result

    
    return msg


def info(word, lexicon='csw'):
    my_result = ''
    msg = ""
    if lexicon == 'csw':
        try:
            my_result = CSW[word]
        except KeyError:
            msg = "No such word"
    elif lexicon == 'twl':
        try:
            my_result = TWL[word]
        except KeyError:
            msg = "No such word"
    counter = -1
    for x in my_result:
        counter = counter + 1
        if counter == 0:
            msg = word + " - "
            counter += 1
        if counter == 1:
            msg = msg + x + "\n"
        if counter == 2:
            msg = msg + "Front Hooks: " + x + "\n"
        if counter == 3:
            msg = msg + "Back Hooks: " + x + "\n"
        if counter == 4:
            msg = msg + "Probability: " + str(x) + "\n"
        if counter == 5:
            msg = msg + "Alphagram: " + x
    msg = msg + "\nMiddle Hooks: "

    if lexicon == 'twl':
        for x in middle_hooks(word, 'twl'):
            msg = msg + x + " "
    if lexicon == 'csw':
        for x in middle_hooks(word, 'csw'):
            msg = msg + x + " "
    return msg


def random_word(lexicon='csw'):
    msg = ''
    if lexicon == 'csw':
        my_result = random.choice(list(CSW))
        msg = my_result + " - " + CSW[my_result][0]
    elif lexicon == 'twl':
        my_result = random.choice(list(TWL))
        msg = my_result + " - " + TWL[my_result][0]
    return msg


def anagram_1(word, lexicon='csw'):
    global cache_count
    my_result = ''
    if lexicon == 'csw':
        my_result = anagram(word, 'CSW')
    elif lexicon == 'twl':
        my_result = anagram(word, 'TWL')
    num_results = len(my_result)
    p = -1
    msg = ''
    for x in my_result:
        p += 1
        if p < 30:
            msg += my_result[p] + "   "
        else:
            msg += '\nLimited to first 30 results'
            break
    return num_results, msg


def drop_one(s):
    # RETURNS LIST OF STRINGS WITH ONE LETTER DROPPED
    result = []
    for x in range(0, len(s)):
        front = s[0:x]
        back = s[x + 1:]
        result.append(front + back)
    return result


def anagram(s, db='csw'):
    # RETURNS ANAGRAMS OF S, DB IS LEXICON
    my_result = []
    word_length = len(s)
    num_blanks = list(s).count('?')
    s = s.replace('?', '').upper()
    word2 = sorted(s.replace('?', ''))
    word3 = ''
    for y in range(num_blanks):
        word3 = word3 + '.?'
    for x in word2:
        word3 = word3 + x
        for y in range(num_blanks):
            word3 = word3 + '.?'
    expression = '^' + ''.join(word3) + '$'
    if db == 'CSW':
        for x in CSW:
            if re.search(expression, CSW[x][4]) and len(x) == word_length:
                my_result.append(x)
    elif db == 'TWL':
        for x in TWL:
            if re.search(expression, TWL[x][4]) and len(x) == word_length:
                my_result.append(x)
    return my_result


def middle_hooks(s, dic='csw'):
    # FINDS LETTERS THAT CAN BE ADDED TO THE MIDDLE OF A WORD
    result = []
    for x in range(1, len(s)):
        word1 = s[0:x] + '.' + s[x:]
        if dic == 'csw':
            for w in CSW:
                if re.search('^' + word1.upper() + '$', w):
                    result.append(w)
        elif dic == 'twl':
            for w in TWL:
                if re.search('^' + word1.upper() + '$', w):
                    result.append(w)
    return result




def open_files():
   

    # CSW DICTIONARY
    f = open("csw.dat", "r")
    line = f.readline().strip("\n").split('	')
    while line != ['']:
        CSW[line[0]] = line[1:]
        line = f.readline().strip("\n").split('	')
    f.close()


open_files()
