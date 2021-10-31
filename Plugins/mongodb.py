import pymongo
from common import log

def MongodbScan(info):
    MongodbUnauth(info)



def MongodbUnauth(info):
    try:
        conn = pymongo.MongoClient(info.Host, info.Ports, socketTimeoutMS=4000)
        dbname = conn.list_database_names()
        result = "[+] Mongodb:{} unauthorized".format(info.Host+":"+info.Ports)
        conn.close()
        log.LogSuccess(result)
    except Exception as e:
        result = "[-] Mongodb {}:{} {}".format(info.Host, info.Ports, e.__str__())
        log.LogError(result)


'''
def  MongodbUnauth_GO(info):
    flag = False
    senddata =bytes([58, 0, 0, 0, 167, 65, 0, 0, 0, 0, 0, 0, 212, 7, 0, 0, 0, 0, 0, 0, 97, 100, 109, 105, 110, 46, 36, 99,
                109, 100, 0,
                0, 0, 0, 0, 255, 255, 255, 255, 19, 0, 0, 0, 16, 105, 115, 109, 97, 115, 116, 101, 114, 0, 1, 0, 0, 0,
                0])

    getlogdata =bytes([72, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 212, 7, 0, 0, 0, 0, 0, 0, 97, 100, 109, 105, 110, 46, 36, 99,
                  109, 100, 0, 0,
                  0, 0, 0, 1, 0, 0, 0, 33, 0, 0, 0, 2, 103, 101, 116, 76, 111, 103, 0, 16, 0, 0, 0, 115, 116, 97, 114,
                  116, 117, 112,
                  87, 97, 114, 110, 105, 110, 103, 115, 0, 0])

    realhost="{}:{}".format(info.Host, info.Ports)
    try:
        conn = pymongo.MongoClient(info.Host, info.Ports, socketTimeoutMS=4000)
        #以tcp的方式连接realhost ，设置超时info.Timeout
        # 设置 read操作的期限是now+info.Timeout
        # conn.Write(senddata)
        buf =bytes(1024)
        # count=conn.Read(buf)
        text=bytesToStr(buf[0:count])
        if "totalLinesWritten" in text:
            flag=true
            result = "[+] Mongodb:{} unauthorized".format(realhost)
            # TODO .LogSuccess(result)
            print(result)
    finally:
        # 关闭连接
        return  flag
        
'''