import math as m
import sys
a = float(sys.argv[1])
e = float(sys.argv[4])
c = 20.0
t = 3.13

f = open("POSCAR", 'w')
f.write("1H-unitcell\n")
f.write("1.0\n")
f.write(str(a*(1.0+e)) + '\t' + str(0) + '\t' + str(0) + '\n')
f.write(str(0) + '\t' + str(m.sqrt(3) * a) + '\t' + str(0) + '\n')
f.write(str(0) + '\t' + str(0) + '\t' + str(c) + '\n')
f.write(sys.argv[2] + ' ' +  sys.argv[3] + '\n')
f.write(str(2) + ' ' + str(4) + '\n')
f.write('Direct\n')
f.write(str(0.5) + '\t' + str(1 / 6.0) + '\t' + str(0.25) + '\n')
f.write(str(0) + '\t' + str( 2 / 3.0) + '\t' + str(0.25) + '\n')
f.write(str(0.5) + '\t' + str(5 / 6.0) + '\t' + str(0.25 + (t / (2.0 * c))) + '\n')
f.write(str(0) + '\t' + str(1 / 3.0) + '\t' + str(0.25 + (t / (2.0 * c))) + '\n')
f.write(str(0) + '\t' + str(1 / 3.0) + '\t' + str(0.25 - (t / (2.0 * c))) + '\n')
f.write(str(0.5) + '\t' + str(5 / 6.0) + '\t' + str(0.25 - (t / (2.0 * c))) + '\n')

f.close()


