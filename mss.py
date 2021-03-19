#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import re
import time
import os

def getImg(url, headers):
    response = requests.get(url, headers = headers)
    name = url.split("/")[-1]
    with open(name, "wb")as f:
        f.write(response.content)
        time.sleep(3)

def getUrl(url, headers):
    r = requests.get(url, headers = headers)
    html = r.text
    src = html.split("\n")
    for i in src:
        if i.strip()[:18] == "<div class='page'>":
            jpg = re.findall(r"img src=\"(.+?)\" alt", i)
            if jpg:
                getImg(jpg[0], headers)
            break

def getHtml(url, headers):
    r = requests.get(url, headers = headers)
    html = r.text
    src = html.split("\n")
    for i in src:
        if i.strip()[:18] == "<div class='page'>":
            list_html = re.findall(r"a href='(.+?)'>", i.strip())
            if list_html:
                print(url)
                getUrl(url, headers)
                for j in list_html:
                    new = "/".join(url.split("/")[:-1]) + "/" + j
                    print(new)
                    getUrl(new, headers)
            break

def getName(url, headers):
    r = requests.get(url, headers = headers)
    r.encoding = 'gbk'
    html = r.text
    src = html.split("\n")
    path = os.getcwd()
    for i in src:
        if i.strip()[:15] == '<div id="list">':
            list_title = re.findall(r"<a href='(.+?)' title", i)
            if list_title:
                for j in list_title:
                    temp = "/".join((j.split("/")[-4:]))
                    folder = j.split("/")[-1][:-5]
                    if not os.path.exists(folder):
                        os.mkdir(folder)
                        os.chdir(folder)
                    else:
                        continue
                    getHtml("" + temp, headers)
                    os.chdir(path)
            break
            
def main():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"}
    list_url = ["",
                ""]
    for url in list_url:
        getName(url, headers)


if __name__=='__main__':                                       
    main()
