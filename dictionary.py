import re
import random

wordlist = {}
f = open('config.dat','r')
irct = f.readline()
clienti = f.readline()
nickn = f.readline().strip().lower()
initc = f.readline().split(',')
lexicon = f.readline()
f.close()


def related(word):
    my_result = []
 
    for w in wordlist:
        x = wordlist[w][0].upper()
        if re.search("[^a-zA-Z]" + word + "[^a-zA-Z]", x) \
                or re.search("[^a-zA-Z]" + word + "S[^a-zA-Z]", x) \
                or re.search("[^a-zA-Z]" + word + ",[^a-zA-Z]", x):
            if len(wordlist[w]) == 6:
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


def starts_with(word):
    my_result = []
    
    for w in wordlist:
        if re.search("^" + word, w):
            if len(wordlist[w]) == 6:
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


def contains(word):
    global cache_count
    global cache
    word = word.replace('?', '.').upper()
    my_result = []
    
    for w in wordlist:
        if re.search(word, w):
            if len(wordlist[w]) == 6:
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


def hidden(word, length):
    phrase = word.replace(" ", "")
    msg = 'No hidden words'
    
    for x in range(0, len(phrase) - length + 1):
        if phrase[x:x + length] in wordlist:
            msg = msg + phrase[x:x + length] + " "
    return msg


def pattern(word):
    global cache_count
    global cache
    word = ('^' + word + '$').upper()
    word = word.replace('?','.')
    word = word.replace('*','.*')
    my_result = []
    for w in wordlist:
        if re.search(word, w):
            if len(wordlist[w]) == 6:
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

def regex(word):
    global cache_count
    global cache
    my_result = []
    for w in wordlist:
        if re.search(word, w):
            if len(wordlist[w]) == 6:
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


def ends_with(word):
    global cache_count
    global cache
    word = word.replace('?', '.').upper()
    my_result = []
    
    for w in wordlist:
        if re.search(word + "$", w):
            if len(wordlist[w]) == 6:
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

def define(word):
    my_result = ''
    num_results = 1
    
    try:
            
        my_result = wordlist[word][0]
            
    except KeyError:
        my_result = 'not found'
    try:
        if len(wordlist[word]) == 6:
            msg = word.upper() + "# - " + my_result
        else:
            msg = word.upper() + " - " + my_result
    except KeyError:
        msg = word.upper() + " - " + my_result
   
    
    return msg


def info(word):
    my_result = ''
    msg = ""
    
    try:
        my_result = wordlist[word]
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


    for x in middle_hooks(word):
        msg = msg + x + " "
    return msg


def random_word():
    msg = ''
    
    my_result = random.choice(list(wordlist))
    if len(wordlist[my_result]) == 6:
        msg = my_result + "# - " + wordlist[my_result][0]
    else:
        msg = my_result + " - " + wordlist[my_result][0]

    return msg


def anagram_1(word):
    global cache_count
    my_result = ''
    
    my_result = anagram(word)
    
    num_results = len(my_result)
    msg = ''
    for n,x in enumerate(my_result):
        if len(msg) > 450 - len(my_result[n]):
            msg += f'Limited to first {n} results'
            break
        else:
            msg += my_result[n] + " "
    return num_results, msg


def anagram(s):
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
    
    for x in wordlist:
        if re.search(expression, wordlist[x][4]) and len(x) == word_length:
            if len(wordlist[x]) == 6:
                my_result.append(x+'#')
            else:
                my_result.append(x)
   
    return my_result


def middle_hooks(s):
    # FINDS LETTERS THAT CAN BE ADDED TO THE MIDDLE OF A WORD
    result = []
    for x in range(1, len(s)):
        word1 = s[0:x] + '.' + s[x:]
        
        for w in wordlist:
            if re.search('^' + word1.upper() + '$', w):
                result.append(w)
    return result

def crypto(word):
    newword = []
    groups = []
    dropped = 0
    for n,letter in enumerate(word):
        if letter in groups:

            newword.append(r'\ '[0]+f'{groups.index(letter)+1}')
        else:
            add = r'\ '[0]+r'|\ '[:-1].join(f'{n+1}' for n in range(len(groups)))
            if len(newword)>0:
                newword.append(f'(?!{add})')
            newword.append(f'(.)')
            
            groups.append(letter)
    return regex(f'^{"".join(newword)}$')



def open_files():
   

    # wordlist DICTIONARY
    f = open(f"{lexicon}.dat", "r")
    line = f.readline().strip("\n").split('	')
    while line != ['']:
        wordlist[line[0]] = line[1:]
        line = f.readline().strip("\n").split('	')
    f.close()


open_files()

if __name__ == '__main__':
    print(crypto('XCCXBB'))
