#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
import tkinter
import tkinter.filedialog

class ReadLog:
    def __init__(self, file):
        self.file = file
        self.flag = 0
        self.list_temp_crash = []
        self.list_temp_anr = []
        self.temp = ''
        self.d_crash = {}
        self.d_anr = {}
        self.pid = ''
        self.num = 0
        with open(self.file, encoding='charmap')as self.f:
            for i in self.f:
                self.line = i
                self.flag = self.read_log()
                print(self.num)
                self.num += 1
        with open('result.txt','a')as h:
            h.write("crash问题\n")
            for k, v in self.d_crash.items():
                print(k)
                q = k.split("_")
                if len(q) == 2:
                    h.write(q[0] + ' ' + q[1] + ' ' + str(v) + '\n')
                else:
                    h.write(k + ' ' + str(v) + '\n')
            h.write("\nanr问题\n")
            for k, v in self.d_anr.items():
                h.write(k + ' ' + str(v) + '\n')

    def read_log(self):
        # 初始状态
        if self.flag == 0:
            if re.findall(r"FATAL EXCEPTION:", self.line.strip()):
                self.list_temp_crash.append(self.line)
                self.flag = 1
                return self.flag
            elif re.findall(r"E/ActivityManager(.+): ANR in (.+)\n", self.line):
                process_anr = re.findall(r'ANR in (.+)\n', self.line)
                if process_anr[0] not in self.d_anr:
                    self.d_anr[process_anr[0]] = 1
                    self.list_temp_anr.append(self.line)
                    pid = re.findall(r"E/ActivityManager(.+?):", self.line)
                    self.pid = pid[0]
                    self.flag = 3
                    return self.flag
                else:
                    self.d_anr[process_anr[0]] += 1
                    return self.flag
            else:
                return self.flag
                
        # 识别到Crash标志，获取进程
        elif self.flag == 1:
            process_crash = re.findall(r"Process: (.+), PID", self.line)
            if process_crash:
                self.list_temp_crash.append(self.line)
                self.temp = process_crash[0]
                self.flag = 2
                return self.flag
            else:
                self.flag = 0
                self.list_temp_crash = []
                return self.flag

        # 获取错误类型和PID
        elif self.flag == 2:
            # 可能会没有错误类型
            exception_crash = re.findall(r': (.+?):', self.line)
            if exception_crash:
                self.temp = self.temp + '_' + exception_crash[0]
            print(self.temp)
            # 获取PID作为后续判断条件
            if self.temp not in self.d_crash:
                self.d_crash[self.temp] = 1
                self.list_temp_crash.append(self.line)
                pid = re.findall(r'E/AndroidRuntime(\(\d+\)|\(\s+\d+\)):', self.line)
                if pid:
                    self.pid = pid[0]
                    self.flag = 5
                    return self.flag
            else:
                self.d_crash[self.temp] += 1
                self.flag = 0
                self.list_temp_crash = []
                return self.flag
        
        # 识别到anr标志，加入anr临时列表，获取PID
        elif self.flag == 3:
            pid_temp = re.findall(r"(\(.+?\)):", self.line)
            if pid_temp:
                if pid_temp[0] == self.pid:
                    self.list_temp_anr.append(self.line)
                    return self.flag
                else:
                    with open("result_anr.txt", 'a')as g:
                        for i in self.list_temp_anr:
                            g.write(i)
                        g.write('\n===================\n\n')
                    self.list_temp_anr = []
                    self.flag = 0
                    return self.flag
            else:
                with open("result_anr.txt", 'a')as g:
                    for i in self.list_temp_anr:
                        g.write(i)
                    g.write('\n===================\n\n')
                self.list_temp_anr = []
                self.flag = 0
                return self.flag

        # 以PID作为判断条件获取完整的crash信息
        elif self.flag == 5:
            pid_temp = re.findall(r'(\(.+?\)):', self.line)
            if pid_temp:
                if pid_temp[0] == self.pid:
                    self.list_temp_crash.append(self.line)
                    return self.flag
                else:
                    with open('result_crash.txt', 'a')as g:
                        for i in self.list_temp_crash:
                           g.write(i)
                        g.write('\n===================\n\n')
                    self.list_temp_crash = []
                    self.flag = 0
                    self.flag = self.read_log()
                    return self.flag
            else:
                with open('result_crash.txt', 'a')as g:
                    for i in self.list_temp_crash:
                        g.write(i)
                    g.write('\n===================\n\n')
                self.list_temp_crash = []
                self.flag = 0
                return self.flag

def selectPath():
    path = tkinter.filedialog.askdirectory()
    for i in os.listdir(path):
        if i == 'logcat.log':
            ReadLog(os.path.join(path, i))
        
def main():
    window = tkinter.Tk()
    window.title('monkey_log')
    window.geometry('400x300')
    tkinter.Label(window,text='选择包含有logcat的文件夹', font=('宋体', 14)).pack(padx=5,pady=45)
    tkinter.Button(window, command = selectPath, text='选择文件夹', font=('宋体', 16), width=15, height=10).pack(padx=50,pady=60)
    window.mainloop()

if __name__ == '__main__':
    main()
