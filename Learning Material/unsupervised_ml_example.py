import numpy as np
from sklearn.cluster import MeanShift
from sklearn.datasets.samples_generator import makeblobs
import matplotlib.pyplot as plt

centers = [[1, 1], [5, 5]]

X,  = make_blobs(n_samples=500, centers=centers, clusterstd=1)

plt.scatter(X[:, 0], X[:, 1])
plt.show()

ms = MeanShift()

ms.fit(X)
labels = ms.labels
cluster_centers = ms.clustercenters

print(cluster_centers)

nclusters = len(np.unique(labels))

print("number of estimated clusters:", nclusters)

colors = 10 * ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']

print(colors)
print(labels)

for i in range(len(X)):
    plt.plot(X[i][0], X[i][1], colors[labels[i]], markersize=10)

plt.scatter(cluster_centers[:, 0], cluster_centers[:, 1], marker="X", size=150, linewidths=5, zorder=10)

plt.show()