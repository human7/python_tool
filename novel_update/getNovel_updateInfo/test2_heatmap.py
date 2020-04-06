import pandas as pdb
import pyecharts as pec

from pyecharts.charts import HeatMap

import datetime
import random
import os,sys

os.chdir(sys.path[0])  # 改变目录

begin = datetime.date(2018, 1, 1) #设置起始日期
end   = datetime.date(2019, 12, 31) #设置终止日期
data =[
        [str(begin + datetime.timedelta(days=i)), random.randint(1000, 25000)] #设置日期间隔，步数范围
        for i in range((end - begin).days + 1)
    ]

heatmap_k = HeatMap('2018年')

heatmap_k.add(
    '',
    data,
    is_calendar_heatmap = True,
    visual_range = [1000, 25000],
    is_visualmap = True,
    calendar_data_range = [data[0][0], data[-1][0] ],
    visual_orient = 'horizontal',
    visual_pos = 'center',
    visual_top = '90%',
    calendar_cell_size = [25, 35]
)

heatmap_k.render('heatmap.html')