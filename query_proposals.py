#!/bin/env python
import requests

'''
query_proposal.py

Return details about proposals you belong to, including time allocations.
'''

API_TOKEN = 'PlaceApiTokenHere'  # API token obtained from https://observe.lco.global/accounts/profile/

response = requests.get(
    'https://observe.lco.global/api/proposals/',
    headers={'Authorization': 'Token {}'.format(API_TOKEN)}
)


# Make sure this api call was successful
try:
    response.raise_for_status()
except requests.exceptions.HTTPError as exc:
    print('Request failed: {}'.format(response.content))
    raise exc

proposals_dict = response.json()  # api returns a json dictionary containing proposal information

print('Member of {} proposals'.format(proposals_dict['count']))

# loop over each proposal and print some things about it.
for proposal in proposals_dict['results']:
    print('Proposal: {}'.format(proposal['id']))
    for time_allocation in proposal['timeallocation_set']:
        print('{0:.3f} out of {1} standard hours used on telescope class {2} for semester {3}\n'.format(
            time_allocation['std_time_used'],
            time_allocation['std_allocation'],
            time_allocation['telescope_class'],
            time_allocation['semester'],
        ))
