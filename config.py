import json
def json_decoder(obj):
    try:
        return Config(obj['irc_token'], 
                    obj['client_id'], 
                    obj['nick'],
                    obj['channels'],
                    )
    except KeyError:
        return obj
      
class Config:
    def __init__(self,irc_token,client_id,nick,channels):
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
    f = open('custom_commands.json', 'r')
    commands = json.loads(f.read())
    f.close()
    return commands
    
