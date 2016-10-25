import urllib
import json
from changeUtilMOD import *
import datetime

class Util(ChangeUtil):
    def __init__(self, host, user, password, dbName):
        ChangeUtil.__init__(self, host, user, password, dbName)
        self.num = 500
        if dbName == 'gm_aosp':
            self.span = 500
            self.statuses = ['open', 'merged', 'abandoned']
            self.url = 'https://android-review.googlesource.com/changes/?o=ALL_REVISIONS&o=ALL_FILES&o=ALL_COMMITS&o=MESSAGES&o=DETAILED_ACCOUNTS&n=%s' %self.num
            self.getChangesUseS(dbName)
        elif dbName == 'gm_qt':
            self.N = None
            self.statuses = ['open', 'merged', 'abandoned', 'deferred']
            self.url = 'https://codereview.qt-project.org/changes/?o=ALL_REVISIONS&o=ALL_FILES&o=ALL_COMMITS&o=MESSAGES&o=DETAILED_ACCOUNTS&n=%s' %self.num
            self.getChangesUseN(dbName)
        elif dbName == 'gm_openstack':
            self.N = None
            self.statuses = ['open', 'merged', 'abandoned']
            self.url = 'https://review.openstack.org/changes/?o=ALL_REVISIONS&o=ALL_FILES&o=ALL_COMMITS&o=MESSAGES&o=DETAILED_ACCOUNTS&n=%s' %self.num
            self.getChangesUseN(dbName)
	elif dbName == 'gm_eclipse':
            self.span = 500
            self.statuses = ['open', 'merged', 'abandoned']
            self.url = 'https://git.eclipse.org/r/changes/?o=ALL_REVISIONS&o=ALL_FILES&o=ALL_COMMITS&o=MESSAGES&o=DETAILED_ACCOUNTS&n=%s' %self.num
            self.getChangesUseS(dbName)
        elif dbName == 'gm_libreoffice':
            self.span = 500
            self.statuses = ['open', 'merged', 'abandoned']
            self.url = 'https://gerrit.libreoffice.org/changes/?o=ALL_REVISIONS&o=ALL_FILES&o=ALL_COMMITS&o=MESSAGES&o=DETAILED_ACCOUNTS&n=%s' %self.num
            self.getChangesUseS(dbName)
        elif dbName == 'gm_gerrithub':
            self.span = 500
            self.statuses = ['open', 'merged', 'abandoned']
            self.url = 'https://review.gerrithub.io/changes/?o=ALL_REVISIONS&o=ALL_FILES&o=ALL_COMMITS&o=MESSAGES&o=DETAILED_ACCOUNTS&n=%s' %self.num
            self.getChangesUseS(dbName)
    """
    This function for Gerrit v2.9-2.11 REST API. use S parameter
    """
    def getChangesUseS(self, dbName):
        print('...' + dbName.split('gm_')[1] + ' start...')
        for status in self.statuses:
            print('status:' + status)
            isMore = True
            span = 0
            while isMore:
                # Set status parameter and S parameter to url.
                url = self.url + '&q=status:%s&S=%s' %(status, span)
                # The respond data looks like )]}'[...]
                changeStr = urllib.urlopen(url).read()[4:]
                try:
                    changeJson = json.loads(changeStr)
                except ValueError, e:
                    getError(e)
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
        for status in self.statuses:
            print('status:' + status)
            isMore = True
            while isMore:
                url = self.url + '&q=status:%s' %status
                if not self.N is None:
                    url = url + '&N=%s' %self.N
                changeStr = urllib.urlopen(url).read()[4:]
                try:
                    changeJson = json.loads(changeStr)
                except ValueError, e:
                    getError(e)
                self.convertToBeans(changeJson)
                if len(changeJson) < 1:
                    isMore = False
                    self.N = None
                else:
                    self.N = changeJson[len(changeJson) - 1]['_sortkey']
        print('...' + dbName.split('gm_')[1] + ' done...')

    """
    Print error log
    """
    def getError(self, e):
        print e
        filename = "Errorlog\\" + datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S')
        file_ = open(filename, 'w')
        file_.write(changeStr)
        file_.close()
