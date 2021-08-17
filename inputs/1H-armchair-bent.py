# This script create a bent armchair nanoribbon of 1H MoS2 passivated by Hydrogen 
# python 1H-armchair-bent.py
# Written by Niraj K. Nepal, Ph.D.
# To obtain nanoribbon for different 1H TMD, simply change lattice constant, and S-S vertical distance (thickness).
# The initial structure is created as arc of a circle. 2 Metallic atoms at the end will be fixed along aperiodic direction, while relax along
# a length direction. All other atoms are fully relaxed. Here the length is along y direction.

import math as m
import sys
a = 3.19281 #lattice constat
b = m.sqrt(3) * a

# Total number of MoS2 units will be 2*N
N = int(input("provide number of Mo atoms: "))
R = float(input("provide radius of curvature in degree: "))
vacuum = float(input("provide vacuum: "))

t = 3.13239 #S-S thickness

l = ((N-1) * a) #total length
#Note the total length for bent ribbon is slightly off by a/2 compared to flat ribbon.
#This is the length of first Mo group, as seen in xz plane
#Second Mo group will be shifted by a / 2.0 compared to the first one. 
# Similar situation is for S atoms.
 
R1 = R - (t/2.0) # radius of curvature for inner S
R2 = R + (t/2.0) # radius of curvature for outer S

#Center of arc is at origin.
theta = l*180/(R * m.pi) #angle corresponds to arc for particular R. (180 degree __\theta/__ 0 degree)  
theta1 = (180 - theta)/2.0 # __\ /theta1__ = (180 - __\theta/__) / 2.0

#alpha = a * 180/(2 * m.sqrt(3) * R * m.pi) # angle shift of Mo from S along periodic direction
beta = theta / (N-1) #dividing theta among number of Mo
alpha = beta / 2.0
a_min = R2 * m.cos((theta + theta1)*m.pi/180)      #shifting coordinates along a direction
a_max = R2 * m.cos((theta + theta1 - (N*beta))*m.pi/180)
a_shift = (a_max - a_min)/2.0

c_min = R2 * m.sin((theta + theta1)*m.pi/180) #estimating c with vacuum
c_max = R2
c = vacuum + c_max - c_min


#Writing POSCAR for VASP calculations
f = open('{}.vasp'.format(R), 'w')
f.write("bent-mos2" + '\n')
f.write(str(1.0) + '\n')
f.write(str(vacuum+l) + "\t" + "0\t" + "0\n")
f.write("0\t" + str(b) + "\t" + "0\n")
f.write("0\t" + "0\t" + str(c)+ '\n')
f.write("Mo\t" + "S\t" + "H\n")
f.write(str(2*N) + "\t" + str(4*N)+ '\t' + str(8) + '\n')
f.write("Selective dynamics\n")
f.write("Cartesian\n")
#AMo
for i in range(N):
  x1 = (vacuum/2.0) + R * m.cos((theta+theta1-i*beta)*m.pi/180) + a_shift
  y1 = (b / 3.0)
  z1 = R * m.sin((theta+theta1-i*beta)*m.pi/180) + (vacuum / 2.0)
  f.write(str(x1) + '\t' + str(y1) + '\t' + str(z1) + '\t T\t T\t T\n')
#BMo
for i in range(N):
  x1 = (vacuum/2.0) + R * m.cos((theta+theta1-alpha-i*beta)*m.pi/180) + a_shift
  y1 = 5.0 * b / 6.0
  z1 = R * m.sin((theta+theta1-alpha-i*beta)*m.pi/180) + (vacuum / 2.0)
  f.write(str(x1) + '\t' + str(y1) + '\t' + str(z1) + '\t T\t T\t T\n')

#AS1
for i in range(N):
  x1 = (vacuum/2.0) + R1 * m.cos((theta+theta1-alpha-i*beta)*m.pi/180) + a_shift
  x2 = (vacuum/2.0) + R2 * m.cos((theta+theta1-alpha-i*beta)*m.pi/180) + a_shift
  y1 = b / 6.0
  z1 = R1 * m.sin((theta+theta1-alpha-i*beta)*m.pi/180) + (vacuum / 2.0)
  z2 = R2 * m.sin((theta+theta1-alpha-i*beta)*m.pi/180) + (vacuum / 2.0)
  f.write(str(x1) + '\t' + str(y1) + '\t' + str(z1) + '\t T\t T\t T\n')
  f.write(str(x2) + '\t' + str(y1) + '\t' + str(z2) + '\t T\t T\t T\n')

#BS1
for i in range(N):
  x1 = (vacuum/2.0) + R1 * m.cos((theta+theta1-i*beta)*m.pi/180) + a_shift
  x2 = (vacuum/2.0) + R2 * m.cos((theta+theta1-i*beta)*m.pi/180) + a_shift
  y1 = 2.0 * b / 3.0
  z1 = R1 * m.sin((theta+theta1-i*beta)*m.pi/180) + (vacuum / 2.0)
  z2 = R2 * m.sin((theta+theta1-i*beta)*m.pi/180) + (vacuum / 2.0)
  f.write(str(x1) + '\t' + str(y1) + '\t' + str(z1) + '\t T\t T\t T\n')
  f.write(str(x2) + '\t' + str(y1) + '\t' + str(z2) + '\t T\t T\t T\n')

f.write(str((vacuum/2.0) + R * m.cos((theta+theta1-alpha-(N-1)*beta)*m.pi/180) + a_shift - 1.203496) + '\t' + str(5.0 * b / 6.0) + '\t' + str(R * m.sin((theta+theta1-alpha-(N-1)*beta)*m.pi/180) - 1.203496 + (vacuum / 2.0)) + '\t T\t T\t T\n')
f.write(str((vacuum/2.0) + R * m.cos((theta+theta1-alpha-(N-1)*beta)*m.pi/180) + a_shift + 1.203496) + '\t' + str(5.0 * b / 6.0) + '\t' + str(R * m.sin((theta+theta1-alpha-(N-1)*beta)*m.pi/180) - 1.203496 + (vacuum / 2.0)) + '\t T\t T\t T\n')
f.write(str((vacuum/2.0) + R1 * m.cos((theta+theta1-alpha-(N-1)*beta)*m.pi/180) + a_shift) + '\t' + str((b / 6.0)) + '\t' + str(R1 * m.sin((theta+theta1-alpha-(N-1)*beta)*m.pi/180) - 1.36408 + (vacuum / 2.0)) + '\t T\t T\t T\n')
f.write(str((vacuum/2.0) + R2 * m.cos((theta+theta1-alpha-(N-1)*beta)*m.pi/180) + a_shift) + '\t' + str((b / 6.0)) + '\t' + str(R2 * m.sin((theta+theta1-alpha-(N-1)*beta)*m.pi/180) - 1.36408 + (vacuum / 2.0)) + '\t T\t T\t T\n')

f.write(str((vacuum/2.0) + R * m.cos((theta+theta1)*m.pi/180) + a_shift - 1.203496) + '\t' + str(b / 3.0) + '\t' + str(R * m.sin((theta+theta1)*m.pi/180) - 1.203496 + (vacuum / 2.0)) + '\t T\t T\t T\n')
f.write(str((vacuum/2.0) + R * m.cos((theta+theta1)*m.pi/180) + a_shift + 1.203496) + '\t' + str(b / 3.0) + '\t' + str(R * m.sin((theta+theta1)*m.pi/180) - 1.203496 + (vacuum / 2.0)) + '\t T\t T\t T\n')
f.write(str((vacuum/2.0) + R1 * m.cos((theta+theta1)*m.pi/180) + a_shift) + '\t' + str((2 * b / 3.0)) + '\t' + str(R1 * m.sin((theta+theta1)*m.pi/180) - 1.36408 + (vacuum / 2.0)) + '\t T\t T\t T\n')
f.write(str((vacuum/2.0) + R2 * m.cos((theta+theta1)*m.pi/180) + a_shift) + '\t' + str((2 * b / 3.0)) + '\t' + str(R2 * m.sin((theta+theta1)*m.pi/180) - 1.36408 + (vacuum / 2.0)) + '\t T\t T\t T\n')


f.close()
