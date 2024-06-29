import requests
import configparser
from dotenv import load_dotenv
import os

def download_image(url, save_as):
    response = requests.get(url)
    with open(save_as, 'wb') as file:
        file.write(response.content)

def get_logos():
    load_dotenv()
    
    config = configparser.ConfigParser()
    config.read('streamers.ini')
    names = config['DEFAULT'].get('names', '')
    name_list = [name.strip() for name in names.split(',') if name.strip()]
    for name in name_list:
        url = 'https://api.twitch.tv/helix/search/channels?query='+name
        headers = {
            'Authorization': 'Bearer ' + os.getenv('api_key'),
            'Client-Id': os.getenv('client_id')
        }
        response = requests.get(url, headers=headers)
        data = response.json()

        for streamer in data['data']:
            if streamer['broadcaster_login'] == name:
                logo_url = streamer['thumbnail_url']
                break

        link=logo_url

        save_as = 'assets/logos/'+name+'.jpg'

        download_image(link, save_as)
        
def get_logo(name):
    load_dotenv()
    
    url = 'https://api.twitch.tv/helix/search/channels?query='+name
    headers = {
        'Authorization': 'Bearer ' + os.getenv('api_key'),
        'Client-Id': os.getenv('client_id')
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    
    for streamer in data['data']:
        if streamer['broadcaster_login'] == name:
            logo_url = streamer['thumbnail_url']
            break

    link=logo_url

    save_as = 'assets/logos/'+name+'.jpg'

    download_image(link, save_as)
