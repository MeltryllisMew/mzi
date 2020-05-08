#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import datetime
import tkinter
import tkinter.filedialog

def findFile(path):
    #path = r'D:\log'
    upcoming = []
    yesterdayTest = []
    today = datetime.datetime.now().strftime("%Y-%m-%d")                         
    for root, dirs, files in os.walk(path):                          
        for i in files:                                   
            if i[-25:] == "_dumpsys_batterystats.log":                           
                upcoming.append(os.path.join(root, i))
                if i[:10] == today:
                    yesterdayTest.append(os.path.join(root, i))
    return upcoming, yesterdayTest

def strToTime(end):
    a = end.index('h')
    b = end.index('m')
    seconds = int(end[:a]) * 3600 + int(end[a+1:b]) * 60 + int(end[b+1:-1])
    return seconds

def readLog(file):
    with open(file, encoding='utf-8')as f:
        raw = f.readlines()
    for i in range(len(raw)):
        if re.search(r"RESET:TIME:", raw[i]):
            startTime = (datetime.datetime.strptime(raw[i][-20:-1], "%Y-%m-%d-%H-%M-%S")).strftime("%Y-%m-%d %H:%M:%S")
            
            print("开始时间：" + startTime)
            startBattery = re.findall(r' (\d{3}) ', raw[i+1])[0]
            print("初始电量：" + startBattery)
        elif re.search(r'Per-PID Stats:', raw[i]):
            #end = re.findall(r'\d+h\d+m\d+s', raw[i-2])[0]
            endBattery = re.findall(r' (\d{3}) ', raw[i-2])[0]
            if endBattery == '001':
                endBattery = '000'
            #usedSeconds = strToTime(end)
            #stats = strToTime(end) / 3600
            #print("耗电时长：" + str(stats))
            print("剩余电量：" + endBattery)
            break                               

    '''
    写完才发现文件名就是结束时间，不用算…
    begin_hour = datetime.datetime.strptime(startTime, "%Y-%m-%d-%H-%M-%S")
    end_hour = (begin_hour + datetime.timedelta(seconds = usedSeconds)).strftime("%Y-%m-%d %H:%M:%S")
    print("结束时间：" + end_hour)
    '''
    
    endTime = (datetime.datetime.strptime(os.path.split(file)[-1][:19].replace('_', '-'), "%Y-%m-%d-%H-%M-%S")).strftime("%Y-%m-%d %H:%M:%S")
    
    begin_hour = datetime.datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S")
    end_hour = datetime.datetime.strptime(os.path.split(file)[-1][:19].replace('_', '-'), "%Y-%m-%d-%H-%M-%S")
    usedSeconds_2 = (end_hour - begin_hour).total_seconds()
    stats_2 = usedSeconds_2 / 3600
    print("耗电时长：" + str(stats_2))
    
    print("结束时间：" + endTime)
    
    standardBattery = stats_2 * 20
    print("标准耗电量：" + str(standardBattery))
    used = int(startBattery) - int(endBattery)
    usedBattery = used * 3300 / 100
    print("实际耗电量：" + str(usedBattery))

    version = ''
    try:
        v = '//'.join(os.path.split(file)[0:-1]) + '//versionNumber'
        with open(v)as h:
            text = h.read()
        version = text.split('_')[0]
    except:
        pass
    
    with open('out.txt', 'a', encoding='utf-8')as g:
        g.write(os.path.split(file)[-1][:16].replace('_', '-') + ' ' + version + '\n')
        g.write("开始时间：" + startTime + '\n')
        g.write("结束时间：" + endTime + '\n')
        g.write("耗电时长：" + str(stats_2) + '\n')
        
        g.write("初始电量：" + startBattery + '\n')
        g.write("剩余电量：" + endBattery + '\n')
        g.write("耗费电量：" + str(used) + '\n')
        
        g.write("实际耗电：" + str(usedBattery) + '\n')
        g.write("标准耗电：" + str(standardBattery) + '\n\n')
        g.write("=====================\n\n")
        
def selectPath():
    path = tkinter.filedialog.askdirectory()
    upcoming, yesterdayTest = findFile(path)
    with open('out.txt', 'w')as f:
        pass
    for i in upcoming:
        readLog(i)
    '''
    print("BatteryLog总计%d个\n其中日期今天的%d个\n\n直接回车计算日期为今天的log\n输入任意字符回车计算全部log" % (len(upcoming), len(yesterdayTest)))
    temp = input()
    if temp:
        for i in upcoming:
            readLog(i)
    else:
        for j in yesterdayTest:
            readLog(j)
    '''
    if upcoming:
        os.startfile('out.txt')
    #input('退出')

def main():
    window = tkinter.Tk()
    window.title('BatteryLog')
    window.geometry('300x200')
    tkinter.Label(window,text='计算该文件夹内的BatteryLog', font=('宋体', 14)).pack(padx=5,pady=25)
    tkinter.Button(window, command = selectPath, text='选择文件夹', font=('宋体', 16), width=15, height=10).pack(padx=20,pady=30)
    window.mainloop()
    
if __name__=='__main__':                                       
    main()
