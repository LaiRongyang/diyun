from common import config
from common import ParseIP
from Plugins import nmapScan
def Scan(info):
    print("start infoscan")
    Hosts = ParseIP.parseIP(info.Host,config.HostFile,config.NoHosts)
    # TODO 下面几行谁需要再翻译成python的代码吧
    # TODO  lib.Inithttp(common.Pocinfo)
    # TODO var ch = make(chan struct{}, common.Threads)
    # TODO var wg = sync.WaitGroup{}
    if len(Hosts)>0:
        if not config.IsPing:
            Hosts = nmapScan.hostDiscover(' '.join(Hosts))  # TODO Hosts = ICMPRun(Hosts,config.Ping)
            print("alive hosts len is:", len(Hosts)) # TODO print("icmp alive hosts len is:", len(Hosts))
        if info.Scantype == "icmp" :
            return
        AlivePorts= nmapScan.portScan(' '.join(Hosts), info.Ports) # TODO AlivePorts= nmapScan.portScan(' '.join(Hosts), ','.join(info.Ports), info.Timeout)
        print("alive ports len is:", len(AlivePorts))
        if info.Scantype == "portscan":
            return
        severports=[]
        for ser, port in config.PORTList:
            severports.append(str(port))
        print("start vulscan")
        for targetIP in AlivePorts:
            info.Host = targetIP.split(':')[0]
            info.Ports = targetIP.split(':')[1]
            if info.Scantype == "all":
                if info.Ports == '445':
                    return





def IsContain(items,item):
    if item in items :
        return True
    return False

if __name__ == "__main__":
    print("test")