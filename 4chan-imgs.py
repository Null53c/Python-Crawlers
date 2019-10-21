#!/usr/bin/python

import os, json, urllib2

CDN_LINK    =   "http://i.4cdn.org/b/"
THREAD_LINK =   "http://a.4cdn.org/b/thread/"

threadId = input("Thread Number: ")
threadLink = THREAD_LINK + str(threadId) + ".json"

req = urllib2.urlopen(threadLink)
threadData = json.loads(req.read())

if not os.path.exists(str(threadId)):
    os.makedirs(str(threadId))

fileLoc = None
fileName = None
contentLink = None
for post in threadData["posts"]:
    if "filename" in post:
        fileName = str(post["tim"]) + post["ext"]
       
        print("Downloading: %s" % fileName)
       
        contentLink = CDN_LINK + fileName
       
        req = urllib2.urlopen(contentLink)
       
        fileLoc = str(threadId) + "/" + fileName

        img = open(fileLoc, "wb");
        img.write(req.read())
        img.close()
