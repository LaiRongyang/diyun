from pyfiglet import Figlet
import argparse
from common import config
from common import log
from common import ParseIP
import sys
import os

parser = argparse.ArgumentParser(conflict_handler='resolve')


def banner():
    print(Figlet(font='standard').renderText("Di Yun"))
    print("version: 0.0\n")


# 参数是HostInfo类型
def argParse(Info):
    banner()

    parser.add_argument("-h", default="",
                        help="IP address of the host you want to scan,for example: 192.168.11.11 | 192.168.11.11-255 | 192.168.11.11,192.168.11.12")
    parser.add_argument("-hn", default="", help="the hosts no scan,as: -hn 192.168.1.1/24")
    parser.add_argument("-p", default=config.DefaultPorts, help="Select a port,for example: 22 | 1-65535 | 22,80,3306")
    parser.add_argument("-pn", default="", help="the ports no scan,as: -pn 445")
    parser.add_argument("-c", default="", help="exec command (ssh)")
    parser.add_argument("-sshkey", default="", help="sshkey file (id_rsa)")
    parser.add_argument("-domain", default="", help="smb domain")
    parser.add_argument("-user", default="", help="username")
    parser.add_argument("-pwd", default="", help="password")
    parser.add_argument("-time", default=3, help="Set timeout")
    parser.add_argument("-m", default="all", help="Select scan type ,as: -m ssh")
    parser.add_argument("-path", default="", help="fcgi、smb romote file path")
    parser.add_argument("-t", default=600, help="Thread nums")
    parser.add_argument("-hf", default="", help="host file, -hf ip.txt")
    parser.add_argument("-userf", default="", help="username file")
    parser.add_argument("-pwdf", default="", help="password file")
    parser.add_argument("-rf", default="", help="redis file to write sshkey file (as: -rf id_rsa.pub) ")
    parser.add_argument("-rs", default="", help="redis shell to write cron file (as: -rs 192.168.1.1:6666) ")
    parser.add_argument("-nopoc", default=False, help="not to scan web vul")
    parser.add_argument("-np", default=False, help="not to ping")
    parser.add_argument("-ping", default=False, help="using ping replace icmp")
    parser.add_argument("-o", default="result.txt", help="Outputfile")
    parser.add_argument("-no", default=False, help="not to save output log")
    parser.add_argument("-debug", default=60, help="every time to LogErr")
    parser.add_argument("-silent", default=False, help="silent scan")
    parser.add_argument("-u", default="", help="url")
    parser.add_argument("-uf", default="", help="urlfile")
    parser.add_argument("-pocname", default="", help="use the pocs these contain pocname, -pocname weblogic")
    parser.add_argument("-proxy", default="", help="set poc proxy, -proxy http://127.0.0.1:8080")
    parser.add_argument("-cookie", default="", help="set poc cookie")
    parser.add_argument("-wt", default=5, help="Set web timeout")
    parser.add_argument("-num", default=20, help="poc rate")

    args = parser.parse_args()

    Info.Host = args.h
    config.NoHosts = args.hn
    Info.Ports = args.p
    config.NoPorts = args.pn
    Info.Command = args.c
    Info.SshKey = args.sshkey
    Info.Domain = args.domain
    Info.Username = args.user
    Info.Password = args.pwd
    Info.Timeout = args.time
    Info.Scantype = args.m
    Info.Path = args.path
    config.Threads = args.t
    config.HostFile = args.hf
    config.Userfile = args.userf
    config.Passfile = args.pwdf
    config.RedisFile = args.rf
    config.RedisShell = args.rs
    config.IsWebCan = args.nopoc
    config.IsPing = args.np
    config.Ping = args.ping
    config.TmpOutputfile = args.o
    config.TmpSave = args.no
    log.WaitTime = args.debug
    log.Silent = args.silent
    config.URL = args.u
    config.UrlFile = args.uf
    config.Pocinfo.PocName = args.pocname
    config.Pocinfo.Proxy = args.proxy
    config.Pocinfo.Cookie = args.cookie
    config.Pocinfo.Timeout = args.wt
    config.Pocinfo.Num = args.num


def parse(Info):
    parseScantype(Info)
    parseUser(Info)
    parsePass(Info)
    parseInput(Info)


def parseScantype(Info):
    if (Info.Scantype not in config.PORTList):
        showmode()
    if Info.Scantype != "all":
        if Info.Ports == config.DefaultPorts:
            if Info.Scantype == "web":
                Info.Ports = config.Webport
            elif Info.Scantype == "ms17010":
                Info.Ports = "445"
            elif Info.Scantype == "cve20200796":
                Info.Ports = "445"
            elif Info.Scantype == "portscan":
                Info.Ports = config.DefaultPorts
            elif Info.Scantype == "main":
                Info.Ports = config.DefaultPorts
            else:
                port = config.PORTList[Info.Scantype]
                Info.Ports = str(port)
            print("-m ", Info.Scantype, " start scan the port:", Info.Ports)


def showmode():
    print("The specified scan type does not exist")
    print("-m")
    for name in config.PORTList.keys():
        print("   [" + name + "]")
    sys.exit(1)


def parseUser(Info):
    if Info.Username == "" and config.Userfile == "":
        return
    if Info.Username != "":
        Info.Usernames = Info.Username.split(",")
    if config.Userfile != "":
        users = readfile(config.Userfile)
        for user in users:
            Info.Usernames.append(user)
    Info.Usernames = ParseIP.removeDuplicate(Info.Usernames)
    for name in config.Userdict.keys():
        config.Userdict[name] = Info.Usernames


def parsePass(Info):
    if Info.Password != "":
        passs = Info.Password.split(",")
        for ps in passs:
            if ps != "":
                Info.Passwords.append(ps)
        config.Passwords = Info.Passwords
    if config.Passfile != "":
        passs = readfile(config.Passfile)
        for ps in passs:
            if ps != "":
                Info.Passwords.append(ps)
        config.Passwords = Info.Passwords
    if config.UrlFile != "":
        urls = readfile(config.UrlFile)
        urls = ParseIP.removeDuplicate(urls)
        for url in urls:
            if url != "":
                config.Urls.append(url)


def parseInput(Info):
    if Info.Host == "" and config.HostFile == "" and config.URL == "" and config.UrlFile == "":
        print("Host is none")
        parser.print_help()
        sys.exit(1)
    config.Outputfile = getpath() + "result.txt"
    if config.TmpOutputfile != "":
        if '/' not in config.TmpOutputfile or '\\' not in config.TmpOutputfile:
            config.Outputfile = getpath() + config.TmpOutputfile
        else:
            config.Outputfile = config.TmpOutputfile
    if config.TmpSave:
        config.IsSave = False
    if Info.Ports == config.DefaultPorts:
        Info.Ports = Info.Ports + "," + config.Webport


def getpath():
    path = os.path.dirname(os.path.realpath(__file__))  # 文件所在文件夹路径
    if '\\' in path or '/' in path:
        tmp = os.path.dirname(path)
        if tmp != "":
            path = tmp
    return os.path.join(path, "")


# 参数是文件路径 返回值是string 列表
def readfile(filename):
    content = []
    try:
        f = open(filename, mode='r')
        for line in f:
            text = line.strip()
            content.append(text)
    except:
        print("Open %s error\n" % filename)
        sys.exit(1)
    else:
        f.close()
    return content


def CheckErr(*args):
    # python 只需要raise自定义的Error
    # 然后用 try except 过滤
    sys.exit(0)
    return


if __name__ == "__main__":
    Info = config.HostInfo()
    argParse(Info)
    parse(Info)
    print(config.Outputfile)
