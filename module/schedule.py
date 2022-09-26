import requests

from typing import Any, Dict, List, Union
from datetime import date
from util import logger
import json
import re
import os

# Path Setup
PATH = os.getcwd()
if 'requirements.txt' not in os.listdir():
    os.chdir("..")
os.chdir(f"{os.getcwd()}/key")

# input twitter bearer token for access to twitter api
with open('twitter.json', 'r') as token_file:
    access_token_list: Dict = json.load(token_file)

# GET bearer token for access to twitter api
BEARER_TOKEN: str = access_token_list['BEARER_TOKEN']

# HoloEN MetaData Setup for Get Twitter ID
USER_LIST: List[str] = ['watsonameliaEN', 'moricalliope', 'gawrgura',
                        'takanashikiara', 'irys_en', 'ceresfauna',
                        'ninomaeinanis', 'ourokronii', 'nanashimumei_en',
                        'hakosbaelz']

# make schedule image directory
os.chdir("..")
if 'images' not in os.listdir():
    for vtuber in USER_LIST:
        os.makedirs(f'images/{vtuber}')

class Schedule:
    
    def __init__(self):
        
    
    def timeline_search(self) -> Dict:
        BASEURL: str = 'https://api.twitter.com/2/tweets/search/recent'
        query_params: Dict = {
            'tweet.fields': 'created_at',
            'media.fields': 'url',
            'expansions': 'attachments.media_keys',
            'query': ''
        }
        HEADERS: Dict = {
            'Authorization': f'Bearer {BEARER_TOKEN}'
        }

        result: Dict = {}

        for vtuber in USER_LIST:
            query_params['query'] = f'(has:images -is:retweet from: {vtuber}) schedule'
            response = requests.get(
                url=BASEURL,
                headers=HEADERS,
                params=query_params
            )

            res_json: Dict = json.loads(response.content)

            # GET TweetUrl
            pattern = re.compile(r'((https:\/\/)(t.co)\/(\w)*)')
            data: Union(None, Dict) = None if res_json is None else res_json.get('data')
            text: Union(None, str) = None if data is None else data[0].get('text')
            tweet_url: Union(None, str) = None if text is None else pattern.findall(text)[-1][0]
            created_date: Union(None, str) = None if data is None else data[0].get('created_at')

            # GET Schedule Image Url
            includes: Union(None, Dict) = None if res_json is None else res_json.get('includes')
            media: Union(None, Dict) = None if includes is None else includes.get('media')
            media_url: Union(None, str) = None if media is None else media[0].get('url')

            # print(f'[{vtuber}] \nmedia -> {media_url}\ntweetURL: {tweet_url}\n')
            if created_date is not None:
                result[f'{vtuber}'] = {
                    'name': vtuber,
                    'date': created_date,
                    'media_url': media_url,
                    'tweet_url': tweet_url
                }

        return result


    def image_download(self, schedule_list) -> None:
        vtuber: str = None
        image_url: str = None
        response = requests.get(image_url)
        open(f"{vtuber}.jpg", "wb").write(response.content)
        
    def __repr__(self):
        pass


if __name__ == "__main__":
    schedule = timeline_search()
    print(schedule)
