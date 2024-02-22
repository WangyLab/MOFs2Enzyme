import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame, Series

df1 = pd.read_csv("D:\OneDrive - USTC\代码\mof\聚类\\testout.csv", index_col=0)
df = df1.loc[df1['聚类类别'] == 0]
# df.to_csv('out.csv',header=None)

dfdel = df.drop(['聚类类别'], axis=1)
print(dfdel)

res = dfdel.values.tolist()
# print(res)

a = []
for i in range(0, 2700):
    a.append(i)

for i in res:
    plt.plot(a, i[0:2700], 'k', linewidth=0.05)

plt.plot(a, res[15][0:2700], 'r', linewidth=3, label='CA')
plt.title('''MOFs and CA's IR Spectra''')
plt.legend()
plt.show()