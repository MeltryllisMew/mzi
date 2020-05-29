#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
import random
import time

def foo(t):
    print("开始执行" + str(t) + "\n")
    time.sleep(t)
    print("终止执行" + str(t) + "\n")
    
def main():
    print("主线程开始")
    
    nums = []
    for i in range(3):
        t = random.randint(1, 10)
        thread = threading.Thread(target=foo, args=(t,))
        
        #设置守护线程，守护线程会在主线程结束时自动退出
        #当非守护线程全部退出时，程序才会退出
        #IDLE无效
        #thread.daemon = True
        
        thread.start()
        nums.append(thread)

    for j in nums:
        #阻塞父线程，实现并行
        #当子线程运行完毕后，主线程才会结束
        j.join()
    
    print("主线程结束")
    
if __name__ == '__main__':
    main()
