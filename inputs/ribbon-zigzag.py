# This script create a flat zigzag nanoribbon of 1H MoS2 passivated by Hydrogen 
# python ribbon-zigzag.py
# Developed by Niraj K. Nepal, Ph.D.
# To obtain nanoribbon for different 1H TMD, simply change lattice constant, and S-S vertical distance (thickness).
#
import math as m
import sys
a = 3.19281 #lattice constat

N = int(input("provide number of Mo atoms: "))
vacuum = float(input("provide vacuum: "))

t = 3.13239 #S-S thickness
c = t + vacuum
l = (N-1) * a + (a / (2 * m.sqrt(3))) #total length
print(l)
b_shift = m.sqrt(3) * a / 2.0
Mo_H = 1.702
H_Mo_H = 68.0304
S_H = 1.36408
H_S_S = 69.5433

mo_shift = a / (2.0*m.sqrt(3)) # angle shift of Mo from S along periodic direction
f = open("flat-ribbon.vasp", 'w')
f.write("unbent-mos2\n")
f.write(str(1.0) + '\n')
f.write(str(a) + "\t" + "0\t" + "0\n")
f.write("0\t" + str(vacuum + l) + "\t" + "0\n")
f.write("0\t" + "0\t" + str(c)+ '\n')
f.write("Mo\t" + "S\t" + "H\n")
f.write(str(N) + "\t" + str(2*N)+ '\t' + str(4) + '\n')
f.write("Cartesian\n")
# Mo
for i in range(N):
  if i % 2 == 0:
    x1 = a/4.0
  else:
    x1 = 3 * a / 4.0
  
  y1 = (vacuum/2.0) + mo_shift + (i * b_shift)
  z1 = c / 2.0
  f.write(str(x1) + '\t' + str(y1) + '\t' + str(z1) + '\n')

#S
for j in range(N):
  if j % 2 == 0:
    x2 = 3 * a / 4.0
  else:
    x2 = a / 4.0

  y2 = (vacuum / 2.0) + (j * b_shift)
  z2 = (c / 2.0) - (t/2.0)
  y3 = (vacuum / 2.0) + (j * b_shift)
  z3 = (c / 2.0) + (t/2.0)
  f.write(str(x2) + '\t' + str(y2) + '\t' + str(z2) + '\n')
  f.write(str(x2) + '\t' + str(y3) + '\t' + str(z3) + '\n')

f.write(str(3*a/4.0) + '\t' + str((vacuum / 2.0) - (S_H * m.sin(H_S_S*m.pi/180))) + '\t' + str(z2 + (S_H * m.cos(H_S_S*m.pi/180))) + '\n')
f.write(str(3*a/4.0) + '\t' + str((vacuum / 2.0) - (S_H * m.sin(H_S_S*m.pi/180))) + '\t' + str(z3 - (S_H * m.cos(H_S_S*m.pi/180))) + '\n')
f.write(str(3*a/4.0) + '\t' + str((vacuum / 2.0) + ((N-1)*b_shift) + mo_shift+ (Mo_H * m.cos(H_Mo_H*m.pi/(2*180)))) + '\t' + str(z1 + (Mo_H * m.sin(H_Mo_H*m.pi/(2*180)))) + '\n')
f.write(str(3*a/4.0) + '\t' + str((vacuum / 2.0) + ((N-1)*b_shift) + mo_shift+ (Mo_H * m.cos(H_Mo_H*m.pi/(2*180)))) + '\t' + str(z1 - (Mo_H * m.sin(H_Mo_H*m.pi/(2*180)))) + '\n')
f.close()
