import paramiko
from concurrent.futures import ThreadPoolExecutor
import sys
import threading
from common import  config
def sshTest():
    try:

        # 创建一个ssh的客户端，用来连接服务器
        ssh = paramiko.SSHClient()
        # 创建一个ssh的白名单
        know_host = paramiko.AutoAddPolicy()
        # 加载创建的白名单
        ssh.set_missing_host_key_policy(know_host)
        # 连接服务器
        ssh.connect(
            hostname="172.27.236.199",
            port=22,
            username="zzet",
            password="1234567lsy."
        )
        # 执行命令
        stdin, stdout, stderr = ssh.exec_command("ls")
        # stdin  标准格式的输入，是一个写权限的文件对象
        # stdout 标准格式的输出，是一个读权限的文件对象
        # stderr 标准格式的错误，是一个写权限的文件对象
        print(stdout.read().decode())
        ssh.close()
    except Exception as e:
        print(e)
def sshTest2():
    try:
        private_key_path = '/home/auto/.ssh/id_rsa'
        pkey = paramiko.RSAKey.from_private_key_file(private_key_path)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect('IP', 22, '用户名', pkey)
        stdin, stdout, stderr = ssh.exec_command('df')
        print(stdout.read().decode())
        ssh.close()
    except Exception as e:
        print(e)




ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
is_find = False


def SshCheck(info,user,pwd):
    try:
        Host = info.Host
        Port = info.Ports
        Username = user
        Password = pwd
        if info.SshKey != "":
            try:
                pkey = paramiko.RSAKey.from_private_key_file(info.SshKey)
            except Exception as ee:
                print(ee.__str__())
                return
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(Host, Port, Username, pkey)
        else:
            ssh.connect(Host, Port, Username, Password, timeout=1.5)
        if info.Command != "" :
            stdin, stdout, stderr = ssh.exec_command(info.Command)
            out = stdout.read()
            result="[+] SSH:{}:{}:{} {} \n{}".format(Host, Port, Username, Password, out.decode())
            if info.SshKey != "":
                result="[+] SSH:{}:{} sshkey correct \n{}" .format( Host, Port, out.decode())
            print(result)
            # TODO Log
        else:
            result = ("[+] SSH:{}:{}:{} {} ".format(Host, Port, Username, Password))
            if info.SshKey != "":
                result="[+] SSH:{}:{} sshkey correct" .format( Host, Port)
            print(result)
            # TODO Log
    except Exception as e:
        print("[-] ssh %s:%s %s %s %s" % (info.Host, info.Ports, user,pwd, e.__str__()))
        # TODO logErr
    finally:
        ssh.close()


if __name__ == "__main__":
    info =config.HostInfo()
    info.Host="172.27.236.199"
    info.Ports=22
    info.Command="ls"
    SshCheck(info,"zzet","1234567lsy..")