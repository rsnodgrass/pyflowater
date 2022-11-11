#!/usr/local/bin/python3

import logging
import os
import pprint
import sys

from pyflowater import PyFlo


def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def main():
    user = os.getenv("FLO_USER", None)
    password = os.getenv("FLO_PASSWORD", None)

    if (user == None) or (password == None):
        print("ERROR! Must define env variables FLO_USER and FLO_PASSWORD")
        raise SystemExit

    # setup_logger()
    pp = pprint.PrettyPrinter(indent=2)

    flo = PyFlo(user, password)

    print(f"User = #{flo.user_id}")

    print("\n--Data--")
    pp.pprint(flo.data())

    print("\n--Locations--")
    locations = flo.locations()
    pp.pprint(locations)

    print("\n--Single Location--")
    location_info = locations[0]
    location_id = location_info["id"]
    pp.pprint(flo.location(location_id))

    for location in locations:
        print(f"\n--Location {location['id']}--")

        for device in location["devices"]:
            id = device["id"]

            print("\n--Devices--")
            pp.pprint(device)

            print("\n--Device Info--")
            pp.pprint(flo.device(id))

            print("\n--Consumption--")
            pp.pprint(flo.consumption(id))


if __name__ == "__main__":
    main()
