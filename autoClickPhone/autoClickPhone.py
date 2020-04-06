#!/usr/bin/env python
# coding: utf-8


import os
import time
import winsound
# import random


def task1():
    for i in range(1, 21):
        print('===== 逛*****店({}/20) ======'.format(i))
        os.system('adb shell input tap 900 1200')   # 进入逛店
        initlocal()
        print('进入店铺，浏览中，请等待 16 秒')
        time.sleep(16)
        goback()
        time.sleep(1)
    print('已完成逛店任务')
    
def task2():
    print('====== 浏览会场 ======')
    for i in range(1, 4):
        os.system('adb shell input tap 900 1350')   # 点击去浏览
        initlocal()
        print('进入会场，浏览中，请等待 16 秒')
        time.sleep(16)
        goback()
    print('已完成浏览会场任务')
    print('====== 浏览其他会场 ======')
    for i in range(1, 4):
        os.system('adb shell input tap 900 1600')   # 点击去浏览1
        time.sleep(2)   # 滑动前休息2秒，避免网络不好
        initlocal()
        print('进入会场，浏览中，请等待 16 秒')
        time.sleep(16)
        goback()

def task3():
    print('====== 浏览会场 ======')
    for i in range(1, 3):
        os.system('adb shell input tap 900 1400')   # 点击去浏览
        time.sleep(2)   # 滑动前休息2秒，避免网络不好
        initlocal()
        print('进入会场，浏览中，请等待 16 秒')
        time.sleep(16)
        goback()
    print('已完成浏览会场任务')
    print('====== 浏览其他会场 ======')
    for i in range(1, 4):
        os.system('adb shell input tap 900 1650')   # 点击去浏览1
        time.sleep(2)   # 滑动前休息2秒，避免网络不好
        initlocal()
        print('进入会场，浏览中，请等待 16 秒')
        time.sleep(16)
        goback()



# =================================================
# 模拟滑动
def initlocal():
    time.sleep(2)   # 滑动前休息2秒，避免网络不好
    os.system('adb shell input swipe 900 1200 900 500')  # 模拟从下往上滑动
    time.sleep(2)   # 滑动后休息2秒，避免开始计时延迟

# =================================================
# 返回上一页面
def goback():
    os.system('adb shell input keyevent KEYCODE_BACK')  # 返回
    time.sleep(2)
    print('\t退出\n')



# =================================================
def task_end_1(cnt):
    print('\n====== 浏览最后一个项目 ======')
    print('一共[%d]次'%cnt)
    for i in range(1, cnt+1):
        os.system('adb shell input tap 900 1950')   # 点击去浏览
        time.sleep(2)  # 滑动前休息2秒，避免网络不好
        initlocal()  # 来回移动
        print('第[%d]次 进入会场，浏览中，请等待 16 秒'%(i))
        time.sleep(16)
        goback()
# =================================================
def task_end_2(cnt):
    print('\n====== 浏览倒数第2个项目 ======')
    print('一共[%d]次'%cnt)
    for i in range(1, cnt+1):
        os.system('adb shell input tap 900 1770')   # 点击去浏览
        time.sleep(2)  # 滑动前休息2秒，避免网络不好
        initlocal()  # 来回移动
        print('第[%d]次 进入会场，浏览中，请等待 16 秒'%(i))
        time.sleep(16)
        goback()
# =================================================
def task_end_3(cnt):
    print('\n====== 浏览倒数第3个项目 ======')
    print('一共[%d]次'%cnt)
    for i in range(1, cnt+1):
        os.system('adb shell input tap 900 1560')   # 点击去浏览
        time.sleep(2)  # 滑动前休息2秒，避免网络不好
        initlocal()  # 来回移动
        print('第[%d]次 进入会场，浏览中，请等待 16 秒'%(i))
        time.sleep(16)
        goback()

# =================================================
def task_end_4(cnt):
    print('\n====== 浏览倒数第4个项目 ======')
    print('一共[%d]次'%cnt)
    for i in range(1, cnt+1):
        os.system('adb shell input tap 900 1340')   # 点击去浏览
        time.sleep(2)  # 滑动前休息2秒，避免网络不好
        initlocal()  # 来回移动
        print('第[%d]次 进入会场，浏览中，请等待 16 秒'%(i))
        time.sleep(16)
        goback()

def tapTask(cnt, x, y, waitTime=5):
    """
    @cnt: 循环点击次数
    @x: 手机像素位置x
    @y: 手机像素位置y
    @waitTime: 等待时间
    """
    print('\t-------------------------------------')
    print('\t浏览(%d,%d) %d 次，每次 %d 秒'%(x, y, cnt, waitTime))
    adbStr = 'adb shell input tap %d %d'%(x, y)
    for i in range(1, cnt+1):
        os.system(adbStr)   # 点击去浏览
        time.sleep(2)  # 滑动前休息2秒，避免网络不好
        # initlocal()  # 来回移动
        print('\t\t第[%d]次 进入任务，浏览中，请等待 %d 秒'%(i, waitTime))
        time.sleep(waitTime)
        goback()
        
        #os.system('adb kill-server')  # 第一条命令是杀ADB的服务，


def jd_nianshou():  # 京东年兽
    tapTask(1,  840, 1262, 35)  # 2会场
    tapTask(15, 840, 1337, 1)   # 3 加购精选好物
    tapTask(17, 840, 1604, 1)   # 4 逛逛好店
    tapTask(2,  840, 1772, 1)   # 5
    tapTask(5,  840, 1938, 1)   # 6 好玩互动
    tapTask(4,  840, 2123, 1)   # 7 视频

def jd_cww_1():  # 京东 宠汪汪-年货精品 一共10个
    print('====================================')
    print('京东 宠汪汪-年货精品')
    print('====================================')
    l_X = [325, 746,  325,  746, 325,  746]
    l_Y = [746, 1277, 1795, 746, 1277, 1795]
    
    # 前6个
    for i,x in enumerate(l_X):
        y = l_Y[i]
        print('第%d次, 坐标[%d,%d]'%(i,x,y))
        tapTask(1, x, y, 5)   # 5秒
    
    os.system('adb shell input swipe 900 1200 900 500')  # 模拟从下往上滑动
    os.system('adb shell input swipe 900 1200 900 500')  # 模拟从下往上滑动
    os.system('adb shell input swipe 900 1200 900 500')  # 模拟从下往上滑动
    
    # 后面6个-只点4个
    for i,x in enumerate(l_X):
        if i>4:
            print('done')
            return 0
        y = l_Y[i]
        print('第%d次, 坐标[%d,%d]'%(i,x,y))
        tapTask(1, x, y, 5)   # 5秒
    
    
def jd_cww_2(cnt_1=6, cnt_2=10):  # 京东 一级目录下的
    """
    cnt_1:逛会场次数
    cnt_2:关注商品次数
    """
    
    tapTask(cnt_1,  852, 1902, 5)  # 逛逛会场  次 1902 1657
    tapTask(cnt_2,  852, 2130, 5)  # 关注商品  次
    
def jd_cww_3(num=8):  # 京东 二级菜单，最开始关注店铺，拉到最底下
    print('====================================')
    print('京东 关注店铺 %d 个 拉到最下面'%num)
    print('====================================')
    
    if num==10:  # 10个的
        l_X = [254,755,    185,498,857,       839,  839,  839,  839,  839]  # 10个
        l_Y = [390,390,    712,712,712,      1004, 1263, 1522, 1781, 2040]
    elif num==8:  # 8个的
        # 第1层 2个
        # 第2层 3个
        # 第3，4，5层，各1个
        # ------- old ------- 
        l_X = [ 185,857,     185,  512, 839,     839,  839,  839 ]
        l_Y = [ 712,712,     1263,1263,1263,    1522, 1781, 2040 ]
        # ------- new ------- 
        l_X = [ 305,790,     179,  547, 846,     868,  868,  868 ]
        l_Y = [ 765,765,     1208,1208,1208,    1523, 1790, 2052 ]
    elif num==9:  # 9个的
        l_X = [ 185,857,     185,  512, 839,      839,  839,  839,  839 ]
        l_Y = [ 712,712,     1004,1004,1004,     1263, 1522, 1781, 2040 ]
    elif num==7:
        l_X = [324,821,   224,532,910,       890,872]
        l_Y = [882,935,  1379,1383,1387,   1666,1970]


    for i,x in enumerate(l_X):
        y = l_Y[i]
        print('第%d次, 坐标[%d,%d]'%(i,x,y))
        tapTask(1, x, y, 5)   # 5秒


def jd_cww_4(num=8):  # 京东 二级菜单，关注频道
    print('====================================')
    print('京东 关注频道 %d 个 拉到最下面'%num)
    print('====================================')

    if num==8:  # 8个的
        # 拉倒最下面，从下向上，x相同，y递减
        l_X = [ 875,  875,  875,  875,  875,  875,  875,  875]
        l_Y = [2085, 1810, 1535, 1260,  985,  710,  435,  272]
    elif num==7:
        l_X = [ 875,  875,  875,  875,  875,  875,  875]
        l_Y = [2085, 1810, 1535, 1260,  985,  710,  435]


    for i,x in enumerate(l_X):
        y = l_Y[i]
        print('第%d次, 坐标[%d,%d]'%(i,x,y))
        tapTask(1, x, y, 5)   # 5秒

def jd_jiaoshui_1_jdrw(num = 7):
    # 原先是4次，我就一个地方多点几次
    tapTask(num,  920, 1810, 2)  # 浇水-进店任务  次



def play_music():
    winsound.PlaySound('alert', winsound.SND_ASYNC)
    time.sleep(3)
def play_Beep(duration=500):
    frequency = [256, 288,320,341,384,427,480,512]
    for freq in frequency:
        # print(freq)
        winsound.Beep(freq, duration)  # Hz, ms


# =================================================
#                    main
# =================================================



if __name__ == "__main__":
    
    os.system('adb kill-server')  # 第一条命令是杀ADB的服务，
    #os.system('taskkill /f /im adb.exe')  # 第二条命令是杀ADB的进程！
    
    
    #jd_cww_1()  # 点我有惊喜 2级菜单
    #jd_cww_3(7)  # 京东 二级菜单，最开始关注店铺，拉到最底下
    #jd_cww_2(8, 6)  # 1级菜单，逛逛会场cnt_1次 和 关注商品cnt_2次
    jd_cww_4(7)  # 京东 二级菜单，关注频道
    
    # 浇水-营养液
    # 进店任务4个
    #jd_jiaoshui_1_jdrw(7) # 

    print('====================================')
    print('\t全部任务已完成')
    print('====================================')
    play_Beep()
    play_music()
    os.system("pause")
    
