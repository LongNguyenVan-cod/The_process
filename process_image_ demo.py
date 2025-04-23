import matplotlib.pyplot as plt 
import numpy
from sklearn.cluster import KMeans

image = plt.imread('a.jpg')
print(image.shape) 

width = image.shape[0]
height = image.shape[1]

# 3 the hien la anh mau RGB
image = image.reshape((width*height), 3)
print(image.shape)

kmeans = KMeans(n_clusters=4).fit(image)

labels = kmeans.predict(image)
clusters = kmeans.cluster_centers_
print(labels)

image_2 = numpy.zeros((width,height,3), dtype=numpy.uint8)

index = 0
for i in range(width):
	for j in range(height):
		image_2[i][j] = clusters[labels[index]]
		index += 1

plt.imshow(image_2)
plt.show()
