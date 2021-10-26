from common import config
from common import ParseIP
from Plugins import nmapScan
from Plugins import  base
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
                    # //AddScan(info.Ports, info) //smb
                    AddScan("1000001", info)  # ms17010
                    AddScan("1000002", info)  # smbghost
                elif info.Ports == "9000":
                    AddScan(info.Ports, info)  # fcgiscan
                    AddScan("1000003", info)   # http
                elif info.Ports in severports:
                    AddScan(info.Ports, info)   # plugins scan
                else:
                    AddScan("1000003", info)   # webtitle
            else:
                port=config.PORTList[info.ScanType]
                scantype=str(port)
                AddScan(scantype ,info)
    if config.URL!= "":
        info.Url=config.URL
        AddScan("1000003",info)
    if len(config.Urls)>0:
        for url in config.Urls:
            info.Url=url
            AddScan("1000003",info)
    print("已完成 %v/%v".format( config.End, config.Num))


def AddScan(scantype , info):
    # TODO 多线程运行扫描函数
    ScanFunc(base.PluginList,scantype,info)


# scantype是端口
# TODO info 后面可拓展为可变参
def ScanFunc(PluginList, scantype, info):
    # 反射获取这个类型的函数，并调用
    try:
        import Plugins.redisScan
        m = __import__(PluginList[scantype][0], fromlist=True)
        f = getattr(m, PluginList[scantype][1], None)
        f(info)
    except Exception as e:
        print(e)
        print("插件调用错误")
    return


def IsContain(items,item):
    if item in items :
        return True
    return False


def test(port, info):
    try:
        import Plugins.redisScan
        m = __import__(base.PluginList[port][0], fromlist=True)
        f = getattr(m, base.PluginList[port][1], None)
        f(info)
    except Exception as e:
        print(e)
        print("插件调用错误")


if __name__ == "__main__":
    info=config.HostInfo()
    info.Host="172.27.236.199"
    info.Ports="6379"
    test("6379",info)