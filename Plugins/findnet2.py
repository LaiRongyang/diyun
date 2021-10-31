import binascii
import socket
from common import log
bufferV1 = bytes.fromhex("05000b03100000004800000001000000b810b810000000000100000000000100c4fefc9960521b10bbcb00aa0021347a00000000045d888aeb1cc9119fe808002b10486002000000")
bufferV2 = bytes.fromhex("050000031000000018000000010000000000000000000500")
bufferV3 = bytes.fromhex("0900ffff0000")
# bufferV3 len=6
BUFSIZ=65535

def Findnet(info):
    FindnetScan(info)


def FindnetScan(info):
    realhost = "{}:{}".format(info.Host, 135)
    try:
        socket.setdefaulttimeout(info.Timeout)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((info.Host, 135))
        s.send(bufferV1)
        reply = s.recv(BUFSIZ).decode()
        s.send(bufferV2)
        reply = s.recv(BUFSIZ)
        if len(reply)<42:
            return
        text = reply[42:]
        flag = True
        for i in range(len(text)-5):
            if text[i:i+6] == bufferV3 :
                text = text[:i-4]
                flag =False
                break
        if flag:
            return
        read(text)
        # 关闭连接
    except Exception as e:
        print(e)
    return

# test
# src =bytes("hello",'utf-8')
# print(str(binascii.b2a_hex(src)))

# text是字节数组 host 是str
def read(text,host):
    try:
        encodedStr = str(binascii.b2a_hex(text)) # 如果text是 b'h'  encodedStr 是用字符串展示16进制形式 ‘68’
        hostnames = encodedStr.replace("0700", "")
        hostname=hostnames.split("000000")
        result = "NetInfo:\n[*]" + host
        for i in range(len(hostname)):
            hostname[i]=hostname[i].replace("00", "")
            host = bytes.fromhex(hostname[i]) # hostname[i] 是 用一个字节存储十六进制的值（一个十六进制的值是 xx的形式）
            result += "\n   [->]" + str(host)
        log.LogSuccess(result)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    realhost = "{}:{}".format("info.Host", 135)
    print(realhost)
    if b'\t\x00\xff\xff\x00\x00' == bufferV3:
        print("dad")
    print(bufferV3)
