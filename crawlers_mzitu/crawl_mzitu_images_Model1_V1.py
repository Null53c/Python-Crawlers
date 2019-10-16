#-------------------------------------------------------------------------------
# Purpose/Question: Creepy chinese girl image grabber/crawler
# All the information is stores inside the <li> tags
#
#
# Author:      Olivier Laflamme
#
# Created:     16-10-2019
# Copyright:   (c) Boschko 2019
# Licence:     MIT
#-------------------------------------------------------------------------------
# encoding = utf-8
import concurrent
import os
from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup

# Loop to get the contents of each page with bs4 and put it into the url
# this gets the url of every 'poster' on the page
def get_page_urls():
    for i in range(1,230):
        baseurl = 'https://www.mzitu.com/page/{}'.format(i)
        html = request_page(baseurl)
        soup = BeautifulSoup(html, 'lxml')
        list = soup.find(class_='postlist').find_all('li')
        urls=  []
        for item in list:
            url =item.find('span').find('a').get('href')
            urls.append(url)
    return urls

# get pictures in groups with the image address and get the total
# number of pages and title of the groups
def download(url):
    html = request_page(url)
    soup = BeautifulSoup(html, 'lxml')
    total = soup.find(class_='pagenavi').find_all('a')[-2].find('span').string
    title = soup.find('h2').string
    image_list = []
    for i in range(int(total)):
        html = request_page(url + '/%s' % (i + 1))
        soup = BeautifulSoup(html, 'lxml')
        img_url = soup.find('img').get('src')
        image_list.append(img_url)
    download_Pic(title, image_list)
    # traverse the obtained list
    for url in list_page_urls:
        download(url)

# start downloading the images
def download_Pic(title, image_list):
    # new folder
    os.mkdir(title)
    j = 1
    # download image
    for item in image_list:
        filename = '%s/%s.jpg' % (title,str(j))
        print('downloading....%s : NO.%s' % (title,str(j)))
        with open(filename, 'wb') as f:
            img = requests.get(item,headers=header(item)).content
            f.write(img)
        j+=1

# open multithreading

def download_all_images(list_page_urls):
    # Scrap everything
    works = len(list_page_urls)
    with concurrent.futures.ThreadPoolExecutor(works) as exector:
        for url in list_page_urls:
            exector.submit(download,url)