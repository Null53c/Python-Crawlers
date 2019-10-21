# -*- coding: utf-8 -*-
import requests
import os
from lxml import etree
from threading import *
from time import sleep

nMaxThread = 3  #This setting requires several threads to be opened
ThreadLock = BoundedSemaphore(nMaxThread)

gHeads = {
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
}

class Meizitu(Thread):
    def __init__(self,mainReferer,url,title):
        Thread.__init__(self)
        self.MainReferer = mainReferer
        self.url = url  #The url here needs to be used in subsequent referer s
        self.title = title

    def run(self):
        try:
            PhotoUrl,Page = self.GetPhotoUrlAndPageNum()
            if PhotoUrl and Page > 0:
                self.SavePhoto(PhotoUrl,Page)
        finally:
            ThreadLock.release()

    def GetPhotoUrlAndPageNum(self):
        html = requests.get(self.url,headers=gHeads)
        if html.status_code == 200:
            xmlContent = etree.HTML(html.text)
            PhotoUrl = xmlContent.xpath("//Div[@class='main-image']/p/a/img/@src') [0][: -6] #01.jpg happens to be-6")
            PageNum = xmlContent.xpath("//div[@class='pagenavi']/a[5]/span/text()")[0]
            return PhotoUrl,int(PageNum)
        else:
            return None,None

    def SavePhoto(self,url,page):
        savePath = "./photo/%s" % self.title
        if not os.path.exists(savePath):
            os.makedirs(savePath)
        for i in range(page):
            heads = {
                "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
                "Referer": "%s/%d" %(self.url,i+1),
                "Accept": "image/webp,image/apng,image/*,*/*;q=0.8"
            }
            j = 0
            while j<5:
                print (u"Download : %s/%d.jpg" % (self.title, i + 1))
                html = requests.get("%s%02d.jpg"%(url,i+1),headers=heads)
                if html.status_code == 200:
                    with open(savePath + "/%d.jpg"%(i+1),"wb") as f:
                        f.write(html.content)
                    break
                elif html.status_code == 404:
                    j+=1
                    sleep(0.05)
                    continue
                else:
                    return None


def main():
    while True:
        try:
            nNum = int(raw_input(u"Please enter a few pages to download: "))
            if nNum>0:
                break
        except ValueError:
            print(u"Please enter a number.")
            continue
    for i in range(nNum):
        url = "https://www.mzitu.com/xinggan/page/%d/"%(i+1)
        html = requests.get(url,headers=gHeads)
        if html.status_code == 200:
            xmlContent = etree.HTML(html.content)
            hrefList = xmlContent.xpath("//ul[@id='pins']/li/a/@href")
            titleList = xmlContent.xpath("//ul[@id='pins']/li/a/img/@alt")
            for i in range(len(hrefList)):
                ThreadLock.acquire()
                t = Meizitu(url,hrefList[i],titleList[i])
                t.start()


if __name__ == '__main__':
    main()