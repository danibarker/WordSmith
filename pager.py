from dictionary import mark
import re

def plural(word, lastword):
    return re.fullmatch(rf'{lastword}(ES|S)', word)

def merge(elements, lexicon):
    msg = ''
    lastmarking = None
    lastword = None
    for n, element in enumerate(elements):
        word, entry = element
        marking = mark(entry, lexicon, '')
        suffix = plural(word, lastword) if lastword else None
        if lastword and marking == lastmarking and suffix:
            msg = msg[:(-2 if marking else -1)] + f'[-{suffix.group(1)}]'
            lastmarking, lastword = '', None
        elif lastword and not lastmarking and suffix:
            msg = msg[:-1] + (f'[-{suffix.group(1)}%s]' % marking)
            marking, lastword = '', None
        else:
            msg += word
            lastmarking, lastword = marking, word
        msg += marking + ' '
    return msg[:-1].split(' ')

def paginate(elements, lexicon, page, limit=455):
    msg = ''
    merged = merge(elements, lexicon)
    for n, element in enumerate(merged):
        if len(msg) + len(element) > limit and len(msg) + len(' '.join(merged[n:])) > limit + 25:
            if page > 1:
                msg = ''
                page -= 1
            else:
                msg += f'Limited to first {n} results '
                break
        msg += element + ' '
    return len(elements), msg[:-1]

def truncate(delimiter, results, limit=495):
    msg = delimiter.join(results)
    while len(msg) > limit:
        results = results[:-1]
        msg = delimiter.join(results)
    return msg
