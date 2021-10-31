# -*- coding: utf-8 -*-
import psycopg2
import os, sys, re, socket, time
import pymssql
import queue
from common import config
import threading
from common import log

threadnum = 10


def PostgresScan(info):
    qlist = queue.Queue()
    for user in config.Userdict["postgresql"]:
        for pwd in config.Passwords:
            pwd = pwd.replace("{user}", user)
            qlist.put(user + ':' + pwd)
    threads = []
    for x in range(1, threadnum + 1):
        t = threading.Thread(target=scan, args=(qlist, info.Host, info.Ports, info.Timeout))
        threads.append(t)
        t.setDaemon(True)  # 主线程完成后不管子线程有没有结束，直接退出
        t.start()
    try:
        while True:
            if qlist.empty():
                break
            else:
                time.sleep(1)
    except KeyboardInterrupt:
        print("Exit the program...")


def scan(qlist, host, port, Timeout):
    while not qlist.empty():
        user, pwd = qlist.get().split(':')
        try:
            psycopg2.connect(host=host, user=user, passwd=pwd, db="Postgres",port=port)
            result = "[+] postgresql:{}:{}:{} {}".format(host, port, user, pwd)
            log.LogSuccess(result)
        except Exception as e:
            result = "[-] postgresql {}:{} {} {} {}".format(host, port, user, pwd, e.__str__())
            log.LogError(result)
            pass




