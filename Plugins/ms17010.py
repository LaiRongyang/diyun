import socket
import binascii
from common import config
from common import log


# user='172.27.176.243'
def MS17010(info):
    try:
        scan(info.Host, info.Timeout)
    except Exception as e:
        result = "[-] Ms17010 {} {}" .format(info.Host, e.__str__())
        log.LogError(result)


def scan(host ,timeout):
    payload0 = binascii.unhexlify ('00000085ff534d4272000000001853c00000000000000000000000000000fffe00004000006200025043204e4554574f524b2050524f4752414d20312e3000024c414e4d414e312e30000257696e646f777320666f7220576f726b67726f75707320332e316100024c4d312e325830303200024c414e4d414e322e3100024e54204c4d20302e313200')
    payload1 = binascii.unhexlify('00000088ff534d4273000000001807c00000000000000000000000000000fffe000040000dff00880004110a000000000000000100000000000000d40000004b000000000000570069006e0064006f007700730020003200300030003000200032003100390035000000570069006e0064006f007700730020003200300030003000200035002e0030000000')
    payload2 = binascii.unhexlify('00000060ff534d4275000000001807c00000000000000000000000000000fffe0008400004ff006000080001003500005c005c003100390032002e003100360038002e003100370035002e003100320038005c00490050004300240000003f3f3f3f3f00')
    payload3 = binascii.unhexlify('0000004eff534d4232000000001807c00000000000000000000000000008fffe000841000f0c0000000100000000000000a6d9a40000000c00420000004e0001000e000d0000000000000000000000000000')
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout(timeout)
    port=445

    s.connect((host,port))

    #print('[+]{}Ready to send'.format(host))
    s.send(payload0)
    s.recv(1024)

    #print('[+]{}Setting request'.format(host))
    s.send(payload1)
    session_setup_response=s.recv(1024)

    user_id=session_setup_response[32:34]
    #print(host,'User ID=%s'%struct.unpack('<H',user_id)[0])

    modified_tree_connect_request=list(payload2)
    modified_tree_connect_request[32]=user_id[0]
    modified_tree_connect_request[33]=user_id[1]
    modified_tree_connect_request= "".join(modified_tree_connect_request)

    #print('[+]{}Send connection'.format(host))
    s.send(modified_tree_connect_request)
    tree_connect_response=s.recv(1024)

    tree_id=tree_connect_response[28:30]
    #print('[+]{}'.format(host),'Tree ID=%s'%struct.unpack('<H',tree_id)[0])

    modified_trans2_session_setup=list(payload3)
    modified_trans2_session_setup[28]=tree_id[0]
    modified_trans2_session_setup[29]=tree_id[1]
    modified_trans2_session_setup[32]=user_id[0]
    modified_trans2_session_setup[33]=user_id[1]
    modified_trans2_session_setup="".join(modified_trans2_session_setup)

    #print('[+]{}Sending success is actually returning.'.format(host))
    s.send(modified_trans2_session_setup)
    final_respone=s.recv(1024)

    s.close()

    if final_respone[34]=="\x51":
        result='[*] {} existence MS17-010'.format(host)
        log.LogSuccess(result)



if __name__ == "__main__" :
    info=config.HostInfo()
    info.Host="172.27.176.243"
    MS17010(info)