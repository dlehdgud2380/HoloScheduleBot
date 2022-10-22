import requests

from typing import Any, Dict, List, Union
from datetime import datetime
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
BEARER_TOKEN: str = access_token_list['bearer_token']

# HoloEN MetaData Setup for Get Twitter ID
USER_LIST: List[str] = [
        'watsonameliaEN',
        'moricalliope',
        'gawrgura',
        'takanashikiara',
        'irys_en',
        'ceresfauna',
        'ninomaeinanis',
        'ourokronii',
        'nanashimumei_en',
        'hakosbaelz',
    ]

# make schedule image directory
os.chdir("..")
if 'images' not in os.listdir():
    for vtuber in USER_LIST:
        os.makedirs(f'images/{vtuber}')

class Schedule:

    def __init__(self):
        self.holoen_schedule: Dict = self.timeline_search()
        for schedule in self.holoen_schedule.values():
            self.image_download(schedule)

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

            if created_date is not None:
                created_date: datetime = datetime.strptime(created_date[0:19], '%Y-%m-%dT%H:%M:%S')
                created_date = created_date.date().isoformat()
                result[f'{vtuber}'] = {
                    'name': vtuber,
                    'date': created_date,
                    'media_url': media_url,
                    'tweet_url': tweet_url
                }

        return result


    def image_download(self, vtuber_schedule) -> None:
        vtuber: str = vtuber_schedule['name']
        image_url: str = vtuber_schedule['media_url']
        date: str = vtuber_schedule['date']
        response = requests.get(image_url)
        image_file = open(f"images/{vtuber}/{date}.jpg", "wb")
        image_file.write(response.content)
        image_file.close()

    def __repr__(self):
        return json.dumps(self.holoen_schedule, indent=4, ensure_ascii=True)


if __name__ == "__main__":
    schedule = Schedule()
    print(schedule)
