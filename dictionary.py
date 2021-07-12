import inflect
import re
import random

csw = {}
twl = {}
mw = {}
wordlist = {"csw":csw,"twl":twl, "mw":mw, "csw#":csw}
engine = inflect.engine()


def related(stem, lexicon):
    stem = stem.replace('?', '.')
    pattern = re.compile(rf'(?<![a-z])(?:{re.escape(stem)})s?(?![a-z])', re.IGNORECASE)
    my_result = []
 
    for word in wordlist[lexicon]:
        definition = wordlist[lexicon][word][0]
        if pattern.search(definition) and not offensive(definition):
            if len(wordlist[lexicon][word]) == 6 and lexicon == 'csw#':
                my_result.append(word+'#')
            else:
                my_result.append(word)
    
    num_results = len(my_result)
    msg = ''
    for n,x in enumerate(my_result):
        if len(msg) > 450 - len(my_result[n]):
            msg += f'Limited to first {n} results'
            break
        else:
            msg += my_result[n] + " "
    return num_results, msg


def starts_with(hook, lexicon):
    hook = hook.replace('?', '.')
    hook_length = len(hook)
    pattern = re.compile(rf'^(?:{hook})', re.IGNORECASE)
    my_result = []
    
    for word in wordlist[lexicon]:
        if len(word) >= hook_length and pattern.match(word):
            definition = wordlist[lexicon][word][0]
            if not offensive(definition):
                if len(wordlist[lexicon][word]) == 6 and lexicon == 'csw#':
                    my_result.append(word+'#')
                else:
                    my_result.append(word)
   
    num_results = len(my_result)
    msg = ''
    for n,_ in enumerate(my_result):
        if len(msg) > 450 - len(my_result[n]):
            msg += f'Limited to first {n} results'
            break
        else:
            msg += my_result[n] + " "
    return num_results, msg


def contains(stem, lexicon):
    stem = stem.replace('?', '.')
    stem_length = len(stem)
    pattern = re.compile(stem, re.IGNORECASE)
    my_result = []
    
    for word in wordlist[lexicon]:
        if len(word) >= stem_length and pattern.search(word):
            definition = wordlist[lexicon][word][0]
            if not offensive(definition):
                if len(wordlist[lexicon][word]) == 6 and lexicon == 'csw#':
                    my_result.append(word+'#')
                else:
                    my_result.append(word)

    num_results = len(my_result)
    msg = ''
    for n,_ in enumerate(my_result):
        if len(msg) > 450 - len(my_result[n]):
            msg += f'Limited to first {n} results'
            break
        else:
            msg += my_result[n] + " "
    return num_results, msg


def hidden(length, phrase, lexicon):
    phrase = phrase.replace(' ', '')
    msg = 'No hidden words'
    
    for x in range(0, len(phrase) - length + 1):
        word = phrase[x:x + length]
        if word in wordlist[lexicon]:
            definition = wordlist[lexicon][word][0]
            if not offensive(definition):
                msg = msg + word + ' '
    return msg


def pattern(stem, lexicon):
    stem = stem.replace('?','.')
    stem = stem.replace('*','.*')
    stem = re.sub('(\\d+)','.{\\1}', stem)
    pattern = re.compile(rf'^(?:{stem})$', re.IGNORECASE)
    my_result = []

    for word in wordlist[lexicon]:
        if pattern.match(word):
            definition = wordlist[lexicon][word][0]
            if not offensive(definition):
                if len(wordlist[lexicon][word]) == 6 and lexicon == 'csw#':
                    my_result.append(word+'#')
                else:
                    my_result.append(word)
   
    num_results = len(my_result)
    msg = ''
    for n,_ in enumerate(my_result):
        if len(msg) > 450 - len(my_result[n]):
            msg += f'Limited to first {n} results'
            break
        else:
            msg += my_result[n] + " "
    return num_results, msg


def regex(stem, lexicon):
    pattern = re.compile(stem, re.IGNORECASE)
    my_result = []

    for word in wordlist[lexicon]:
        if pattern.search(word):
            definition = wordlist[lexicon][word][0]
            if not offensive(definition):
                if len(wordlist[lexicon][word]) == 6 and lexicon == 'csw#':
                    my_result.append(word+'#')
                else:
                    my_result.append(word)
   
    num_results = len(my_result)
    msg = ''
    for n,_ in enumerate(my_result):
        if len(msg) > 450 - len(my_result[n]):
            msg += f'Limited to first {n} results'
            break
        else:
            msg += my_result[n] + " "
    return num_results, msg


def ends_with(hook, lexicon):
    hook = hook.replace('?', '.')
    hook_length = len(hook)
    pattern = re.compile(rf'(?:{hook})$', re.IGNORECASE)
    my_result = []
    
    for word in wordlist[lexicon]:
        if len(word) >= hook_length and pattern.search(word):
            definition = wordlist[lexicon][word][0]
            if not offensive(definition):
                if len(wordlist[lexicon][word]) == 6 and lexicon == 'csw#':
                    my_result.append(word+'#')
                else:
                    my_result.append(word)
  
    num_results = len(my_result)
    msg = ''
    for n,_ in enumerate(my_result):
        if len(msg) > 450 - len(my_result[n]):
            msg += f'Limited to first {n} results'
            break
        else:
            msg += my_result[n] + " "
    return num_results, msg


def check(stem, lexicon):
    if stem in wordlist[lexicon]:
        definition = wordlist[lexicon][stem][0]
        return offensive(definition), True
    else:
        return False, False


def offensive(definition):
    pattern = re.compile(rf'\([a-z ]*\boffensive\b[a-z ]*\)|\boffensive\b(?:,| term| word)', re.IGNORECASE)
    return pattern.search(definition)


def define(stem, lexicon):
    offensive, valid = check(stem, lexicon)
    if offensive:
        return None
    elif valid:
        word = wordlist[lexicon][stem][0]
        if len(wordlist[lexicon][stem]) == 6 and lexicon == 'csw#':
            msg = word.upper() + '# - ' + word
        else:
            msg = word.upper() + ' - ' + word
        return msg
    else:
        return stem + '* - not found'


def info(stem, lexicon, alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    msg = ""
    
    try:
        if stem in wordlist[lexicon]:
            entry = wordlist[lexicon][stem]
            counter = -1
            for x in entry:
                counter = counter + 1
                if counter == 0:
                    msg = stem
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

    hooks = middle_hooks(stem, lexicon)
    if hooks:
        msg = msg + " Middle Hooks:"
        for x in hooks:
            msg = msg + " " + x
    return msg


def hook(stem, lexicon):
    msg = stem
    
    try:
        if stem in wordlist[lexicon]:
            entry = wordlist[lexicon][stem]
            counter = -1
            for x in entry:
                counter = counter + 1
                if counter == 1 and x:
                    msg = msg + " Front Hooks: " + x
                if counter == 2 and x:
                    msg = msg + " Back Hooks: " + x
        else:
            msg = msg + "*"
    except KeyError:
        return "No such lexicon"

    hooks = middle_hooks(stem, lexicon)
    if hooks:
        msg = msg + " Middle Hooks:"
        for x in hooks:
            msg = msg + " " + x
    return msg.lstrip()


def random_word(word_length, lexicon):
    if word_length <= 1 or word_length > 15:
        word_length = None
    msg = ''
    if wordlist[lexicon]:
        words = list(wordlist[lexicon])
        word = select_random_word(word_length, words)
        definition = wordlist[lexicon][word][0]
        while offensive(definition):
            word = select_random_word(word_length, words)
            definition = wordlist[lexicon][word][0]
        if len(wordlist[lexicon][word]) == 6 and lexicon == 'csw#':
            msg = word + '# - ' + wordlist[lexicon][word][0]
        else:
            msg = word + ' - ' + wordlist[lexicon][word][0]
    return msg


def select_random_word(word_length, words):
    word = random.choice(words)
    while word_length is not None and len(word) != word_length:
        word = random.choice(words)
    return word


def anagram_1(rack, lexicon):
    # RETURNS ANAGRAMS OF RACK, DB IS LEXICON
    my_result = anagram(rack, lexicon)
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
                msg += my_result[n] + ' '
    return num_results, msg.rstrip()


def anagram(rack, lexicon):
    # RETURNS ANAGRAMS OF RACK, DB IS LEXICON
    words = []
    word_length = len(rack)
    num_blanks = list(rack).count('?')
    letters = sorted(rack.replace('?', '').upper())
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
            definition = wordlist[lexicon][word][0]
            if not offensive(definition):
                if len(wordlist[lexicon][word]) == 6 and lexicon == 'csw#':
                    words.append(word+'#')
                else:
                    words.append(word)
    return words


def middle_hooks(stem, lexicon):
    # FINDS LETTERS THAT CAN BE ADDED TO THE MIDDLE OF A WORD
    stem = stem.replace('?', '.')
    stem_length = len(stem)
    result = []

    for x in range(1, stem_length):
        pattern = re.compile(rf'^(?:{stem[0:x]}.{stem[x:]})$', re.IGNORECASE)
        for word in wordlist[lexicon]:
            if len(word) > stem_length and pattern.match(word):
                definition = wordlist[lexicon][word][0]
                if not offensive(definition):
                    result.append(word)
    return result


def crypto(cipher, lexicon):
    words = []
    groups = []
    for letter in cipher:
        if letter in groups:
            words.append(r'\ '[0]+f'{groups.index(letter)+1}')
        else:
            add = r'\ '[0]+r'|\ '[:-1].join(f'{n+1}' for n in range(len(groups)))
            if len(words)>0:
                words.append(f'(?!{add})')
            words.append(f'(.)')
            
            groups.append(letter)
    return regex(f'^{"".join(words)}$', lexicon)



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

