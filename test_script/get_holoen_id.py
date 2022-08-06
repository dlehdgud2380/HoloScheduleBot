# simple get holoen_vtuber info script

from typing import Dict, List
import os
from pathlib import Path
import requests
import json


# Path Setup
PATH = os.getcwd()
os.chdir(f"{Path(PATH)}/etc")

# input twitter bearer token for access to twitter api
with open ("api_access.json", "r") as token_file:
    access_token_list: Dict = json.load(token_file)

# GET bearer token for access to twitter api
bearer_token: str = access_token_list['BEARER_TOKEN'] 

# GET HoloEN
user_list: List[str] = ['watsonameliaEN', 'moricalliope', 'gawrgura', 'takanashikiara',
                    'irys_en', 'ceresfauna', 'ourokronii', 'nanashimumei_en', 'hakosbaelz']
BASEURL: str = "https://api.twitter.com/2/users/by/username/"
headers: Dict = {
    'Authorization': f'Bearer {bearer_token}'
}

# Get Vtuber twitter id
holoen_info: Dict = {}
for user in user_list:
    response = requests.get(BASEURL + user, headers=headers).content
    data = dict(json.loads(response))['data']
    holoen_info[data['username']] = data['id']
    
# Write using json and export to project etc directory
with open ("vtuber_id_list.json", 'w') as json_file:
    json_file.write(json.dumps(holoen_info, indent=4))
    json_file.close()