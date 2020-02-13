import os
import sys


class Rename():
    def __init__(self):
        pass

    def show_Tip(self, flg, param=0):
        str_comment = '#####################################################'
        
        print('\n' + str_comment)
        # ============================
        if flg==0:            
            print('\t请输入数字！！！')            
        elif flg==1:            
            print('\t输入[ %d ]超过选择范围，请重新输入！'%param)
        elif flg==2:
            print("一共修改了[ %d ]个文件"%param)
        else:
            pass
        # ============================
        print(str_comment + '\n')

    def run(self):
        str_show = """
        =================================
                 选择重命名方式：
        =================================
        0 : 在原来名字前面加上前缀，例如：
            前缀：emoj
            旧名：happy.jpg
            新名：emoj_happy.jpg
        ---------------------------------
        1 : 按照一定的规律命名，例如：
            原来文件扩展名：png
            主体：girl
            新名：girl_001.png,..., girl_999.png
            数字扩展的占位符可以设置
        ---------------------------------

        你的选择是 : """  # 提示文字

        # ============================
        # step1. 选择类型
        # ============================
        try:
            choose = int( input(str_show) )
        except:
            self.show_Tip(0)  # 提示，输入不是数字
            self.run()
            return
        
        # ============================
        # step2. 获取共同需要的变量
        # ============================
        self.rootPath  = input(r"请输入路径(例如D:\picture)：")
        self.fileList  = os.listdir(self.rootPath)
        
        
        # ============================
        # step3. 精细化重命名
        # ============================
        if choose == 0:
            # 前缀选择
            self.choose_0()
        elif choose == 1:
            # 按照规律选择
            self.choose_1()
        else:
            self.show_Tip(1, choose)  # 提示，输入超过范围
            self.run()
            return



    def choose_0(self):
        """加前缀的重命名方式"""
        prefix   = input("请输入重命名的前缀：")
        count    = 0   
        
        
        for file in self.fileList:
            oldPath = os.path.join(self.rootPath, file)      # 旧的文件路径
            if os.path.isdir(oldPath):
                continue                                     # 如果是文件夹，继续
            
            NewFile = prefix + '_' + file                    # 新的文件名字 = 前缀_原文件名
            newPath  = os.path.join(self.rootPath, NewFile)  # 新的文件路径
            
            str_show = "%s\n==>\t%s"%(file, NewFile)
            print(str_show)                                  # 显示
            os.rename(oldPath, newPath)
            count += 1
        
        # 提示，修改了多少文件
        self.show_Tip(2, count)  
        

    
    def choose_1(self):
        """按照一定的规律重命名文件"""
        name      = input("请输入重命名的主体：")
        extension = input("请输入文件的扩展名(例如pdf,png等，不需要加.)：")
        extension = '.' + extension.lower()  # 想要筛选的文件扩展名

        width     = int(input("请输入数字宽度(不够前面会补0)："))
        count     = 0   
        
        
        
        for file in self.fileList:
            oldPath = os.path.join(self.rootPath, file)    # 旧的文件路径

            fileExten = os.path.splitext(file)[1].lower()  # 文件扩展名
            
            if (fileExten != extension):
                continue

            if os.path.isdir(oldPath):
                continue                                            # 如果是文件夹，继续
            
            strNum = str(count)
            NewFile = name + '_' + strNum.zfill(width) + extension  # 新的文件名字 = name_数字.扩展名
            newPath  = os.path.join(self.rootPath, NewFile)         # 新的文件路径
            
            str_show = "%s\n==>\t%s"%(file, NewFile)
            print(str_show)                                  # 显示
            os.rename(oldPath, newPath)                      # 重命名
            count += 1
        
        # 提示，修改了多少文件
        self.show_Tip(2, count)






    
if __name__ == "__main__":
    #rename()
    t = Rename()
    t.run()