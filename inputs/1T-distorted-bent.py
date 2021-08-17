# This script creates a bent nanoribbon of distorted 1T MoS2 passivated by Hydrogen# python 1T-distorted-bent.py
# Written by Niraj K. Nepal, Ph.D.
# To obtain nanoribbon for different distorted 1T TMD, simply change lattice constant, and S-S vertical distance (thickness).
#
import math as m
import sys
a = 3.19281 #lattice constat

N = int(input("provide number of Mo atoms: "))
R = float(input("provide radius of curvature: "))
vacuum = float(input("provide vacuum: "))

t = 3.13239 #S-S thickness

l = (m.sqrt(3)*a*(N-1)) + (m.sqrt(3) * a / 2.0 ) #total length
R1 = R - (t/2.0) # radius of curvature for inner S
R2 = R + (t/2.0) # radius of curvature for outer S

theta = l*180/(R * m.pi) #angle corresponds to arc for particular R.  
theta1 = (180 - theta)/2.0 # ___\theta1___ 

alpha_Mo = m.sqrt(3) * a * 180/(2 * R * m.pi) 
print(alpha_Mo)# angle shift of Mo2 from Mo1 along non-periodic direction
alpha_S1 = a * 180/(m.sqrt(3) * R * m.pi)
alpha_S4 = a * 180/(2 * m.sqrt(3) * R * m.pi)
beta = theta / (2*N-1) #dividing theta among number of Mo
angle = m.sqrt(3) * a * 0.10 * 180/(2 * R * m.pi)
b_min = R2 * m.cos((theta + theta1)*m.pi/180)      #shifting coordinates along b direction
b_max = R2 * m.cos((theta + theta1 - ((2*N-1)*beta))*m.pi/180)
b_shift = (b_max - b_min)/2.0

c_min = R2 * m.sin((theta + theta1)*m.pi/180) #estimating c with vacuum
c_max = R2
c_shift= (c_max - c_min) / 2.0
c = vacuum + c_max - c_min

f = open('bent.vasp', 'w')
f.write("bent-mos2" + '\n')
f.write(str(1.0) + '\n')
f.write(str(a) + "\t" + "0\t" + "0\n")
f.write("0\t" + str(vacuum + b_max - b_min) + "\t" + "0\n")
f.write("0\t" + "0\t" + str(c)+ '\n')
f.write("Mo\t" + "S\t" + "H\n")
f.write(str(2*N) + "\t" + str(4*N)+ '\t' + str(4) + '\n')
f.write("Cartesian\n")
# Mo
for i in range(2*N):
  if i % 2 == 0:
    x1 = a/4.0
    y1 = (vacuum/2.0) + b_shift + R * m.cos((theta+theta1-i*beta-angle)*m.pi/180)
    z1 = R * m.sin((theta+theta1-i*beta)*m.pi/180) 
  else:
    x1 = 3 * a / 4.0
    y1 = (vacuum/2.0) + b_shift + R * m.cos((theta+theta1-i*beta + angle)*m.pi/180)
    z1 =   R * m.sin((theta+theta1 - i*beta)*m.pi/180) 
  f.write(str(x1) + '\t' + str(y1) + '\t' + str(z1) + '\n')

#S
for j in range(2*N):
  if j % 2 == 0:
    x1 =  a / 4.0
    y1 = (vacuum / 2.0) + b_shift + R1 * m.cos((theta + theta1 - alpha_S1 - j*beta)*m.pi/180)
    z1 =  R1 * m.sin((theta + theta1 - alpha_S1 - j*beta)*m.pi/180) 
  else:
    x1 = 3.0 * a / 4.0
    y1 = (vacuum / 2.0) + b_shift + R1 * m.cos((theta + theta1 - alpha_S1 - j*beta)*m.pi/180)
    z1 =  R1 * m.sin((theta + theta1 - alpha_S1 - j*beta)*m.pi/180) 

  f.write(str(x1) + '\t' + str(y1) + '\t' + str(z1) + '\n')

for j in range(2*N):
  if j % 2 == 0:
    x1 = 3.0 * a / 4.0
    y1 = (vacuum / 2.0) + b_shift + R2 * m.cos((theta + theta1 - alpha_S4 - j*beta)*m.pi/180)
    z1 =  R2 * m.sin((theta + theta1 - alpha_S4 - j*beta)*m.pi/180)
    
  else:
    x1 =  a / 4.0
    y1 = (vacuum / 2.0) + b_shift + R2 * m.cos((theta + theta1 - alpha_S4 - j*beta)*m.pi/180)
    z1 =  R2 * m.sin((theta + theta1 - alpha_S4 - j*beta)*m.pi/180) 
  f.write(str(x1) + '\t' + str(y1) + '\t' + str(z1) + '\n')

f.write(str(3*a/4.0) + '\t' + str((vacuum / 2.0) + b_shift + R1 * m.cos((theta + theta1 - alpha_S1 - (2*N - 1)*beta)*m.pi/180)) + '\t' + str(R1 * m.sin((theta + theta1- alpha_S1 - (2*N - 1)*beta)*m.pi/180)- 1.36408) + '\n')
f.write(str(a/4.0) + '\t' + str((vacuum / 2.0) + b_shift + R2 * m.cos((theta + theta1 - alpha_S4 - (2*N - 1)*beta)*m.pi/180)) + '\t' + str(R2 * m.sin((theta + theta1- alpha_S4 - (2*N - 1)*beta)*m.pi/180)- 1.36408) + '\n')
f.write(str(a/4.0) + '\t' + str((vacuum/2.0) + b_shift + R * m.cos((theta+theta1)*m.pi/180) + 1.203496) + '\t' + str(R * m.sin((theta+theta1)*m.pi/180) - 1.203496 ) + '\n')
f.write(str(a/4.0) + '\t' + str((vacuum/2.0) + b_shift + R * m.cos((theta+theta1)*m.pi/180) - 1.203496) + '\t' + str(R * m.sin((theta+theta1)*m.pi/180) - 1.203496 ) + '\n')
  

f.close()
