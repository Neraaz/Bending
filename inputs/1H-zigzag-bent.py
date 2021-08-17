# This script creates a bent zigzag nanoribbon of 1H MoS2 passivated by Hydrogen# python 1H-zigzag-bent.py
# Developed by Niraj K. Nepal, Ph.D.
# To obtain nanoribbon for different 1H TMD, simply change lattice constant, and S-S vertical distance (thickness).
#
import math as m
import sys
#a = sys.argv[1]
#N = sys.argv[2]
#R = sys.argv[3]
#t = sys.argv[4]
a = 3.19281 #lattice constat
#a = float(input("provide lattice constant a: "))

N = int(input("provide number of Mo atoms: "))
R = float(input("provide radius of curvature: "))
vacuum = float(input("provide vacuum: "))

t = 3.13239 #S-S thickness

l = m.sqrt(3)*a*(N-1)/2.0 #total length
R1 = R - (t/2.0) # radius of curvature for inner S
R2 = R + (t/2.0) # radius of curvature for outer S

theta = l*180/(R * m.pi) #angle corresponds to arc for particular R.  
theta1 = (180 - theta)/2.0 # ___\theta1___ 

alpha = a * 180/(2 * m.sqrt(3) * R * m.pi) # angle shift of Mo from S along periodic direction
beta = theta / (N-1) #dividing theta among number of Mo
b_min = R2 * m.cos((theta + theta1)*m.pi/180)      #shifting coordinates along b direction
b_max = R2 * m.cos((theta + theta1 - (N*beta))*m.pi/180)
b_shift = (b_max - b_min)/2.0

c_min = R2 * m.sin((theta + theta1)*m.pi/180) #estimating c with vacuum
c_max = R2
c = vacuum + c_max - c_min
cshift = vacuum / 4.0
f = open('bent.vasp', 'w')
f.write("bent-mos2" + '\n')
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
  
  y1 = (vacuum/2.0) + b_shift + R * m.cos((theta+theta1-alpha-i*beta)*m.pi/180)
  z1 = R * m.sin((theta+theta1-alpha-i*beta)*m.pi/180)
  f.write(str(x1) + '\t' + str(y1) + '\t' + str(z1 + cshift) + '\n')

#S
for j in range(N):
  if j % 2 == 0:
    x2 = 3 * a / 4.0
  else:
    x2 = a / 4.0

  y2 = (vacuum / 2.0) + b_shift + R1 * m.cos((theta + theta1 - j*beta)*m.pi/180)
  z2 = R1 * m.sin((theta + theta1 - j*beta)*m.pi/180)
  y3 = (vacuum / 2.0) + b_shift + R2 * m.cos((theta + theta1 - j*beta)*m.pi/180)
  z3 = R2 * m.sin((theta + theta1 - j*beta)*m.pi/180)
  f.write(str(x2) + '\t' + str(y2) + '\t' + str(z2+cshift) + '\n')
  f.write(str(x2) + '\t' + str(y3) + '\t' + str(z3 + cshift) + '\n')

f.write(str(3*a/4.0) + '\t' + str((vacuum / 2.0) + b_shift + R1 * m.cos((theta + theta1)*m.pi/180)-1.16958) + '\t' + str(R1 * m.sin((theta + theta1)*m.pi/180)-0.701431+cshift) + '\n')
f.write(str(3*a/4.0) + '\t' + str((vacuum / 2.0) + b_shift + R2 * m.cos((theta + theta1)*m.pi/180)-0.41163444) + '\t' + str(R2 * m.sin((theta + theta1)*m.pi/180)-1.299769+cshift) + '\n')
f.write(str(3*a/4.0) + '\t' + str((vacuum/2.0) + b_shift + R * m.cos((theta+theta1-alpha-(N-1)*beta)*m.pi/180) + 0.132718) + '\t' + str(R * m.sin((theta+theta1-alpha-(N-1)*beta)*m.pi/180) - 1.6958995+cshift) + '\n')
f.write(str(3*a/4.0) + '\t' + str((vacuum/2.0) + b_shift + R * m.cos((theta+theta1-alpha-(N-1)*beta)*m.pi/180) + 1.62165304) + '\t' + str(R * m.sin((theta+theta1-alpha-(N-1)*beta)*m.pi/180) - 0.51546593+cshift) + '\n')

f.close()
