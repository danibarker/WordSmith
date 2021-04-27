import inflect
import re
import random

csw = {}
twl = {}
mw = {}
wordlist = {"csw":csw,"twl":twl, "mw":mw, "csw#":csw}
engine = inflect.engine()


def related(word,lexicon):
    word = word.replace('?', '.')
    pattern = re.compile(rf'(?<![A-Za-z])(?:{re.escape(word)})S?(?![A-Za-z])', re.IGNORECASE)
    offensive = re.compile(rf'\(.*offensive.*\)|offensive(?:,| term| word)', re.IGNORECASE)
    my_result = []
 
    for w in wordlist[lexicon]:
        x = wordlist[lexicon][w][0]
        if pattern.search(x) and not offensive.search(x):
            if len(wordlist[lexicon][w]) == 6 and lexicon == 'csw#':
                my_result.append(w+'#')
            else:
                my_result.append(w)
    
    num_results = len(my_result)
    msg = ''
    for n,x in enumerate(my_result):
        if len(msg) > 450 - len(my_result[n]):
            msg += f'Limited to first {n} results'
            break
        else:
            msg += my_result[n] + " "
    return num_results, msg


def starts_with(word,lexicon):
    word = word.replace('?', '.')
    word_length = len(word)
    pattern = re.compile(rf'^(?:{word})', re.IGNORECASE)
    my_result = []
    
    for w in wordlist[lexicon]:
        if len(w) >= word_length and pattern.match(w):
            if len(wordlist[lexicon][w]) == 6 and lexicon == 'csw#':
                my_result.append(w+'#')
            else:
                my_result.append(w)
   
    num_results = len(my_result)
    msg = ''
    for n,_ in enumerate(my_result):
        if len(msg) > 450 - len(my_result[n]):
            msg += f'Limited to first {n} results'
            break
        else:
            msg += my_result[n] + " "
    return num_results, msg


def contains(word,lexicon):
    word = word.replace('?', '.')
    word_length = len(word)
    pattern = re.compile(word, re.IGNORECASE)
    my_result = []
    
    for w in wordlist[lexicon]:
        if len(w) >= word_length and pattern.search(w):
            if len(wordlist[lexicon][w]) == 6 and lexicon == 'csw#':
                my_result.append(w+'#')
            else:
                my_result.append(w)

    num_results = len(my_result)
    msg = ''
    for n,_ in enumerate(my_result):
        if len(msg) > 450 - len(my_result[n]):
            msg += f'Limited to first {n} results'
            break
        else:
            msg += my_result[n] + " "
    return num_results, msg


def hidden(word, length,lexicon):
    phrase = word.replace(" ", "")
    msg = 'No hidden words'
    
    for x in range(0, len(phrase) - length + 1):
        if phrase[x:x + length] in wordlist[lexicon]:
            msg = msg + phrase[x:x + length] + " "
    return msg


def pattern(word,lexicon):
    word = word.replace('?','.')
    word = word.replace('*','.*')
    word = re.sub('(\\d+)','.{\\1}', word)
    pattern = re.compile(rf'^(?:{word})$', re.IGNORECASE)
    my_result = []

    for w in wordlist[lexicon]:
        if pattern.match(w):
            if len(wordlist[lexicon][w]) == 6 and lexicon == 'csw#':
                my_result.append(w+'#')
            else:
                my_result.append(w)
   
    num_results = len(my_result)
    msg = ''
    for n,_ in enumerate(my_result):
        if len(msg) > 450 - len(my_result[n]):
            msg += f'Limited to first {n} results'
            break
        else:
            msg += my_result[n] + " "
    return num_results, msg


def regex(word,lexicon):
    pattern = re.compile(word, re.IGNORECASE)
    my_result = []

    for w in wordlist[lexicon]:
        if pattern.search(w):
            if len(wordlist[lexicon][w]) == 6 and lexicon == 'csw#':
                my_result.append(w+'#')
            else:
                my_result.append(w)
   
    num_results = len(my_result)
    msg = ''
    for n,_ in enumerate(my_result):
        if len(msg) > 450 - len(my_result[n]):
            msg += f'Limited to first {n} results'
            break
        else:
            msg += my_result[n] + " "
    return num_results, msg


def ends_with(word,lexicon):
    word = word.replace('?', '.')
    word_length = len(word)
    pattern = re.compile(rf'(?:{word})$', re.IGNORECASE)
    my_result = []
    
    for w in wordlist[lexicon]:
        if len(w) >= word_length and pattern.search(w):
            if len(wordlist[lexicon][w]) == 6 and lexicon == 'csw#':
                my_result.append(w+'#')
            else:
                my_result.append(w)
  
    num_results = len(my_result)
    msg = ''
    for n,_ in enumerate(my_result):
        if len(msg) > 450 - len(my_result[n]):
            msg += f'Limited to first {n} results'
            break
        else:
            msg += my_result[n] + " "
    return num_results, msg


def check(word, lexicon):
    my_result = ''
    try:
        my_result = wordlist[lexicon][word][0]
        return word.upper() + ' is valid VoteYea'
    except KeyError:
        return word.upper() + '* not found VoteNay'


def define(word, lexicon):
    if word in wordlist[lexicon]:
        my_result = wordlist[lexicon][word][0]
        if len(wordlist[lexicon][word]) == 6 and lexicon == 'csw#':
            msg = word.upper() + "# - " + my_result
        else:
            msg = word.upper() + " - " + my_result
        return msg
    else:
        return word + '* - not found'


def info(word,lexicon,alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    msg = ""
    
    try:
        if word in wordlist[lexicon]:
            my_result = wordlist[lexicon][word]
            counter = -1
            for x in my_result:
                counter = counter + 1
                if counter == 0:
                    msg = word
                    counter += 1
                if counter == 1:
                    msg = msg + " - " + x
                if counter == 2 and x:
                    msg = msg + " Front Hooks: " + x
                if counter == 3 and x:
                    msg = msg + " Back Hooks: " + x
                if counter == 4:
                    msg = msg + " Probability: " + str(x)
                if counter == 5:
                    order = dict(zip(alphabet, range(len(alphabet))))
                    msg = msg + " Alphagram: " + ''.join(sorted(x, key=lambda c:order[c]))
        else:
            return "No such word"
    except KeyError:
        return "No such lexicon"

    hooks = middle_hooks(word,lexicon)
    if hooks:
        msg = msg + " Middle Hooks:"
        for x in hooks:
            msg = msg + " " + x
    return msg


def hook(word,lexicon):
    msg = word
    
    try:
        if word in wordlist[lexicon]:
            my_result = wordlist[lexicon][word]
            counter = -1
            for x in my_result:
                counter = counter + 1
                if counter == 1 and x:
                    msg = msg + " Front Hooks: " + x
                if counter == 2 and x:
                    msg = msg + " Back Hooks: " + x
        else:
            msg = msg + "*"
    except KeyError:
        return "No such lexicon"

    hooks = middle_hooks(word,lexicon)
    if hooks:
        msg = msg + " Middle Hooks:"
        for x in hooks:
            msg = msg + " " + x
    return msg.lstrip()


def random_word(word_length,lexicon):
    if word_length <= 1 or word_length > 15:
        word_length = None
    msg = ''
    if wordlist[lexicon]:
        words = list(wordlist[lexicon])
        my_result = select_random_word(word_length, words)
        if len(wordlist[lexicon][my_result]) == 6 and lexicon == 'csw#':
            msg = my_result + "# - " + wordlist[lexicon][my_result][0]
        else:
            msg = my_result + " - " + wordlist[lexicon][my_result][0]
    return msg


def select_random_word(word_length,words):
    my_result = random.choice(words)
    while word_length is not None and len(my_result) != word_length:
        my_result = random.choice(words)
    return my_result


def anagram_1(word,lexicon):
    
    my_result = anagram(word,lexicon)
    num_results = len(my_result)
    if num_results == 0:
        msg = 'No anagrams found'
    else:
        msg = ''
        for n,_ in enumerate(my_result):
            if len(msg) > 450 - len(my_result[n]):
                msg += f'Limited to first {n} results'
                break
            else:
                msg += my_result[n] + " "
    return num_results, msg.rstrip()


def anagram(s,lexicon):
    # RETURNS ANAGRAMS OF S, DB IS LEXICON
    my_result = []
    word_length = len(s)
    num_blanks = list(s).count('?')
    letters = sorted(s.replace('?', '').upper())
    mask = ''
    alpha = 'A'
    for letter in letters:
        if num_blanks > 0 and letter != alpha:
            if num_blanks == 1:
                mask = mask + ('[%c-%c]?' % (alpha, chr(ord(letter)-1)))
            else:
                mask = mask + ('[%c-%c]{0,%d}' % (alpha, chr(ord(letter)-1), num_blanks))
            alpha = letter
        mask = mask + letter
    if num_blanks > 0:
        if num_blanks == 1:
            mask = mask + ('[%c-Z]?' % (alpha))
        else:
            mask = mask + ('[%c-Z]{0,%d}' % (alpha, num_blanks))
    pattern = re.compile('^%s$' % ''.join(mask), re.IGNORECASE)
    
    for word in wordlist[lexicon]:
        if len(word) == word_length and pattern.match(wordlist[lexicon][word][4]):
            if len(wordlist[lexicon][word]) == 6 and lexicon == 'csw#':
                my_result.append(word+'#')
            else:
                my_result.append(word)
   
    return my_result


def middle_hooks(word,lexicon):
    # FINDS LETTERS THAT CAN BE ADDED TO THE MIDDLE OF A WORD
    word = word.replace('?', '.')
    word_length = len(word)
    result = []

    for x in range(1, len(word)):
        pattern = re.compile(rf'^(?:{word[0:x]}.{word[x:]})$', re.IGNORECASE)
        for w in wordlist[lexicon]:
            if len(w) > word_length and pattern.match(w):
                result.append(w)
    return result

def crypto(word,lexicon):
    newword = []
    groups = []
    for letter in word:
        if letter in groups:

            newword.append(r'\ '[0]+f'{groups.index(letter)+1}')
        else:
            add = r'\ '[0]+r'|\ '[:-1].join(f'{n+1}' for n in range(len(groups)))
            if len(newword)>0:
                newword.append(f'(?!{add})')
            newword.append(f'(.)')
            
            groups.append(letter)
    return regex(f'^{"".join(newword)}$',lexicon)



def open_files():
    # wordlist DICTIONARY
    try:
        f = open("csw.dat", "r")
        line = f.readline().strip("\n").split('	')
        while line != ['']:
            csw[line[0]] = line[1:]
            line = f.readline().strip("\n").split('	')
        f.close()
    except FileNotFoundError:
        print("csw.dat not found")
    try:
        f = open("twl.dat", "r")
        line = f.readline().strip("\n").split('	')
        while line != ['']:
            twl[line[0]] = line[1:]
            line = f.readline().strip("\n").split('	')
        f.close()
    except FileNotFoundError:
        print("twl.dat not found")
    try:
        f = open("mw.dat", "r")
        line = f.readline().strip("\n").split('	')
        while line != ['']:
            mw[line[0]] = line[1:]
            line = f.readline().strip("\n").split('	')
        f.close()
    except FileNotFoundError:
        print("mw.dat not found")

if __name__ == '__main__':
    print(crypto('XCCXBB','csw'))
