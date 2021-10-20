#!/usr/bin/python
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import requests,sys
import threading,getopt
from threading import Semaphore
from urllib import parse
from bs4 import BeautifulSoup
from contextlib import closing
import datetime
nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
nowTime=str(nowTime).replace(' ','-').replace(':','-')
#from fake_useragent import UserAgent
#ua = UserAgent()
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
ThreadsNumber=5
inputfile='url.txt'
timeout=5

help="""轻量级Title批量获取器V1.1
-t      线程数         默认5个线程
-f      url文本文件    默认打开当前目录的url.txt

使用如下：
python3 webtitle.py -f url.txt -t 10  #从url中读取url进行批量访问，以10个线程。

"""



sem=Semaphore(ThreadsNumber)
lock=threading.Lock()
def UsRandom():
 return {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"}


def isfile(url):
    try:
        with closing(requests.get(url, stream=True,timeout=5)) as response:
            size=int(response.headers['content-length'])
            print(url,str(size)+' kb')
            return 0
    except Exception as e:
        print(e)
        pass
        return 1


reslist=[]
def GetTitle(url,sem):
    global timeout
    try:
        if 'http' not in  url:
            url='http://'+url
        print(url)
        if isfile(url)!= 0:
            sem.release()
            return 0
        req=requests.get(url=url,headers=UsRandom(),verify=False,timeout=3,stream=True)
        #lock.acquire()
        req.encoding=req.apparent_encoding
        datalen=len(req.text)
        suop = BeautifulSoup(req.text, 'html.parser')
        try:
            title=str(suop.title.text).strip()
        except Exception as e:
            title='title:Null'
        host=parse.urlparse(url).netloc
        #print('Url:'+url,'      Status: '+str(req.status_code),'      Title: '+title,'                 Ip: '+host)

        res={
            'URL': url,
            'Status':str(req.status_code),
            'Title':title,
            'Ip':host,
            'len':str(datalen)
        }
        print(res)
        '''
        lock.acquire()
        open('Result'+nowTime+'.txt','a',encoding='utf-8').write(str(res)+'\n')
        lock.release()
        '''

        #lock.release()
    except Exception as e:
        print(url,str(e))
    sem.release()




if __name__ == "__main__":
    sem.acquire()
    threading.Thread(target=GetTitle, args=("epo.cug.edu.cn", sem,)).start()

    print('task Complete******* ')

