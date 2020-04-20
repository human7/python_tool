#  获得小说

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



class GetNovelBase():
    '''爬取保存小说，解析针对网址[http://www.qiushuge.net/zhongjidouluo/?a748=fy!_1560655927105232546]
    原理:先爬取目录页，得到所有章节的网址信息, 然后选择要爬取的章节，爬取所有的章节
    修改继承：只需要修改两个函数
    1.解析目录 parseContent()
    2.解析章节 parseChapter()
    '''
    def __init__(self,
                 url,
                 timeout=10,
                 filePath='data.txt',        
                 fileEncode='utf-8',
                 novelName=None):
        self.urlContent = url  # 目录的url
        self.timeout  = timeout       # 爬取超时
        self.filePath = filePath        
        self.fileEncode = fileEncode
        self.li_Content = []  # 章节信息: Content = [ 1,'','']  # ID，章节名, URL
        
        self.begin_time = datetime.datetime.now()
        self.novelName  = novelName  # 小说名字

        self.writeText2File('', 'w')


    # 运行
    def run(self):
        # ----------------
        # Step1. 获取目录
        # ----------------
        ret = False
        while(not ret):
            ret = self.parseContent()  # 如果解析失败 一直解析
            #print('解析目录失败，重新爬取')
            time.sleep(10)  # 等待一段时间在重新爬取

        # ---------------------
        # Step2. 选择要爬取的章节
        # ---------------------
        cnt = len(self.li_Content)
        _RANGE = 20  # 显示范围
        while(_RANGE-cnt>0):
            _RANGE = _RANGE - 1 # 不要让显示范围超过总共的章节数
        
        print('==============================')        
        for i in range(0,5): # 显示前五章
            item = self.li_Content[i]
            print('【%d】: %s'%( i, item[0]))
        print('...\n...\n...')

        for i in range(cnt-_RANGE,cnt): # 显示后_RANGE章节
            item = self.li_Content[i]
            print('【%d】: %s'%( i, item[0]))
        print('\n==============================')
        print('[0]爬取全部\n[1]选择爬取')
        choose = input('> 你的选择:')
        if choose == '0':
            print('爬取全部章节，共%d章'%cnt)
            ID_beg = 0     # 第一章
            ID_end = cnt-1 # 最后一章
        elif choose == '1':
            ID_beg = int(input('选择爬取起始id：'))
            ID_end = int(input('选择爬取结束id：'))
        else:
            print('选择错误，退出!')
            return 0
        


        # ---------------------
        # Step3. 爬取章节
        # ---------------------
        cnt = 0  # 实际爬取的章节数
        for i in range(ID_beg, ID_end+1):
            # 3.1. 爬取章节
            cnt = cnt + 1
            item  = self.li_Content[i]
            title = item[0]
            url   = item[1]
            print( '[%d]正在爬取 [%s] ...'%(cnt,title) )
            ret = False
            while(not ret):
                ret, chapterTxT = self.parseChapter(url, title)  # 如果解析失败 一直解析
                if ret: break
                time.sleep(1)  # 等待一段时间在重新爬取

            # 3.2. 写入文本
            chapterTxT = title + '\n' + chapterTxT + '\n\n'
            self.writeText2File(chapterTxT, 'a')
        # ---------------------
        # Step4. 爬完了
        # ---------------------
        print('\n==============================')
        print('\t爬取完毕')
        print('==============================')
        return 1
        

    def show(self, flg):
        pass
      
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
    def writeText2File(self, content, mode):
        filePath = self.filePath        
        fileEncode = self.fileEncode
        f = open(filePath, mode, encoding=fileEncode)
        f.write(content)
        f.close()

    # 获取html
    def getHTMLText(self,url):
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


    # 解析目录
    def parseContent(self):
        [flg, html] = self.getHTMLText(self.urlContent)
        try:
            print('解析目录中...')
            soup = BeautifulSoup(html, "html.parser")            
            # Get_CNT   = 0 # 
            Get_title = ''
            Get_url   = ''

            tag_div = soup.find('div', attrs={"class":"panel"})
            tag_a_s = tag_div.findAll('a')

            self.li_Content = [] 
            for tag_a in tag_a_s:
                # Get_CNT   = Get_CNT + 1
                Get_url   = tag_a.get('href')
                Get_title = tag_a.text
                #Content   = [ Get_CNT, Get_title, Get_url ]
                Content   = [ Get_title, Get_url ]
                self.li_Content.append(Content)
            return True  # 解析成功

        except:
            print('解析目录失败!')
            return False  # 解析失败


    # 解析章节
    def parseChapter(self, url, title='本文'):
        [flg, html] = self.getHTMLText(url)
        try:
            soup = BeautifulSoup(html, "html.parser")            

            tag_div = soup.find('div', attrs={"class":"content"})  

            chapterTxT = tag_div.text

            chapterTxT = re.sub( r'下一篇:.*', '', chapterTxT) # .*(点-星)匹配除了换行外的所有字符
            chapterTxT = re.sub( r'上一篇:.*', '', chapterTxT) # .*(点-星)匹配除了换行外的所有字符

            return True, chapterTxT  # 解析成功

        except:
            print('解析 [%s] 失败!'%title)
            return False, 'Fail'  # 解析失败
        


if __name__ == "__main__":

    os.chdir(sys.path[0])  # 改变目录


    url = 'http://www.qiushuge.net/zhongjidouluo/?a748=fy!_1560655927105232546'
    dldl = GetNovelBase(url, filePath='斗罗大陆4.txt',novelName='斗罗大陆4')
    dldl.run()
