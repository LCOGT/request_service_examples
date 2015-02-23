"""
example_time_allocation_query.py - A simple example script demonstration a query requesting the current time
used/available.

Author:
    Martin Norbury (mnorbury@lcogt.net)

February 2015
"""
import urllib
import json
import getpass
import argparse


def _query_available_time(args):
    url = '{0:s}://{1:s}/observe/proposal/{2:s}/time_summary/'.format('https' if args.secure else 'http',
                                                                      args.host,
                                                                      args.proposal)

    print 'Using url %s' % url

    credentials = {'username': args.user,
                   'password': getpass.getpass(), }

    connection = urllib.urlopen(url, data=urllib.urlencode(credentials))
    response = connection.read()
    connection.close()

    return response


def _parse_response(response):
    try:
        response = json.loads(response)
    except ValueError:
        pass

    return response


def _print_telescope_class_summary(telescope_class, time_for_proposal):
    print '%s time :-' % telescope_class
    print
    for key, value in time_for_proposal[telescope_class].iteritems():
        print '{0:<30} {1}'.format(key, value)

    print
    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='scheduler-dev')
    parser.add_argument('-u', '--user', default='mnorbury@lcogt.net')
    parser.add_argument('-p', '--proposal', default='LCOSchedulerTest')
    parser.add_argument('-s', '--secure', action='store_true')
    configuration_arguments = parser.parse_args()

    raw_response = _query_available_time(configuration_arguments)

    time_allocation = _parse_response(raw_response)

    for telescope_class in time_allocation[configuration_arguments.proposal].keys():
        _print_telescope_class_summary(telescope_class, time_allocation[configuration_arguments.proposal])

