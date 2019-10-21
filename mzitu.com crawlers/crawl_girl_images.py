#-------------------------------------------------------------------------------
# Purpose/Question: Crawling Asian Girl Images
#
# Mention: Crawl more girl images. I have no shame.
#
# Author:      Olivier Laflamme
#
# Created:     11-07-2019
# Copyright:   (c) Boschko 2019
# Licence:     MIT
#-------------------------------------------------------------------------------
import requests
import re

# Grabbing
url = ('http://www.meizitu.com/a/sexy_1.html')
Response = requests.get(url)
return response

#analysis
p = r'<img src="([^"]+\.jpg)"'
Img_addrs = re.findall(p, html)

# storeage
with open(filename,'wb') as f:
    img = url_open(each).content
    f.write(img)