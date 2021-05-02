import requests


def equity(rack, lexicon):
    parameters = {'rack': rack, 'lexicon': lexicon}
    response = requests.get('https://cross-tables.com/leaves_values.php', headers={'User-Agent': 'wordsmith-bot'}, params=parameters)
    try:
        values = response.json()
        return values['rack'] + ': ' + str(values['rack-value'])
    except KeyError:
        return response.text
