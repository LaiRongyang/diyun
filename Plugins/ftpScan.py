import queue
import socket
import threading
import time
from ftplib import FTP
import  ftplib
from common import  log
from  common import  config


def FtpScan(info):
    flag = anonLogin(info.Host)
    if flag:
        return

    host=info.Host
    userList=config.Userdict["ftp"]
    pwList=[pwd for pwd in config.Passwords]
    qlist = queue.Queue()
    timeout = info.Timeout
    ftpScan(host, userList, pwList , qlist , timeout)
    try:
        while True:
            if qlist.empty():
                break
            else:
                time.sleep(1)
    except KeyboardInterrupt:
        print("Exit the program...")


def ftpScan(host,userList,pwList,qlist,timeout):
    threadnum = 10
    result = []
    for name in userList:
        for pwd in pwList:
            name = name.strip()
            pwd = pwd.strip()
            pwd.replace("{user}",name)
            qlist.put(name + ':' + pwd)
    threads = []
    for x in range(1, threadnum + 1):
        t = threading.Thread(target=scan,args=(qlist,host,timeout,result))
        threads.append(t)
        t.setDaemon(True)  # 主线程完成后不管子线程有没有结束，直接退出
        t.start()


#可以开多个线程运行本函数
def scan(qlist,host,timeout,result):
    while not qlist.empty():
        try:
            name, pwd = qlist.get().split(':')
            ftp = FTP()
            ftp.connect(host, 21, timeout)
            ftp.login(name, pwd)
            time.sleep(0.05)
            result= "[+] ftp://{}:{}:{} {}".format(host, 21, name, pwd)
            retList = returnDefault(ftp)
            for fileName in retList:
                if len(fileName) > 50:
                    result += "\n   [->]" + fileName[:50]
                else:
                    result += "\n   [->]" + fileName
            log.LogSuccess(result)
        except Exception as e:
            result = "[-] ftp://{}:{} {} {}".format(host, 21, name, e.__str__())
            log.LogError(result)
        finally:
            ftp.quit()

def anonLogin(info):
    try:
        ftp = ftplib.FTP(info.Host)
        ftp.login('anonymous', '')
        result = "[+] ftp://{}:{}:{} {}".format(info.Host, info.Ports, "anonymous", "")
        retList= returnDefault(ftp)
        for fileName in retList:
            if len(fileName)>50:
                result += "\n   [->]" + fileName[:50]
            else:
                result += "\n   [->]" + fileName
        log.LogSuccess(result)
        return True
    except Exception as e:
        result = "[-] ftp://{}:{} {} {}".format(info.Host, info.Ports, "anonymous", e.__str__())
        log.LogError(result)
        return False
    finally:
        ftp.quit()

#登陆上ftp服务后，客户以通过ftp.nlst()方法查找所有文件的名字，
#遍历找寻index.htm，index.asp等文件。
def returnDefault(ftp):
    try:
        dirList = ftp.nlst()
    except:
        dirList = []
        # print( '[-] Could not list directory contents.')
        return
    retList = []
    for fileName in dirList:
        fn = fileName.lower()
        """
        if '.php' in fn or '.htm' in fn or '.asp' in fn:
            print ('[+] Found default page: ' + fileName)
        """
        retList.append(fileName)
    return retList

if __name__ == "__main__":
    host=""
    userList=[]
    pwList=[]
    qlist = queue.Queue()
    anonLogin(host)# 先试一试匿名登录
    ftpScan(host, userList, pwList,qlist)
    try:
        while True:
            if qlist.empty():
                break
            else:
                time.sleep(1)
    except KeyboardInterrupt:
        print("Exit the program...")