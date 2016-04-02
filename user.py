from flask import Flask,jsonify,request


from common import parse_json_in_str,logger,write_dict_to_file
import One
import task
import logging
import logging.config
import sys
import os


app = Flask(__name__)

fileName = 'config'

config = {}

shell = {
    "start":"ssserver -c /etc/shadowsocks.json -d start",
    "stop":"ssserver -c /etc/shadowsocks.json -d stop",
    "restart":"ssserver -c /etc/shadowsocks.json -d restart"
}

ssConfig = {
    "server": "0.0.0.0",
    "local_port": 1080,
    "timeout": 300,
    "method": "aes-256-cfb",
    "fast_open": True
}

@app.route('/addUser', methods=['GET'])
def addUser():
    newUser = One.User()
    (newName, newPassword) = newUser.addUser(config['file'])
    ssConfig['port_password'] = newUser.ssDict
    logger.info("users = %s" , newUser.userDict)
    logger.info("config = %s", ssConfig)

    write_dict_to_file(config['ssFile'], ssConfig)
    os.system(shell['restart'])
    return jsonify({'name':newName,'password':newPassword})


@app.route('/addTestUser', methods=['GET'])
def addTestUser():
    newUser = One.User()
    (newName, newPassword) = newUser.addUser(config['file'], test=True)

    ssConfig['port_password'] = newUser.ssDict
    logger.info("users = %s" , newUser.userDict)
    logger.info("config = %s", ssConfig)
    write_dict_to_file(config['ssFile'], ssConfig)

    os.system(shell['restart'])
    return jsonify({'name':newName,'password':newPassword})


@app.route('/addUserTime', methods=['POST'])
def addUserTime():
    data = request.json
    logger.info("data = %s" + str(data))
    name = data['name']
    days = data['days']
    if name is None or days is None:
        return "param is null"
    newUser = One.User()
    newUser.addUserTime(config['file'], int(name), days)
    return "ok!"



def queryCurrentUser():
    newUser = One.User()
    ssDict = {}
    userDict = {}
    try:
        userFile = open(config['file'], "r")
        for line in userFile:
            line=line.strip('\n')
            oneUserStr = line.split(",")
            oneUser = [oneUserStr[0], oneUserStr[1], oneUserStr[2]]
            userName =  int(oneUserStr[0])
            userDict[userName] = oneUser
            ssDict[oneUserStr[0]] = oneUserStr[1]
        userFile.close()
    except IOError as ioe:
        logger.error(ioe)
        f = open(config['file'], 'w')
        f.close()

    newUser.ssDict = ssDict;
    newUser.userDict = userDict;
    return



if __name__ == '__main__':
    #query config
    with open(fileName, 'rb') as f:
        try:
            config = parse_json_in_str(f.read().decode('utf8'))
        except ValueError as e:
            logging.error('found an error in config.json: %s',
                          e.message)
            sys.exit(1)

    queryCurrentUser()

    newUser = One.User()
    ssConfig['port_password'] = newUser.ssDict
    write_dict_to_file(config['ssFile'], ssConfig)


    os.system(shell['start'])

    newUser = One.User()
    thread1 = task.myThread(1, "Thread-1", 1, newUser, config)
    thread1.start()

    app.run(host="0.0.0.0", port=10000,debug=False)



