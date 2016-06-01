import httplib
import urllib
import json

constraints = {'max_airmass' : 3.0}

# This helps specify the specific location, or group of locations to perform this observation on
# This should specify the specific telescope, site, dome you want to perform a calibration on
location = {
    # Required fields
    'telescope_class':'1m0',

    # Optional Fields
    'site'       : 'lsc',
    'observatory': 'doma',
    'telescope'  : '1m0a', # Should further specify the 'telescope_class'
}

# A valid proposal with time on the telescopes you are requesting on is necessary for all requests
# Enter your odin user_id (email) and password in the script here
proposal = {
            'proposal_id'   : 'LCOSchedulerTest',
            'user_id'       : 'user@lcogt.net',
            'password'      : 'password',
    }

# You can use this to set up a single User Request to perform several calibration molecules in order.
molecule = {
    # Required fields for all molecules
    'exposure_count'  : 10,  # The number of consecutive exposures
    # This resolves to the main science camera on the scheduled resource. It must be a class.
    # Valid instrument classes: '1M0-SCICAM-SBIG', '1M0-SCICAM-SINISTRO', '2M0-FLOYDS-SCICAM', '2M0-SCICAM-SPECTRAL',
    # '2M0-SCICAM-MEROPE', '0M8-SCICAM-SBIG', '0M4-SCICAM-SBIG', '2M0-FLOYDS-AG'
    'instrument_name' : '1M0-SCICAM-SBIG',

    # Required for AUTO_FOCUS, ZERO_POINTING, DARK, STANDARD, EXPOSE, SPECTRUM molecules
    'exposure_time'   : 60.0,  # Exposure time, in secs

    # Required for AUTO_FOCUS, ZERO_POINTING, STANDARD, SKY_FLAT, EXPOSE molecules
    'filter'          : 'ip',  # The generic filter name


    # Optional fields. Defaults are as below.
    # Change the type to whatever molecule type you want for calibration,
    # Calibration molecule types include: 'BIAS', 'DARK', 'AUTO_FOCUS', 'ZERO_POINTING', 'SKY_FLAT', 'STANDARD'
    'type'            : 'EXPOSE',  # The type of the molecule
    # fill_window should be defined as True on a maximum of one molecule per request, or you should receive an error when scheduling
    'fill_window'     : False, # set to True to cause this molecule to fill its window (or all windows of a cadence) with exposures, calculating exposure_count for you
    'ag_name'         : '',  # '' to let it resolve; same as instrument_name for self-guiding
    'ag_mode'         : 'Optional',
    'bin_x'           : 2,  # Your binning choice. Right now these need to be the same.
    'bin_y'           : 2,
    'defocus'         : 0.0  # Mechanism movement of M2, or how much focal plane has moved (mm)
    }

# define the target
target = {
          'name'              : "Test Target",
          'ra'                : 12.0,  # RA (degrees)
          'dec'               : 34.4,  # Dec (Degrees)
          'epoch'             : 2000,
    }

# This is the window the scheduler will use to schedule this observation. You will want to change this before submitting
window = {
          'start' : "2015-12-24T22:00:00",  # str(datetime)
          'end' : "2015-12-24T23:00:00",  # str(datetime)
    }

# A Request can have one or more molecules
request = {
    "constraints" : constraints,
    "location" : location,
    "molecules" : [molecule],
    "observation_note" : "",
    "observation_type" : "NORMAL",
    "target" : target,
    "type" : "request",
    "windows" : [window],
    }

# A User Request can have one or more Requests
user_request = {
    "operator" : "single",
    "requests" : [request],
    # ipp_value is an optional field that acts as a multiplier to your proposal base priority.
    "ipp_value": 1.0,
    "type" : "compound_request"
    }

# This is the python code necessary to send the json request to the requestdb. You should be able to re-use this section
# in any scripts you create to send the requests you generate to the requestdb.
json_user_request = json.dumps(user_request)
params = urllib.urlencode({'username': proposal['user_id'],
                           'password': proposal['password'],
                           'proposal': proposal['proposal_id'],
                           'request_data' : json_user_request})
conn = httplib.HTTPSConnection("lcogt.net")
conn.request("POST", "/observe/service/request/submit", params)
conn_response = conn.getresponse()

# The status can tell you if sending the request failed or not. 200 or 203 would mean success, 400 or anything else fail
status_code = conn_response.status

# If the status was a failure, the response text is a reason why it failed
# If the status was a success, the response text is tracking number of the submitted request
response = conn_response.read()

response = json.loads(response)
print response

if status_code == 200:
    try:
        print "http://lcogt.net/observe/request/" + response['id']
    except KeyError:
        print response['error']
