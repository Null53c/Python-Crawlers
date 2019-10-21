#-------------------------------------------------------------------------------
# Purpose: finding the url of the picture to be crawled and then downloading
#
# Author:      Olivier (Boschko) Laflamme
# Created:     20/10/2019
# Copyright:   (c) Olivier (Boschko) Laflamme 2019
#-------------------------------------------------------------------------------
import requests
from lxml import etree

# We put it in a dictionary because the latter type requirement is a dictionary
# Then use the Request library to connect to the website.

headers = {
     ' Referer ' : ' https://www.85814.com/meinv/gaotiaomeinv/ ' ,
     ' User-Agent ' : ' ozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36 '
}

url = ' https://www.85814.com/meinv/gaotiaomeinv/ '
resp = requests.get(url,headers= headers)
pass

# Next we have to get the url of the image
# Below is a matching pattern, .//p[@id="l"] .//p will match all p tags under the current page.
# Here with the attribute id ="i" limit, find the main box, then double slash in p [@id="l"] matches
# all img below. Behind /@src is to get all the src which is the url

html = etree.HTML(resp.text)
srcs = html.xpath( ' .//p[@id="l"]//img/@src ' )

# The resulting srcs is a list. Just traverse this list and download the image for each url.

for src in srcs:
    time.sleep( 0.2 )
    filename = src.split( ' / ' )[-1 ]
    img = requests.get(src, headers=headers,timeout=10,verify= False)
    with open( ' imgs/ ' + filename, ' wb ' ) as file:
        file.write(img.content)