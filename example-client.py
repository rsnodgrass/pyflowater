#!/usr/local/bin/python3

import os
import sys
import pprint
import logging
import json

from pyflowater import PyFlo

def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def main():
    user = os.getenv('FLO_USER', None)
    password = os.getenv('FLO_PASSWORD', None)

    if (user == None) or (password == None):
        print("ERROR! Must define env variables FLO_USER and FLO_PASSWORD")
        raise SystemExit

    #setup_logger()
    pp = pprint.PrettyPrinter(indent = 2)
 
    flo = PyFlo(user, password)

    print('--Locations--')
    locations = flo.locations
    pp.pprint(locations)

    print("\n--All Devices--")
    for location in locations['locations']:
        pp.pprint( location['devices'] )

if __name__ == "__main__":
    main()
