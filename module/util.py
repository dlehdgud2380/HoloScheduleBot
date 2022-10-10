
from typing import Dict
import json
import os


def generate_api_info(service, **kwargs):
    os.chdir(f"{os.getcwd()}/key")
    print(os.getcwd())

    twitter: Dict = {
        'bearer_token': '',
        'api_key': '',
        'api_key_secret': '',
        'access_token:': '',
        'access_token_secret': '',
        'client_id': '',
        'client_secret': '',
    }

    telegram: Dict = {}

    discord: Dict = {}

    if service == 'twitter':
        twitter['bearer_token'] = kwargs['bearer_token']
        twitter['api_key'] = kwargs['api_key']
    else:
        return

    file = open('twitter.json', 'w')
    file.write(json.dumps(twitter, indent=4))
    file.close()

if __name__ == '__main__':
    generate_api_info(
        service='twitter',
        bearer_token='AAAAAAAAAAAAAAAAAAAAAGA%2FeQEAAAAAZjex3fj4MX5WeZ1QZk7%2BTvSgscA%3DJe2UJqXpC96inQp82gVYQgRsOBCtxpxyzQfDPKhH3SHpQShBJw',
        api_key='1G55m1bxDEOmm1562ck9jOZNO',
        api_key_secret='JcgeEIb7QtKC9CgfyRRyRFdGaTOgrkgMYdduw685yDQLIYHb75',
        access_token='251528138-oAwJpfYZL38s8tKWlVSIIkEQ3XJ14vCNdWJCqyF',
        access_token_secret='0my6CwXinVz1NRj8IazBeVuHr2j5INC46qgJz5mjMoRdU',
        client_id='WEtXM0tOVWNua3FVQmNqRU5pUFY6MTpjaQ',
        client_secret='13N3M4Or2MTqvPvPQbd0QaPmZbAIsjHU-TudlSeRrNYMkizjOn',
    )
