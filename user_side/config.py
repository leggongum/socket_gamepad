from json import loads


with open('settings.json', 'r', encoding='utf-8') as f:
    config = loads(f.read())
    HOST = config['ip']
    PORT = config['port']
    KEYS = config['keys']
