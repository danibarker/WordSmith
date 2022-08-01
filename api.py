import requests


def common(word):
    authorization = { 'authority': 'woogles.io', 'origin': 'https://woogles.io', 'User-Agent': 'wordsmith-bot' }
    request = { 'lexicon': 'ECWL', 'words': [word], 'definitions': False }
    response = requests.post('https://woogles.io/twirp/word_service.WordService/DefineWords', json=request, headers=authorization)
    values = response.json()
    try:
        return values['results'][word]['v']
    except KeyError:
        return response.text


def equity(rack, lexicon):
    authorization = { 'User-Agent': 'wordsmith-bot' }
    parameters = { 'rack': rack, 'lexicon': lexicon }
    response = requests.get('https://cross-tables.com/leaves_values.php', headers=authorization, params=parameters)
    values = response.json()
    try:
        return (values['rack'], values['rack-value'])
    except KeyError:
        return response.text


def poll(config, name, tiles):
    authorization = { 'Authorization': 'Bearer ' + config.api_token, 'Client-Id': config.client_id }
    parameters = { 'login': name }
    response = requests.get('https://api.twitch.tv/helix/users', headers=authorization, params=parameters)
    values = response.json()
    try:
        broadcasterID = values['id']
    except KeyError:
        return str(values['status']) + ' ' + values['message']

    choices = []
    for tile in sorted(tiles):
        choices.append({ 'title': tile })
    request = { 'broadcaster_id': broadcasterID, 'title': 'Which tile?', 'choices': choices, 'duration': 300 }
    response = requests.post('https://api.twitch.tv/helix/polls', json=request, headers=authorization)
    values = response.json()
    try:
        return values['title'] + ': ' + str(values['status'])
    except KeyError:
        return str(values['status']) + ' ' + values['message']


def predict(config, name, player, opponent):
    authorization = { 'Authorization': 'Bearer ' + config.api_token, 'Client-Id': config.client_id }
    parameters = { 'login': name }
    response = requests.get('https://api.twitch.tv/helix/users', headers=authorization, params=parameters)
    values = response.json()
    try:
        broadcasterID = values['id']
    except KeyError:
        return str(values['status']) + ' ' + values['message']

    outcomes = [{ 'title': player }, { 'title': opponent }]
    request = { 'broadcaster_id': broadcasterID, 'title': 'Who will win?', 'outcomes': outcomes, 'prediction_window': 300 }
    response = requests.post('https://api.twitch.tv/helix/predictions', json=request, headers=authorization)
    values = response.json()
    try:
        return values['title'] + ': ' + str(values['status'])
    except KeyError:
        return str(values['status']) + ' ' + values['message']
