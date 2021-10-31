# smb 爆破
import time
from smb import SMBConnection
import queue
from common import config
import threading
from common import log

threadnum = 10

def SmbScan(info):
    qlist = queue.Queue()
    for user in config.Userdict["smb"]:
        for pwd in config.Passwords:
            pwd.replace("{user}", user)
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
        s = SMBConnection.SMBConnection(user, pwd, '', '')
        try:
            if s.connect(host) == True:
                s.close()
                result = "[+] SMB:{}:{}:{} {}".format(host, port, user, pwd)
                print(result)
            else:
                errlog = "[-] smb {}:{} {} {} ".format(host, 445, user, pwd)
                print(errlog)
        except Exception as e:
            errlog = "[-] smb {}:{} {} {} {}".format(host, 445, user, pwd, e.__str__())
            print(errlog)





