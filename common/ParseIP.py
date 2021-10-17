import IPy
import socket
import re
import sys


# raise ParseIPErr() 时，如果没有被捕获，就会执行__str__(self)
# 捕获方法
# except ParseIPErr as e:
#    print (e.args)
#    print(e) 会输出两次 内部调用__str__() 输出一次  print()输出一次
class ParseIPErr(RuntimeError):
    def __init__(self, *args):
        self.args = ("host parsing error\n" \
                     "format: \n" \
                     "192.168.1.1\n" \
                     "192.168.1.1/8\n" \
                     "192.168.1.1/16\n" \
                     "192.168.1.1/24\n" \
                     "192.168.1.1,192.168.1.2\n" \
                     "192.168.1.1-192.168.255.255\n" \
                     "192.168.1.1-255",)

    def __str__(self):
        for arg in self.args:
            print(arg)
        return self.args[0]


def removeDuplicate(old):
    new = []
    for s in old:
        if s not in new:
            new.append(s)
    return new


def parseIP(ip, filename, nohost):
    hosts = []
    if ip != "":
        hosts = paraseIPs(ip, True)  # host 是一个 列表 [ip1,ip2,域名1....]
    if filename != "":
        filehost = readIPFile(filename)  # filehost 是一个 列表 [ip1,ip2,域名1....]
        hosts = hosts + filehost
    hosts = set(hosts)  # 去重
    if nohost != "":
        nohosts = paraseIPs(nohost, True)  # nohost 是一个 列表 [ip1,ip2,域名1....]
        if len(nohost) > 0:
            nohosts = set(nohosts)
            hosts = hosts - nohosts
    hosts = list(hosts)
    hosts.sort()
    return hosts


def paraseIPs(ip, *flag):
    flag1 = True
    hosts = []
    if len(flag) > 0:
        flag1 = flag[0]
    if ',' in ip:
        IPList = ip.split(",")
        for IP in IPList:
            ips = ParseIPone(IP)
            # CheckErr()
            hosts = hosts + ips
    else:
        hosts = ParseIPone(ip)

    return hosts


def ParseIPone(ip):
    """
    安装go版的逻辑：
    如果ip最后三个字符有"/24"则返回 ParseIPA(ip) 解析  192.168.1.1/24
    如果ip最后三个字符有"/16"则返回 ParseIPA(ip) 解析  192.168.1.1/16
    如果ip最后三个字符有"/8"则返回 ParseIPA(ip) 解析  192.168.1.1/8
    如果ip 里有 “-”  则返回ParseIPC(ip)  192.168.1.1-192.168.255.255 192.168.1.1-255
    如果ip是能解析出ip的域名 则直接返回 [ip]  www.baidu.com
    否则 检查ip格式 是否有效  有效则返回 [ip]
    """
    if "/24" in ip or "/16" in ip or "/8" in ip:
        parts = ip.split(".")
        if len(parts) != 4:
            raise ParseIPErr()
        if "/24" in ip:
            ip = parts[0] + "." + parts[1] + "." + parts[2] + ".0/24"
        elif "/16" in ip:
            ip = parts[0] + "." + parts[1] + ".0.0/16"
        else:
            ip = parts[0] + ".0.0.0/8"
        AllIP = []
        ipObj = IPy.IP(ip)
        for per_ip in ipObj:
            AllIP.append(str(per_ip))
        return AllIP
    elif "-" in ip:
        IPRange = ip.split("-")
        if len(IPRange[1]) > 4:
            return gen_ip(ip)
        else:
            part4 = IPRange[0].split(".")[3]
            part4_start = int(part4)
            part4_end = int(IPRange[1])
            start = ip2num(IPRange[0])
            end = start + (part4_end - part4_start)
            return [num2ip(num) for num in range(start, end + 1) if num & 0xff]
    elif judge_legal_ip(ip):
        return [ip]
    else:
        if judge_legal_admin(ip):
            return [ip]


def ip2num(ip):
    ips = [int(x) for x in ip.split('.')]
    return ips[0] << 24 | ips[1] << 16 | ips[2] << 8 | ips[3]


def num2ip(num):
    return '%s.%s.%s.%s' % ((num >> 24) & 0xff, (num >> 16) & 0xff, (num >> 8) & 0xff, (num & 0xff))


def gen_ip(ip):
    start, end = [ip2num(x) for x in ip.split('-')]
    return [num2ip(num) for num in range(start, end + 1) if num & 0xff]


def get_ip_list(domain):  # 获取域名解析出的IP列表
    ip_list = []
    try:
        addrs = socket.getaddrinfo(domain, None)
        for item in addrs:
            if item[4][0] not in ip_list:
                ip_list.append(item[4][0])
    except Exception as e:
        print(str(e))
        raise ParseIPErr()
    return ip_list


def judge_legal_admin(domain):
    try:
        addrs = socket.getaddrinfo(domain, None)
    except Exception as e:
        print(str(e))
        raise ParseIPErr()
    return True


def judge_legal_ip(ip):
    compile_ip = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if compile_ip.match(ip):
        return True
    else:
        return False


def readIPFile(filename):
    content = []
    try:
        f = open(filename, mode='r')
        for line in f:
            text = line.strip()
            hosts = paraseIPs(text)
            content = content + hosts
    except:
        print("Open %s error\n" % filename)
        sys.exit(1)
    else:
        f.close()
    return content


if __name__ == "__main__":
    ret = parseIP("192.168.1.1-255", "", "192.168.1.1,192.168.1.2")
    print(len(ret))

    raise ParseIPErr()

