"""
这个模块用于实现 主机发现(H)+操作系统侦测(O)+端口扫描(P)+服务版本侦测(S)
使用nmap包来实现功能
（原go版的一些代码就不需要抄了，比如Plugins/icmp.go ）
"""

import nmap
import json


# host 之间用空格隔开172.27.236.16 172.27.236.18
# TODO 用ICMP
def hostDiscover(Hosts, IsPing=True):
    aliveHosts = []
    nm = nmap.PortScanner()
    result = 0
    if IsPing:
        result = nm.scan(hosts=Hosts, arguments='-n -sP ')
    else:
        result = nm.scan(hosts=Hosts, arguments='-n -PE ')

    # print(json.dumps(result, sort_keys=False, indent=4))
    # print(result['scan'].keys())
    for host in result['scan'].keys():
        if result['scan'][host]['status']['state'] == 'up':
            aliveHosts.append(host)
            print("({}) Target '{}' is alive".format(result['scan'][host]['status']['reason'], host))
    return aliveHosts


# hostDiscover("172.27.236.16 172.27.236.18")


# TODO 这里不知道除了TCP还会不会有其他的协议来扫描端口
# Hosts格式 '172.27.73.80,172.27.73.81,172.27.73.82'
# Ports格式 ‘21,22,80,81,135,139,443'
def portScan(Hosts, Ports="20-27017", IsServeVersion=False, IsOS=False):
    openPorts = []  # 元素格式 host:port
    nm = nmap.PortScanner()
    args = ""
    if IsServeVersion:
        args += " -sV –version-light "
    if IsOS:
        args += " -O"
    result = nm.scan(hosts=Hosts, ports=Ports, arguments=args)

    # print(json.dumps(result, sort_keys=False, indent=4))
    for host in result['scan'].keys():
        if result['scan'][host]['status']['state'] == 'up':
            hostInfo = result['scan'][host]
            if 'tcp' in hostInfo.keys():
                # print(json.dumps(hostInfo['tcp'], sort_keys=False, indent=4))
                for port in hostInfo['tcp'].keys():
                    if hostInfo['tcp'][port]['state'] == 'open':
                        print("{}:{} open".format(host, port))
                        openPorts.append(host + ":" + str(port))

    return openPorts
# portScan("172.27.73.80")


if __name__ == "__main__":
    hostDiscover("172.27.236.16 172.27.236.18")
    portScan("172.27.73.80")
