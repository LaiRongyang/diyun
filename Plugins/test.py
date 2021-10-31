# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# code by cseroad

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

def scan(host):
    port_list = [80,81,82,443,4433,7001,8000,8001,8008,8009,8080,8081,8088,8089,8443,8800,8888,8889,9090,9999]
    try:
        for port in port_list:
            s = socket.socket()
            s.settimeout(0.5)
            if s.connect_ex((str(host), (port))) == 0:
                print(str(host)+':'+str(port),'open')
                try:
                    if int(port) == 443:
                        url = 'https://' + str(host)
                    elif int(port) == 8443:
                        url = 'https://' + str(host)
                    elif int(port) == 4433:
                        url  = 'https://' + str(host) 
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
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
        response = requests.get(url,headers=headers,timeout=3,verify=False).text
        soup = BeautifulSoup(response,'lxml')
        span = soup.title.string
        print("\033[1;37;40m"+url+"\ttitle:"+span+"\033[0m")
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
        t = threading.Thread(target = worker,args = ())
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