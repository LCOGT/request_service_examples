import urllib
import httplib
import json
import getpass
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--host', default='scheduler-dev')
parser.add_argument('-u', '--user', default='mnorbury@lcogt.net')
parser.add_argument('-p', '--proposal', default='LCOSchedulerTest')
parser.add_argument('-s', '--secure', action='store_true')
args = parser.parse_args()

protocol = 'https' if args.secure else 'http'
url='%s://%s/observe/proposal/%s/time_summary/' % (protocol,
                                                   args.host,
                                                   args.proposal)

print 'Using url %s' % url

credentials = {'username' : args.user,
               'password' : getpass.getpass(),
              }

connection = urllib.urlopen(url, data=urllib.urlencode(credentials))
response = connection.read()
try:
    response = json.loads(response)
except ValueError:
    pass
print response
print
print

print '2m time :-'
print
for key, value in response[args.proposal]['2m0'].iteritems():
    print '{0:<30} {1}'.format(key, value)
