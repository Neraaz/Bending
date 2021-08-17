# This script creates a flat nanoribbon of distorted 1T MoS2 passivated by Hydrogen# python 1T-distorted-ribbon.py
# Written by Niraj K. Nepal, Ph.D.
# To obtain nanoribbon for different distorted 1T TMD, simply change lattice constant, and S-S vertical distance (thickness).
#
import math as m
import sys
a = 3.19281 #lattice constat

N = int(input("provide number of Mo atoms: "))
vacuum = float(input("provide vacuum: "))

t = 3.13239 #S-S thickness
c = t + vacuum
l = (N-1) * m.sqrt(3) * a + 5 * a / (2.0 * m.sqrt(3))#total length

print(l)

Mo_H = 1.702
H_Mo_H = 68.0304
S_H = 1.36408
H_S_S = 69.5433

#mo_shift = a / (2.0*m.sqrt(3)) # angle shift of Mo from S along periodic direction
f = open("flat-ribbon.vasp", 'w')
f.write("unbent-mos2\n")
f.write(str(1.0) + '\n')
f.write(str(a) + "\t" + "0\t" + "0\n")
f.write("0\t" + str(vacuum + l) + "\t" + "0\n")
f.write("0\t" + "0\t" + str(c)+ '\n')
f.write("Mo\t" + "S\t" + "H\n")
f.write(str(2*N) + "\t" + str(4*N)+ '\t' + str(4) + '\n')
f.write("Cartesian\n")
# Mo1
for i in range(N):
  y1 = (vacuum/2.0) + (i * m.sqrt(3) * a)
  x1 = a/4.0
  z1 = c / 2.0
  f.write(str(x1) + '\t' + str(y1) + '\t' + str(z1) + '\n')
#Mo2
for i in range(N):
  y1 = (vacuum/2.0) + (i * m.sqrt(3) * a) + (m.sqrt(3) * a / 2.0)
  x1 = 3.0 * a / 4.0
  z1 = c / 2.0
  f.write(str(x1) + '\t' + str(y1) + '\t' + str(z1) + '\n')

#S1 and S2
for j in range(N):
  x1 = a / 4.0
  y1 = (a / m.sqrt(3)) +  (vacuum / 2.0) + (j * m.sqrt(3) * a)
  z1 = (c / 2.0) - (t/2.0)
  y2 = (m.sqrt(3) * a / 2.0) + (a/(2*m.sqrt(3))) + (j * m.sqrt(3) * a) + (vacuum / 2.0)
  z2 = (c / 2.0) + (t/2.0)
  f.write(str(x1) + '\t' + str(y1) + '\t' + str(z1) + '\n')
  f.write(str(x1) + '\t' + str(y2) + '\t' + str(z2) + '\n')

#S3 and S4
for j in range(N):
  x1 = 3.0 * a / 4.0
  y1 = (a / (2 * m.sqrt(3))) +  (vacuum / 2.0) + (j * m.sqrt(3) * a)
  z1 = (c / 2.0) + (t/2.0)
  y2 = (vacuum / 2.0) + (j * m.sqrt(3) * a) - (a / (2.0 * m.sqrt(3))) + (m.sqrt(3) * a)
  z2 = (c / 2.0) - (t/2.0)
  f.write(str(x1) + '\t' + str(y1) + '\t' + str(z1) + '\n')
  f.write(str(x1) + '\t' + str(y2) + '\t' + str(z2) + '\n')

f.write(str(3*a/4.0) + '\t' + str((vacuum / 2.0) + ((N-1) * m.sqrt(3) * a) - (a / (2.0 * m.sqrt(3))) + (m.sqrt(3) * a) + S_H) + '\t' + str((c/2.0) - (t/2.0)) + '\n')
f.write(str(a/4.0) + '\t' + str((m.sqrt(3) * a / 2.0) + (a/(2*m.sqrt(3))) + ((N-1) * m.sqrt(3) * a) + (vacuum / 2.0) + S_H) + '\t' + str((c/2.0) + (t/2.0)) + '\n')
f.write(str(a/4.0) + '\t' + str((vacuum / 2.0) - (Mo_H * m.cos(H_Mo_H*m.pi/(2*180)))) + '\t' + str((c/2) + (Mo_H * m.sin(H_Mo_H*m.pi/(2*180)))) + '\n')
f.write(str(a/4.0) + '\t' + str((vacuum / 2.0) - (Mo_H * m.cos(H_Mo_H*m.pi/(2*180)))) + '\t' + str((c/2) - (Mo_H * m.sin(H_Mo_H*m.pi/(2*180)))) + '\n')
f.close()
