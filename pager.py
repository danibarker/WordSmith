def paginate(elements, page, limit=455):
    msg = ''
    lastmark = None
    lastword = None
    for n, element in enumerate(elements):
        word, mark = element
        if lastword and mark == lastmark and word == lastword + 'S':
            msg = msg[:(-2 if mark else -1)] + '[-S]'
            lastmark, lastword = None, None
        elif len(msg) + len(word) > limit:
            if page > 1:
                msg = ''
                page -= 1
            else:
                msg += f' Limited to first {n} results '
                break
        else:
            msg += word 
            lastmark, lastword = mark, word
        msg += (mark if mark else '') + ' '
    return len(elements), msg[:-1]
