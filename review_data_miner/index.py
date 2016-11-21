import sys
import json
sys.path.append('MOD')
from utilMOD import *

with open('config.json', 'r') as f:
    config = json.load(f)

if config:
    host = config['host']
    user = config['user']
    password = config['password']
    dbName = config['db_name']
    hasDB = config['has_db']
    statusList = config['status_list']
    currentStatus = config['current_status']
else:
    print("config file not exist")
    raise

"""
Database list so far:

gm_aosp (some problems)
gm_qt (official API problem)
gm_openstack
gm_eclipse
gm_libreoffice
gm_gerrithub

"""

statuses = []
    
for s in statusList:
    if currentStatus == s['status'] or len(statuses) != 0:
        statuses.append(s['status'])

for status in statuses:
    config['current_status'] = status
    config['has_db'] = 'y'
    with open('config.json', 'w') as f:
        json.dump(config, f)
    
    Util(host, user, password, dbName, hasDB, status)
