from SQLConnectorMOD import *
from objectsMOD import *

class ChangeUtil:

        def __init__(self, host, user, password, dbName):
                # For create database and tables and save datas to database.
                self.sqlConnector = MysqlDBConnector(host, user, password, dbName)
                
        """
        This function converts json string to object classes.
        And save object classes to database.
        """
        def convertToBeans(self, changeJson):
                # Convert json string to a list of Change object.
                changeList = self.convertChange(changeJson)
                # Save Change objects to database.
                self.sqlConnector.saveChanges(changeList)
                
        """
        This function converts json string to Change object.
        """
        def convertChange(self, changeJson):
                # A list of Change objects
                changeList = []
                for change in changeJson:
                        changeObj = Change()
                        changeObj.uniqueChangeId = change['id']
                        changeObj.changeId = change['change_id']
                        changeObj.project = change['project']
                        changeObj.branch = change['branch']
                        # Some data has no owner information.
                        # If there was no owner information, set the authorId as ''.
                        if not change['owner']:
                                changeObj.authorId = ''
                        # If there has owner infromation, set the authorId as the author's id.
                        else:
                                changeObj.authorId = change['owner']['_account_id']
                        changeObj.createdTime = change['created']
                        changeObj.status = change['status']
                        # Get a list of Revision objects.
                        changeObj.revisions = self.convertRevisions(change)
                        # Get a list of History objects.
                        changeObj.histories = self.convertHistories(change)
                        changeList.append(changeObj)
                return changeList
                
        """
        This fuction converts the json string to Revision object.
        """
        def convertRevisions(self, change):
                revisionList = []
                revisionsJson = change['revisions']
                for key, revision in revisionsJson.iteritems():
                        revisionObj = Revision()
                        revisionObj.revisionId = key
                        if 'commit' in revision.keys():
                                revisionObj.subject = revision['commit']['subject']
                                revisionObj.message = revision['commit']['message']
                                revisionObj.authorName = revision['commit']['author']['name']
                                revisionObj.createdTime = revision['commit']['author']['date']
                                revisionObj.committerName = revision['commit']['committer']['name']
                                revisionObj.committedTime = revision['commit']['committer']['date']
                        revisionObj.patchSetNum = revision['_number']
                        if 'files' in revision.keys():
                                revisionObj.files = self.convertFiles(revision)
                        # Get a list of File objects.
                        revisionList.append(revisionObj)
                return revisionList
        
        """
        This function converts the json string to File object.
        """
        def convertFiles(self, revision):
                fileList = []
                fileJson = revision['files']
                for fileName, fileInfo in fileJson.iteritems():
                        fileObj = File()
                        fileObj.fileName = fileName
                        # Some data has 'lines_inserted' key, but some data did not have.
                        # So it should be checked.
                        if 'lines_inserted' in fileInfo.keys():
                                fileObj.linesInserted = fileInfo['lines_inserted']
                        # Same as above, it should be checked.
                        if 'lines_deleted' in fileInfo.keys():
                                fileObj.linesDeleted = fileInfo['lines_deleted']
                        fileList.append(fileObj)
                return fileList
        
        """
        This function converts json string to History object.
        """
        def convertHistories(self, change):
                historyList = []
                historiesJson = change['messages']
                for i in range(0, len(historiesJson)):
                        historyObj = History()
                        message = historiesJson[i]
                        historyObj.historyId = message['id']
                        # Some data has 'author' key, but some not.
                        # And in the datas have the 'author' key, some have an empty value, and some have values.
                        # So it should be checked.
                        if ('author' not in message.keys()) or (not message['author']):
                                historyObj.authorId = ''
                                historyObj.authorName = ''
                                historyObj.email = ''
                        else:
                                historyObj.authorId = message['author']['_account_id']
                                if 'name' in message['author'].keys():
                                        historyObj.authorName = message['author']['name']
                                if 'email' in message['author'].keys():
                                        historyObj.email = message['author']['email']
                                
                        historyObj.message = message['message']
                        historyObj.createdTime = message['date']
                        if '_revision_number' in message.keys():
                                historyObj.patchSetNum = message['_revision_number']
                        else:
                                if len(historiesJson) > 1:
                                        if i is 0:
                                                historyObj.patchSetNum = 0
                                        else:
                                                historyObj.patchSetNum = historyList[i - 1].patchSetNum
                                else:
                                        historyObj.patchSetNum = 0
                        historyList.append(historyObj)
                return historyList
