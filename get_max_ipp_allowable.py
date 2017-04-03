#!/usr/bin/env python

'''
get_max_ipp_allowable.py - Example usage of the LCOGT Request submission API

This script is a working Python example of how to get the maximum allowable ipp_value for a simple Request through
 the LCOGT programmatic API.

Author: Eric Saunders
March 2016
'''

import httplib
import urllib
import json
import getpass

 # If you want to limit the maximum airmass, set it here
constraints = {'max_airmass' : 1.6}

# This observation can be made on any 1m telescope
location = {
            'telescope_class' : '1m0',
}

# A valid proposal with time on the telescopes you are requesting on is necessary for all requests
# Enter your odin user_id (email) in the script here
proposal = {
            'proposal_id' : 'LCOSchedulerTest',
            'user_id'     : 'jnation@lcogt.net',
            'password'    : getpass.getpass(),
    }

molecule = {
      # Required fields
    'exposure_time'   : 60.0,  # Exposure time, in secs
    'exposure_count'  : 10,  # The number of consecutive exposures
    'filter'          : 'ip',  # The generic filter name
    # Optional fields. Defaults are as below.
    'fill_window'     : False, # set to True to cause this molecule to fill its window (or all windows of a cadence) with exposures, calculating exposure_count for you
    'type'            : 'EXPOSE',   # This should be 'EXPOSE' for all normal imaging observations
    'ag_name'         : '',         # You should never need to set this
    'ag_mode'         : 'Optional', # Choose from 'On', 'Off' or 'Optional'
    'instrument_name' : '1M0-SCICAM-SINISTRO',  # 1m:  Choose from '1M0-SCICAM-SBIG' or '1M0-SCICAM-SINISTRO'
                                            # 2m:  Choose from '2M0-FLOYDS-SCICAM', '2M0-SCICAM-SPECTRAL', '2M0-SCICAM-MEROPE'
                                            # 0m4: Choose '0M4-SCICAM-SBIG'
    'bin_x'           : 2,  # Your binning choice. Right now these need to be the same.
    'bin_y'           : 2,
    'defocus'         : 0.0  # Mechanism movement of M2, or how much focal plane has moved (mm)
    }

# Define the (sidereal) target
target = {
          'name'    : 'Test Target',
          'ra'      : 12.0,  # RA (degrees)
          'dec'     : 34.4,  # Dec (Degrees)
          'epoch'   : 2000,
         }

# This is the window of time within which the scheduler will schedule this observation.
window = {
          'start' : '2016-04-24T22:00:00',  # str(datetime)
          'end' : '2016-04-29T23:00:00',  # str(datetime)
         }

# A Request can have one or more molecules
request = {
            'constraints'      : constraints,
            'location'         : location,
            'molecules'        : [molecule],
            'observation_note' : '',
            'observation_type' : 'NORMAL',  # 'NORMAL' or 'TARGET_OF_OPPORTUNITY'
            'target'           : target,
            'type'             : 'request',
            'windows'          : [window],
          }

# A User Request can have one or more Requests
user_request = {
                 'operator' : 'single',
                 'requests' : [request],
                 'type'     : 'compound_request'
               }

# Send the constructed JSON request to LCOGT.
json_user_request = json.dumps(user_request)
params = urllib.urlencode({'username': proposal['user_id'],
                           'password': proposal['password'],
                           'proposal': proposal['proposal_id'],
                           'request_data' : json_user_request})
headers = {'Content-type': 'application/x-www-form-urlencoded'}
conn = httplib.HTTPSConnection('test.lcogt.net')
conn.request('POST', '/observe/service/request/get_max_allowed_ipp', params, headers)
conn_response = conn.getresponse()

# The status can tell you if sending the request failed or not.
# 200 or 203 would mean success, 400 or anything else fail
status_code = conn_response.status

# If the status was a failure, the response text is a reason why it failed
# If the status was a success, the response text is tracking number of the submitted request
response = conn_response.read()

if status_code == 200 or status_code == 203:
    response = json.loads(response)
    print response
else:
    print "request failed, status code = {}, response = {}".format(status_code, response)


