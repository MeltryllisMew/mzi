#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import datetime
import threading
import uiautomator2

'''
0.手机：USB调试，锁屏无，WiFi，GPS，中文，休眠30分钟
1.每五分钟获取当前时间进行判断
2.获取设备ID
3.多线程执行

'''

def test(strDevID):
    d = uiautomator2.connect(strDevID)

    if not d.info.get("ScreenOn"):
        d.screen_on()
    time.sleep(1)
    d.press("home")
    time.sleep(1)

    if not d.info.get("ScreenOn"):
        d.screen_on()
    time.sleep(1)
    d.press("home")
    time.sleep(1)
    
    d.app_start("com.tencent.mm")
    time.sleep(3)
    
    if d(text="请填写微信密码").wait(timeout=3):
        d(text="请填写微信密码").set_text("666")
        time.sleep(1)
        if d(text="登录").wait(timeout=3):
            d(text="登录").click()
            time.sleep(60)
    
    d.screen_on()
    time.sleep(1)
    
    d(text="通讯录").click()
    time.sleep(1)
    d(text="科技").click()
    time.sleep(1)
    d(text="打卡").click()
    time.sleep(30)
    d.press("back")
    time.sleep(2)
    d(text="打卡").click()
    time.sleep(2)

    print("要打卡了")
    x = d.window_size()[0]
    y = d.window_size()[1]
    for i in range(6, 18):
        d.click(0.5 * float(x), i/20 * float(y))
        time.sleep(2)
    time.sleep(5)

    for i in range(5):
        d.press("back")
    d.press("home")
    
    print("第二次")
    d.app_start("com.tencent.mm")
    time.sleep(3)
    if d(text="请填写微信密码").wait(timeout=3):
        d(text="请填写微信密码").set_text("666")
        time.sleep(1)
        if d(text="登录").wait(timeout=3):
            d(text="登录").click()
            time.sleep(60)
    
    d(text="通讯录").click()
    time.sleep(1)

    d(text="科技").click()
    time.sleep(1)
    d(text="打卡").click()
    time.sleep(30)
    d.press("back")
    time.sleep(2)
    d(text="打卡").click()
    time.sleep(2)

    x = d.window_size()[0]
    y = d.window_size()[1]
    for i in range(6, 18):
        d.click(0.5 * float(x), i/20 * float(y))
        time.sleep(2)
    time.sleep(5)
    
    for i in range(5):
        d.press("back")
    d.press("home")
       
def clock(t):
    work = datetime.datetime.strptime(t, "%Y-%m-%d %H:%M:%S")
    while True:
        now = datetime.datetime.now()
        result = (work - now).total_seconds()
        if result > 0:
            print("未到设定时间" + str(result))
            time.sleep(300)
        else:
            break

def main():
    print("锁屏无，初始化，中文，WiFi，GPS，休眠30分钟，USB调试")
    t = "2020-04-21 08:15:00"
    clock(t)
    os.system("python -m uiautomator2 init")
    
    
    r = os.popen("adb devices")
    text = r.read()
    temp = text.split()
    result = []
    for i in range(len(temp)):
        if temp[i] == "device":
            result.append(temp[i-1])
    for j in result:
        thread = threading.Thread(target = test, args = (j,))
        thread.start()
        print(j + "启动")
    

if __name__ == '__main__':
    main()
