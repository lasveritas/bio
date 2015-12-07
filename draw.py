from hcluster import pdist, linkage, dendrogram, average, weighted
import numpy 
from numpy.random import rand
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams["axes.grid"] = True

plt.text(1, 37, '2')

Y = [5, 4, 7, 7, 10, 7, 6, 9, 6, 5, 8, 11, 8, 9, 8]

Z = [[ 0,2,2,2 ],
     [ 1,6,3,3 ],
     [ 3,4,2.5,4 ],
     [ 7,8,4,5 ],
     [ 5,9,4.5,6]]


print(Z)
letters = ['A', 'B', 'C', 'D', 'E', 'F']
dendrogram(Z, labels = letters, orientation="right",show_contracted=True, truncate_mode='mlab') 
plt.show()
