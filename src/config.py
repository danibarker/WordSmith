import json
def json_decoder(obj):
    try:
        return Config(obj['api_token'],
                    obj['irc_token'],
                    obj['client_id'],
                    obj['nick'],
                    obj['channels'],
                    )
    except KeyError:
        return obj
      
class Config:
    def __init__(self,api_token,irc_token,client_id,nick,channels):
       self.api_token = api_token
       self.irc_token = irc_token
       self.client_id = client_id
       self.nick = nick
       self.channels=channels
def config():       
    f = open('config.json', 'r')
    config = json.loads(f.read(), object_hook=json_decoder)
    f.close()
    return config
def save(config):
    jfile = json.dumps(config.__dict__, indent=2)
    f = open(f'config.json', 'w')
    f.write(jfile)
    f.close()
def custom_commands():
    try:
        f = open('custom_commands.json', 'r')
    except FileNotFoundError:
        commands = {}
    else:
        commands = json.loads(f.read())
        f.close()
    return commands
    
