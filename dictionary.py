import re
import random

csw = {}
twl = {}
mw = {}
wordlist = {"csw":csw,"twl":twl, "mw":mw, "csw#":csw}


def related(word,lexicon):
    my_result = []
 
    for w in wordlist[lexicon]:
        x = wordlist[lexicon][w][0].upper()
        if re.search("[^a-zA-Z]" + word + "[^a-zA-Z]", x) \
                or re.search("[^a-zA-Z]" + word + "S[^a-zA-Z]", x) \
                or re.search("[^a-zA-Z]" + word + ",[^a-zA-Z]", x):
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
    my_result = []
    
    for w in wordlist[lexicon]:
        if re.search("^" + word, w):
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
    word = word.replace('?', '.').upper()
    my_result = []
    
    for w in wordlist[lexicon]:
        if re.search(word, w):
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
    word = ('^' + word + '$').upper()
    word = word.replace('?','.')
    word = word.replace('*','.*')
    my_result = []
    for w in wordlist[lexicon]:
        if re.search(word, w):
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
    my_result = []
    for w in wordlist[lexicon]:
        if re.search(word, w):
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
    
    word = word.replace('?', '.').upper()
    my_result = []
    
    for w in wordlist[lexicon]:
        if re.search(word + "$", w):
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
    s = s.replace('?', '').upper()
    word2 = sorted(s.replace('?', ''))
    word3 = ''
    for _ in range(num_blanks):
        word3 = word3 + '.?'
    for x in word2:
        word3 = word3 + x
        for _ in range(num_blanks):
            word3 = word3 + '.?'
    expression = '^' + ''.join(word3) + '$'
    
    for x in wordlist[lexicon]:
        if re.search(expression, wordlist[lexicon][x][4]) and len(x) == word_length:
            if len(wordlist[lexicon][x]) == 6 and lexicon == 'csw#':
                my_result.append(x+'#')
            else:
                my_result.append(x)
   
    return my_result


def middle_hooks(s,lexicon):
    # FINDS LETTERS THAT CAN BE ADDED TO THE MIDDLE OF A WORD
    result = []
    for x in range(1, len(s)):
        word1 = s[0:x] + '.' + s[x:]
        
        for w in wordlist[lexicon]:
            if re.search('^' + word1.upper() + '$', w):
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

open_files()

if __name__ == '__main__':
    print(crypto('XCCXBB','csw'))
