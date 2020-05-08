

import subprocess
import threading
import time
import re
import os

'''
1.下划线分割字符串，未改 line38
2.连续有两个crash或anr，第二个不识别 line108
'''

class ReadLog:
    def __init__(self, file):
        self.file = file
        self.path = os.path.split(os.path.split(self.file)[0])[0]
        self.result = os.path.join(self.path, 'result.txt')
        self.result_crash = os.path.join(self.path, 'result_crash.txt')
        self.result_anr = os.path.join(self.path, 'result_anr.txt')
        self.flag = 0
        self.list_temp_crash = []
        self.list_temp_anr = []
        self.temp = ''
        self.d_crash = {}
        self.d_anr = {}
        self.pid = ''
        self.num = 0
        print(self.file, '分析开始')
        with open(self.file, encoding='charmap')as self.f:
            for i in self.f:
                self.line = i
                self.flag = self.read_log()
        with open(self.result,'a')as h:
            h.write("crash问题\n")
            for k, v in self.d_crash.items():
                q = k.split("_")
                h.write(q[0] + ' ' + q[1] + ' ' + str(v) + '\n')
            h.write("\nanr问题\n")
            for k, v in self.d_anr.items():
                h.write(k + ' ' + str(v) + '\n')
        print(self.file, '分析完毕')

    def read_log(self):
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

        elif self.flag == 2:
            exception_crash = re.findall(r': (.+?):', self.line)
            if exception_crash:
                self.temp = self.temp + '_' + exception_crash[0]
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
        
        elif self.flag == 3:
            pid_temp = re.findall(r"(\(.+?\)):", self.line)
            if pid_temp:
                if pid_temp[0] == self.pid:
                    self.list_temp_anr.append(self.line)
                    return self.flag
                else:
                    with open(self.result_anr, 'a')as g:
                        for i in self.list_temp_anr:
                            g.write(i)
                        g.write('\n===================\n\n')
                    self.list_temp_anr = []
                    self.flag = 0
                    return self.flag
            else:
                with open(self.result_anr, 'a')as g:
                    for i in self.list_temp_anr:
                        g.write(i)
                    g.write('\n===================\n\n')
                self.list_temp_anr = []
                self.flag = 0
                return self.flag

        elif self.flag == 5:
            pid_temp = re.findall(r'(\(.+?\)):', self.line)
            if pid_temp:
                if pid_temp[0] == self.pid:
                    self.list_temp_crash.append(self.line)
                    return self.flag
                else:
                    with open(self.result_crash, 'a')as g:
                        for i in self.list_temp_crash:
                           g.write(i)
                        g.write('\n===================\n\n')
                    self.list_temp_crash = []
                    self.flag = 0
                    return self.flag
            else:
                with open(self.result_crash, 'a')as g:
                    for i in self.list_temp_crash:
                        g.write(i)
                    g.write('\n===================\n\n')
                self.list_temp_crash = []
                self.flag = 0
                return self.flag

def runInstance(path):
    file = os.path.join(path, 'sdcard', 'log', 'logcat.log')
    ReadLog(file)

def getFile():
    list_devices = os.listdir(r'result')
    for d in list_devices:
        path = os.path.join(r'result', d)
        thread = threading.Thread(target = runInstance, args = (path, ))
        thread.start()
        
def getLog():
    print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "开始获取日志......")
    p_log = subprocess.Popen(".\MULTI-PULLLOGS.bat", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    strline = p_log.stdout.readline()
    while(strline != b""):
        print(strline.decode("gbk"))
        strline = p_log.stdout.readline()
    p_log.wait()
    if p_log.returncode == 0:
        print("获取日志成功！")
        getFile()
    else:
        print("获取日志失败！")
    
    p_log.kill()
        
while(True):
    nDelay = input("Monkey多少小时后，获取Log到本地（0为不自动获取）：")
    if nDelay.replace('.', '', 1).isdigit():
        break
nDelay = float(nDelay)

print("开始调用Monkey程序......")
p = subprocess.Popen(".\MUlLTI-MONKEYS.bat", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
curline = p.stdout.readline()
while b'......' not in curline:
    print(curline.decode("gbk"))
    curline = p.stdout.readline()
print(curline.decode("gbk"))
#除非另起线程，否则这边将一直等待monkey的bat执行完毕，等不到的，也没必要等，省的另起线程开启定时器了。
#p.wait()

if False:
    print("Monkey程序调用失败！")
else:
    if nDelay == 0:
        pass
    else:
        timer = threading.Timer(nDelay*3600, getLog)
        timer.start()

input()


