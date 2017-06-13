#!/bin/env/python
import requests

'''
query_requests.py

Query the request API for UserRequests belong to a specific proposal.
'''

API_TOKEN = 'PlaceApiTokenHere'  # API token obtained from https://observe.lco.global/accounts/profile/

PROPOSAL_ID = 'FTPEPO2014A-004'  # Proposal IDs may be found here: https://observe.lco.global/proposals/

# Use the requests library to make an HTTP request to the API
response = requests.get(
    'https://observe.lco.global/api/userrequests?proposal={}'.format(PROPOSAL_ID),
    headers={'Authorization': 'Token {}'.format(API_TOKEN)}
)

# Make sure this api call was successful
try:
    response.raise_for_status()
except requests.exceptions.HTTPError as exc:
    print('Request failed: {}'.format(response.content))
    raise exc

# Loop over the returned UserRequests and print some information about them
for request in response.json()['results'][:5]:  # Get the first 5 UserRequests
    print('Request {0} status is {1}. Last updated: {2}'.format(
        request['group_id'], request['state'], request['modified']
    ))
    print('https://observe.lco.global/userrequests/{}/\n'.format(
        request['id']
    ))
