from typing import Dict, List
import os
from pathlib import Path
import requests
import json

# result message for data extract result
class ResultMessage:
    def __init__(self, code=None, message=None):
        self.code = code
        self.message = message
        
result_message: object = None

# Path Setup
PATH = os.getcwd()
os.chdir(f"{Path(PATH)}/etc")

# input twitter bearer token for access to twitter api
with open("api_access.json", "r") as token_file:
    access_token_list: Dict = json.load(token_file)

# GET bearer token for access to twitter api
bearer_token: str = access_token_list['BEARER_TOKEN']

# HoloEN MetaData Setup for Get Twitter ID
user_list: List[str] = ['watsonameliaEN', 'moricalliope', 'gawrgura',
                        'takanashikiara', 'irys_en', 'ceresfauna',
                        'ourokronii', 'nanashimumei_en', 'hakosbaelz']
BASEURL: str = "https://api.twitter.com/2/users/by/username/"
headers: Dict = {
    'Authorization': f'Bearer {bearer_token}'
}

# Get Vtuber twitter id
holoen_info: Dict = {}
for user in user_list:
    try:
        response = requests.get(BASEURL + user, headers=headers)
        if response.status_code != 200:
            result_message = ResultMessage(response.status_code, response.reason)
            break
        else:
            result_message = ResultMessage(response.status_code, response.reason)
            data = dict(json.loads(response.content))['data']
            holoen_info[data['username']] = data['id']
    except requests.ConnectionError or requests.ConnectTimeout as error:
        result_message = ResultMessage(message=error)

# Print Result
if result_message.__dict__["code"] != 200:
    print(result_message.__dict__)
else:
    print(result_message.__dict__)
    print(json.dumps(holoen_info, indent=4))