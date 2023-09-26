import os
import shutil
count = 0
def is_empty_dir(dir):
    global count
    flag = False
    file_list = os.listdir(dir)
    if len(file_list) == 0:
        print(dir)
    if len(file_list) != 15:
        print(dir)
        print(len(file_list))
        print(file_list)
    x = []
    for j in os.listdir(dir):
        x.append(os.path.getsize(dir+'/'+j))
    avg = sum(x) / len(x)
    # print(avg)
    for i in x:
        if abs(i - avg) > 10000:
            print(dir+'/')
            print(i)
            flag = True
    if flag:
        count = count+1

str = 'pcaps/'
filelist = os.listdir(str)
for file in filelist:
    is_empty_dir(str+file+'/')


print(count)