import numpy as np
import sys
import matplotlib.pyplot as plt
from scipy import stats
import heapq
def LOCPOT(filename):
    # We can also read data from np.genfromtxt module
    with open(filename, "r") as f:
        lines = f.readlines()
    
    x = float(lines[2].split()[0])
    y = float(lines[3].split()[1])
    z = float(lines[4].split()[2])
    # look for grid size
    if sys.argv[2] == "1H": 
        nx = int(lines[77].split()[0])
        ny = int(lines[77].split()[1])
        nz = int(lines[77].split()[2])
        # Data starts after nx ny nz line mostly with 5 columns.
        lines1 = lines[78:(nx * ny * nz / 5) + 78]
    else:
        nx = int(lines[45].split()[0])
        ny = int(lines[45].split()[1])
        nz = int(lines[45].split()[2])
        lines1 = lines[46:(nx * ny * nz / 5) + 46]

    lst = []
    for i in range(len(lines1)):
        B = lines1[i].split()
        A = [float(j) for j in B]
        for k in A:
            lst.append(k)
    array = np.array(lst)
    array2 = array.reshape(nz, nx*ny)
    locpot = array2.mean(axis=1)
    x = np.linspace(0, z, num=nz, endpoint=False)
    plt.plot(x, locpot, linewidth=1.0)
    print(sys.argv[1].split('_')[1].split('.')[0] + " " + str(np.array(heapq.nlargest(40, locpot)).mean()))
    plt.show()

if __name__ == "__main__":
    LOCPOT(sys.argv[1])
