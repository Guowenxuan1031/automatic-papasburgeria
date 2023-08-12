
import numpy as np



dataAll = np.loadtxt(open("papaall.csv","r"),delimiter=",")
print("dataAll.size",dataAll.size)

for i in range(44):
    for j in range(44):
        counter = 0
        for k in range(9):
            if dataAll[i][k] != dataAll[j][k]:
                counter += 1
        print(counter,end=" ")
    print("")