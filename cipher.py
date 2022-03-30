def cipher(text):
    pattern = ''
    letters = ''
    for letter in text:
        if key := letters.find(letter)+1:
            pattern += f'\\{key}'
        else:
            key = '|'.join(f'\\{n+2}' for n in range(len(letters)))
            if pattern:
                pattern += f'(?!{key})'
            pattern += '(.)'
            letters += letter
    return pattern
