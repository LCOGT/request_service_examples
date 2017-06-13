#!/bin/env python
import requests

'''
query_ipp.py

Return details about Intra Proposal Priority that can be used with this request.
'''

API_TOKEN = 'PlaceApiTokenHere'  # API token obtained from https://observe.lco.global/accounts/profile/
PROPOSAL_ID = 'LCOEngineering'  # Proposal IDs may be found here: https://observe.lco.global/proposals/

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

# The windows in which this request should be considered for observing. In this example we only provide one.
windows = [{
    'start': '2017-05-02 00:00:00',
    'end': '2017-09-02 00:00:00'
}]

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
    'group_id': 'Example Request 3',  # The title
    'proposal': PROPOSAL_ID,
    'ipp_value': 1.05,
    'operator': 'SINGLE',
    'observation_type': 'NORMAL',
    'requests': [{
        'target': target,
        'molecules': molecules,
        'windows': windows,
        'location': location,
        'constraints': constraints
    }]
}

# Now that we have a fully formed UserRequest, we can submit it to the api.
response = requests.post(
    'https://observe.lco.global/api/userrequests/max_allowable_ipp/',
    headers={'Authorization': 'Token {}'.format(API_TOKEN)},
    json=userrequest  # Make sure you use json!
)

# Make sure this api call was successful
try:
    response.raise_for_status()
except requests.exceptions.HTTPError as exc:
    print('Request failed: {}'.format(response.content))
    raise exc

ipp = response.json()  # The API will return json with details about IPP available on this request.

# Print out the url on the portal where we can view the submitted request
print(ipp)
