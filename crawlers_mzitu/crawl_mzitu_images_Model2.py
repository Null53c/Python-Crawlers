import requests
from lxml import etree
import os


def a ():
    url = 'http://www.mzitu.com/page/1/'
    response = requests.get(url)

    # with open('mzitu.html' , 'wb' ) as f :
    #     f.write(response.content)
    html_ele = etree.HTML(response.text)
    # li_ele_list = html_ele.xpath('//ul[@id="pins"]/li/a/@href')
    # print(li_ele_list)
    max_list = html_ele.xpath('//nav[@class="navigation pagination"]/div/a/text()')[3]
    # print(max_list)
    for i in range(1,int(max_list)+1):
        z_url = 'http://www.mzitu.com/page/{}/'.format(i)
        # print(z_url)
        response = requests.get(z_url)
        html_ele = etree.HTML(response.text)
        li_ele_list = html_ele.xpath('//ul[@id="pins"]/li')
        for href_ele in li_ele_list:
            href_url = href_ele.xpath('./a/@href')[0]
            print(href_url)
            name = href_ele.xpath('./span/a/text()')[0]
            print(name)
            b(href_url, name)
        # break



def b(href_url,name):
    if not os.path.exists('meizitu/'+name):
        os.makedirs('meizitu/'+name)
    headers = {
    'Referer': str(href_url),
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',

    }
    # print(headers)
    response = requests.get(href_url,headers=headers)
    html_ele = etree.HTML(response.text)
    # print(html_ele)
    xq_max_list = html_ele.xpath('//div[@class="pagenavi"]/a')[-2]
    # print(xq_max_list)
    max_list = xq_max_list.xpath('./span/text()')[0]
    # print(max_list)
    for i in range(1,int(max_list)):
        xq_url = str(href_url)+'/'+str(i)
        print(xq_url)
        response = requests.get(xq_url,headers = headers)
        html_ele = etree.HTML(response.text)
        src_page = html_ele.xpath('//div[@class="main-image"]/p/a/img/@src')
        src_page = src_page[0]

        print(src_page)
        tname = src_page.split('/')[-1]
        print(tname)
        response = requests.get(src_page, headers=headers)
        with open( 'meizitu/'+name+'/'+tname,'wb' ) as f:
            f.write(response.content)
if __name__ == '__main__':
    a()

