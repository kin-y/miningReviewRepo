from utilMOD import *

class ChangesUtil:
        def __init__(self, host, user, password, dbNames):
                for dbName in dbNames:
                        Util(host, user, password, dbName)
