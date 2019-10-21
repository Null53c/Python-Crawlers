#-------------------------------------------------------------------------------
# Purpose: I was lying in bed and I knew in my heart, something was wrong.
# We never got the high definition images what is wrong with us.
#
# Author:      Olivier (Boschko) Laflamme
# Created:     20/10/2019
# Copyright:   (c) Olivier (Boschko) Laflamme 2019
#-------------------------------------------------------------------------------
from concurrent import futures
import requests
import os
from lxml import etree
from threading import *
from time import sleep

# Collected Common Header
my_headers = [
     " Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 " ,
     " Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 " ,
     " Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0 " ,
     " Mozilla/5.0 (Macintosh Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14 " ,
     " Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/ 6.0)" ,
     ' Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11 ' ,
     ' Opera/9.25 (Windows NT 5.1; U; en) ' ,
     ' Mozilla /4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727) ' ,
     ' Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu) ' ,
     ' Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12 ' ,
     ' Lynx/2.8.5rel .1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9 ',
     " Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7 " ,
     " Mozilla/5.0 (X11; Ubuntu; Linux i686; rv :10.0) Gecko/20100101 Firefox/10.0 "
]

url = 'https://www.85814.com/meinv/zhifumeinv/'
link_base ='https://www.85814.com/'


def main():
    url = 'https://www.85814.com/meinv/zhifumeinv/'
    link_base ='https://www.85814.com/'
    rootdirnames = url.split('/')[-2] + '/'
    if not os.path.exists(rootdirnames):    # root path, the path does not exist, then automatically creates OS requires Import
        os.makedirs(rootdirnames)
    #requesting master
    resp = requests.get(url, headers=headers,timeout=10,verify=False)
    html = etree.HTML(resp.text)
    #acquires the main page, the path into the personal portfolio
    Inner_Link = html.xpath('.//p[@id="l"]/a/@href')
    # Multi-threading, open 50, concurrent processing of 30 images in the main page download
    ex = futures.ThreadPoolExecutor(max_workers=30)
    num = 1         # used to name the path
    # 16 for each atlas
    for url_inner in Inner_Link:
        time.sleep(0.2)
        # spliced portfolio of a single URL
        url = link_base +url_inner
        dirname = '{}/{}/'.format(rootdirnames,str(num))
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        # multithreaded first argument is the name of the function After receiving the parameter list of the first incoming function, here is just submit thread
        ex.submit(download_pack, url, dirname)
        #download_pack(url, dirname)
        #download_pack(url, dirname) # single-thread mode, comment multi-threading, billing Threads can compare the speed of
        num = num + 1

def download_pack(url,dirname):
    #randomly select masquerading browser
    headers['User-Agent'] = random.choice(my_headers)
    cur_num = 2;
    while url:
        resp_Inner = requests.get(url, headers=headers,timeout=10,verify=False)
        if resp_Inner.status_code != 200:
            print("{} download over!".format(url.split('_')[0]))
            break
        html_Inner = etree.HTML(resp_Inner.text)
        src = html_Inner.xpath('.//dd[@class="p"]/p/img/@src')
        #requested image
        # the src obtained by xpath is a list, only takes a value 0 on the line
        img = requests.get(src[0], headers=headers, timeout=10, verify=False)
        #can see what src is.jpg followed by one! 800 removed here to get the file name
        filename = src[0].split('/')[-1].split('!')[0]
        print(filename)
        with open('{}/{}'.format(dirname,filename),'wb') as file:
            file.write(img.content)
        #The next url with cur_num to make "flip."
        if 2==cur_num:
            url =  "{}_{}.html".format(url.split('.html')[0],cur_num)
        else:
            url = "{}_{}.html".format(url.split('_')[0], cur_num)
        cur_num=cur_num+1








