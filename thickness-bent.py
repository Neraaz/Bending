# This script calculate the distance between 2 consecutive ions along the bending plane (yz) within the same layer for 
# bent nanoribbon. If xz is the bending plane, then we need to use (x,z) coordinates.
# It is required to calculate the local strain. We also calculate the physical thickness between 2 chalcogen layers at different
# part of the ribbon.
# python thickness-bent.py CONTCAR. First execute code for flat ribbon to get L0.dat.
import numpy as np
import sys
import matplotlib
import math as m
matplotlib.use('agg')
import matplotlib.pyplot as plt
from scipy import stats
import heapq
import pylab
import math as m
from scipy.optimize import fmin_cobyla
import numpy.polynomial.polynomial as poly
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
        x1.append(lines[9+j].split()[0])
        y1.append(lines[9+j].split()[1])
        z1.append(lines[9+j].split()[2])
    x1 = [float(i) for i in x1]
    y1 = [float(i) for i in y1]
    z1 = [float(i) for i in z1]

    with open("L0.dat", "r") as f:
        L0 = f.readlines()
    L_0 = float(L0[0].split()[1])
    L_1 = (max(y1) - min(y1)) * b
    import sympy as sy
    from sympy.abc import k
    from sympy import nsolve
    kappa = nsolve(sy.sin(L_0 * k / 2.0)-(L_1 * k / 2.0), 0.05)

    y = []
    z = []
    x = []
    for k in range(na):
        x.append(lines[9+k].split()[0])
        y.append(lines[9+k].split()[1])
        z.append(lines[9+k].split()[2])
    x = [float(i) for i in x]
    y = [float(i) for i in y]
    z = [float(i) for i in z]
    x = np.array(x) * a
    y = np.array(y) * b
    z = np.array(z) * c
    x1 = x[12:23]
    y1 = y[12:23]
    z1 = z[12:23]
    mx = x[:12]
    my = y[:12]
    mz = z[:12]
    #print(np.mean(z1))
    x2 = x[24:35]
    y2 = y[24:35]
    z2 = z[24:35]
    z2[np.where((z2 - np.mean(z)) > c / 2.15)] -= c
    z2[np.where((np.mean(z) - z2) > c / 2.0)] += c
    z1[np.where((z1 - np.mean(z)) > c / 2.1)] -= c
    z1[np.where((np.mean(z) - z1) > c / 2.1)] += c
    mz[np.where((mz - np.mean(z)) > c / 2.1)] -= c
    mz[np.where((np.mean(z) - mz) > c / 2.1)] += c

    plt.scatter(y1, z1, s = 50, color = 'red')
    plt.scatter(y2, z2, s = 50, color = 'red')
    plt.scatter(my, mz, s = 100, color='blue')
    # fitting 10 degree polynomial, we only used 6 degree polynomial in paper.
    coefs1 = poly.polyfit(y1, z1, 10)
    coefs2 = poly.polyfit(y2, z2, 10)
    coefs3 = poly.polyfit(my, mz, 10)
    from sympy.solvers import solve
    from sympy import Symbol
    x = Symbol('x')
    f1 = coefs1[0] +  coefs1[1]*x +  coefs1[2] * x**2 +  coefs1[3] * x**3 +  coefs1[4] * x**4 +  coefs1[5] * x**5 + coefs1[6] * x**6 + coefs1[7] * x**7 + coefs1[8] * x**8 + coefs1[9] * x**9 + coefs1[10] * x**10
    f2 = coefs2[0] +  coefs2[1]*x +  coefs2[2] * x**2 +  coefs2[3] * x**3 +  coefs2[4] * x**4 +  coefs2[5] * x**5 + coefs2[6] * x**6 + coefs2[7] * x**7 + coefs2[8] * x**8 + coefs2[9] * x**9 + coefs2[10] * x**10
    f3 = coefs3[0] +  coefs3[1]*x +  coefs3[2] * x**2 +  coefs3[3] * x**3 +  coefs3[4] * x**4 +  coefs3[5] * x**5 + coefs3[6] * x**6 + coefs3[7] * x**7 + coefs3[8] * x**8 + coefs3[9] * x**9 + coefs3[10] * x**10
    # finding extrema of the curve.
    p1 = f1.diff(x)
    p2 = f2.diff(x)
    p3 = f3.diff(x)
    y01 = np.array(solve(p1, x))
    y02 = np.array(solve(p2, x))
    y03 = np.array(solve(p3, x))
    print(y01, y02, y03)
    z01 = [str(i) for i in y01]
    z02 = [str(i) for i in y02]
    z03 = [str(i) for i in y03]
    y01 = []
    y02 = []
    y03 = []
    for i in z01:
        # ignoring complex result. Only real roots.
        if "I" not in i:
            y01.append(float(i))
    for i in z02:
        if "I" not in i:
            y02.append(float(i))
    for i in z03:
        if "I" not in i:
            y03.append(float(i))
    # Now we take a  coordinate for the ions in the bent structure.
    for i in y01:
        o = int(round(i))
        for j in y02:
            p = int(round(j))
            for k in y03:
                q = int(round(k))
                if abs(o-np.mean(my)) < 1.1 and abs(p-np.mean(my)) < 1.1 and abs(q-np.mean(my)) < 1.1:
                    if abs(o-p) <= 1.0 and abs(p-q) <= 1.0 and abs(q-o) <= 1.0:
                        y01 = [i]
                        y02 = [j]
                        y03 = [k]
    
    teq = abs(f1.subs(x, y01[0]) - f2.subs(x, y02[0]))
    tup = abs(f3.subs(x, y03[0]) - f2.subs(x, y02[0]))
    tdn = abs(f3.subs(x, y03[0]) - f1.subs(x, y01[0]))
    ##distance between 2 fitted layers at different point.
    y0 = y2[np.array([1, 5, 7, 9])]
    z0 = np.array([f2.subs(x, i) for i in y0])
    
    with open("Thickness-bent.dat", "a") as g:
        g.write("#" + str(round(kappa, 4)) + '\n')
        # This calculates the shortest distance from point to polynomial.
        for i, j in zip(y0, z0):
            P = (i, j)
            def f(x):
                return coefs1[0] +  coefs1[1]*x +  coefs1[2] * x**2 +  coefs1[3] * x**3 +  coefs1[4] * x**4 +  coefs1[5] * x**5 + coefs1[6] * x**6 + coefs1[7] * x**7 + coefs1[8] * x**8 + coefs1[9] * x**9 + coefs1[10] * x**10
            def objective(X):
                x,y = X
                return m.sqrt((x - P[0])**2 + (y - P[1])**2)
            def c1(X):
                x,y = X
                return f(x) - y
            X = fmin_cobyla(objective, x0=[10.0,15.0], cons=[c1])
            g.write(str(i) + " " + str(j) + " " + str(round(objective(X), 4)) + "\n")
            plt.plot(i, j, 'bo', label='point')
            plt.plot([i, X[0]], [j, X[1]], 'b-')
    # Thickness plot finished. 
    # Now we gather data for local strain calculations for bent ribbons.
                
    with open("GEOM-bent.dat", "a") as f:
        f.write("#" + str(round(kappa, 4)) + '\n')
        f.write("#" + 'teq: ' + str(round(teq, 4)) + ' ' + 'tup: ' + str(round(tup, 4)) + ' ' + 'tdn: ' + str(round(tdn, 4)) + '\n')
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
    
    ffit1 = poly.Polynomial(coefs1)
    ffit2 = poly.Polynomial(coefs2)
    ffit3 = poly.Polynomial(coefs3)
    plt.plot(y1, ffit1(y1), 'k--')
    plt.plot(y2, ffit2(y2), 'k--')
    plt.plot(my, ffit3(my), 'k--')
    plt.plot(np.array([y01[0], y02[0]]), np.array([f1.subs(x, y01[0]), f2.subs(x, y02[0])]), 'k-')
    plt.title("curvature: " + str(round(kappa, 4)) + ' ' + "thickness: " + str(round(teq, 4)))
    plt.axis('equal') 
    plt.savefig('thickness.pdf', format='pdf',bbox_inches='tight')
    plt.savefig('thickness.png', format='png',bbox_inches='tight')


if __name__ == "__main__":
    LOCPOT(sys.argv[1])
