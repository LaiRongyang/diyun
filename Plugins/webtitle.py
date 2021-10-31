# -*- coding: utf-8 -*-
import socket
from optparse import OptionParser
import requests
import threading
import time
import queue
import ipaddress
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import requests, sys
import threading, getopt
from urllib import parse
from bs4 import BeautifulSoup
from contextlib import closing
from common import log

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def WebTitle(info):
    if info.Url == "":
        if info.Ports == "80":
            info.Url = "http://{}".format(info.Host)
            get_title(info.Url)
        elif info.Ports == "443":
            info.Url = "https://{}".format(info.Host)
            get_title(info.Url)
        else:
            info.Url = "{}://{}:{}".format("http", info.Host, info.Ports)
            get_title(info.Url)
            info.Url = "{}://{}:{}".format("https", info.Host, info.Ports)
            get_title(info.Url)
            """
            host = "{}:{}".format(info.Host, info.Ports)
            protocol = GetProtocol(host, info.Timeout)
            info.Url = "{}://{}:{}".format(protocol,info.Host, info.Ports)
            
            """
    else:
        if "://" not in info.Url:
            info.Url = "{}://{}".format("http", info.Url)
            get_title(info.Url)
            info.Url = "{}://{}".format("https", info.Url)
            get_title(info.Url)
            """
            protocol = GetProtocol(info.Url, info.Timeout)
            info.Url = "{}://{}".format(protocol, info.Url)
            """
        else:
            get_title(info.Url)



# 版本一
def GetTitle(url):
    try:
        # print(url)
        if isfile(url) != 0:
            return 0
        req = requests.get(url=url, headers=UsRandom(), verify=False, timeout=3, stream=True)
        # lock.acquire()
        req.encoding = req.apparent_encoding
        datalen = len(req.text)
        suop = BeautifulSoup(req.text, 'html.parser')
        try:
            title = str(suop.title.text).strip()
        except Exception as e:
            title = 'title:Null'
        host = parse.urlparse(url).netloc
        '''
        res={
            'URL': url,
            'Status':str(req.status_code),
            'Title':title,
            'Ip':host,
            'len':str(datalen)
        }
        print(res) 
        '''
        result = "[*] WebTitle:{} code:{} len:{} title:{}".format(url, str(req.status_code), str(datalen), title)
        log.LogSuccess(result)
    except Exception as e:
        # print(url, str(e))
        pass


def UsRandom():
    return {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"}


def isfile(url):
    try:
        with closing(requests.get(url, stream=True, timeout=5)) as response:
            size = int(response.headers['content-length'])
            # print(url, str(size) + ' kb')
            return 0
    except Exception as e:
        print("error" + e.__str__())
        pass
        return 1


"""
版本二
python3 写的多线程扫描IP段爬取title。在一定线程下，代理探测内网资产title的非常使用。
在代理进行内网渗透时内网资产不容易找到,适用于内网、外网环境。

注解
1.使用ipaddress模块获取C段地址，也可以是B段；
2.只使用threading模块，没有添加队列queue；
3.增加了queue队列，和多线程threading配合使用。更加实用；
"""


def scan(host):
    port_list = [80, 81, 82, 443, 4433, 7001, 8000, 8001, 8008, 8009, 8080, 8081, 8088, 8089, 8443, 8800, 8888, 8889,
                 9090, 9999]
    try:
        for port in port_list:
            s = socket.socket()
            s.settimeout(0.5)
            if s.connect_ex((str(host), (port))) == 0:
                print(str(host) + ':' + str(port), 'open')
                try:
                    if int(port) == 443:
                        url = 'https://' + str(host)
                    elif int(port) == 8443:
                        url = 'https://' + str(host)
                    elif int(port) == 4433:
                        url = 'https://' + str(host)
                    else:
                        url = 'http://' + str(host) + ':' + str(port)
                    get_title(url)
                except:
                    pass
            s.close()
    except Exception as e:
        print(e)


def get_title(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
        response = requests.get(url, headers=headers, timeout=3, verify=False).text
        soup = BeautifulSoup(response, 'lxml')
        span = soup.title.string
        #print("\033[1;37;40m" + url + "\ttitle:" + span + "\033[0m")
        result = "[*] WebTitle:{}  title:{}".format(url,  span.strip())
        log.LogSuccess(result)
    except Exception as e:
        pass


def worker():
    while not q.empty():
        host = q.get()
        try:
            scan(host)
        finally:
            q.task_done()


def thread(threads):
    thread_list = []
    for t in range(threads):
        t = threading.Thread(target=worker, args=())
        thread_list.append(t)
    for t in thread_list:
        t.start()
    for t in thread_list:
        t.join()


if __name__ == '__main__':
    """
    parser = OptionParser("get_webtitle.py -i 192.168.1.0/24 -t threads")
    parser.add_option("-i", "--cidrip",action="store",type="string",dest="cidrip",help="192.168.1.0/24")
    parser.add_option("-t","--threads",action="store",type="int",dest="threads",default=20,help="threads")
    (options, args) = parser.parse_args()
    if options.cidrip:
        t1 = time.time()
        q = queue.Queue()
        cidrip = options.cidrip
        threads = options.threads
        ips = ipaddress.ip_network(cidrip)
        for host in ips.hosts():
            q.put(host)
        thread(threads)
        q.join()
        print('end time:',time.time()-t1)
    else:
        parser.error('incorrect number of arguments')
"""


    get_title("http://epo.cug.edu.cn/")
