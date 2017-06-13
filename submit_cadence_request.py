#!/bin/env python
import requests

'''
submit_cadence_request.py

Submit a UserRequest to the cadence endpoint, generating a new UserRequest that observes on a cadence.
This new UserRequest can then be submitted again to actually schedule the UserRequest.
'''

API_TOKEN = 'PlaceApiTokenHere'  # API token obtained from https://observe.lco.global/accounts/profile/
PROPOSAL_ID = 'LCOEngineering'  # Proposal IDs may be found here: https://observe.lco.global/proposals/

# The cadence we want for this observation
cadence = {
    'start': '2017-05-01 00:00:00',
    'end': '2017-06-01 00:00:00',
    'period': 24,
    'jitter': 12.0
}

# The target of the observation
target = {
    'name': 'm83',
    'type': 'SIDEREAL',
    'ra': 204.253,
    'dec': -29.865,
    'epoch': 2000
}

# The configurations for this request. In this example we are taking 2 exposures with different filters.
molecules = [
    {
        'type': 'EXPOSE',
        'instrument_name': '1M0-SCICAM-SINISTRO',
        'filter': 'v',
        'exposure_time': 30,
        'exposure_count': 1,
    },
    {
        'type': 'EXPOSE',
        'instrument_name': '1M0-SCICAM-SINISTRO',
        'filter': 'b',
        'exposure_time': 30,
        'exposure_count': 1,
    }
]

# We do not provide windows for a cadence request
windows = []

# The telescope class that should be used for this observation
location = {
    'telescope_class': '1m0'
}

# Additional constraints to be added to this request
constraints = {
    'max_airmass': 1.6,
    'min_lunar_distance': 30
}


# The full userrequest, with additional meta-data
userrequest = {
    'group_id': 'Cadence Example 2',  # The title
    'proposal': PROPOSAL_ID,
    'ipp_value': 1.05,
    'operator': 'SINGLE',
    'observation_type': 'NORMAL',
    'requests': [{
        'cadence': cadence,
        'target': target,
        'molecules': molecules,
        'windows': windows,
        'location': location,
        'constraints': constraints
    }]
}

# Now that we have a fully formed UserRequest with a cadence, we can submit it to the api.
response = requests.post(
    'https://observe.lco.global/api/userrequests/cadence/',
    headers={'Authorization': 'Token {}'.format(API_TOKEN)},
    json=userrequest  # Make sure you use json!
)

# Make sure this api call was successful
try:
    response.raise_for_status()
except requests.exceptions.HTTPError as exc:
    print('Request failed: {}'.format(response.content))
    raise exc

# The api has returned a new userrequest with the cadence filled out. We can review and submit if it looks good.
cadence_request = response.json()

print('Cadence generated {} requests'.format(len(cadence_request['requests'])))
i = 1
for request in cadence_request['requests']:
    print('Request {0} window start: {1} window end: {2}'.format(
        i, request['windows'][0]['start'], request['windows'][0]['end']
    ))
    i = i + 1

# Looks good? Submit to the regular /userrequests/ endpoint

response = requests.post(
    'https://observe.lco.global/api/userrequests/',
    headers={'Authorization': 'Token {}'.format(API_TOKEN)},
    json=cadence_request  # Make sure you use json!
)

# Make sure this api call was successful
try:
    response.raise_for_status()
except requests.exceptions.HTTPError as exc:
    print('Request failed: {}'.format(response.content))
    raise exc

userrequest_dict = response.json()

# Print out the url on the portal where we can view the submitted request
print('View this observing request: https://observe.lco.global/userrequests/{}/'.format(userrequest_dict['id']))
