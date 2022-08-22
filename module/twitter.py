from typing import Any, Dict, List, Union
from xmlrpc.client import ResponseError
import requests
import json
import re
import logging

# input twitter bearer token for access to twitter api
with open('etc/api_access.json', 'r') as token_file:
    access_token_list: Dict = json.load(token_file)

# GET bearer token for access to twitter api
BEARER_TOKEN: str = access_token_list['BEARER_TOKEN']

# HoloEN MetaData Setup for Get Twitter ID
USER_LIST: List[str] = ['watsonameliaEN', 'moricalliope', 'gawrgura',
                        'takanashikiara', 'irys_en', 'ceresfauna',
                        'ninomaeinanis', 'ourokronii', 'nanashimumei_en',
                        'hakosbaelz']

payload = {'key1': 'value1', 'key2': ['value2', 'value3']}
r = requests.get('https://httpbin.org/get', params=payload)


def twitter_timeline_search():
    BASEURL: str = 'https://api.twitter.com/2/tweets/search/recent'
    query_params: Dict = {
        'media.fields': 'url',
        'expansions': 'attachments.media_keys',
        'query': ''
    }
    HEADERS: Dict = {
        'Authorization': f'Bearer {BEARER_TOKEN}'
    }

    for vtuber in USER_LIST:
        query_params['query'] = f'(has:images -is:retweet from: {vtuber}) schedule'
        response = requests.get(
            url=BASEURL,
            headers=HEADERS,
            params=query_params
        )

        res_json: Dict = json.loads(response.content)

        # GET TweetUrl
        pattern = re.compile('(http(s)?:\/\/)([a-z0-9\w]+\.*)+[a-z0-9]{2,4}\/([a-z0-9\w]+\.*)')
        data: Union(
            None, Dict) = None if res_json is None else res_json.get('data')
        text: Union(None, str) = None if data is None else data[0].get('text')
        tweet_url = None if text is None else pattern.search(text).group()

        # GET Schedule Image Url
        includes: Union(None, Dict) = None if res_json is None else res_json.get('includes')
        media: Union(None, Dict) = None if includes is None else includes.get('media')
        media_url: Union(None, str) = None if media is None else media[0].get('url')

        print(f'[{vtuber}] \nmedia -> {media_url}\ntweetURL: {tweet_url}\n')


def twitter_image_download():
    pass


if __name__ == '__main__':
    twitter_timeline_search()
