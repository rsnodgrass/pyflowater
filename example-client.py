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

    print(f"User = #{flo.user_id}")

    print("\n--Data--")
    pp.pprint( flo.data() )

    print("\n--Locations--")
    locations = flo.locations()
    pp.pprint( locations )

    print("\n--Single Location--")
    location_info = locations[0]
    location_id = location_info['id']    
    pp.pprint( flo.location(location_id) )

    print("\n--Consumption--")
    for location in locations:
        for device in location['devices']:
            pp.pprint( device )
            id = device['id']
            print( id )
            pp.pprint( flo.consumption(id) )

if __name__ == "__main__":
    main()
