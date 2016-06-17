import sys
import json
import re
from pprint import pprint

def listUsers(client, key):
    luser = client.user.list_users(key)
    data = {}
    for user in list:
        alter = {'login': user.get('login'), 'login_uc': user.get('login_uc'), 'name': user.get('name'), 'email': user.get('email')}
        data.update(alter)    
        
    json_data = data
   
    return(json_data)


