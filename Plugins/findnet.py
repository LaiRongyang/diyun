# -*- coding: utf-8 -*-

import os
import threading
import argparse


# 从网关获取所有IP，如192.168.1.1-255，返回一个list存储
def get_all_ip(gateway):
    ip = list()
    # 改进，支持指定范围IP

    ip_prefix = gateway.split('.')

    # 对输入的gateway进行判断
    # 第一种输入192.168.1.1-255
    if '-' in gateway:
        parts = ip_prefix[3].split('-')
        start = int(parts[0])
        end = int(parts[1])
        prefix = ip_prefix[0] + '.' + ip_prefix[1] + '.' + ip_prefix[2] + '.'
        for i in range(start, end):
            ip.append(prefix + str(i))
    # 第二种只输入一个ip
    else:
        ip_prefix = ip_prefix[0] + '.' + ip_prefix[1] + '.' + ip_prefix[2] + '.'
        for i in range(255):
            ip.append(ip_prefix + str(i))

    # 返回一个包含所有IP的list
    return ip


def ping(ip):
    # 执行系统命令以一个管道返回
    output = os.popen('ping -n 2 %s' % ip)
    result = output.read().encode('utf-8')
    # 返回命令执行结果
    # print result
    # 根据返回结果当中是否包含关键词TTL 进行判断
    if 'TTL' in result:
        print('[-] ' + ip + '\tis up')


def main(ip):
    # 采用多线程，创建一个线程池
    threads = []
    ips = get_all_ip(ip)
    for ip in ips:
        # 加入线程
        t = threading.Thread(target=ping, args=(ip,))
        threads.append(t)
    print('[+] Scaning start')
    for i in threads:
        i.start()
    for i in threads:
        t.join()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='This a script to scan the LAN')
    parser.add_argument('ip', default='192.168.1.1', help='Eg:  192.168.1.1 or 192.168.1.1-33')
    args = parser.parse_args()
    main(args.ip)
    print("test")
