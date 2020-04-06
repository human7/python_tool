# ==================================
#    将数据处理后，生产 “日历html”
# ==================================

import datetime
import pandas as pd

from pyecharts import options as opts
from pyecharts.charts import Calendar
import os,sys


def drawCalendar(data, year, title, min=0, max=5, filePath='.'):
    """保存日历图"""
    strYear = str(year)
    calendar=(
            Calendar(init_opts=opts.InitOpts(width='1280px', height='350px'))
            .add("", data, calendar_opts=opts.CalendarOpts(range_=[year]))
            .set_global_opts(
                title_opts=opts.TitleOpts(title=title),
                visualmap_opts=opts.VisualMapOpts(
                    max_=max,
                    min_=min,
                    orient="horizontal",
                    is_piecewise=True,
                    pos_top="230px",
                    pos_left="100px",
                ),
            )
        )

    calendar.render(filePath)


if __name__ == "__main__":


    # 改变目录
    os.chdir(sys.path[0]) 

    
    
    # =========================
    #        处理数据
    # =========================
    # 读取数据
    fileName            = 'ntxs.txt.pkl'
    novelInfos_dateTime = pd.read_pickle(fileName) # [(更新时间，章节名，字数), (), (), ...]


    novelInfos = []   # 保存的全是日期
    for item in novelInfos_dateTime:
        date = datetime.datetime.date(item[0])
        novelInfos.append( [date, item[1], item[2]] )


    # 处理数据为字典
    dict_novelInfo = {}  # 更新时间:(章节名，章节数，字数总和)    
    for item in novelInfos:
        date, chapter, wordsCNT = item

        if date in dict_novelInfo.keys(): # 原本就有，更新了的
            tmp      = dict_novelInfo[date]
            ch       = tmp[0] + ' # ' + chapter # 更新的章节名字组合
            num      = tmp[1] + 1               # 更新数++
            wCNT     = tmp[2] + wordsCNT        # 更新字数
            dict_novelInfo[date] = (ch, num, wCNT)            
        else:
            dict_novelInfo[date] = (chapter, 1, wordsCNT)

    # 处理数据为列表 [[更新时间,章节名，章节数，字数总和],[],[]...]
    novelInfos_date = [] # [[更新时间,章节名，章节数，字数总和],[],[]...]
    novel_updateCNT = [] # [[更新时间,更新的章节数],[],[],[]...]
    novel_wordsCNT  = [] # [[更新时间,字数总和],[],[],[]...]
    for key, values in dict_novelInfo.items():
        ch, num, wCNT = values
        novelInfos_date.append( [key, ch, num, wCNT ] )
        novel_updateCNT.append( [key, num]) # [[更新时间,更新的章节数],[],[],[]...]
        novel_wordsCNT.append( [key, wCNT]) # [[更新时间,字数总和],[],[],[]...]

    print( len(novelInfos_dateTime) )
    print( len(novelInfos_date) )
    print( len(dict_novelInfo) )

    # =========================
    #        生产html
    # =========================
    years = [2014,2015,2016,2017,2018,2019,2020]
    for y in years:
        filePath = 'ntxs%d更新情况.html'%y  # 保存地址
        title    = '逆天邪神%d更新情况'%y    # 标题
        # 生产html
        drawCalendar(novel_updateCNT, y, title, filePath=filePath)

