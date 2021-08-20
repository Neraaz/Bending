# This script calculate the distance between 2 consecutive ions along the bending plane within the same layer for 
# flat nanoribbon.
# It is required to calculate the local strain.
# python thickness-flat.py CONTCAR
import numpy as np
import sys
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from scipy import stats
import heapq
import pylab
import math as m
#from statistics import mean
def LOCPOT(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
    
    a = float(lines[2].split()[0])
    b = float(lines[3].split()[1])
    c = float(lines[4].split()[2])
    nlist = lines[6].split()
    na = 0
    for i in range(len(nlist)):
        na += int(nlist[i])
    x1 = []
    y1 = []
    z1 = []
    for j in range(int(nlist[0])):
        x1.append(lines[8+j].split()[0])
        y1.append(lines[8+j].split()[1])
        z1.append(lines[8+j].split()[2])
    x1 = [float(i) for i in x1]
    y1 = [float(i) for i in y1]
    z1 = [float(i) for i in z1]
    with open('L0.dat', "w") as f:
        f.write('length: ' + str((max(y1) - min(y1)) * b))
 
    y = []
    z = []
    x = []
    for k in range(na):
        x.append(lines[8+k].split()[0])
        y.append(lines[8+k].split()[1])
        z.append(lines[8+k].split()[2])
    x = [float(i) for i in x]
    y = [float(i) for i in y]
    z = [float(i) for i in z]
    x = np.array(x) * a
    y = np.array(y) * b
    z = np.array(z) * c
   
    # provide a file "indices.dat" with a succesive indices of the ions.
    # metallic indices
    # lower chalcogen indices
    # upper chalcogen indices
    indx = np.genfromtxt("indices.dat")
    print(indx)
    Tindx = indx[0,:].astype('int')
    X1indx = indx[1,:].astype('int')
    X2indx = indx[2,:].astype('int')
    mx = x[Tindx]
    my = y[Tindx]
    mz = z[Tindx]
    x1 = x[X1indx]
    x2 = x[X2indx]
    z1 = z[X1indx]
    z2 = z[X2indx]
    y1 = y[X1indx]
    y2 = y[X2indx]
    
   # print(len(z), len(y))
    zdn = z1.mean()
    zup = z2.mean()
    zmid = mz.mean()
    with open("GEOM.dat" , "w") as f:
        f.write("#" + str(zup - zdn) + ' ' + str(zup - zmid) + ' ' + str(zmid - zdn) + '\n')

        f.write('#metal - metal\n')
        for i in range(len(mz) - 1):
            k1 = np.array([my[i], mz[i]])
            k2 = np.array([my[i+1], mz[i+1]])
            d1 = np.linalg.norm(k1-k2)
            f.write(str(i+1) + " " + str(round(d1, 4)) + '\n')
        f.write('#X-X-inner\n')
        for i in range(len(y1) - 1):
            k1 = np.array([y1[i], z1[i]])
            k2 = np.array([y1[i+1], z1[i+1]])
            d1 = np.linalg.norm(k1-k2)
            f.write(str(i+1) + " " + str(round(d1, 4)) + '\n')
        f.write('#X-X-outer\n')
        for i in range(len(y2) - 1):
            k1 = np.array([y2[i], z2[i]])
            k2 = np.array([y2[i+1], z2[i+1]])
            d1 = np.linalg.norm(k1-k2)
            f.write(str(i+1) + " " + str(round(d1, 4)) + '\n')
    #print(sys.argv[1].split('_')[1].split('.')[0] + " " + str(np.array(heapq.nlargest(40, locpot)).mean()))
    

if __name__ == "__main__":
    LOCPOT(sys.argv[1])
