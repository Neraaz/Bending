# This script create a flat armchair nanoribbon of 1H MoS2 passivated by Hydrogen 
# python ribbon-armchair.py
# Developed by Niraj K. Nepal, Ph.D.
# To obtain nanoribbon for different 1H TMD, simply change lattice constant, and S-S vertical distance (thickness).
#

import math as m
import sys

#input parameters############################################
a = 3.19281 #provide lattice constant
b = m.sqrt(3) * a

# 2*N represents the number of MoS2 units which determine the width of nanoribbon.
N = int(input("provide number of Mo atoms: "))
vacuum = float(input("provide vacuum: "))


t = 3.13239 #S-S thickness
c = t + vacuum
l = ((N-1)*a) + (a/2.0)#total length
print(l)
##############################################################

# Writing POSCAR in VASP format.

f = open("flat-armchair.vasp", 'w')
f.write("unbent-mos2\n")
f.write(str(1.0) + '\n')
f.write(str(l+vacuum) + "\t" + "0\t" + "0\n")
f.write("0\t" + str(b) + "\t" + "0\n")
f.write("0\t" + "0\t" + str(c)+ '\n')
f.write("Mo\t" + "S\t" + "H\n")
f.write(str(2*N) + "\t" + str(4*N) + '\t' + str(8) + '\n')
f.write("Cartesian\n")
#AMo First group of Mo atoms, while viewing xy plane.
for i in range(N):
  x1 = (vacuum / 2.0) + i*a
  y1 = (b / 3.0)
  z1 = c / 2.0
  f.write(str(x1) + '\t' + str(y1) + '\t' + str(z1) + '\n')

#BMo Second group of Mo atoms, while viewing xy plane.
for i in range(N):
  x1 = (vacuum / 2.0) + (a / 2.0) + i*a
  y1 = (5 * b / 6.0)
  z1 = c / 2.0
  f.write(str(x1) + '\t' + str(y1) + '\t' + str(z1) + '\n')


#AS1
for j in range(N):
  x1 = (vacuum / 2.0) + (a / 2.0) + (j * a)
  y2 = b / 6.0
  z2 = (c / 2.0) - (t/2.0)
  z3 = (c / 2.0) + (t/2.0)
  f.write(str(x1) + '\t' + str(y2) + '\t' + str(z2) + '\n')
  f.write(str(x1) + '\t' + str(y2) + '\t' + str(z3) + '\n')

#BS1
for j in range(N):
  x1 = (vacuum / 2.0) + (j * a)
  y2 = (2.0 * b / 3.0)
  z2 = (c / 2.0) - (t/2.0)
  z3 = (c / 2.0) + (t/2.0)
  f.write(str(x1) + '\t' + str(y2) + '\t' + str(z2) + '\n')
  f.write(str(x1) + '\t' + str(y2) + '\t' + str(z3) + '\n')

# Attaching hydrogen to the edge atoms.

f.write(str((vacuum / 2.0) + l + 1.36408) + '\t' + str(b / 6.0) + '\t' + str((c / 2.0) - (t / 2.0)) + '\n')
f.write(str((vacuum / 2.0) + l + 1.36408) + '\t' + str(b / 6.0) + '\t' + str((c / 2.0) + (t / 2.0)) + '\n')
f.write(str((vacuum / 2.0) + l + 1.203496) + '\t' + str((5 * b / 6.0)) + '\t' + str((c / 2.0) + 1.203496) + '\n')
f.write(str((vacuum / 2.0) + l + 1.203496) + '\t' + str((5 * b / 6.0)) + '\t' + str((c / 2.0) - 1.203496) + '\n')

f.write(str((vacuum / 2.0) - 1.36408) + '\t' + str(2.0 * b / 3.0) + '\t' + str((c / 2.0) - (t / 2.0)) + '\n')
f.write(str((vacuum / 2.0) - 1.36408) + '\t' + str(2.0 * b / 3.0) + '\t' + str((c / 2.0) + (t / 2.0)) + '\n')
f.write(str((vacuum / 2.0) - 1.203496) + '\t' + str((b / 3.0)) + '\t' + str((c / 2.0) + 1.203496) + '\n')
f.write(str((vacuum / 2.0) - 1.203496) + '\t' + str((b / 3.0)) + '\t' + str((c / 2.0) - 1.203496) + '\n')
f.close()
