import requests
import configparser
from dotenv import load_dotenv
import os
import json

def get_data(name):
    load_dotenv()
    
    config = configparser.ConfigParser()
    config.read('streamers.ini')
    names = config['DEFAULT'].get('names', '')
    name_list = [name.strip() for name in names.split(',') if name.strip()]
    url = 'https://api.twitch.tv/helix/search/channels?query='+name
    headers = {
        'Authorization': 'Bearer ' + os.getenv('api_key'),
        'Client-Id': os.getenv('client_id')
    }
    response = requests.get(url, headers=headers)
    data = response.json()

    
    data_array = data['data']
    
    variable_name = name

    matching_entries = []
    for entry in data_array:
        if entry.get("display_name").lower() == variable_name.lower():
            filtered_entry = {
                "display_name": entry.get("display_name", ""),
                "game_name": entry.get("game_name", ""),
                "tags": entry.get("tags", []),
                "title": entry.get("title", ""),
                "started_at": entry.get("started_at", "")
            }
            matching_entries.append(filtered_entry)

    return matching_entries