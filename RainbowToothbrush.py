#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import re
import time

def method(headers, url):
    try:
        r = requests.get(url, headers = headers)
        r.raise_for_status()
        #r.encoding = r.apparent_encoding
        r.encoding = "utf-8"
        return r.text
    except:
        print("Fail")
        return 

def get_note(text):
    note_list = []
    html = text.split("\n")
    for i in range(len(html)):
        if html[i].strip() == '<div class="source">':
            link = re.findall(r'<a href=\"(.+)\" t', html[i+4])
            if link:
                note_list.append(link[0])
    return note_list

def get_text(text):
    txt = []
    html = text.split("\n")
    for i in range(len(html)):
        if html[i].strip() == "<title>":
            txt.append(html[i+1].strip())
        elif html[i].strip()[:18] == '<div class="note">':
            temp = html[i].strip().replace("らいち", "荔枝")
            txt.extend(temp.split("<br>"))
        else:
            continue
    return txt

def write(txt):
    with open("RainbowToothbrush.txt", "a+", encoding="utf-8")as f:
        for i in txt:
            try:
                j = i.replace('<div class="note">', '')
                k = j.replace("</div>", "")
                f.write(k + "\n")
            except Exception as e:
                print(i)
                print(e)
        f.write("\n")
    return

def main():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
    }
    #doulist = ""
    doulist_text = method(headers, doulist)
    note_list = get_note(doulist_text)
    for i in note_list:
        note_text = method(headers, i)
        txt = get_text(note_text)
        write(txt)
        time.sleep(5)

if __name__ == '__main__':
    main()
