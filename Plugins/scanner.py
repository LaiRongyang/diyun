from common import config
from common import ParseIP
from Plugins import nmapScan
def Scan(info):
    print("start infoscan")
    Hosts = ParseIP.parseIP(info.Host,config.HostFile,config.NoHosts)
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


def IsContain(items,item):
    if item in items :
        return True
    return False

if __name__ == "__main__":
    print("test")