import pymysql

def sqlConct(host,user,passwd,dbname,port,use_unicode=True,charset="utf8"):
    conn = pymysql.connect(host,user,passwd,dbname,port,use_unicode,charset)
    return conn

def truncateData(conn,sql):
    csr = conn.cursor()
    try:
        csr.execute(sql)
        conn.commit()
    except:
        conn.rollback()

def sqlcls(conn):
    conn.close()