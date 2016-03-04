import random
from common import logger


commonStr = 'abcdefghijklmnopqrstuvwxyz1234567890'

passwordSize = 10

month = 30

year = 12

port = 8000

class Singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            new = super(Singleton, cls)
            cls._instance = new.__new__(cls, *args, **kw)
        return cls._instance

class User(Singleton):
    userDict = {}
    ssDict = {}

    def getUserDict(self):
        return self.userdict

    def addUser(self, fileName, test = False):
        (newName, newPassword) = self.generateNewUser()
        logger.info('newName,newPassword:' + str(newName) + ',' + newPassword)

        time = 3
        if (test == False):
            time = month * year
        value = [newName, newPassword, time]

        with open(fileName, "a") as f:
            f.write(str(newName) + ',' + newPassword + ',' + str(time) + '\n')

        self.userDict[newName] = value
        self.ssDict[newName] = newPassword
        return (newName, newPassword)

    def generateNewUser(self):
        # name is port
        newName = ''
        newPassword = ''

        while(1):
            global port
            newName = port + 1;
            port = port + 1;

            if (self.userDict.has_key(newName)):
                continue

            i = 1
            while(i <= passwordSize):
                newPassword += random.choice(commonStr)
                i += 1

            break

        return (newName, newPassword)