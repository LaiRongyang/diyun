import socket


def MemcachedScan(info):
    try:
        socket.setdefaulttimeout(5)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((info.Host,  info.Ports))
        s.send(bytes('stats\r\n', 'UTF-8'))
        if 'version' in s.recv(1024).decode():
            result="[+] Memcached {} unauthorized".format(info.Host+":"+info.Ports)
            print(result)
            # TODO LogSuccess
        s.close()
    except Exception as e:
        errlog="[-] Memcached {}:{} {}".format(info.Host, info.Ports, e.__str__())
        print(errlog)
        pass