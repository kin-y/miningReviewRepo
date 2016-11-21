import mysql.connector
from objectsMOD import *

"""
This class is created for connect to MySQL database, initialize the database and operates the database.
"""
class MysqlDBConnector:
        def __init__(self, host, user, password, dbName, hasDB, status):
                self.config = {
                        'host': host,
                        'user': user,
                        'password': password,
                        'charset': 'utf8'
                        }
                self.dbName = dbName
                self.status = status
                self.db = mysql.connector.connect(**self.config)
                self.cursor = self.db.cursor()
                if hasDB == 'n' or hasDB == 'no':
                        self.initDatabase(dbName)
                else:
                        self.cursor.execute('USE %s' %dbName)
        
        """
        Create database and tables.
        """
        def initDatabase(self, dbName):
                self.cursor.execute('DROP DATABASE IF EXISTS %s' %dbName)
                self.cursor.execute('CREATE DATABASE %s' %dbName)
                self.db.cmd_init_db(dbName)
                # Create tables.
                self.initTables()

        """
        Create tables.
        """
        def initTables(self):
                TABLES = {}
                # t_change table
                TABLES ['t_change'] = (
                        "CREATE TABLE t_change ("
                        " id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,"
                        " ch_id varchar(256) DEFAULT NULL,"
                        " ch_changeId VARCHAR(64) DEFAULT NULL,"
			" ch_changeIdNum INT(11) DEFAULT NULL,"
                        " ch_project VARCHAR(128) DEFAULT NULL,"
                        " ch_branch VARCHAR(128) DEFAULT NULL,"
                        " ch_topic VARCHAR(128) DEFAULT NULL,"
                        " ch_authorAccountId VARCHAR(16) DEFAULT NULL,"
                        " ch_createdTime DATETIME DEFAULT NULL,"
			" ch_updatedTime DATETIME DEFAULT NULL,"
                        " ch_status VARCHAR(16) DEFAULT NULL,"
                        " ch_mergeable VARCHAR(16) DEFAULT NULL"
                        ") ENGINE=InnoDB DEFAULT CHARSET=utf8"
                        )
                # t_revision table
                TABLES ['t_revision'] = (
                        "CREATE TABLE t_revision ("
                        " id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,"
                        " rev_id varchar(64) DEFAULT NULL,"
                        " rev_subject LONGTEXT DEFAULT NULL,"
                        " rev_message LONGTEXT DEFAULT NULL,"
                        " rev_authorUsername VARCHAR(64) DEFAULT NULL,"
                        " rev_createdTime DATETIME DEFAULT NULL,"
                        " rev_committerUsername VARCHAR(64) DEFAULT NULL,"
                        " rev_committedTime DATETIME DEFAULT NULL,"
                        " rev_ref VARCHAR(256) DEFAULT NULL,"
                        " rev_git VARCHAR(256) DEFAULT NULL,"
                        " rev_repo VARCHAR(256) DEFAULT NULL,"
                        " rev_http VARCHAR(256) DEFAULT NULL,"
                        " rev_ssh VARCHAR(256) DEFAULT NULL,"
                        " rev_patchSetNum INT(11) DEFAULT NULL,"
                        " rev_changeId INT(11) DEFAULT NULL"
                        ") ENGINE=InnoDB DEFAULT CHARSET=utf8"
                        )
                # t_history table
                TABLES ['t_history'] = (
                        "CREATE TABLE t_history ("
                        " id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,"
                        " hist_id VARCHAR(64) DEFAULT NULL,"
                        " hist_message LONGTEXT DEFAULT NULL,"
                        " hist_authorAccountId VARCHAR(16) DEFAULT NULL,"
                        " hist_createdTime DATETIME DEFAULT NULL,"
                        " hist_patchSetNum INT(11) DEFAULT NULL,"
                        " hist_changeId INT(11) DEFAULT NULL,"
                        " INDEX(hist_changeId)"
                        ") ENGINE=InnoDB DEFAULT CHARSET=utf8"
                        )
                # t_file table
                TABLES ['t_file'] = (
                        "CREATE TABLE t_file ("
                        " id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,"
                        " f_fileName VARCHAR(512) DEFAULT NULL,"
                        " f_linesInserted INT(11) DEFAULT NULL,"
                        " f_linesDeleted INT(11) DEFAULT NULL,"
                        " f_revisionId INT(11) DEFAULT NULL"
                        ") ENGINE=InnoDB DEFAULT CHARSET=utf8"
                        )

                # t_people table
                TABLES ['t_people'] = (
                        "CREATE TABLE t_people ("
                        " id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,"
                        " p_accountId VARCHAR(16) DEFAULT NULL,"
                        " p_name VARCHAR(64) DEFAULT NULL,"
                        " p_email VARCHAR(64) DEFAULT NULL,"
                        " p_userName VARCHAR(64) DEFAULT NULL"
                        ") ENGINE=InnoDB DEFAULT CHARSET=utf8"
                        )

                for name, sql in TABLES.iteritems():
                        self.cursor.execute(sql)

        """
        This function save changes data to database.
        """
        def saveChanges(self, changeList):
                for change in changeList:
                        # There has duplicated data, so it has necessary to check if the data exists in database before insert.
                        if self.ifExistsChange(change):
                                continue
                        else:
                                sql = 'insert into t_change(ch_id, ch_changeId, ch_changeIdNum, ch_project, ch_branch, ch_topic, ch_authorAccountId, ch_createdTime, ch_updatedTime, ch_status, ch_mergeable) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                                data = (change.uniqueChangeId, change.changeId, change.changeIdNum, change.project, change.branch, change.topic, change.authorAccountId, change.createdTime, change.updatedTime, change.status, change.mergeable)
                                self.cursor.execute(sql, data)
                                self.db.commit()
                                # Get the primary key id (It was auto incremented.).
                                change.id = self.cursor.lastrowid
                                # Save revisions.
                                self.saveRevisions(change)
                                # Save histories.
                                self.saveHistories(change)
                                
        """
        This function save revisions data to database.
        """
        def saveRevisions(self, change):
                for revision in change.revisions:
                        sql = 'insert into t_revision(rev_id, rev_subject, rev_message, rev_authorUsername, '\
                              'rev_createdTime, rev_committerUsername, rev_committedTime, rev_ref, rev_git, rev_repo, '\
                              'rev_http, rev_ssh, rev_patchSetNum, rev_changeId) '\
                              'values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                        data = (revision.revisionId, revision.subject, revision.message, revision.authorUsername,
                                revision.createdTime, revision.committerUsername, revision.committedTime, revision.ref,
                                revision.git, revision.repo, revision.http, revision.ssh, revision.patchSetNum, change.id)
                        self.cursor.execute(sql, data)
                        self.db.commit()
                        # Get the primary key id (It was auto incremented.).
                        revision.id = self.cursor.lastrowid
                        self.saveFiles(revision)
                  
        """
        This function save files data to database.
        Some files data has more than 80000 datas, and it will cause exception when insert into the database at one time (It was overed the limit.).
        So it designed as commit to database when gots 10000 datas.
        """
        def saveFiles(self, revision):
                sql = 'insert into t_file(f_fileName, f_linesInserted, f_linesDeleted, f_revisionId) values(%s, %s, %s, %s)'
                data = []
                for revFile in revision.files:
                        data.append((revFile.fileName, revFile.linesInserted, revFile.linesDeleted, revision.id))
                        if len(data) % 10000 is 0:
                               self.cursor.executemany(sql, data)
                               self.db.commit()
                               data = []
                if len(data) > 0:
                        self.cursor.executemany(sql, data)
                        self.db.commit()
                       
        """
        This function save histories data to database.
        """
        def saveHistories(self, change):
                for history in change.histories:
                        sql = 'insert into t_history(hist_id, hist_message, hist_authorAccountId, hist_createdTime, hist_patchSetNum, hist_changeId) values(%s, %s, %s, %s, %s, %s)'
                        data = (history.historyId, history.message, history.authorAccountId, history.createdTime, history.patchSetNum, change.id)
                        self.cursor.execute(sql, data)
                        self.db.commit()
                        self.savePeople(history);
                        
        def savePeople(self, history):
                sql = 'insert into t_people(p_accountId, p_name, p_email, p_userName) values(%s, %s, %s, %s)'
                if self.ifExistsPeople(history.authorAccountId) == False and history.authorAccountId != '':
                        data = (history.authorAccountId, history.authorName, history.email, history.authorUserName)
                        self.cursor.execute(sql, data)
                        self.db.commit()

        def ifExistsPeople(self, id):
                sql = 'select p_accountId from t_people where p_accountId="%s"' %id
                self.cursor.execute(sql)
                result = self.cursor.fetchall()
                if len(result)>0:
                        return True
                else:
                        return False
                
        """
        This function checks if current data exists in the database.
        """
        def ifExistsChange(self, change):
                sql = 'select id from t_change where ch_id="%s"' %change.uniqueChangeId
                self.cursor.execute(sql)
                result = self.cursor.fetchall()
                if len(result)>0:
                        return True
                else:
                        return False

        def getChangeIds(self):
                sql = 'select id from t_change where ch_status="%s" or ch_status="%s"' %('ABANDONED', 'MERGED')
                self.cursor.execute(sql)
                result = self.cursor.fetchall()
                ids = []
                for r in result:
                        ids.append(r[0])
                return ids

        def getAuthorId(self, changeId):
                sql = 'select ch_authorId from t_change where id=%s' %changeId
                self.cursor.execute(sql)
                result = self.cursor.fetchone()
                authorId = result[0]
                return authorId

        def getHistories(self, changeId):
                sql = 'select hist_authorId, hist_createdTime, hist_message from t_history where hist_changeId=%s' %changeId
                self.cursor.execute(sql)
                result = self.cursor.fetchall()
                histories = []
                for r in result:
                        history = History()
                        history.authorAccountId = r[0]
                        history.createdTime = r[1][0:10]
                        history.message = r[2]
                        histories.append(history)
                return histories
        
        def getStartPoint(self):
                clause = ''
                if self.status == 'open':
                        clause = 'NEW'
                elif self.status == 'merged':
                        clause = 'MERGED'
                elif self.status == 'abandoned':
                        clause = 'ABANDONED'
                else:
                        print("SQL: status error")
                        raise
                sql = 'SELECT count(*) FROM %s.t_change where ch_status = "%s"' %(self.dbName, clause)
                print(sql)
                self.cursor.execute(sql)
                result = self.cursor.fetchone()
                return result[0]
