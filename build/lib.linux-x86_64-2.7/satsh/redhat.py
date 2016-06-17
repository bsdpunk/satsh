#!/usr/bin/python
from datetime import datetime
import time
import xmlrpclib
import ssl

SATELLITE_URL = "https://t2rarhs701/rhn/rpc/api"
SATELLITE_LOGIN = "tsadlc"
SATELLITE_PASSWORD = "Echo--1984"

client = xmlrpclib.Server(SATELLITE_URL, verbose=0,context=ssl._create_unverified_context())

key = client.auth.login(SATELLITE_LOGIN, SATELLITE_PASSWORD)
list = client.user.list_users(key)
for user in list:
   print user.get('login')

client.auth.logout(key)
