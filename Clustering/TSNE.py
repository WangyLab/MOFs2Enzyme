import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.cluster import Birch
from pandas import DataFrame, Series
from sklearn.manifold import TSNE

datafile = 'IR_Raman.csv'
outfile = 'testout.csv'
data = pd.read_csv(datafile, header=None)
d = DataFrame(data)
print(d)

mod = KMeans(n_clusters=4, max_iter=2000, n_init=100)
y_pred = mod.fit_predict(d)
print(y_pred)

r = pd.concat([d, pd.Series(mod.labels_, index=d.index)], axis=1)
r.columns = list(d.columns) + [u'聚类类别']
r.columns = r.columns.astype(str)
print(r)
r.to_csv(outfile)

ts = TSNE()
ts.fit_transform(r)
ts = pd.DataFrame(ts.embedding_, index=r.index)

a = ts[r[u'聚类类别'] == 0]
plt.plot(a[0], a[1], 'ko', markersize=6)
a = ts[r[u'聚类类别'] == 1]
plt.plot(a[0], a[1], 'go', markersize=6)
a = ts[r[u'聚类类别'] == 2]
plt.plot(a[0], a[1], 'bo', markersize=6)
a = ts[r[u'聚类类别'] == 3]

a = ts.iloc[[31]]
plt.plot(a[0], a[1], 'r*', markersize=15, label='CA')
plt.title('TSNE Scatter Plot')
plt.show()
