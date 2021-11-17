import api


def alphagram(rack, alphabet):
    order = dict(zip(alphabet, range(len(alphabet))))
    return ''.join(sorted(rack, key=lambda c:order[c]))
