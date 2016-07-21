import httplib
import urllib
import json

constraints = {'max_airmass' : 2.0}

# this selects any telescope on the 1 meter network
location = {
            'telescope_class':'1m0',
}

proposal = {
            'proposal_id'   : 'PROPOSAL_001',
            'user_id'       : 'user@lcogt.net',
            'password'      : 'password',
    }

molecule = {
      # Required fields
    'exposure_time'   : 300.0,  # Exposure time, in secs
    'exposure_count'  : 1,  # The number of consecutive exposures
    'filter'          : 'ip',  # The generic filter name
    # Optional fields. Defaults are as below.
    # fill_window should be defined as True on a maximum of one molecule per request, or you should receive an error when scheduling
    'fill_window'     : False, # set to True to cause this molecule to fill its window (or all windows of a cadence) with exposures, calculating exposure_count for you
    'type'            : 'EXPOSE',  # The type of the molecule
    'ag_name'         : '',  # '' to let it resolve; same as instrument_name for self-guiding
    'ag_mode'         : 'Optional',
    'instrument_name' : '1M0-SCICAM-SBIG',  # This resolves to the main science camera on the scheduled resource
    'bin_x'           : 2,  # Your binning choice. Right now these need to be the same.
    'bin_y'           : 2,
    'defocus'         : 0.0  # Mechanism movement of M2, or how much focal plane has moved (mm)
    }

# define the target
target = {
          'name'              : "Test Target",
          'ra'                : 166.0,  # RA (degrees)
          'dec'               : -33.0,  # Dec (Degrees)
          'epoch'             : 2000,
    }

# A cadence operation must have exactly one request given, which will then become N copies within the cadence window.
request = {
    "constraints" : constraints,
    "location" : location,
    "molecules" : [molecule],
    "observation_note" : "",
    "observation_type" : "NORMAL",
    "target" : target,
    "type" : "request",
    "windows": [],
    }

# cadence parameters for choosing the windows of the requests
cadence = {
    "start" : "2016-07-22 22:00:00",
    "end" : "2016-07-23 23:00:00",
    "period" : 6.0,
    "jitter" : 2.0
}

user_request = {
    "operator" : "single",
    "requests" : [request],
    "type" : "compound_request",
    "cadence" : cadence,
    }

json_user_request = json.dumps(user_request)
params = urllib.urlencode({'username': proposal['user_id'],
                           'password': proposal['password'],
                           'proposal': proposal['proposal_id'],
                           'request_data' : json_user_request})
headers = {'Content-type': 'application/x-www-form-urlencoded'}
conn = httplib.HTTPSConnection("www.lcogt.net")
conn.request("POST", "/observe/service/request/get_cadence_requests", params, headers)
conn_response = conn.getresponse()

# The status can tell you if sending the request failed or not. 200 or 203 would mean success, 400 or anything else fail
status_code = conn_response.status

# If the status was a failure, the response text is a reason why it failed
# If the status was a success, the response text is a json user_request filled with requests for the cadence
response = conn_response.read()

if status_code == 200:
    json_response = json.loads(response)

    # Now this json_user_request can be submitted to the submit endpoint as-is, using code similar to the above, but
    # sending the params to /submit instead of /get_cadence_requests. You can also use it to see how many requests
    # in the cadence were visible / possible.
    json_user_request = json.dumps(json_response)
else:
    print response['error']

