import httplib
import urllib
import json
import getpass

constraints = {'max_airmass' : 3.0}

# this selects any telescope on the 1 meter network
location = {
            'telescope_class':'2m0',
#            'site' : 'lsc'
}

proposal = {
            'proposal_id'   : 'LCOSchedulerTest',
            'user_id'       : 'esaunders@lcogt.net',
            'password'      : getpass.getpass(),
    }

molecule = {
      # Required fields
    'exposure_time'         : 60.0,  # Exposure time, in secs
    'exposure_count'        : 10,  # The number of consecutive exposures
    'spectra_slit'          : 'slit_6.0as',  # The generic filter name
    # Optional fields. Defaults are as below.
    'acquire_mode'          : 'Brightest',
    'acquire_radius_arcsec' : 4.3,
    'type'                  : 'SPECTRUM',  # The type of the molecule
    'ag_name'               : '',  # '' to let it resolve; same as instrument_name for self-guiding
    'ag_mode'               : 'Optional',
    'instrument_name'       : '2M0-FLOYDS-SCICAM',  # This resolves to the main science camera on the scheduled resource
    'bin_x'                 : 2,  # Your binning choice. Right now these need to be the same.
    'bin_y'                 : 2,
    'defocus'               : 0.0  # Mechanism movement of M2, or how much focal plane has moved (mm)
    }

# define the target
target = {
          'name'              : "ODIN API - acquire on brightest (WITH acquire 2)",
          'ra'                : 146.4117,  # RA (degrees)
          'dec'               : -31.1911,  # Dec (Degrees)
          'epoch'             : 2000,
    }

# this is the actual window
window = {
          'start' : "2015-02-12T00:00:00",  # str(datetime)
          'end' : "2015-02-15T00:00:00",  # str(datetime)
    }

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

user_request = {
    "operator" : "single",
    "requests" : [request],
    "type" : "compound_request"
    }

json_user_request = json.dumps(user_request)
params = urllib.urlencode({'username': proposal['user_id'],
                           'password': proposal['password'],
                           'proposal': proposal['proposal_id'],
                           'request_data' : json_user_request})
conn = httplib.HTTPSConnection("test.lcogt.net")
conn.request("POST", "/observe/service/request/submit", params)
response = conn.getresponse().read()
print response
response = json.loads(response)
print response

try:
    print "http://test.lcogt.net/observe/request/" + response['id']
except KeyError:
    print response['error']
