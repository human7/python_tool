import os
import sys
def rename():
    path     = input("请输入路径(例如D:\\\\picture)：")
    prefix   = input("请输入重命名的前缀(例如 art_)：")
    
    
    count    = 0
    filelist = os.listdir(path)
    
    
    for file in filelist:
        Olddir = os.path.join(path,file)       # 旧的文件路径
        if os.path.isdir(Olddir):
            continue                           # 如果是文件夹，继续
        
        NewFile = prefix + file                # 新的文件名字
        Newdir  = os.path.join(path,NewFile)  # 新的文件路径
        
        str_show = "%s\n\t -> \t %s\n"%(file, NewFile)
        print(str_show)
        os.rename(Olddir,Newdir)
        count+=1
    
    print("一共修改了"+str(count)+"个文件")
    
if __name__ == "__main__":
    rename()