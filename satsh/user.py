import sys
import json
import re
from pprint import pprint

def list_users(key):
    luser = key["client"].user.list_users(key["key"])
    #pprint(luser)
    data = {}
    for user in luser:
        alter = {'login': user.get('login'), 'login_uc': user.get('login_uc'), 'name': user.get('name'), 'email': user.get('email')}
        data[user.get('login')]=alter
        
    json_data = data
   
    return(json_data)


