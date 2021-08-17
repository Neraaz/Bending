#band structure plot.
# For SCAN and hybrid we peform one SCF calculations along with the band calculations as 
# chargcar doesn't have kinetic energy density. For that we change IBZKPT to KPOINTS and add
# kpath with weight zero. If we have 5 kpoint is IBZ in IBZKPT and want to calculate band
# structure for 30 points along gamma (0,0,0) to X(0.5, 0.,0.). We will have 35 k-points with
# nband. We have 6 lines (second line is nkpt, third is nband), followed by one space, then comes k point with nband and correponding energy with a space.
# sed -i '6s/'35'/'30'/g' EIGENVAL *This will change nkpt from 35 to 30 (having zero weight).
# sed -i.original -e '8,1617d' EIGENVAL *This will remove the bands for IBZKPTS having weight.
# 1617 can be replace by n = 8 + (nband*N-IBZKPT-with-weight) + 2*N-IBZKPT-with-weight - 1 (leaving 1 space)
# Now we have EIGENVAL similar to PBE. 
# python band.py EIGENVAL fermi-level S ( S for semiconductor or insulator, otherwise it is metal)
import sys
import matplotlib
matplotlib.use('Agg')
import pylab
import numpy as np
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
# Now we will identify 3 bands below fermi level and 3 bands above fermi level. We can add more.
CB = []
VB = []
CB1 = []
VB1 = []
CB2 = []
VB2 = []
dic = {}
for i in range(nkpoints):
    x, y, z, weight = [float(x) for x in f.readline().split()]
    for j in range(nbands):
        fields = f.readline().split()
        print(i,j,fields)
        id, energy = int(fields[0]), float(fields[1])
        band_energies[id - 1].append(energy)
# find k point where we have CBM and VBM. MoS2 nanoribbon has them at the Gamma point. so i=0.
# We can change it depending on extrema..
        print(band_energies)
        if (energy - fermi) < 0 and (i==0):
            VB.append(energy)
        if (energy - fermi) > 0 and (i==0):
            CB.append(energy)
    blankline = f.readline()
f.close()
print(len(CB),len(VB))
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
# For semiconductor or insulator, create a file with bandgaps.
if t == "S":
    with open(sys.argv[1] + "-band", "w") as f:
        f.write("first edge state\n")
        f.write("Ec: " + str(min(CB)) + " Ev: " + str(max(VB)) + " " + "Eg: " + str(min(CB) - max(VB)) + "\n")
        f.write("second edge state\n")
        f.write("Ec: " + str(min(CB1)) + " Ev: " + str(max(VB1)) + " " + "Eg: " + str(min(CB1) - max(VB1)) + "\n")
        f.write("third band gap\n")
        f.write("Ec: " + str(min(CB2)) + " Ev: " + str(max(VB2)) + " " + "Eg: " + str(min(CB2) - max(VB2)) + "\n")
import matplotlib.pyplot as plt
plt.plot(range(nkpoints), np.zeros(nkpoints) + fermi, 'b--', lw = 2)
import numpy as np
bandn = []
for i in range(nbands):
    plt.plot(range(nkpoints), np.array(band_energies[i]))
    for j in [min(CB), max(VB), min(CB1), max(VB1), min(CB2), max(VB2)]:
        if j in band_energies[i]:
            bandn.append(i)
            print(i, j)
    if i in bandn:
        if t == 'S':
            plt.plot(range(nkpoints), np.array(band_energies[i]), 'r', lw=1.2)
            plt.plot(np.zeros(6), np.array([min(CB), max(VB), min(CB1), max(VB1), min(CB2), max(VB2)]), 'ro')
        else:
             plt.plot(range(nkpoints), np.array(band_energies[i]), 'g', lw=1.2)
             plt.plot(np.zeros(1),np.array([fermi]), 'ro')

    else:
        if t == 'S':
            plt.plot(range(nkpoints), np.array(band_energies[i]), 'b', lw = 2)
        else:
            plt.plot(range(nkpoints), np.array(band_energies[i]), 'g', lw = 2)
ax = plt.gca()
#ax.set_yticks([fermi, fermi1])
ax.set_xticks([0, 29])
ax.set_xticklabels([r'$\Gamma$', 'X']) # no tick marks
plt.xlabel("k-vector")
plt.xticks(fontsize=14)
plt.ylabel("Energy (eV)")
plt.ylim((-7, -1)) #change this depending on the energy levels.
plt.savefig(sys.argv[1] + ".png")
pylab.savefig(sys.argv[1] + '.pdf', format='pdf',bbox_inches='tight')
plt.show()
