#!/usr/bin/env python

# Command:      ops_getservicestatus
# Description:  Provide a servicelist for a Domain
# Author:       Rohit <rohitr@one.com>

import requests
import json
import getopt
import sys

message =  """
Usage:
ops_getservicestatus <domain>
"""
if len(sys.argv) < 2:
    print ("Error: Domain not provided")
    sys.exit(message)
elif len(sys.argv) > 2:
    print ("Error: Multiple arguments not allowed")
    sys.exit(message)

try:
    domain= sys.argv[1]
    url = "https://systemsapi.one.com/v1/domains/" + domain + "/" + "services"
    headers = {'Accept': 'application/vnd.api+json','Content-Type': 'application/vnd.api+json'}
    r =requests.get(url, headers=headers)
    data = json.loads(r.text)

    exit=False
    if not data["data"]:
        print ("Error: Invalid domain")
        sys.exit(message)

    from prettytable import PrettyTable
    x = PrettyTable()
    x.field_names = ["Name" , "status"]

    for i in data['data']:
     try:

        if (i['attributes']['suspensions']['Default']) == False:
            x.add_row((i['id'], "Not Suspended"))
            x.add_row(('Server', i['attributes']['server']))
            x.add_row(('Marked for deletion', i['attributes']['marked_for_deletion']))
            x.add_row(('Provisioned', i['attributes']['provisioned']))
            x.add_row(('-----------------------','--------------------------------------'))

        else:

            x.add_row((i['id'], "suspended"))
            x.add_row(('Server', i['attributes']['server']))
            x.add_row(('Marked for deletion', i['attributes']['marked_for_deletion']))
            x.add_row(('Provisioned', i['attributes']['provisioned']))
            x.add_row(('Quota', i['attributes']['suspensions']['Quota']))
            x.add_row(('-----------------------','--------------------------------------'))

     except KeyError :
        pass
except Exception as e:
    print message
print x

