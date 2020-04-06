

from pyecharts.charts import Bar,Pie,Scatter,Gauge,HeatMap,Funnel,WordCloud,Line,Grid,Map,Liquid
import random
import os,sys


os.chdir(sys.path[0])  # 改变目录

author = 'damao'

"""柱状图"""
skill = ['Q','W','E','R']
var1 = [110,60,5,200]
var2 = [90,100,300,500]
bar = Bar("英雄联盟","League of Legends")
bar.add("无极剑圣",skill,var1,s_more_utils=True)
bar.add("诡术妖姬",skill,var2,is_more_utils=True)
bar.show_config()
bar.render(r".\my_first_Bar.html")

"""饼图"""
attr = ["衬衫","羊毛衫","雪纺衫","裤子","高跟鞋","鞋子"]
v1 = [11,12,13,10,10,10]
pie = Pie("各产品销售情况")
pie.add("",attr,v1,is_label_show=True)
pie.render(r".\my_first_Pie.html")

"""环形图"""
attr = ["衬衫","羊毛衫","雪纺衫","裤子","高跟鞋","鞋子"]
v1 = [11,12,13,10,10,10]
pie = Pie("饼图—圆环图示例",title_pos="center")
pie.add("",attr,v1,radius=[40,75],label_text_color=None,
       is_label_show=True,legend_orient="vertical",
       legend_pos="left")
pie.render(r".\my_first_Huanxing.html")

"""散点图"""
v1=[10,20,30,40,50,60]
v2=[10,20,30,40,50,60]
scatter=Scatter("散点图示例")
scatter.add("A",v1,v2)
scatter.add("B",v1[::-1],v2)
scatter.render(r".\my_first_Sandian.html")

"""仪表盘"""
gauge=Gauge("业务指标完成率—仪表盘")
gauge.add("业务指标","完成率",66.66)
gauge.render(r".\my_first_Yibiaopan.html")

"""热力图"""
x_axis=[
    "12a","1a","2a","3a","4a","5a","6a","7a","8a","9a","10a","11a",
    "12p","1p","2p","3p","4p","5p","6p","7p","8p","9p","10p","11p",]
y_axis=[
    "Saturday","Friday","Thursday","Wednesday","Tuesday","Monday","Sunday"]
data=[[i,j,random.randint(0,50)] for i in range(24) for j in range(7)]
heatmap=HeatMap()
heatmap.add("热力图直角坐标系",x_axis,y_axis,data,is_visualmap=True,
           visual_text_color="#000",visual_orient="horizontal")
heatmap.render(r".\my_first_Hotmap.html")

"""漏斗图"""
attr=["潜在","接触","意向","明确","投入","谈判","成交"]
value=[140,120,100,80,60,40,20]
funnel=Funnel("销售管理分析漏斗图")
funnel.add("商品",attr,value,is_label_show=True,
          label_pos="inside",label_text_color="#fff")
funnel.render(r".\my_first_Loudou.html")

"""词云图"""
name=[
    "Sam s  Club","Macys","Amy Schumer","Jurassic World","Charter Communications",
    "Chick Fil A","Planet Fitness","Pitch Perfect","Express","Home","Johnny Depp",
    "Lena Dunham","Lewis Hamilton","KXAN","Mary Ellen Mark","Farrah Abraham",
    "Rita Ora","Serena Williams","NCAA baseball tournament","Point Break"
]
value=[
    10000,6181,4386,4055,2467,2244,1898,1484,1112,
    965,847,582,555,550,462,366,360,282,273,265]
wordcloud=WordCloud(width=1300,height=620)
wordcloud.add("",name,value,word_size_range=[20,100])
wordcloud.render(r".\my_first_Ciyun.html")

"""组合图"""
line=Line("折线图",width=1200)
attr=["周一","周二","周三","周四","周五","周六","周日"]
line.add("最高气温",attr,[11,11,15,13,12,13,10],
        mark_point=["max","min"],mark_line=["average"])
line.add("最低气温",attr,[1,-2,2,5,3,2,0],
        mark_point=["max","min"],mark_line=["average"],
        legend_pos="20%")
attr=["衬衫","羊毛衫","雪纺衫","裤子","高跟鞋","袜子"]
v1=[11,12,13,10,10,10]
pie=Pie("饼图",title_pos="55%")
pie.add("",attr,v1,radius=[45,65],center=[65,50],
       legend_pos="80%",legend_orient="vertical")
grid=Grid()
grid.add(line,grid_right="55%")
grid.add(pie,grid_left="60%")
grid.render(r".\my_first_Zuhetu.html")

"""水球图"""
liquid = Liquid("水球图示例")
liquid.add("Liquid", [0.8])
liquid.show_config()
liquid.render(r".\my_first_Shuiqiu1.html")

liquid = Liquid("水球图示例")
liquid.add("Liquid", [0.6, 0.5, 0.4, 0.3], is_liquid_animation=False, shape='diamond')
liquid.show_config()
liquid.render(r".\my_first_Shuiqiu2.html")

"""地图"""
value = [155, 10, 66, 78, 33, 80, 190, 53, 49.6]
attr = ["福建", "山东", "北京", "上海", "甘肃", "新疆", "河南", "广西", "西藏"]
map = Map("Map 结合 VisualMap 示例", width=1200, height=600)
map.add("", attr, value, maptype='china', is_visualmap=True, visual_text_color='#000')
map.show_config()
map.render(r".\my_first_Ditu.html")
