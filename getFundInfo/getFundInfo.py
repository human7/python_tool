
import requests
import re
from bs4 import BeautifulSoup
import bs4
import os,sys
import time

import datetime
import pandas as pd
import pickle

class GetFundInfo():
    def __init__(self,
                 url,
                 timeout=10,
                 filePath='data.txt',
                 mode='w',
                 fileEncode='utf-8',
                 holdShare=0,        # 持有份额
                 holdCostPrice=0.5  # 持仓成本价
                 ):
        self.url = url
        self.timeout  = timeout       # 爬取超时
        self.filePath = filePath
        self.mode     = mode
        self.fileEncode = fileEncode

        # stock_name:    基金名称 <div class="stock-name">
        # stock_current: 今日市值 <div class="stock-current">
        # stock_change:  市值改变 <div class="stock-change">
        # stock_time:    时间 <div class="stock-time">
        self.stock_info = ['', 0, '', '']
                
        # holdShare:     持有基金的份额
        # holdCostPrice: 持仓成本价
        self.holdInfo = [holdShare, holdCostPrice]
        



        self.begin_time = datetime.datetime.now()
        self.time_reGetHtml = 10   # 等待一段时间在重新爬取
        self.CNT_getHtml    = 0    # 爬取html的次数

    # 运行
    def run(self):
        """
        程序的运行主程序
        获取基金的信息，计算其值        
        """
        
        # Step1.爬取数据
        ret = False
        while(not ret):
            ret = self.parseHtml()  # 如果解析失败 一直解析
            self.CNT_getHtml = self.CNT_getHtml + 1  # 爬取次数
            time.sleep(self.time_reGetHtml)  # 等待一段时间在重新爬取
        
        # Step2.计算和显示
        earn_money = self.clacShow()



        return earn_money

        
    def clacShow(self):
        self.end_time = datetime.datetime.now()
        
        str_startTime = self.begin_time.strftime('%H:%M:%S')
        str_endTime   = self.end_time.strftime('%H:%M:%S')
        str_runTime   = str(self.end_time - self.begin_time)       

        # print('起始时间: ',str_startTime)
        # print('当前时间: ',str_endTime)
        # print('运行时间: ',str_runTime)

        # ===========================================
        # stock_name:    基金名称 <div class="stock-name">
        # stock_current: 今日市值 <div class="stock-current">
        # stock_change:  市值改变 <div class="stock-change">
        # stock_time:    时间 <div class="stock-time">
        # self.stock_info = ['', 0, '', '']
        # ===========================================
        
        # ===========================================
        # holdShare:     持有基金的份额
        # holdCostPrice: 持仓成本价
        # self.holdInfo = [holdShare, holdCostPrice]
        # ===========================================

        
        # step1. 计算
        holdShare     = self.holdInfo[0]         # 持有基金的份额
        holdCostPrice = self.holdInfo[1]         # 持仓成本价
        holdMoney     = holdShare*holdCostPrice  # 购入价值

        stock_name    = self.stock_info[0]  # 基金名称 <div class="stock-name">
        stock_current = self.stock_info[1]  # 今日市值 <div class="stock-current">
        stock_change  = self.stock_info[2]  # 市值改变 <div class="stock-change">
        stock_time    = self.stock_info[3]  # 时间 <div class="stock-time">
        currentMoney  = holdShare*stock_current  # 当前价值

        earn_money    = currentMoney - holdMoney  # 盈余
        
        # step2. 显示
        strShow = """====================================
%s\t\t%s
        涨   幅：%s
        持有份额：%f
        购入价格：%f,\t购入资金：%f
        当前价格：%f,\t当前价值：%f
盈   余：%f
====================================
        """%( stock_name, stock_time, 
              stock_change,
              holdShare, 
              holdCostPrice, holdMoney,  
              stock_current, currentMoney,
              earn_money )

        print(strShow)

        return earn_money


    # 读文本文件
    def readText(self):
        content = ''
        try:
            with open(self.filePath, "r", encoding=self.fileEncode) as f:  # 打开文件
                content = f.read()  # 读取文件
                #print(content)
        except:
            content = ''


        return content

    # 写到文本文件中
    def writeText2File(self, content):
        filePath = self.filePath
        mode = self.mode
        fileEncode = self.fileEncode
        f = open(filePath, mode, encoding=fileEncode)
        f.write(content)
        f.close()

    # 获取html
    def getHTMLText(self):
        url = self.url
        timeout = self.timeout
        flags = False
        try:
            kv = {'user-agent': 'Mozilla/5.0'}
            r = requests.get(url, headers=kv, timeout=timeout)
            # print(r.status_code)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            flags = True
            return flags, r.text
        except requests.exceptions.Timeout as e:
            flags = False
            return flags, str(e)
        except requests.exceptions.ConnectionError as e:
            flags = False
            return flags, str(e)
        except requests.exceptions.HTTPError as e:
            flags = False
            return flags, str(e)

    # 解析html
    def parseHtml(self):
        [flg, html] = self.getHTMLText()
        try:
            soup = BeautifulSoup(html, "html.parser")            
            
            stock_name    = ''    # 基金名称 <div class="stock-name">
            stock_current = 0.0   # 今日市值 <div class="stock-current">
            stock_change  = ''    # 市值改变 <div class="stock-change">
            stock_time    = ''    # 时间 <div class="stock-time">

            self.stock_info[0] = stock_name
            self.stock_info[1] = stock_current
            self.stock_info[2] = stock_change
            self.stock_info[3] = stock_time
            

            return True  # 解析成功

        except:
            print('解析html失败!')
            return False  # 解析失败



        

class XueQiu(GetFundInfo):
    # ============================
    # 针对雪球网：https://xueqiu.com/
    # 继承类-重写解析html函数
    # ============================
    def parseHtml(self):
        [flg, html] = self.getHTMLText()
        try:
            soup = BeautifulSoup(html, "html.parser")          

            # 更新到全局变量            
            stock_name    = ''    # 基金名称 <div class="stock-name">
            stock_current = 0.0   # 今日市值 <div class="stock-current">
            stock_change  = ''    # 市值改变 <div class="stock-change">
            stock_time    = ''    # 时间 <div class="stock-time">

            stock_name      = soup.find('div', attrs={"class":"stock-name"}).text
            strStockCurrent = soup.find('div', attrs={"class":"stock-current"}).text
            stock_current   = float(strStockCurrent)
            stock_change    = soup.find('div', attrs={"class":"stock-change"}).text
            stock_time      = soup.find('div', attrs={"class":"stock-time"}).text



            self.stock_info[0] = stock_name
            self.stock_info[1] = stock_current
            self.stock_info[2] = stock_change
            self.stock_info[3] = stock_time
            
  
            return True  # 解析成功

        except:
            print('解析html失败!')
            return False  # 解析失败


if __name__ == "__main__":    
    
    # 改变目录
    os.chdir(sys.path[0])


    # 华安标普全球石油
    url = 'https://xueqiu.com/S/F160416'
    xq = XueQiu(url, holdShare=170.1535, holdCostPrice=0.5877)
    earn_money1 = xq.run()

    # 嘉实原油
    url = 'https://xueqiu.com/S/F160723'
    xq = XueQiu(url, holdShare=53.4405, holdCostPrice=0.7485)
    earn_money2 = xq.run()


    # 南方原油
    url = 'https://xueqiu.com/S/F006476'
    xq = XueQiu(url, holdShare=13.7893, holdCostPrice=0.7252)
    earn_money3 = xq.run()

    earnMoneyAll = earn_money1 + earn_money2 + earn_money3

    print("合计盈余：%f\n"%earnMoneyAll)

