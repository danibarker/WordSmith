from alphagram import alphagram
import random
import re

csw = {}
twl = {}
mw = {}
wordlist = {"csw":csw, "twl":twl, "mw":mw, "csw#":csw}


def related_command(stem, lexicon):
    words = related(stem,lexicon)
    my_result = []
    for word in words:
        my_result.append(decorate(word, lexicon))
    return my_result


def related(stem, lexicon):
    stem = stem.replace('?', '.')
    pattern = re.compile(rf'(?<![a-z]){re.escape(stem)}s?(?![a-z])', re.IGNORECASE)
    my_result = []
 
    for word in wordlist[lexicon]:
        definition = wordlist[lexicon][word][0]
        if pattern.search(definition) and not offensive(definition):
            my_result.append(word)
    return my_result


def begins_with(hook, lexicon):
    hook = hook.replace('?', '.')
    hook_length = len(hook)
    pattern = re.compile(rf'^{hook}', re.IGNORECASE)
    my_result = []
    
    for word in wordlist[lexicon]:
        if len(word) >= hook_length and pattern.match(word):
            definition = wordlist[lexicon][word][0]
            if not offensive(definition):
                my_result.append(decorate(word, lexicon))
    return my_result


def contains(stem, lexicon):
    stem = stem.replace('?', '.')
    stem_length = len(stem)
    pattern = re.compile(stem, re.IGNORECASE)
    my_result = []
    
    for word in wordlist[lexicon]:
        if len(word) >= stem_length and pattern.search(word):
            definition = wordlist[lexicon][word][0]
            if not offensive(definition):
                my_result.append(decorate(word, lexicon))
    return my_result


def hidden(length, phrase, lexicon):
    phrase = phrase.replace(' ', '')
    my_result = []
    for x in range(0, len(phrase) - length + 1):
        word = phrase[x:x + length]
        if word in wordlist[lexicon]:
            definition = wordlist[lexicon][word][0]
            if not offensive(definition):
                my_result.append(decorate(word, lexicon))
    return my_result


def pattern(stem, lexicon):
    stem = stem.replace('?','.')
    stem = stem.replace('*','.*')
    stem = re.sub('(\\d+)','.{\\1}', stem)
    pattern = re.compile(rf'^{stem}$', re.IGNORECASE)
    my_result = []

    for word in wordlist[lexicon]:
        if pattern.match(word):
            definition = wordlist[lexicon][word][0]
            if not offensive(definition):
                my_result.append(decorate(word, lexicon))
    return my_result


def regex(stem, lexicon):
    pattern = re.compile(stem, re.IGNORECASE)
    my_result = []

    for word in wordlist[lexicon]:
        if pattern.search(word):
            definition = wordlist[lexicon][word][0]
            if not offensive(definition):
                my_result.append(decorate(word, lexicon))
    return my_result


def ends_with(hook, lexicon):
    hook = hook.replace('?', '.')
    hook_length = len(hook)
    pattern = re.compile(rf'{hook}$', re.IGNORECASE)
    my_result = []
    
    for word in wordlist[lexicon]:
        if len(word) >= hook_length and pattern.search(word):
            definition = wordlist[lexicon][word][0]
            if not offensive(definition):
                my_result.append(decorate(word, lexicon))
    return my_result


def check(stem, lexicon):
    if stem in wordlist[lexicon]:
        definition = wordlist[lexicon][stem][0]
        return offensive(definition), True
    else:
        return False, False


def common(stem, lexicon):
    cel = []
    try:
        with open("CEL/cel.txt", "r") as f:
            cel = f.read().upper().splitlines()
    except FileNotFoundError:
        print("CEL/cel.txt not found")

    if (stem in cel) and (stem in wordlist[lexicon]):
        definition = wordlist[lexicon][stem][0]
        return offensive(definition), True
    else:
        return False, False


def wordnik(stem, lexicon):
    wordnik = []
    try:
        with open("wordlist/wordlist-20210729.txt", "r") as f:
            wordnik = f.read().replace('"', '').upper().splitlines()
    except FileNotFoundError:
        print("wordlist/wordlist-20210729.txt not found")

    if (stem in wordnik) and (stem in wordlist[lexicon]):
        definition = wordlist[lexicon][stem][0]
        return offensive(definition), True
    else:
        return False, False


def decorate(word, lexicon, mark=None):
    if lexicon == 'csw#' and len(wordlist[lexicon][word]) == 7:
       return (word, wordlist[lexicon][word][-1])
    else:
       return (word, mark)


def offensive(definition):
    pattern = re.compile(rf'\([a-z ]*\boffensive\b[a-z ]*\)|\boffensive\b(?:,| term| word)', re.IGNORECASE)
    return pattern.search(definition)


def define(word, lexicon):
    offensive, valid = check(word, lexicon)
    if offensive:
        return None
    elif valid:
        return ('%s%s' % decorate(word, lexicon, '')) + ' - ' + wordlist[lexicon][word][0]
    else:
        return word + '* - not found'


def inflect(word, lexicon):
    offensive, valid = check(word, lexicon)
    if offensive:
        return None
    elif valid:
        if not re.match('\[.*[A-Z]+\]', wordlist[lexicon][word][1]):
            if stem := re.match('([A-Z]+), .*', wordlist[lexicon][word][0]):
                word = stem.group(1)
        return ('%s%s' % decorate(word, lexicon, '')) + ' ' + wordlist[lexicon][word][1]
    else:
        return word + '* - not found'


def info(stem, lexicon, alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
    msg = ''
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
                    msg = msg + ' - ' + x
                if counter == 2 and x:
                    msg = msg + ' Front Hooks: ' + x
                if counter == 3 and x:
                    msg = msg + ' Back Hooks: ' + x
                if counter == 4:
                    msg = msg + ' Probability: ' + str(x)
                if counter == 5:
                    msg = msg + ' Alphagram: ' + alphagram(x, alphabet)

            hooks = middle_hooks(stem, lexicon)
            if hooks:
                msg = msg + ' Middle Hooks:'
                for x in hooks:
                    msg = msg + ' ' + x
            return msg
        else:
            return 'No such word'
    except KeyError:
        return 'No such lexicon'


def hook(stem, lexicon):
    msg = ''
    try:
        if stem in wordlist[lexicon]:
            entry = wordlist[lexicon][stem]
            counter = -1
            for x in entry:
                counter = counter + 1
                if counter == 1 and x:
                    msg = msg + ' Front: ' + x
                if counter == 2 and x:
                    msg = msg + ' Back: ' + x
        else:
            hooks = front_hooks(stem, lexicon)
            if hooks:
                msg = msg + ' Front:'
                for x in hooks:
                    msg = msg + ' ' + x
            hooks = back_hooks(stem, lexicon)
            if hooks:
                msg = msg + ' Back:'
                for x in hooks:
                    msg = msg + ' ' + x

        hooks = middle_hooks(stem, lexicon)
        if hooks:
            msg = msg + ' Middle:'
            for x in hooks:
                msg = msg + ' ' + x
        return 'No hooks found' if msg == '' else msg.lstrip()
    except KeyError:
        return 'No such lexicon'


def random_word(word_length, lexicon, related_word):
    if word_length <= 1 or word_length > 15:
        word_length = None
    msg = ''
    if wordlist[lexicon]:
        words = list(wordlist[lexicon]) if related_word == '' else related(related_word, lexicon)
        word = select_random_word(word_length, words)
        definition = wordlist[lexicon][word][0]
        while offensive(definition):
            word = select_random_word(word_length, words)
            definition = wordlist[lexicon][word][0]
        msg = ('%s%s' % decorate(word, lexicon, '')) + ' - ' + definition
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
        for n, word in enumerate(my_result):
            if len(msg) + len(word) > 465:
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
                words.append(decorate(word, lexicon))
    return words


def back_hooks(stem, lexicon):
    stem = stem.replace('?', '.')
    stem_length = len(stem)
    result = []

    pattern = re.compile(rf'^{stem}.$', re.IGNORECASE)
    for word in wordlist[lexicon]:
        if len(word) > stem_length and pattern.match(word):
            definition = wordlist[lexicon][word][0]
            if not offensive(definition):
                result.append(decorate(word, lexicon))
    return result


def front_hooks(stem, lexicon):
    stem = stem.replace('?', '.')
    stem_length = len(stem)
    result = []

    pattern = re.compile(rf'^.{stem}$', re.IGNORECASE)
    for word in wordlist[lexicon]:
        if len(word) > stem_length and pattern.match(word):
            definition = wordlist[lexicon][word][0]
            if not offensive(definition):
                result.append(decorate(word, lexicon))
    return result


def middle_hooks(stem, lexicon):
    stem = stem.replace('?', '.')
    stem_length = len(stem)
    result = []

    for x in range(1, stem_length):
        pattern = re.compile(rf'^{stem[:x]}.{stem[x:]}$', re.IGNORECASE)
        for word in wordlist[lexicon]:
            if len(word) > stem_length and pattern.match(word):
                definition = wordlist[lexicon][word][0]
                if not offensive(definition):
                    result.append(decorate(word, lexicon))
    return result


def stem(rack, lexicon):
    rack = rack.replace('?', '.')
    word_length = len(rack)-1
    result = []

    try:
        for x in range(0, word_length+1):
            pattern = re.compile(rf'^{rack[:x]}{rack[x+1:]}$', re.IGNORECASE)
            for word in wordlist[lexicon]:
                if len(word) == word_length and pattern.match(word):
                    definition = wordlist[lexicon][word][0]
                    if not offensive(definition):
                        result.append(word)
        return 'No stems found' if result == [] else ', '.join(result)
    except KeyError:
        return 'No such lexicon'


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
            word, definition = line[0], line[1]
            line[0] = definition
            line[1] = ' '.join(re.findall("\[.*?\]", definition))
            csw[word] = line
            line = f.readline().strip("\n").split('	')
        f.close()
    except FileNotFoundError:
        print("csw.dat not found")
    try:
        f = open("twl.dat", "r")
        line = f.readline().strip("\n").split('	')
        while line != ['']:
            word, definition = line[0], line[1]
            line[0] = definition
            line[1] = ' '.join(re.findall("\[.*?\]", definition))
            twl[word] = line
            line = f.readline().strip("\n").split('	')
        f.close()
    except FileNotFoundError:
        print("twl.dat not found")
    try:
        f = open("mw.dat", "r")
        line = f.readline().strip("\n").split('	')
        while line != ['']:
            word, definition = line[0], line[1]
            line[0] = definition
            line[1] = ' '.join(re.findall("\[.*?\]", definition))
            mw[word] = line
            line = f.readline().strip("\n").split('	')
        f.close()
    except FileNotFoundError:
        print("mw.dat not found")
