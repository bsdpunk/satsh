from __future__ import print_function
import xml.etree.ElementTree as ET
from datetime import datetime
import time
import xmlrpclib
import ssl
import re
import readline
import threading
import sys
#import requests
import json
import os
from pprint import pprint
import signal
import random
import getpass
import urlparse
import argparse
import pkg_resources
#Counters and Toggles
import readline
import codecs
import unicodedata
import readline
import rlcompleter
import user

arg_count = 0
no_auth = 0
server_count = 0
database_count = 0
ddb_count = 0
hist_toggle = 0
prompt_r = 0




#For tab completion
COMMANDS = ['list-users','help', 'quit']

#For X number of arguements
ONE = ['list-users']
TWO = ['domain-resource-list']
THREE = ['domain-resource-list']
FOUR = ['domain-resource-create']
FIVE = ['domain-resource-create']
SIX = ['linode-disk-dist']
#For what class
DOMAIN= ['domain-resource-create']
USER= ['list-users']
HELPER = ['help', 'quit', 'exit']


for arg in sys.argv:
    arg_count += 1

#warnings are ignored because of unverified ssl warnings which could ruin output for scripting
import warnings
warnings.filterwarnings("ignore")



#These are lists of things that are persistent throughout the session
tokens = {}
servers = {}
databases = {}
username = ''
ddi_bast = {}
details = {}
def complete(text, state):
        for cmd in COMMANDS:
                if cmd.startswith(text):
                    if not state:
                        return cmd
                    else:
                        state -= 1


#os expand must be used for 
config_file = os.path.expanduser('~/.satsh')
hist_file = os.path.expanduser('~/.satsh_history')

hfile = open(hist_file, "a")
if os.path.isfile(config_file):
    config=open(config_file, 'r')
    config=json.load(config)
else:
    username = raw_input("Username:")
    password = getpass.getpass("Password:")

    sat_url = "https://t2rarhs701/rhn/rpc/api"
    config= {"default":[{"username":username,"password":password,"sat_url":sat_url}]}
    
    config_file_new = open(config_file, "w")
    config_f = str(config)
    config_f = re.sub("'",'"',config_f)
    config_file_new.write(config_f)
    config_file_new.close() 

#Ending when intercepting a Keyboard, Interrupt
def Exit_gracefully(signal, frame):
    sys.exit(0)



#DUH
def get_sat_key(config):
    signal.signal(signal.SIGINT, Exit_gracefully)
    #global username
    username = config["default"][0]["username"]
    password = config["default"][0]["password"]
    sat_url = config["default"][0]["sat_url"]
    key={}
    key["client"] = xmlrpclib.Server(sat_url, verbose=0,context=ssl._create_unverified_context())

    key["key"]=key["client"].auth.login(username, password)
    try:
        return(key)
    except KeyError:
        print("Bad Credentials!")
        os.unlink(config_file)
        bye()
    return(key)

satsh_p = 'satsh'

#main command line stuff
def cli():
    while True:
        valid = 0

        signal.signal(signal.SIGINT, Exit_gracefully)
        try:
            if 'libedit' in readline.__doc__:
                readline.parse_and_bind("bind ^I rl_complete")
            else:
                readline.parse_and_bind("tab: complete")

            readline.set_completer(complete)
            readline.set_completer_delims(' ')
            cli = str(raw_input(PROMPT))
        except EOFError:
            bye()
        if hist_toggle == 1:
            hfile.write(cli + '\n')
        if 'key' in locals():
            pass
        else:
            key = get_sat_key(config)    

#This is not just a horrible way to take the commands and arguements, it's also shitty way to sanatize the input for one specific scenario

#I miss perl :(


        cli = re.sub('  ',' ', cli.rstrip())
            



##########################################################################################
# This starts the single satsh commands
#######################################################################################

        api_key = get_sat_key(config)
        #Write try statement here for error catching
        command = cli.split(' ', 1)[0]

        if command in DOMAIN:
            l_class = 'domain'
       elif command in USER:
            l_class = 'user'
        else:
            l_class = ''       

        if len(cli.split(' ')) > 0:
            if len(cli.split(' ')) ==6:
                command,arg_one,arg_two,arg_three,arg_four,arg_five = cli.split()
                if command in SIX:
                    command = command.replace("-", "_")
                    l_class = eval(l_class)
                    result = getattr(l_class, command)(api_key, arg_one, arg_two,arg_three,arg_four,arg_five)
                    print(result)
                    valid = 1

            if len(cli.split(' ')) ==5:
                command,arg_one,arg_two,arg_three,arg_four = cli.split()
                if command in FIVE:
                    command = command.replace("-", "_")
                    l_class = eval(l_class)
                    result = getattr(l_class, command)(api_key, arg_one, arg_two,arg_three,arg_four)
                    print(result)
                    valid = 1

            if len(cli.split(' ')) ==4:
                command,arg_one,arg_two,arg_three = cli.split()
                if command in FOUR:
                    command = command.replace("-", "_")
                    l_class = eval(l_class)
                    result = getattr(l_class, command)(api_key, arg_one, arg_two,arg_three)
                    print(result)
                    valid = 1

            if len(cli.split(' ')) ==3:
                command,arg_one,arg_two = cli.split()
                if command in THREE:
                    command = command.replace("-", "_")
                    l_class = eval(l_class)
                    result = getattr(l_class, command)(api_key, arg_one, arg_two)
                    print(result)
                    valid = 1

                valid = 1
            elif len(cli.split(' ')) ==2:
                command,arguement = cli.split()
                if command in TWO:
                    command = command.replace("-", "_")
                    l_class = eval(l_class)
                    result = getattr(l_class, command)(api_key, arguement)
                    print(result)
                    valid = 1
                
                else:
                    print("Invalid Arguements")

            else:
               if cli in ONE:                    
                    cli = cli.replace("-", "_")
                    l_class = eval(l_class)
                    result = getattr(l_class, cli)(api_key)
                    pprint(result)
                    valid = 1
               elif cli in HELPER:
                    if cli == "quit" or cli == "exit":
                        hfile.close()
                        bye()
                    if cli == "help":
                        print(help_menu())
                        valid = 1
               else:
                    print("Invalid Command")



        if valid == 0:
            print("Unrecoginized Command")


def help_menu():
####Why did I space the help like this, cause something something, then lazy
    help_var = """
(required) <optional>

list-users : lists satellite users
help : show commands and usage
"""
    return(help_var)

def bye():
    exit()

if arg_count == 2:
    command = sys.argv[1]
#noauth is essentially for testing
    if command == "noauth":
        no_auth = 1
#history is to toggle writing a history file, there is currently no clean up so it is off by default
    if command == "history":
        hist_toggle = 1
    if command == "roulette":
        rando = random.randint(1, 3)
    if command == "extra":
        satsh_p = config["default"][0]["prompt"]

                 

    if command == "list-servers":
        api_key = get_linode_key(config)
        pprint(servers_action.list_servers(api_key))
        valid = 1
        bye()
    if command == "avail-datacenters":
        api_key = get_linode_key(config)
        pprint(lin_utility.avail_datacenters(api_key))
        valid = 1
        bye()
    if command == "avail-stackscripts":
        api_key = get_linode_key(config)
        pprint(lin_utility.avail_stackscripts(api_key))
        valid = 1
        bye()
    if command == "avail-distributions":
        api_key = get_linode_key(config)
        pprint(lin_utility.avail_distributions(api_key))
        valid = 1
        bye()
    if command == "avail-plans":
        api_key = get_linode_key(config)
        pprint(lin_utility.avail_plans(api_key))
        valid = 1
        bye()
    if command == "nodebal-list":
        api_key = get_linode_key(config)
        pprint(node_balance.nodebal_list(api_key))
        valid = 1
        bye()
    if command == "ip-list":
        api_key = get_linode_key(config)
        pprint(servers_action.ip_list(api_key))
        valid = 1
        bye()



PROMPT = satsh_p + '> '

if no_auth == 1:
    api_key =0
else:
    api_key = get_sat_key(config)

####Again, shit way to do this, Here's hoping it's better in beta :)
    ##You know what, fuck you, it's fine
if arg_count == 3:
    command = sys.argv[1]
    arguement = sys.argv[2]
    if command == "ip-list":
        print(servers_action.ip_list(api_key, arguement))
        valid = 1
        bye()
    if command == "linode-shutdown":
        print(servers_action.linode_shutdown(api_key, arguement))
        valid = 1
        bye()
    if command == "nodebal-node-list":
        api_key = get_linode_key(config)
        print(node_balance.nodebal_node_list(api_key, arguement))
        valid = 1
        bye()
    if command == "nodebal-config-list":
        api_key = get_linode_key(config)
        print(node_balance.nodebal_config_list(api_key, arguement))
        valid = 1
        bye()
    if command == "nodebal-config-list":
        api_key = get_linode_key(config)
        print(node_balance.nodebal_create(api_key, arguement))
        valid = 1
        bye()

 

if arg_count == 4:
    command = sys.argv[1]
    arg_one = sys.argv[2]
    arg_two = sys.argv[3]
    arg_three = sys.argv[4]
    arg_four = sys.argv[5]

    if command == "linode-create":
        api_key = get_linode_key(config)
        print(servers_action.linode_create(api_key, arg_one, arg_two))
        valid = 1
        bye()


 

if arg_count == 5:
    command = sys.argv[1]
    arg_one = sys.argv[2]
    arg_two = sys.argv[3]
    arg_three = sys.argv[4]
    arg_four = sys.argv[5]

if arg_count == 6:
    command = sys.argv[1]
    arg_one = sys.argv[2]
    arg_two = sys.argv[3]
    arg_three = sys.argv[4]
    arg_four = sys.argv[5] 
#######################################################################################
#
#######################################################################################
#
#######################################################################################
#
#######################################################################################
#
#######################################################################################    
#
#######################################################################################
