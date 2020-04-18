import urllib.request
import json
from changeUtilMOD import *
import datetime

class Util(ChangeUtil):
    def __init__(self, host, user, password, dbName, hasDB, status):
        ChangeUtil.__init__(self, host, user, password, dbName, hasDB, status)
        self.num = 100
        self.status = status
        if dbName == 'gm_aosp':
            self.span = 500
            # self.statuses = ['open', 'merged', 'abandoned']
            self.url = 'https://android-review.googlesource.com/changes/?o=ALL_REVISIONS&o=ALL_FILES&o=ALL_COMMITS&o=MESSAGES&o=DETAILED_ACCOUNTS&n=%s' %self.num
            self.getChangesUseS(dbName)
        elif dbName == 'gm_qt':
            self.N = None
            # self.statuses = ['open', 'merged', 'abandoned', 'deferred']
            self.url = 'https://codereview.qt-project.org/changes/?o=ALL_REVISIONS&o=ALL_FILES&o=ALL_COMMITS&o=MESSAGES&o=DETAILED_ACCOUNTS&n=%s' %self.num
            self.getChangesUseN(dbName)
        elif dbName == 'gm_openstack':
            self.span = 500
            # self.statuses = ['open', 'merged', 'abandoned']
            self.url = 'https://review.openstack.org/changes/?o=ALL_REVISIONS&o=ALL_FILES&o=ALL_COMMITS&o=MESSAGES&o=DETAILED_ACCOUNTS&n=%s' %self.num
            self.getChangesUseS(dbName)
        elif dbName == 'gm_eclipse':
            self.span = 500
            # self.statuses = ['open', 'merged', 'abandoned']
            self.url = 'https://git.eclipse.org/r/changes/?o=ALL_REVISIONS&o=ALL_FILES&o=ALL_COMMITS&o=MESSAGES&o=DETAILED_ACCOUNTS&n=%s' %self.num
            self.getChangesUseS(dbName)
        elif dbName == 'gm_libreoffice':
            self.span = 500
            # self.statuses = ['open', 'merged', 'abandoned']
            self.url = 'https://gerrit.libreoffice.org/changes/?o=ALL_REVISIONS&o=ALL_FILES&o=ALL_COMMITS&o=MESSAGES&o=DETAILED_ACCOUNTS&n=%s' %self.num
            self.getChangesUseS(dbName)
        elif dbName == 'gm_gerrithub':
            self.span = 100
            # self.statuses = ['open', 'merged', 'abandoned']
            self.url = 'https://review.gerrithub.io/changes/?o=ALL_REVISIONS&o=ALL_FILES&o=ALL_COMMITS&o=MESSAGES&o=DETAILED_ACCOUNTS&n=%s' %self.num
            self.getChangesUseS(dbName)
        elif dbName == 'gm_chromium':
            self.span = 100
            # self.statuses = ['open', 'merged', 'abandoned']
            self.url = 'https://chromium-review.googlesource.com/changes/?o=ALL_REVISIONS&o=ALL_FILES&o=ALL_COMMITS&o=MESSAGES&o=DETAILED_ACCOUNTS&n=%s' %self.num
            self.getChangesUseS(dbName)
    """
    This function for Gerrit v2.9-2.11 REST API. use S parameter
    """
    def getChangesUseS(self, dbName):
        isMore = True
        span = self.getStart()
        print(dbName.split('gm_')[1] + ", start point: " + str(span))
        while isMore:
            # Set status parameter and S parameter to url.
            url = self.url + '&q=status:%s&S=%s' %(self.status, span)
            print('status: ' + self.status + ', from ' + str(span) + ' to ' + str(span + self.span))
            # The respond data looks like )]}'[...]
            changeStr = urllib.request.urlopen(url).read()[4:]
            try:
                changeJson = json.loads(changeStr)
            except ValueError as e:
                print (e)
            if len(changeJson) is 0:
                isMore = False
            else:
                self.convertToBeans(changeJson)
            span = span + self.span
        print('...' + dbName.split('gm_')[1] + ' done...')

    """
    This function for Gerrit v2.7-2.8 REST API. use N
    """
    def getChangesUseN(self, dbName):
        print('...' + dbName.split('gm_')[1] + ' start...')
        isMore = True
        while isMore:          
            url = self.url + '&q=status:%s' %self.status
            print('status: ' + self.status)
            if not self.N is None:
                url = url + '&N=%s' %self.N
            changeStr = urllib.urlopen(url).read()[4:]
            try:
                changeJson = json.loads(changeStr)
            except ValueError as e:
                print (e)
            self.convertToBeans(changeJson)
            if len(changeJson) < 1:
                isMore = False
                self.N = None
            else:
                self.N = changeJson[len(changeJson) - 1]['_sortkey']
        print('...' + dbName.split('gm_')[1] + ' done...')

