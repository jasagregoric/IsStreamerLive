import requests
import configparser
from dotenv import load_dotenv
import os

def adduser(name):
    load_dotenv()
    
    config = configparser.ConfigParser()
    config.read('streamers.ini')

    nam = config['DEFAULT'].get('names', '')
    check = nam.split(',')
    mut = config['DEFAULT'].get('muted', '')
    mut_check = mut.split(',')

    if name in check:
        return 2

    url = f'https://api.twitch.tv/helix/streams?user_login={name}'
    headers = {
        'Authorization': 'Bearer ' + os.getenv('api_key'),
        'Client-Id': os.getenv('client_id')
    }
    response = requests.get(url, headers=headers)
    data = response.status_code

    if data == 200:
        if nam:
            nam += f',{name}'
            mut += ',false'
        else:
            nam = name
            mut = 'false'

        config['DEFAULT']['names'] = nam
        config['DEFAULT']['muted'] = mut

        try:
            with open('streamers.ini', 'w') as configfile:
                config.write(configfile)
            print("Data successfully written to the .ini file.")
        except Exception as e:
            print(f"Error writing to file: {e}")

        return 0
    else:
        return 1
