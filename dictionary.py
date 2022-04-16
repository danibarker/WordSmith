from alphagram import alphagram
from difflib import SequenceMatcher
import mmap
import os
import random
import re

wordlist = {}


def related(word, lexicon, limit=100):
    word = word.replace('?', '[A-Z]').lower()
    words = []
    cache = {}
    for match in re.finditer(rf'^[A-Z]+\t[^\t]*\b{word}\b.*\b[A-Z]+\b(?:\t.)?\r?$'.encode(), wordlist[lexicon], re.MULTILINE):
        word, entry = parse(match.group(0))
        if not recursive(word, entry, lexicon, cache) and not offensive(entry[1]):
            cache[word] = entry
            words.append((word, entry))
            if len(words) >= limit:
                break
    return words


def begins_with(hook, lexicon):
    lower = len(hook)
    hook = hook.replace('?', '[A-Z]')
    return find(rf'{hook}[A-Z]*', lexicon, lower)


def contains(stem, lexicon):
    lower = len(stem)
    stem = stem.replace('?', '[A-Z]')
    return find(rf'[A-Z]*{stem}[A-Z]*', lexicon, lower)


def hidden(length, phrase, lexicon):
    phrase = phrase.replace(' ', '')
    words = []
    for x in range(len(phrase) - length + 1):
        offensive, word, entry = check(phrase[x:x+length], lexicon)
        if entry and not offensive:
            words.append(decorate(word, entry, lexicon))
    return words


def pattern(stem, lexicon):
    stem = stem.replace('?','[A-Z]')
    stem = stem.replace('*','[A-Z]*')
    stem = re.sub('(\\d+)','[A-Z]{\\1}', stem)
    return find(stem.upper(), lexicon)


def ends_with(hook, lexicon):
    lower = len(hook)
    hook = hook.replace('?', '[A-Z]')
    return find(rf'[A-Z]*{hook}', lexicon, lower)


def read(mm, pos):
    mm.seek(pos)
    return parse(mm.readline())


def parse(line):
    entry = line.decode().strip().split('	')
    word = entry[0]
    entry[0] = ' / '.join(re.findall(rf'\[.*?\]', entry[1]))
    return word, entry


def find(pattern, lexicon, lower=1, upper=15):
    result = []
    for match in re.finditer(rf'^\b({pattern})\b.*\r?$'.encode(), wordlist[lexicon], re.MULTILINE):
        if lower <= len(match.group(1)) <= upper:
            word, entry = parse(match.group(0))
            if not offensive(entry[1]):
                result.append((word, entry))
    return result


def check(word, lexicon):
    result = []
    alphagram = ''.join(sorted(word))
    if match := re.search(rf'^\b({word})\b.*\b[a-z]+\b.*\b\d+\b\t\b{alphagram}\b.*\r?$'.encode(), wordlist[lexicon], re.MULTILINE):
        word, entry = parse(match.group(0))
        return (offensive(entry[1]), word, entry)
    return False, word, None


def common(word):
    return re.search(rf'^{word}\r?$'.encode(), wordlist['cel'], re.MULTILINE)


def wordnik(word):
    return re.search(rf'^"{word}"\r?$'.encode(), wordlist['wordnik'], re.MULTILINE)


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


def uninflect(word, entry, lexicon):
    if match := recursive(word, entry, lexicon):
        word, entry = match
    words = [word]
    pattern = re.compile(rf', also ((?:[A-Z]+(?:, )?)+)')
    for match in re.findall(pattern, entry[1]):
        for word in match.split(', '):
            words.append(word)
    return words


def define(word, entry, lexicon, default):
    if match := recursive(word, entry, lexicon):
        word, entry = match
    return word, entry, entry[1], mark(entry, lexicon, default)


def part(inflection):
    # Checks if the inflection (word) is irregular, or a verb
    # Common root form adjectives and nouns tend to homograph
    # whereas common root form verbs are fewer and distinct
    irregular = re.match(r'\[(?:conj|int|interj|prep|pron)\b', inflection)
    other = re.match(r'\[(?:adj|adv|n)\b', inflection)
    verb = re.match(r'\[v\b', inflection)
    return irregular, other, verb


def inflect(word, entry, lexicon):
    # ASSUME either a word is either a root or an inflection (not both)
    # ASSUME inflections have only one part of speech
    result = []
    irregular, other, verb = part(entry[0])
    roots = uninflect(word, entry, lexicon)
    for root in roots:
        _, root, entry = check(root, lexicon)
        for inflection in entry[0].split(' / '):
            irregular2, other2, verb2 = part(inflection)
            if (irregular and irregular2) or (other and other2) or (verb and verb2):
                result.append(('%s%s' % decorate(root, entry, lexicon, '')) + ' ' + inflection)
    return (' / ' if roots[-1] == word else ', ').join(result)


def info(stem, lexicon, alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
    msg = ''
    try:
        offensive, word, entry = check(stem, lexicon)
        if offensive:
            pass
        elif entry:
            counter = -1
            for x in entry:
                counter = counter + 1
                if counter == 0:
                    msg = stem
                elif counter == 1:
                    msg = msg + ' - ' + x
                elif counter == 2 and x:
                    msg = msg + ' Front Hooks: ' + x
                elif counter == 3 and x:
                    msg = msg + ' Back Hooks: ' + x
                elif counter == 4:
                    msg = msg + ' Probability: ' + str(x)
                elif counter == 5:
                    msg = msg + ' Alphagram: ' + alphagram(x, alphabet)

            hooks = middle_hooks(stem, lexicon)
            if hooks:
                msg = msg + ' Middle Hooks:'
                for _, word, entry in hooks:
                    msg += (' %s%s' % decorate(word, entry, lexicon, ''))
            return msg
        else:
            return 'No such word'
    except KeyError:
        return 'No such lexicon'


def hook(stem, lexicon):
    msg = ''
    try:
        offensive, word, entry = check(stem, lexicon)
        if offensive:
            pass
        elif entry:
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
                for _, word, entry in hooks:
                    msg += (' %s%s' % decorate(word, entry, lexicon, ''))
            hooks = back_hooks(stem, lexicon)
            if hooks:
                msg = msg + ' Back:'
                for _, word, entry in hooks:
                    msg += (' %s%s' % decorate(word, entry, lexicon, ''))

        hooks = middle_hooks(stem, lexicon)
        if hooks:
            msg = msg + ' Middle:'
            for _, word, entry in hooks:
                msg += (' %s%s' % decorate(word, entry, lexicon, ''))
        return 'No hooks found' if msg == '' else msg.lstrip()
    except KeyError:
        return 'No such lexicon'


def recursive(word, entry, lexicon, cache={}):
    if match := re.match(r'[A-Z]{2,}', entry[1]):
        root = match.group(0)
        if root in cache:
            entry2 = cache[root]
        else:
            _, root, entry2 = check(root, lexicon)
        if mark(entry, lexicon, '') == mark(entry2, lexicon, ''):
            return root, entry2
    # check if the uninflected word is used to define the word (WINDY - related to wind)
    if match := re.match(r'(?:\([ A-Za-z]+\) )?(?:[a-z]+ )*([a-z]+)(?:[,;]| \[)', entry[1]):
        root = match.group(1).upper()
        if SequenceMatcher(None, word, root).ratio() >= 0.8:
            if root in cache:
                entry2 = cache[root]
            else:
                _, root, entry2 = check(root, lexicon)
            if mark(entry, lexicon, '') == mark(entry2, lexicon, ''):
                return root, entry2


def random_word(word_length, lexicon):
    if word_length <= 1 or word_length > 15:
        word_length = None
    word, entry = select_random_word(lexicon)
    while (word_length is not None and len(word) != word_length) or recursive(word, entry, lexicon) or offensive(entry[1]):
        word, entry = select_random_word(lexicon)
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
            if letter != alpha:
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

    pattern = (rf'[A-Z]' if (num_blanks) else rf'[{rack}]') * word_length
    for match in re.finditer(rf'^\b{pattern}\b.*\b({mask})\b.*\r?$'.encode(), wordlist[lexicon], re.MULTILINE):
        word, entry = parse(match.group(0))
        if not offensive(entry[1]):
            words.append((word, entry))
    return words


def back_hooks(stem, lexicon):
    lower = len(stem)
    stem = stem.replace('?', '[A-Z]')
    return find(rf'{stem}.', lexicon, lower+1)


def front_hooks(stem, lexicon):
    lower = len(stem)
    stem = stem.replace('?', '[A-Z]')
    return find(rf'.{stem}', lexicon, lower+1)


def middle_hooks(stem, lexicon):
    lower = len(stem) + 1
    pattern = []
    for x in range(1, len(stem)):
        pattern.append(rf'{stem[:x]}.{stem[x:]}')
    pattern = ('|'.join(pattern)).replace('?', '[A-Z]')
    return find(rf'{pattern}', lexicon, lower, lower)


def unhook(rack, lexicon):
    lower = len(rack) - 1
    pattern = []
    for x in range(len(rack)):
        pattern.append(rf'{rack[:x]}{rack[x+1:]}')
    pattern = ('|'.join(pattern)).replace('?', '[A-Z]')
    return find(rf'{pattern}', lexicon, lower, lower)


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
