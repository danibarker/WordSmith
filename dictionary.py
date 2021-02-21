import re
import random

csw = {}
twl = {}
mw = {}
wordlist = {"csw":csw,"twl":twl, "mw":mw, "csw#":csw}


def related(word,lexicon):
    word = word.replace('?', '.')
    pattern = re.compile(rf'(?<![A-Za-z])(?:{re.escape(word)})S?(?![A-Za-z])', re.IGNORECASE)
    my_result = []
 
    for w in wordlist[lexicon]:
        x = wordlist[lexicon][w][0]
        if pattern.search(x):
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

def define(word, lexicon):
    my_result = ''
    
    try:
            
        my_result = wordlist[lexicon][word][0]
            
    except KeyError:
        my_result = 'not found'
    try:
        if len(wordlist[lexicon][word]) == 6 and lexicon == 'csw#':
            msg = word.upper() + "# - " + my_result
        else:
            msg = word.upper() + " - " + my_result
    except KeyError:
        msg = word.upper() + " - " + my_result
   
    
    return msg


def info(word,lexicon):
    my_result = ''
    msg = ""
    
    try:
        my_result = wordlist[lexicon][word]
    except KeyError:
        msg = "No such word"
    
    counter = -1
    for x in my_result:
        counter = counter + 1
        if counter == 0:
            msg = word + " - "
            counter += 1
        if counter == 1:
            msg = msg + x 
        if counter == 2:
            msg = msg + "Front Hooks: " + x 
        if counter == 3:
            msg = msg + "Back Hooks: " + x 
        if counter == 4:
            msg = msg + "Probability: " + str(x) 
        if counter == 5:
            msg = msg + "Alphagram: " + x
    msg = msg + "Middle Hooks: "


    for x in middle_hooks(word,lexicon):
        msg = msg + x + " "
    return msg


def random_word(lexicon):
    msg = ''
    
    if wordlist[lexicon]:
        my_result = random.choice(list(wordlist[lexicon]))
        if len(wordlist[lexicon][my_result]) == 6 and lexicon == 'csw#':
            msg = my_result + "# - " + wordlist[lexicon][my_result][0]
        else:
            msg = my_result + " - " + wordlist[lexicon][my_result][0]

    return msg


def anagram_1(word,lexicon):
    
    my_result = ''
    
    my_result = anagram(word,lexicon)
    
    num_results = len(my_result)
    msg = ''
    for n,_ in enumerate(my_result):
        if len(msg) > 450 - len(my_result[n]):
            msg += f'Limited to first {n} results'
            break
        else:
            msg += my_result[n] + " "
    return num_results, msg


def anagram(s,lexicon):
    # RETURNS ANAGRAMS OF S, DB IS LEXICON
    my_result = []
    word_length = len(s)
    num_blanks = list(s).count('?')
    letters = sorted(s.replace('?', ''))
    mask = ''
    for _ in range(num_blanks):
        mask = mask + '.?'
    for letter in letters:
        mask = mask + letter
        for _ in range(num_blanks):
            mask = mask + '.?'
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
