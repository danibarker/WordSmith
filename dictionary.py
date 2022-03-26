from alphagram import alphagram
import mmap
import os
import random
import re

wordlist = {}


def related(word, lexicon):
    word = word.replace('?', '.')
    pattern = re.compile(rf'(?<![a-z]){re.escape(word)}s?(?![a-z])', re.IGNORECASE)
    words = []
 
    mm = wordlist[lexicon]
    mm.seek(0)
    for line in iter(mm.readline, b''):
        word, entry = parse(line)
        definitions = entry[1]
        if pattern.search(definitions) and not offensive(definitions):
            words.append(decorate(word, entry, lexicon))
    return words


def begins_with(hook, lexicon):
    hook = hook.replace('?', '.')
    return find(rf'{hook}[A-Z]*', lexicon, len(hook))


def contains(stem, lexicon):
    stem = stem.replace('?', '.')
    stem_length = len(stem)
    pattern = re.compile(stem, re.IGNORECASE)
    words = []
    
    mm = wordlist[lexicon]
    mm.seek(0)
    for line in iter(mm.readline, b''):
        word, entry = parse(line)
        # TODO: fix
        if len(word) >= stem_length and pattern.match(word):
            if not offensive(entry[1]):
                words.append(decorate(word, entry, lexicon))
    return words


def hidden(length, phrase, lexicon):
    phrase = phrase.replace(' ', '')
    words = []
    for x in range(0, len(phrase) - length + 1):
        word = phrase[x:x + length]
        offensive, word, entry = check(word, lexicon)
        if entry and not offensive(entry[1]):
            words.append(decorate(word, entry, lexicon))
    return words


def pattern(stem, lexicon):
    stem = stem.replace('?','.')
    stem = stem.replace('*','.*')
    stem = re.sub('(\\d+)','.{\\1}', stem)
    pattern = re.compile(rf'^{stem}$', re.IGNORECASE)
    words = []

    mm = wordlist[lexicon]
    mm.seek(0)
    for line in iter(mm.readline, b''):
        word, entry = parse(line)
        definitions = entry[1]
        if pattern.search(definitions) and not offensive(definitions):
            words.append(decorate(word, entry, lexicon))
    return words


def ends_with(hook, lexicon):
    hook = hook.replace('?', '.')
    return find(rf'[A-Z]*{hook}', lexicon, len(hook))


def read(mm, pos):
    mm.seek(pos)
    return parse(mm.readline())


def parse(line):
    entry = line.decode().strip('\n').split('	')
    word = entry[0]
    entry[0] = ' / '.join(re.findall(rf'\\[.*?\\]', entry[1]))
    return word, entry


def find(pattern, lexicon, lower=1, upper=15):
    result = []
    for match in re.finditer(rf'^\b({pattern})\b.*$'.encode(), wordlist[lexicon], re.MULTILINE):
        if lower <= len(match.group(1)) <= upper:
            word, entry = parse(match.group(0))
            if not offensive(entry[1]):
                result.append((word, entry))
    return result


def check(word, lexicon):
    result = []
    alphagram = sorted(word)
    for match in re.finditer(rf'^\b({word})\b.*\b{alphagram}\b.*$'.encode(), wordlist[lexicon], re.MULTILINE):
        word, entry = parse(match.group(0))
        return (offensive(entry[1]), word, entry)
    return False, word, None


def common(word, entry, lexicon):
    if 'cel' in wordlist:
        mm = wordlist['cel']
        mm.seek(0)
        if mm.readline() == (word.lower()+'\n').encode():
            return offensive(entry[1]), True
        mm.seek(-1, os.SEEK_CUR)
        if mm.find(('\n'+word.lower()+'\t').encode()) != -1:
            return offensive(entry[1]), True
    return False, False


def wordnik(word, entry, lexicon):
    if 'wordnik' in wordlist:
        mm = wordlist['wordnik']
        mm.seek(0)
        if mm.find(('"'+word.lower()+'"').encode()) != -1:
            return offensive(entry[1]), True
    return False, False


def decorate(word, entry, lexicon, default=None):
    return (word, mark(entry, lexicon, default))


def mark(entry, lexicon, default=None):
    if lexicon == 'csw#' and len(entry) == 7 and entry[-1]:
        return entry[-1]
    else:
        return default


def offensive(definitions):
    pattern = re.compile(rf'\([a-z ]*\boffensive\b[a-z ]*\)|\boffensive\b(?:,| term| word)', re.IGNORECASE)
    return pattern.search(definitions)


def uninflect(word, lexicon):
    part = wordlist[lexicon][word][0]
    pattern = re.compile(r'[A-Z]{2,}')
    if match := re.match(pattern, wordlist[lexicon][word][1]):
        word = match.group(0)
    else:
        part = None
    words = [word]
    pattern = re.compile(rf', also ((?:[A-Z]+(?:, )?)+)')
    for match in re.findall(pattern, wordlist[lexicon][word][1]):
        for word in match.split(', '):
            words.append(word)
    return (part, words)


def define(word, entry, lexicon):
    if match := re.match(r'[A-Z]{2,}', entry[1]):
        _, word, entry = check(match.group(0), lexicon)
    return word, entry[1]


def inflect(word, lexicon):
    # ASSUME either a word is either a root or an inflection (not both)
    # ASSUME inflections have only one part of speech
    result = []
    part, roots = uninflect(word, lexicon)
    for root in roots:
        if part is None:
            entries = wordlist[lexicon][root][1].split('] / [')
            result.append('%s%s' % decorate(root, lexicon, '') + ' ' + '; '.join(entries))
        else:
            for inflection in wordlist[lexicon][root][1].split(' / '):
                if part is None or inflection.startswith(part[:2]):
                    result.append(('%s%s' % decorate(root, lexicon, '')) + ' ' + inflection)
    return ', '.join(result)


def info(stem, lexicon, alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
    msg = ''
    try:
        word, entry = find(stem, lexicon)
        if entry:
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
        word, entry = find(stem, lexicon)
        if entry:
            counter = -1
            for x in entry:
                counter = counter + 1
                if counter == 2 and x:
                    msg = msg + ' Front: ' + x
                if counter == 3 and x:
                    msg = msg + ' Back: ' + x
        else:
            hooks = front_hooks(stem, lexicon)
            if hooks:
                msg = msg + ' Front:'
                for word, entry in hooks:
                    msg += (' %s%s' % decorate(word, entry, lexicon, ''))
            hooks = back_hooks(stem, lexicon)
            if hooks:
                msg = msg + ' Back:'
                for word, entry in hooks:
                    msg += (' %s%s' % decorate(word, entry, lexicon, ''))

        hooks = middle_hooks(stem, lexicon)
        if hooks:
            msg = msg + ' Middle:'
            for word, entry in hooks:
                msg += (' %s%s' % decorate(word, entry, lexicon, ''))
        return 'No hooks found' if msg == '' else msg.lstrip()
    except KeyError:
        return 'No such lexicon'


def random_word(word_length, lexicon, related_word):
    if word_length <= 1 or word_length > 15:
        word_length = None
    #words = list(wordlist[lexicon]) if related_word == '' else related(related_word, lexicon)
    word, entry = select_random_word(lexicon)
    while (word_length is not None and len(word) != word_length) or offensive(entry[1]):
        word = select_random_word(lexicon)
    return ('%s%s' % decorate(word, entry, lexicon, '')) + ' - ' + entry[1]


def select_random_word(lexicon):
    # Reads a random '\n' then reads from the beginning of the line
    mm = wordlist[lexicon]
    mm.seek(random.randrange(mm.size()))
    while mm.read(1) != '\n'.encode():
        mm.seek(random.randrange(mm.size()))
    return read(mm, mm.rfind('\n'.encode(), 0, mm.tell())+1)


def anagram(rack, lexicon):
    # RETURNS ANAGRAMS OF RACK, DB IS LEXICON
    words = []
    word_length = len(rack)
    num_blanks = list(rack).count('?')
    letters = sorted(rack.replace('?', '').upper())
    mask = ''
    if num_blanks:
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
        if num_blanks == 1:
            mask = mask + ('[%c-Z]?' % (alpha))
        else:
            mask = mask + ('[%c-Z]{1,%d}' % (alpha, num_blanks))
    else:
        mask = ''.join(letters)

    pattern = '[A-Z]' * word_length
    for match in re.finditer(rf'^\b{pattern}\b.*\b({mask})\b.*$'.encode(), wordlist[lexicon], re.MULTILINE):
        word, entry = parse(match.group(0))
        if not offensive(entry[1]):
            words.append((word, entry))
    return words


def back_hooks(stem, lexicon):
    stem = stem.replace('?', '.')
    return find(rf'{stem}.', lexicon, len(stem)+1)


def front_hooks(stem, lexicon):
    stem = stem.replace('?', '.')
    return find(rf'.{stem}', lexicon, len(stem)+1)


def middle_hooks(stem, lexicon):
    stem = stem.replace('?', '.')
    pattern = []
    for x in range(1, len(stem)):
        pattern.append(rf'{stem[:x]}.{stem[x:]}')
    pattern = '|'.join(pattern)
    return find(rf'{pattern}', lexicon, len(stem)+1, len(stem)+1)


def unhook(rack, lexicon):
    rack = rack.replace('?', '.')
    pattern = []
    for x in range(1, len(rack)):
        pattern.append(rf'{rack[:x]}{rack[x+1:]}')
    pattern = '|'.join(pattern)
    return find(rf'{pattern}', lexicon, len(rack)-1, len(rack)-1)


def open_files():
    # wordlist DICTIONARY
    try:
        with open('csw.dat', 'rb') as f:
            if os.stat(f.name).st_size:
                mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
                wordlist['csw'] = mm
                wordlist['csw#'] = mm
            f.close()
    except FileNotFoundError:
        print('csw.dat not found')
    try:
        with open('twl.dat', 'rb') as f:
            if os.stat(f.name).st_size:
                wordlist['twl'] = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            f.close()
    except FileNotFoundError:
        print('twl.dat not found')
    try:
        with open('mw.dat', 'rb') as f:
            if os.stat(f.name).st_size:
                wordlist['mw'] = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            f.close()
    except FileNotFoundError:
        print('mw.dat not found')
    try:
        with open('CEL/cel.txt', 'rb') as f:
            if os.stat(f.name).st_size:
                wordlist['cel'] = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            f.close()
    except FileNotFoundError:
        print('CEL/cel.txt not found')
    try:
        with open('wordlist/wordlist-20210729.txt', 'rb') as f:
            if os.stat(f.name).st_size:
                wordlist['wordnik'] = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            f.close()
    except FileNotFoundError:
        print('wordlist/wordlist-20210729.txt not found')
