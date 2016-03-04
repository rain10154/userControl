import threading
import time
import datetime
from common import logger,write_dict_to_file
import os


ssConfig = {
    "server": "0.0.0.0",
    "local_port": 1081,
    "timeout": 300,
    "method": "aes-256-cfb"
}

shell = {
    "start":"ssserver -c /etc/shadowsocks.json -d start",
    "stop":"ssserver -c /etc/shadowsocks.json -d stop",
    "restart":"ssserver -c /etc/shadowsocks.json -d restart"
}

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter, newUser, config):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.newUser = newUser
        self.oldTime = datetime.datetime.now()
        self.config = config
    def run(self):
        self.taskLoad()

    def taskLoad(self):
        self.timer_start()
        while True:
            time.sleep(60)

    def timer_start(self):
        t = threading.Timer(60 * 60, self.test_func)
        t.start()

    def test_func(self):
        newTime = datetime.datetime.now()
        logger.info("time is :%s" ,newTime)
        day = int((newTime - self.oldTime).days)
        if day == 0:
            self.lowDays()

        logger.info("day is :%s", day)
        self.oldTime = newTime
        self.timer_start()

    def lowDays(self):
        ssDict = {}
        userDict = {}
        for key in self.newUser.userDict:
            value = self.newUser.userDict[key]
            days = int(value[2])
            if days > 1:
                value[2] = days-1
                userDict[key] = value
                ssDict[key] = value[1]
        self.newUser.userDict = userDict
        self.newUser.ssDict = ssDict
        logger.info("in lowDays,userDict = %s", userDict)
        writeSStoFile(self.config['file'], userDict)
        ssConfig['port_password'] = ssDict
        write_dict_to_file(self.config['ssFile'], ssConfig)
        os.system(shell['restart'])

def writeSStoFile(fileName, userDict):
    f = open(fileName, 'w')
    for key in userDict:
        value = userDict[key]
        f.write(str(value[0]) + ',' + str(value[1]) + ',' + str(value[2]) + '\n')
    f.close()
