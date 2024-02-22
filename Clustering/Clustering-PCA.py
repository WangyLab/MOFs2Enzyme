import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from pandas import DataFrame, Series
from sklearn.decomposition import PCA

datafile = 'IR_Raman.csv'
outfile = 'testout.csv'
data = pd.read_csv(datafile, header=None)
d = DataFrame(data)

# 手肘法
SSE = []
for k in range(2, 9):
    estimator = KMeans(n_clusters=k)
    estimator.fit(d)
    SSE.append(estimator.inertia_)
X = range(2, 9)
plt.xlabel('k')
plt.ylabel('SSE')
plt.plot(X, SSE, 'o-')
plt.show()

# 轮廓系数法
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt

Scores = []  # 存放轮廓系数
for k in range(2, 9):
    estimator = KMeans(n_clusters=k)  # 构造聚类器
    estimator.fit(d)
    Scores.append(silhouette_score(d, estimator.labels_, metric='euclidean'))
X = range(2, 9)
plt.xlabel('k')
plt.ylabel('轮廓系数')
plt.plot(X, Scores, 'o-')
plt.show()


mod = KMeans(n_clusters=4, max_iter=2000, n_init=100)
y_pred = mod.fit_predict(d)
print(y_pred)
r = pd.concat([d, pd.Series(mod.labels_, index=d.index)], axis=1)
r.columns = list(d.columns) + [u'聚类类别']
x = pd.DataFrame(mod.labels_)
r.to_csv(outfile)

pca = PCA(n_components=2)
reduced_data_pca = pca.fit_transform(np.array(d))

pc1 = reduced_data_pca[:, 0]
pc2 = reduced_data_pca[:, 1]

colors = ['orange', 'blue', 'purple', 'green', 'k']

for i in range(len(colors)):
    x = pc1[mod.labels_ == i]
    y = pc2[mod.labels_ == i]
    plt.scatter(x, y, c=colors[i])

plt.plot(pc1[38], pc2[38], 'r*', markersize=14)
plt.title('PCA Scatter Plot')
plt.show()