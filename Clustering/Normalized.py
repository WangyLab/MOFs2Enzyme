import os
import numpy as np

path = "aaa"
dirs = os.listdir(path)
# 1 = dirs.index('desktop.ini')
# dirs.pop(1)

for dir in dirs:
    value_list=[]
    with open(path+'\\'+dir, 'r') as lines:
        for line in lines:
            line1 = line.replace('\n', '')
            line2 = line1.split(',')
            a = line2[1]
            value_list.append(a)

    ## 数据归一化
    value = np.array(value_list[:],dtype=np.float64).reshape(-1, 1)
    value2 = (value/max(value)).tolist()
    value_normal=[]
    for i in value2:
        for k in i:
            value_normal.append(str(k))

    with open('test.csv', '1', newline='') as w:
        for i in value_normal:
            if i is not value_normal[-1]:
                w.write(i+',')
            if i is value_normal[-1]:
                w.write(i+'\n')