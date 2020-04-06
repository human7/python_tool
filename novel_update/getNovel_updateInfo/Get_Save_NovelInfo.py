# 获取小说的章节信息
# 获取小说每个的章节名,章节文字,更新时间
# 保存成 txt 和 pkl 文件
 
import requests
import re
from bs4 import BeautifulSoup
import bs4
import os, sys
import time

import datetime
import pandas as pd
import pickle

class GetWebInfo():
    def __init__(self,
                 url,
                 timeout=10,
                 filePath='data.txt',
                 fileEncode='utf-8',
                 novelName=None):
        self.url = url
        self.timeout  = timeout       # 爬取超时
        self.filePath = filePath
        
        self.fileEncode = fileEncode
        self.li_dataInfo = []  # [(更新时间，章节名，字数), (), (), ...]        
        self.novelName  = novelName  # 小说名字
        
        
        
        self.CNT_getHtml    = 0    # 爬取html的次数

    # 运行
    def run(self):
        """
        程序的运行主程序
        """

        # step1. 爬取和解析数据
        ret = False
        while(not ret):
            ret = self.parseHtml()  # 如果解析失败 一直解析
            self.CNT_getHtml = self.CNT_getHtml + 1  # 爬取次数
            # time.sleep(10)          # 等待一段时间在重新爬取
        
        print('获取了 %d 条数据'%len(self.li_dataInfo))
        # step2. 保存数据
        # step2.1. 保存成好提取的格式
        pkl_filePath = self.filePath + '.pkl'
        print('保存到文件： %s'%pkl_filePath)        
        self.save_variable(self.li_dataInfo, pkl_filePath)
        # step2.2. 保存成文本
        print('保存到文件： %s'%self.filePath)
        self.writeText2File()
        
    
    # 保存变量-使用pickle
    def save_variable(self, v, filename):
        """和pandas数据保存类似
        df = pd.DataFrame(v)
        df.to_pickle(filename)
        """
        f = open(filename,'wb')
        pickle.dump(v,f)
        f.close()
        return filename
    
    # 读取变量-使用pickle
    def load_variavle(self, filename):
        """和pandas数据读取类似        
        v = pd.read_pickle(filename)
        """
        f = open(filename,'rb')
        v = pickle.load(f)
        f.close()
        return v

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
    def writeText2File(self, mode='w'):
        filePath = self.filePath        
        fileEncode = self.fileEncode
        f = open(filePath, mode, encoding=fileEncode)

        for item in self.li_dataInfo:# [(更新时间，章节名，字数), (), (), ...]
            dt, ch, nums = item
            strDt = dt.strftime('%Y-%m-%d %H:%M:%S')
            strWrite = "%s\t%d\t%s\n"%(strDt, nums, ch)
            f.write(strWrite)        
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
            
            updateTime     = None  # 时间格式
            chapterTitle   = ''    # 章节名           
            wordCNT        = 0     # 更新字数


            # 解析


            # 更新到全局变量
            self.li_dataInfo.append( (updateTime, chapterTitle, wordCNT) )  # 更新到元组里面
            
            
            return True  # 解析成功

        except:
            print('解析html失败!')
            return False  # 解析失败



class GetZHNovelInfo(GetWebInfo):
    # 解析html
    def parseHtml(self):
        [flg, html]         = self.getHTMLText()
        data_updateTime     = None  # 时间格式
        data_title          = ''    # 章节名           
        data_wordCNT        = 0     # 更新字数

        try:
            soup = BeautifulSoup(html, "html.parser")          
            div_vols =  soup.find('div', attrs={"class": "volume-list"})
            
            li_guest = soup.findAll('li', attrs={"class": "col-4"})      # 普通
            li_vip   = soup.findAll('li', attrs={"class": "vip col-4"})  # vip
            
            li_tmp = []        

            # 解析普通卷
            for li in li_guest:
                # 解析
                a          = li.find('a')     # 标签
                info       = a.get('title')   # str 内容举例：'第652章 怒火沸腾 字数：3517 更新时间：2016-05-24 23:45 '
                tmp = info.split('字数：')
                tmp = tmp[1].split(' 更新时间：')
                data_wordCNT        = int(tmp[0])    # 更新字数
                data_updateTime     = pd.to_datetime(tmp[1]) # 时间格式 
                data_title = a.text                    # 章节名
                # 保存-更新到全局变量
                li_tmp.append( (data_updateTime, data_title, data_wordCNT) )  # 更新到元组里面
                
            
            # 数据获取完毕
            # 按照时间顺序排序
            self.li_dataInfo = sorted(li_tmp, key=lambda x: x[0])   # 按时间项排序，第1项
            
            
            # # 解析VIP卷
            #  vip 卷在 解析guest时候就包含了
            # for li in li_vip:
            #     # 解析
            #     a          = li.find('a')     # 标签
            #     info       = a.get('title')   # str 内容举例：'第652章 怒火沸腾 字数：3517 更新时间：2016-05-24 23:45 '
            #     tmp = info.split('字数：')
            #     tmp = tmp[1].split(' 更新时间：')
            #     data_wordCNT        = int(tmp[0])    # 更新字数
            #     data_updateTime     = pd.to_datetime(tmp[1]) # 时间格式 
            #     data_title = a.text                    # 章节名
            #     # 保存-更新到全局变量
            #     self.li_dataInfo.append( (data_updateTime, data_title, data_wordCNT) )  # 更新到元组里面
            #     li_2.append( (data_updateTime, data_title, data_wordCNT) )

            
            return True  # 解析成功

        except:
            print('解析html失败!')
            return False  # 解析失败


if __name__ == "__main__":

    os.chdir(sys.path[0])  # 改变目录

    url = 'http://book.zongheng.com/showchapter/408586.html'
    ntxs = GetZHNovelInfo(url, filePath='ntxs.txt',novelName='逆天邪神')
    ntxs.run()


