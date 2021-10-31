import os
import re
import threading
from common import  log

def NetBIOS(host):
    cmd = "nbtstat -A {}".format(host)
    r = os.popen(cmd).read()
    if "<00>" in r:
        r1 = re.findall(r"(\S+.+)<00>", r)  # 截取主机名和工作组
        log.LogSuccess("[+] netbios:host:{} hostname:{} group:{}".format(host, r1[0], r1[1]))

if __name__ == "__main__":
    NetBIOS("172.27.73.214")

    print("结束")
