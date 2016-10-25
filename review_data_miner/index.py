import sys
sys.path.append('MOD')
from changesUtilMOD import *
from notify import *

# host
# e.g., '127.0.0.1'
host = HOSTNAME 
# mysql user name
# e.g. 'root'
user = MYSQL_USER_NAME
# mysql password
password = MYSQL_PWD

# get project name (e.g., aosp, qt, openstack)
project = raw_input("Project name: ")
# if you need to receive a notification email to you email
toaddr = YOUR_EMAIL

dbNames = []
if project == 'aosp':
    dbNames.append('gm_aosp')
elif project == 'qt':
    dbNames.append('gm_qt')
elif project == 'openstack':
    dbNames.append('gm_openstack')
elif project == 'eclipse':
    dbNames.append('gm_eclipse')
elif project == 'libreoffice':
    dbNames.append('gm_libreoffice')
elif project == 'gerrithub':
    dbNames.append('gm_gerrithub')
#elif project == 'all':
#    dbNames.append('gm_aosp')
#    dbNames.append('gm_qt')
#    dbNames.append('gm_openstack')

# get changes
subject = "failed"
try:
    ChangesUtil(host, user, password, dbNames)
    subject = "succeeded"
finally:
    Notify(toaddr, subject)
