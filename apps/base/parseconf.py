from configparser import ConfigParser


def parsedbcf(cfgdir):
    cfp = ConfigParser()
    cfp.read(cfgdir, encoding="utf-8-sig")
    host = cfp.get('mysql', 'host')
    username = cfp.get('mysql', 'username')
    password = cfp.get('mysql', 'password')
    dbname = cfp.get('mysql', 'dbname')
    port = cfp.get('mysql', 'port')
    return {"host": host, "username": username, "password": password, "dbname": dbname, "port": int(port)}

def parsekcpcf(cfgdir):
    cfp = ConfigParser()
    cfp.read(cfgdir, encoding="utf-8-sig")
    login_uri = cfp.get('kcp', 'login_uri')
    username = cfp.get('kcp', 'username')
    password = cfp.get('kcp', 'password')
    appsDete_uri = cfp.get('kcp', 'appsDete_uri')
    kcpCtlAppId = cfp.get('kcp', 'kcpCtlAppId')
    allureDete_uri = cfp.get('kcp','allureDete_uri')
    startTaskTest_uri = cfp.get('kcp', 'startTaskTest_uri')
    return login_uri,username,password,appsDete_uri,kcpCtlAppId,allureDete_uri,startTaskTest_uri

def parseonecf(cfgdir):
    cfp = ConfigParser()
    cfp.read(cfgdir, encoding="utf-8-sig")
    login_uri = cfp.get('one', 'login_uri')
    username = cfp.get('one', 'username')
    password = cfp.get('one', 'password')
    appsDete_uri = cfp.get('one', 'appsDete_uri')
    oneCtlAppId = cfp.get('one', 'oneCtlAppId')
    allureDete_uri = cfp.get('one','allureDete_uri')
    startTaskTest_uri = cfp.get('one', 'startTaskTest_uri')
    return login_uri,username,password,appsDete_uri,oneCtlAppId,allureDete_uri,startTaskTest_uri
