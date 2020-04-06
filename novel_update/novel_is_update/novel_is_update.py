# 获取小说是否更新

import requests
import re
from bs4 import BeautifulSoup
import bs4
import os,sys
import time
import winsound
import datetime

def play_Beep(duration=500):
    frequency = [256, 288,320,341,384,427,480,512]
    for freq in frequency:
        # print(freq)
        winsound.Beep(freq, duration)  # Hz, ms



class GetNovelUpdate():
    def __init__(self,
                 url,
                 timeout=10,
                 filePath='data.txt',
                 mode='w',
                 fileEncode='utf-8',
                 novelName=None):
        self.url = url
        self.timeout  = timeout       # 爬取超时
        self.filePath = filePath
        self.mode     = mode
        self.fileEncode = fileEncode
        self.li_dataInfo = ['','','']  # 更新文本，更新时间, 章节号
        
        self.begin_time = datetime.datetime.now()
        self.novelName  = novelName  # 小说名字
        
        self.time_show      = 3    # 显示 s 提示更新了
        self.time_html      = 600  # 重新更新 s
        self.time_reGetHtml = 10   # 等待一段时间在重新爬取
        self.CNT_getHtml    = 0    # 爬取html的次数

    # 运行
    def run(self):
        """
        程序的运行主程序
        如果没更新：会隔一段时间继续爬取
        如果更新了：就循环提示已经更新
        """
        # ######################################################
        #                循环运行  begin
        # ######################################################
        isUpdate = False  # 是否更新
        while(not isUpdate):
            # ============================================
            # step1.爬取解析网页，如果失败，继续爬取＋解析
            # ============================================
            ret = False
            while(not ret):
                ret = self.parseHtml()  # 如果解析失败 一直解析
                self.CNT_getHtml = self.CNT_getHtml + 1  # 爬取次数
                time.sleep(self.time_reGetHtml)  # 等待一段时间在重新爬取
            
            # ============================================
            # step2.与本地保存的文本进行对比，如果更新了，循环提示
            # ============================================
            isUpdate = self.compare()  # 对比是否更新, true 为更新

            if(isUpdate):  # 更新了
                self.writeText2File( self.li_dataInfo[0] )  # 保存到文本
                # --------------
                #   循环提示
                # --------------
                while(True):
                    self.show(True)  # 跟新了循环提示
                    play_Beep()
                    time.sleep(self.time_show)  # 等待
                    
            # ============================================
            # step3. 没有更新，等待后继续爬取
            # ============================================
            self.show(False)  # 没有更新
            time.sleep(self.time_html)  # 等待
        
        # ######################################################
        #                循环运行  end
        # ######################################################
        
    def show(self, flg):
        self.end_time = datetime.datetime.now()
        
        str_startTime = self.begin_time.strftime('%H:%M:%S')
        str_endTime   = self.end_time.strftime('%H:%M:%S')
        str_runTime   = str(self.end_time - self.begin_time)
        
        str_c1 = "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"  # 更新了     的 分界线
        str_c2 = "========================================"  # 没有更新了 的 分界线
        str_c3 = "----------------------------------------"  # 分界线
        if(flg):
            # 更新了
            print('\n%s'%str_c1)  # 分界线 $$$$
            if self.novelName != None:  # 如果有名字
                print('\t',self.novelName)
                print(str_c3)     # 分界线 ----

            str_show = "\t更新了！！！\n%s\n最新更新时间: %s" % (
            self.li_dataInfo[0], self.li_dataInfo[1])
            print(str_show)
            print('')
            print('起始时间: ',str_startTime)
            print('当前时间: ',str_endTime)
            print('运行时间: ',str_runTime)
            print('%s\n'%str_c1)  # 分界线 $$$$
        else:
            # 没有更新
            print('\n%s'%str_c2)  # 分界线 ====
            if self.novelName != None:  # 如果有名字
                print('\t',self.novelName)
                print(str_c3)     # 分界线 ----

            print( '%s\n\t没更新\n等待重新爬取数据\n已经爬取次数: %d'%(self.li_dataInfo[0], self.CNT_getHtml ))
            print('更新时间: %s'%self.li_dataInfo[1])
            print('')
            print('起始时间: ',str_startTime)
            print('当前时间: ',str_endTime)
            print('运行时间: ',str_runTime)
            print('%s\n'%str_c2)  # 分界线 ===

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
            
            chapterTitle   = ''
            lastUpdateTime = ''
            chapterID      = ''


            # 更新到全局变量            
            self.li_dataInfo[0] = chapterTitle    # 更新文本
            self.li_dataInfo[1] = lastUpdateTime  # 最新更新时间
            self.li_dataInfo[2] = chapterID       # 章节号
            

            return True  # 解析成功

        except:
            print('解析html失败!')
            return False  # 解析失败


    # 对比有没有更新
    def compare(self):
        # 读取文本
        content = self.readText()
        # 与解析后的文本进行对比
        # 如果不一样表示更新了，return True
        if self.li_dataInfo[0] == content:
            return False
        else:
            return True
        

class QiDianUpdate(GetNovelUpdate):
    # ============================
    # 针对起点网的更新
    # 继承类-重写解析html函数
    # ============================
    def parseHtml(self):
        [flg, html] = self.getHTMLText()
        try:
            soup = BeautifulSoup(html, "html.parser")          
            
            
            # 章节ID
            chapterID = soup.find(id='J-catalogCount').text
            chapterID = re.sub("\D", "", chapterID)

            # 章节详细信息
            chapterUpdate = soup.find('li', attrs={"class": "update"})
            # 章节名
            chapterTitle = chapterUpdate.find(
                'a', attrs={
                    "class": "blue"
                }).get("title")
            
            # 更新时间
            lastUpdateTime = chapterUpdate.find(
                'em', attrs={
                    "class": "time"
                }).text

            # 更新到全局变量            
            self.li_dataInfo[0] = chapterTitle    # 更新文本
            self.li_dataInfo[1] = lastUpdateTime  # 最新更新时间
            self.li_dataInfo[2] = chapterID       # 章节号
            
  
            return True  # 解析成功

        except:
            print('解析html失败!')
            return False  # 解析失败



class ZongHengUpdate(GetNovelUpdate):
    # ============================
    # 针对纵横网的更新
    # 继承类-重写解析html函数
    # ============================
    def parseHtml(self):
        [flg, html] = self.getHTMLText()
        try:
            soup = BeautifulSoup(html, "html.parser")
            chapterID = ''

            tmp = soup.find('div', attrs={"class": "book-new-chapter"})
            # 章节名
            chapterTitle = tmp.find('div', attrs={"class": "tit"}).text
            
            # 更新时间
            lastUpdateTime = soup.find('div', attrs={"class": "time"}).text
            lastUpdateTime = re.sub("\r\n", "", lastUpdateTime)
            lastUpdateTime = re.sub(" ", "", lastUpdateTime)
            # 更新到全局变量            
            self.li_dataInfo[0] = chapterTitle    # 更新文本
            self.li_dataInfo[1] = lastUpdateTime  # 最新更新时间
            self.li_dataInfo[2] = chapterID       # 章节号
            
            #print(self.li_dataInfo)

            return True  # 解析成功

        except:
            print('解析html失败!')
            return False  # 解析失败

if __name__ == "__main__":

    os.chdir(sys.path[0])  # 改变目录




    strshow = """爬取数据选择:
[0].元尊
[1].逆天邪神
[2].斗罗大陆IV\n
你的选择是："""
    choose = input(strshow)



    # 0 黑色，1蓝色，2 绿色，3 浅绿色，4红色，5紫色，6黄色，7白色，8灰色，9浅蓝，A浅绿，B浅蓝色，C浅红色，D浅紫色，E浅黄色，F亮白色
    # 恢复默认是黑底白字那应给是：
    # os.system(r"color 07") 
    # 其中：0代表背景色，7代表前景色即字体颜色
    
    
    if choose == '0':
        os.system(r"color 50")
        
        url = 'https://book.qidian.com/info/1014920025'
        yuanZun = QiDianUpdate(url, filePath='yz.txt',novelName='元尊')
        yuanZun.run()
    elif choose == '1':
        os.system(r"color 24")        
        url = 'http://book.zongheng.com/book/408586.html'
        ntxs = ZongHengUpdate(url, filePath='ntxs.txt',novelName='逆天邪神')
        ntxs.run()
    elif choose == '2':
        url = 'https://book.qidian.com/info/1013406185'
        dldl = QiDianUpdate(url, filePath='dldl_IV.txt',novelName='斗罗大陆IV')
        dldl.run()
    else:
        print('选择错误')
    

    

