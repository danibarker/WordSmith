from dictionary import decorate

def merge(elements, lexicon):
    msg = ''
    lastmark = None
    lastword = None
    for n, element in enumerate(elements):
        word, entry = element
        word, mark = decorate(word, entry, lexicon, '')
        if lastword and mark == lastmark and word == lastword + 'S':
            msg = msg[:(-2 if mark else -1)] + '[-S]'
            lastmark, lastword = None, None
        else:
            msg += word
            lastmark, lastword = mark, word
        msg += (mark if mark else '') + ' '
    return msg[:-1].split(' ')

def paginate(elements, lexicon, page, limit=455):
    msg = ''
    for n, element in enumerate(merge(elements, lexicon)):
        if len(msg) + len(element) > limit:
            if page > 1:
                msg = ''
                page -= 1
            else:
                msg += f' Limited to first {n} results '
                break
        msg += element + ' '
    return len(elements), msg[:-1]

def truncate(delimiter, results, limit=495):
    msg = delimiter.join(results)
    while len(msg) > limit:
        results = results[:-1]
        msg = delimiter.join(results)
    return msg
