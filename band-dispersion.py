# This script calculate the effective mass of the charge carrier at the gamma point by performing quadratic fitting at the
# Gamma point. It takes 6 data points near gamma for fitting process. One can increase data points and try to find converge
# result. Keep in mind that, we should not include the points which doesn't follow quadratic behavior.
# python band-dispersion.py EIGENVAL E-fermi S 1H 
import sys
import matplotlib
matplotlib.use('Agg')
import pylab
import numpy as np
import numpy.polynomial.polynomial as poly

f = open(sys.argv[1], 'r')
line1 = f.readline()
line2 = f.readline()
line3 = f.readline()
line4 = f.readline()
comment = f.readline()
unknown, nkpoints, nbands = [int(x) for x in f.readline().split()]
blankline = f.readline()
band_energies = [[] for i in range(nbands)]
fermi = float(sys.argv[2])
t = sys.argv[3]
CB = []
VB = []
CB1 = []
VB1 = []
CB2 = []
VB2 = []
dic = {}
kmesh = []
for i in range(nkpoints):
    x, y, z, weight = [float(x) for x in f.readline().split()]
    if sys.argv[4] == '1H':
        kmesh.append(y)
    else:
        kmesh.append(x)
    for j in range(nbands):
        fields = f.readline().split()
        id, energy = int(fields[0]), float(fields[1])
        band_energies[id - 1].append(energy)
        # For CBM and VBM other than Gamma point change i.
        if (energy - fermi) < 0 and (i == 0):
            VB.append(energy)
        if (energy - fermi) > 0 and (i == 0):
            CB.append(energy)
    blankline = f.readline()
f.close()
for energy in CB:
    if (energy-fermi) > (min(CB) - fermi):
        CB1.append(energy)
for energy in VB:
    if (energy - fermi) < (max(VB) - fermi):
        VB1.append(energy)

for energy in CB1:
    if (energy - fermi) > (min(CB1) - fermi):
        CB2.append(energy)
for energy in VB1:
    if (energy - fermi) < (max(VB1) - fermi):
        VB2.append(energy)
import matplotlib.pyplot as plt

if t == "S":
    with open('dispersion_' + sys.argv[1] + "-band", "w") as f:
        f.write("first edge state\n")
        f.write("Ec: " + str(min(CB)-fermi) + " Ev: " + str(max(VB) - fermi) + " " + "Eg: " + str(min(CB) - max(VB)) + "\n")
        f.write("second edge state\n")
        f.write("Ec: " + str(min(CB1)-fermi) + " Ev: " + str(max(VB1) - fermi) + " " + "Eg: " + str(min(CB1) - max(VB1)) + "\n")
        f.write("third band gap\n")
        f.write("Ec: " + str(min(CB2)-fermi) + " Ev: " + str(max(VB2) - fermi) + " " + "Eg: " + str(min(CB2) - max(VB2)) + "\n")
        bandn = []
        elist = [min(CB), max(VB), min(CB1), max(VB1), min(CB2), max(VB2)]
        f.write("CB-min    VB-max    CB1-min    VB1-max     CB2-min      VB2-min\n")
        f.write(str(elist) + '\n')
        for i in range(nbands):
            for j in elist:
                if j in band_energies[i]:
                    bandn.append(i)
                    f.write("band-number       band-energies\n")
                    f.write(str(i) + " " + str(j) + "\n")
                    band_edge = []
                    kmesh1 = []
                    for l in range(6):
                        f.write(str(kmesh[l]) + " "  + str(band_energies[i][l]) + "\n")
                        band_edge.append(band_energies[i][l])
                        kmesh1.append(kmesh[l])
                    plt.plot(np.array(kmesh1), np.array(band_edge), "bo", alpha=0.6)
                    coefs = poly.polyfit(np.array(kmesh1), np.array(band_edge), 2)
                    x_new = np.linspace(kmesh1[0], kmesh1[-1], 100)
                    ffit = poly.Polynomial(coefs)
                    plt.plot(x_new, ffit(x_new), 'r', lw = 2)
                    plt.xlabel(r'k (1 / $\AA$)' , fontsize=14)
                    plt.ylabel('Energy (eV)', fontsize=14)
                    Me = 9.11 * 10**(-31)
                    e = 1.6 * 10**(-19)
                    h = 1.05361 * 10**(-34)
                    plt.title('band number: ' + str(i) + " " + 'effective mass: ' + str(10**20 * h**2/(2.0 * coefs[2] * e * Me)), fontsize = 12)
                    f.write('band number           effective mass (me)\n')
                    f.write(str(i) + '\t' + str(10**20 * h**2/(2.0 * coefs[2] * e * Me)) + '\n')
                    plt.savefig(sys.argv[1] + "_" + str(i) + "_dispersion.png")
                    pylab.savefig(sys.argv[1] + "_" + str(i) + '_dispersion.pdf', format='pdf',bbox_inches='tight')

print(sys.argv[1] + ': done')
