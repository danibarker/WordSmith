import requests


def equity(rack, lexicon):
    parameters = {'rack': rack, 'lexicon': lexicon}
    response = requests.get('https://cross-tables.com/leaves_values.php', headers={'User-Agent': 'wordsmith-bot'}, params=parameters)
    values = response.json()
    try:
        return values['rack'] + ': ' + str(values['rack-value'])
    except KeyError:
        return response.text


def predict(config, name, opponent):
    authorization = {'Authorization': 'Bearer ' + config.api_token, 'Client-Id': config.client_id}
    response = requests.get('https://api.twitch.tv/helix/users?login='+name, headers=authorization)
    values = response.json()
    try:
        broadcasterID = values['id']
        player = values['display_name']
    except KeyError:
        return str(values['status']) + ' ' + values['message']

    outcomes = [{'title': player}, {'title': opponent}]
    parameters = {'broadcaster_id': broadcasterID, 'title': 'Who will win?', 'outcomes': outcomes, 'prediction_window': 300}
    response = requests.get('https://api.twitch.tv/helix/predictions', headers=authorization, params=parameters)
    values = response.json()
    try:
        return values['title'] + ': ' + str(values['status'])
    except KeyError:
        return str(values['status']) + ' ' + values['message']
