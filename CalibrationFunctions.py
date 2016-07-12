import math
import numpy as np
import os
import matplotlib.pyplot as plt
import glob

#CERN@SEA1 = H
#CERN@SEA2 = G
def neighbourGen(pixelNo):
    neighbours = []
    for xChange in range(-1,2,2):
        for yChange in range(-1,2,2):
            neighbours.append(pixelNo+xChange+256*yChange)
    print(neighbours)
    return neighbours

def NC2E(MNC,calibA,calibB,calibC,calibT):
    #Takes each pixel activation, converts the ToT value to Energy
    #by using the surrogate function
    energyList = []
    i = 0
    for NC in MNC:
        i+=1
        print("I am in frame:"+str(i))
        for pixel in NC:
            inCluster = False
            for neighbour in neighbourGen(pixel[0]):
                if neighbour in [pixel[0] for pixel in NC]:
                    inCluster = True

            if not inCluster and pixel[1] not in [1,11810]: #Max and Min values for chip - taking out background data
                e = surrogateFunction(pixel[1],
                                  calibA[int(pixel[0])],
                                  calibB[int(pixel[0])],
                                  calibC[int(pixel[0])],
                                  calibT[int(pixel[0])])
                energyList.append(e)
    return energyList

def surrogateFunction(tot, a, b, c, t):
    e = (t * a + tot - b + math.sqrt((b + t * a - tot) ** 2 + 4 * a * c)) / (2 * a)
    return e

calibrationMatrixA = np.loadtxt(r"calibs\H05-W0240\caliba.txt").flatten()
calibrationMatrixB = np.loadtxt(r"calibs\H05-W0240\calibb.txt").flatten()
calibrationMatrixC = np.loadtxt(r"calibs\H05-W0240\calibc.txt").flatten()
calibrationMatrixT = np.loadtxt(r"calibs\H05-W0240\calibt.txt").flatten()

path = r"C:\Users\Toby\PycharmProjects\CERN@SEA_utils_\DataFiles1"

dataNC = []# np.loadtxt(r"C:\Users\Toby\PycharmProjects\CERN@SEA_utils_\DataFiles\NC1")
for filename in os.listdir(path):
    dataNC.append(list(np.loadtxt(os.path.join(path,filename))))

#dataNC = np.loadtxt(r"DataFiles\FIRST YEAH")
#print(dataNC)
#print(calibrationMatrixA[0:2])
energyList = NC2E(dataNC,calibrationMatrixA,calibrationMatrixB,calibrationMatrixC,calibrationMatrixT)
print(len(energyList))
bins = 42

y,binEdges=np.histogram(energyList,bins=bins)
bincenters = 0.5*(binEdges[1:]+binEdges[:-1])
#plt.plot(bincenters,y,'-',)
plt.hist(energyList,bins,log=True,range=[0,3500], normed=True)#,log=True)
plt.xlabel("Energy of Gamma (keV)")
plt.ylabel("Intensity")
plt.vlines([600,1450,2600],0,0.001)
plt.show()