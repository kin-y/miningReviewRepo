"""
This class corresponds to t_change table in the databse.
"""
class Change:
	id = None
	uniqueChangeId = None
	changeId = None
	project = None
	branch = None
	authorId = None
	createdTime = None
	status = None
	revisions = []
	histories = []

"""
This class corresponds to t_revision table in the database.
"""
class Revision:
        id = None
        revisionId = None
        subject = None
        message = None
        authorName = None
        committerName = None
        createdTime = None
        committedTime = None
        patchSetNum = None
        changeId = None
        files = []

"""
This class corresponds to t_history table in the database.
"""
class History:
        id = None
        historyId = None
        authorAccountId = None
        authorName = None
        authorUserName = None
        email = None
        message = None
        createdTime = None
        patchSetNum = None
        changeId = None

"""
This class corresponds to t_file table in the database.
"""
class File:
        id = None
        fileName = None
        linesInserted = 0
        linesDeleted = 0
        revisionId = None

"""
This class corresponds to t_people table in the database.
"""
class People:
        id = None
        authorAccountId = None
        authorName = None
        email = None
        authorUserName = None
