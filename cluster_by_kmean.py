from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier
from matplotlib import pyplot as plt
import numpy as np


def clusterByKmean(orders, n):

    # coordinates = np.array([[10, 5], [20, 15], [15, 10], [30, 20], [30, 10], [20, 20]])
    coors = []
    for order in orders:
        coors.append([order.coordinate['lat'], order.coordinate['lon']])

    coordinates = np.array(coors)

    x = coordinates[:, 0]
    y = coordinates[:, 1]
    kmeans = KMeans(n_clusters=n, random_state=0).fit(coordinates)

    # print(kmeans.labels_)

    clustered = kmeans.predict(coordinates)

    for i, order in enumerate(orders):
        order.carNumber = clustered[i]
        # cars.append({
        #     'id': coors[i]['id'],
        #     'coor': coors[i]['coor'],
        #     'carNumber': clustered[i]
        # })

    # neigh = KNeighborsClassifier(n_neighbors=3)
    # neigh.fit(coordinates, clustered)

    # print('clustered',clustered)

    # colors = ("red", "green", "blue","black")
    #
    # _color = [colors[cluster] for cluster in clustered]

    # print(_color)

    # print(neigh.predict([[15,15]]))

    # area = np.pi * 3

    # Plot
    # plt.scatter(x, y, s=area, c=_color, alpha=0.5)
    #
    # plt.title('Scatter plot pythonspot.com')
    # plt.xlabel('x')
    # plt.ylabel('y')
    # plt.show()
    # print('clustered')
    return orders


