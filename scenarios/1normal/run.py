import argparse
import random
import secrets
import time
import requests
import numpy as np
import json
import logging

apis=['employee','department','organization']
objs=dict(zip(apis, [[],[],[]])) 

def gen_obj(type:str):
    if type=='organization':
        e={ "id": secrets.token_hex(16),
            "name": secrets.token_hex(4),
            "address": secrets.token_hex(16) }
        return e
    elif type=='department':
        if len(objs['organization']) ==0:
            return None
        else:
            e={ "id": secrets.token_hex(16),
                "organizationId":objs['organization'][random.randint(0,len(objs['organization'])-1)]["id"],
                "name": secrets.token_hex(4)}
            return e
    elif type=='employee':
        if len(objs['department'])==0:
            return None
        else:
            dep=objs['department'][random.randint(0,len(objs['department'])-1)]
            e={ 
                "organizationId": dep["organizationId"],
                "departmentId": dep["id"],
                "name": secrets.token_hex(4),
                "age": random.randint(18,60),
                "position": secrets.token_hex(4) }
            return e

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', dest='server_ip', action='store', type=str, required=True)
    parser.add_argument('-v', dest='verbose', action='store', type=bool, required=False, default=False)
    args = parser.parse_args()
    # logging.basicConfig(level='DEBUG')
    args.server_ip=args.server_ip.strip('/')
    domain = f"http://{args.server_ip}/"

    try:
        res=requests.get(url=domain+"employee/").content
        all_employees=json.loads(res)
    except Exception as e:
        print(e)

    for i in range(100000):
        try:
            method= np.random.choice(['GET','POST','DELETE'   ],p=[0.6,0.2,0.2])
            api=np.random.choice(apis,p=[0.6,0.3,0.1])

            if method=='GET':
                url= domain+api+'/'
                if api=='employee':
                    target=np.random.choice(['all','id'],p=[0.1,0.9])
                    if target=='all':
                        res=requests.get(url=url).content
                        all_employees=json.loads(res)
                        logging.debug(len(all_employees))
                    else:
                        e=np.random.choice(all_employees)
                        url += str(e['id'])
                        res=requests.get(url=url).content
                        logging.debug(res)
                else:
                    res=requests.get(url=url).content
                    logging.debug(res)
            elif method == 'POST':
                obj=gen_obj(api)
                if obj:
                    url= domain+api+'/'
                    res=requests.post(url=url,json=obj).content
                    objs[api].append(obj)
                    logging.debug(res)
                else:
                    logging.debug("fail gen_obj")
            elif method=='DELETE' and all_employees:
                e=np.random.choice(all_employees)
                url= domain+'employee'+str(e['id'])
                res=requests.delete(url)
                logging.debug(res)

            time.sleep(random.random()*0.5)
        except Exception as e:
            print(e)
            time.sleep(random.randint(1,3))