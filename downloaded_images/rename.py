import os
import shutil#复制文件
def rename(dictory,target_dir):
    count=0
    for files in os.listdir(dictory):#总目录下的文件
        full_path=os.path.join(dictory,files)
        if os.path.isdir(full_path):
            list=[]
            for file in os.listdir(full_path):#文件下的内容
                list.append(file)
            list=sorted(list, key=lambda x: int(os.path.splitext(x)[0]))
            for k in range(len(list)):
                src=os.path.join(full_path,list[k])
                dst=os.path.join(full_path,f'x{k+1+count}.jpg')
                os.rename(src,dst)
                if target_dir:
                    os.makedirs(target_dir,exist_ok=True)
                    shutil.copy2(dst, os.path.join(target_dir, f'{k + 1 + count}.jpg'))

            count+=len(list)

if __name__ == '__main__':
    dictory=input('原路径是：').strip('"')
    target_dir=input('目标路径是：').strip('"')
    rename(dictory,target_dir)



