# local charge density (planar average charge density)
import numpy as np
import sys
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from scipy import stats
import heapq
import pylab
#from statistics import mean
def CHGCAR(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
    
    x = float(lines[2].split()[0])
    y = float(lines[3].split()[1])
    z = float(lines[4].split()[2])
    name = lines[5].split()
    nlist = lines[6].split()
    na = 0
    for i in range(len(nlist)):
        na += int(nlist[i])
    x1 = []
    y1 = []
    z1 = []
    # for 1T and distorted-1T nanoribbons all ions lies differently along the width direction.
    nt = na
    # for 1H armchair nanoribbon each X-T-X has similar coordinates along the width direction.
    # nt = int(nlist[0]), so taking coordinates of T is enough.
    # for 1H zigzag ribbon, two X has same coordinates and T has different.
    # nt = int(nlist[0]) + int(int(nlist[1])/2)
    for j in range(nt):
        x1.append(lines[8+j].split()[0])
        y1.append(lines[8+j].split()[1])
        z1.append(lines[8+j].split()[2])
    x1 = [float(i) for i in x1]
    y1 = [float(i) for i in y1]
    z1 = [float(i) for i in z1]
    L0 = (max(y1[:12]) - min(y1[:12])) * y
    with open('L0.dat', "w") as f:
        f.write('length: ' + str(L0))
    # finding indices that determine narrow region for which we need to
    # calculate plane (xy) average local charge density with respect to z.
    idx1 = int(sys.argv[2])
    idx2 = int(sys.argv[3])
    # fractional position compared to cell dimension.
    a = sorted(y1)[indices1]
    b = sorted(y1)[indices2]
    #for width along x-direction
    # a = sorted(x1)[indices1]
    # b = sorted(x1)[indices2]
 
    # grid dimensions
    nx = int(lines[9+na].split()[0])
    ny = int(lines[9+na].split()[1])
    nz = int(lines[9+na].split()[2])
    # collecting densities.
    if (nx * ny * nz) % 5 == 0:
        lines1 = lines[10+na:10 + na + int((nx * ny * nz / 5))]
    else:
        lines1 = lines[10+na:10 + na + int((nx * ny * nz / 5))]
        lines2 = lines[10 + na + int((nx * ny * nz / 5)):11+na+int((nx*ny*nz/5))]
        for j in lines2[0].split():
            lines1.append(j)

    i1 = int(a * ny)
    i2 = int(b * ny)
    # for width along x direction. i1 = int(a*nx), i2 = int(b*nx)
    lst = []
    for i in range(len(lines1)):
        B = lines1[i].split()
        A = [float(j) for j in B]
        for k in A:
            lst.append(k)
    array = np.array(lst)
    # In VASP CHGCAR, nx is the fastest index and nz is the slowest.
    # Here order is C-like. Look for np.reshape.
    array1 = array.reshape(nz, ny, nx)
    #now should use slicing via index.
    array2 = array1[::,i1:i2,::] 
    array = array2.reshape(nz, nx*(i2-i1))
    #for width along x direction 
    # array2 = array1[::,::,i1:i2]
    # array = array2.reshape(nz,ny*(i2-i1))
    locpot = array.mean(axis=1) / (x*y*z)
    locpot1 = locpot[locpot > 4e-3]
    z1 = int(locpot1.shape[0]) * z / nz
    x0 = np.linspace(0, z1, num=int(locpot1.shape[0]), endpoint=False)
    # writing a file for z and rhobar(z)
    with open('CHARGE-'+name[0]+name[1]+'.dat', "w") as f:
        for i, j in zip(x0, locpot1):
            f.write(str(round(i, 4)) + ' ' + str(round(j, 4)) + '\n') 
    plt.plot(x0, locpot1, 'r', linewidth=2.0)
    plt.title('Charge density')
    plt.xlabel('z' + r'$(\AA)$', fontsize=15)
    plt.ylabel('Charge density ', fontsize=10)
    axes = plt.gca()
    axes.set_xlim([0, z1])
    axes.set_ylim([0,1.5])
    xtick = [i for i in range(0, int(z1)+1, 2)]
    xtick.append(int(z1))
    plt.xticks(xtick, fontsize=10)
    plt.title('max: ' + str(round(max(locpot), 4))) 
    plt.savefig('CHGCAR.pdf', format='pdf',bbox_inches='tight')
    plt.savefig('CHGCAR.png', format='png',bbox_inches='tight')
    
    

if __name__ == "__main__":
    CHGCAR(sys.argv[1])
