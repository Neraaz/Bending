import math as m
import sys
a = float(sys.argv[1])
e = float(sys.argv[4])
c = 20.0
t = 3.13

f = open("POSCAR", 'w')
f.write("1T-unitcell\n")
f.write("1.0\n")
f.write(str(a*(1.0+e)) + '\t' + str(0) + '\t' + str(0) + '\n')
f.write(str(0) + '\t' + str(m.sqrt(3) * a) + '\t' + str(0) + '\n')
f.write(str(0) + '\t' + str(0) + '\t' + str(c) + '\n')
f.write(sys.argv[2] + ' ' +  sys.argv[3] + '\n')
f.write(str(2) + ' ' + str(4) + '\n')
f.write('Cartesian\n')
f.write(str(0) + '\t' + str(0) + '\t' + str(c / 2.0) + '\n')
f.write(str(a / 2.0) + '\t' + str((m.sqrt(3) * a / 2.0)) + '\t' + str(c / 2.0) + '\n')
f.write(str(0) + '\t' + str((a / m.sqrt(3))) + '\t' + str((c/2.0) - (t/ 2.0)) + '\n')
f.write(str(0) + '\t' + str((a / (2 * m.sqrt(3))) + (m.sqrt(3) * a / 2.0)) + '\t' + str((c / 2.0) + (t / 2.0)) + '\n')
f.write(str(a / 2.0) + '\t' + str(a / (2 * m.sqrt(3))) + '\t' + str((c/2.0) + (t / 2.0)) + '\n')
f.write(str(a / 2.0) + '\t' + str((m.sqrt(3) * a) - a / (2.0 * m.sqrt(3))) + '\t' + str((c/2.0) - (t/ 2.0)) + '\n')
f.close()
