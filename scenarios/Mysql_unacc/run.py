from BaseExploit import *

import pymysql

def mysql_unacc(host, port, user, passwd):
    db = pymysql.connect(host=host,port=port,
                        user=user,
                        password=passwd,
                        database='KADB')
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    data = cursor.fetchone()
    # print ("Database version : %s " % data)
    db.close()

Exploit(mysql_unacc, args.host, args.port, "root", "123456")()
