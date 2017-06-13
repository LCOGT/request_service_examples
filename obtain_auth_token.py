#!/bin/env python
import requests

'''
obtain_auth_token.py

Obtain an API token via username/password.

You may also obtain your API key from your profile page: https://observe.lco.global/accounts/profile/
'''

response = requests.post(
    'https://observe.lco.global/api/api-token-auth/',
    data={
        'username': 'username',
        'password': 'password'
    }
)


# Make sure this api call was successful
try:
    response.raise_for_status()
except requests.exceptions.HTTPError as exc:
    print('Request failed: {}'.format(response.content))
    raise exc


# Print out your API token:
print(response.json()['token'])
