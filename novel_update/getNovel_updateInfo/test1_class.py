# 这种用法见：https://www.bbsmax.com/A/ke5jPoXyzr/


import datetime
import random
from pyecharts import options as opts
from pyecharts.charts import Calendar
import os,sys

def calendar_base() -> Calendar:
    begin = datetime.date(2018, 1, 1) #设置起始日期
    end = datetime.date(2019, 12, 31) #设置终止日期
    data =[
            [str(begin + datetime.timedelta(days=i)), random.randint(1000, 25000)] #设置日期间隔，步数范围
            for i in range((end - begin).days + 1)
        ]
    c = (
        Calendar()
        .add('', data, calendar_opts=opts.CalendarOpts(range_='2019')) #添加到日历图，指定显示2019年数据
        .set_global_opts(          #设置底部显示条，解释数据
            title_opts=opts.TitleOpts(title='2019年微信步数的情况',subtitle='From Weix'),
            visualmap_opts=opts.VisualMapOpts(
                max_=20000,
                min_=500,
                orient='vertical',  #设置垂直显示
                pos_top='230px',
                pos_left='100px',
                is_piecewise=True    #是否连续
                )
            )
        )
    
    return  c.render('charts1.html')

if __name__ == "__main__":
    os.chdir(sys.path[0])  # 改变目录
    calendar_base()