import argparse
import lib.api as api

ap = argparse.ArgumentParser()
ap.add_argument("-u", "--user", help="username of account to scan")
ap.add_argument("-l", "--location", action="store_true", help="try to get life places location of this person")
args = vars(ap.parse_args())

if args['user']:
    api.user_info(username=args["user"])

if args['location']:
    api.location_info(username=args["user"])


