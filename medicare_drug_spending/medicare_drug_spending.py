import pandas
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import cycle

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import AffinityPropagation

fname = 'data/Medicare_Drug_Spending_Dashboard_Data_02_17_2016.xlsx'
df = pandas.read_excel(fname, header=2, skip_footer=3, na_values=['n/a', '*'])

features = df.iloc[:, 6:]
frac_null = features.isnull().sum() / features.shape[0]
dense_features = features.loc[:, frac_null < 0.2]
percent_features = df.iloc[:, -4:]

# scale features such that they have zero mean and unit standard deviation
scaler = StandardScaler()
#X = scaler.fit_transform(dense_features)
X = scaler.fit_transform(percent_features)

af = AffinityPropagation(preference=-50).fit(X)
cluster_centers_indices = af.cluster_centers_indices_
labels = af.labels_
n_clusters_ = len(cluster_centers_indices)



from itertools import cycle

plt.close('all')
plt.figure(1)
plt.clf()

colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
for k, col in zip(range(n_clusters_), colors):
    class_members = labels == k
    cluster_center = X[cluster_centers_indices[k]]
    plt.plot(X[class_members, 0], X[class_members, 1], col + '.')
    plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
             markeredgecolor='k', markersize=14)
    for x in X[class_members]:
        plt.plot([cluster_center[0], x[0]], [cluster_center[1], x[1]], col)

plt.title('Estimated number of clusters: %d' % n_clusters_)
plt.show()
