# Observation API Examples

**THIS PROJECT IS DEPRECATED**
**It has been replaced with [observation-portal-api-examples](https://github.com/LCOGT/observation-portal-api-examples)**

This repository contains python scripts demonstrating the use of the [LCO Request API](https://observe.lco.global/api/).
They may be used as a starting point for writing custom scripts for submitting/querying observations on the LCO
network programatically.

**All scripts assume the [requests](http://docs.python-requests.org/en/master/) library is installed.**

### Full Documentation

The example scripts included here are basic. To view the full API documentation, please see the
[LCO Developers Page](https://developers.lco.global).

### Authentication

Most (if not all) examples require the use of an authentication token. This token is similar to a password:
it is used to authenticate you with the API and make sure you have permission to perform specific actions.
This token is placed in the HTTP `Authorization` header and is valid forever (or until you revoke it).

You can obtain your authentication token from your [profile page](https://observe.lco.global/accounts/profile/)
on the observation portal.

If for some reason you are unable to access your profile page (on a server without a graphical interface, for example)
you can also obtain your token via API. The [obtain_auth_token.py](obtain_auth_token.py) example does just that.


### Examples

* [query_requests.py](query_requests.py) Query the requests api for the status of your requests.
* [submit_request.py](submit_request.py) Submit an observation request.
* [submit_spectrograph_request.py](submit_spectrograph_request.py) Submit a spectrograph request.
* [submit_cadence_request.py](submit_cadence_request.py) Submit a request on a cadence.
* [query_ipp.py](query_ipp.py) Query details about Intra Proposal Priority available with a request.
* [query_proposals.py](query_proposals.py) Query proposal details, including time allocations.
* [obtain_auth_token.py](obtain_auth_token.py) Obtain API auth token.
