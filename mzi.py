#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import re
import time
import os

def method(headers, view):
    imgSrc = re.findall(r'<img class="blur" src="(.+)" alt=', view)
    if imgSrc:
        response = requests.get(imgSrc[0], headers = headers)
        name = imgSrc[0].split('/')[-1]
        try:
            with open(name, 'wb')as f:
                f.write(response.content)
                time.sleep(3)
        except:
            pass
    href = re.findall(r'<a href="(.+)" ><img', view)
    if href:
        if href[0].count('/') == 4:
            getImg(headers, href[0])
        
def getImg(headers, url):
    time.sleep(3)
    r = requests.get(url, headers = headers)
    html = r.text
    src = html.split('\n')
    for i in src:
        if i.strip()[:24] == '<div class="main-image">':
            view = i.strip()
            method(headers, view)
            break
    
def main():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
        "Referer": "https://www.mzitu.com/xinggan/"
        }
    url = input("url: ")
    
    folder = url.split('/')[-1]
    if not os.path.exists(folder):
        os.mkdir(folder)
    os.chdir(folder)
    getImg(headers, url)
    
if __name__=='__main__':                                       
    main()
