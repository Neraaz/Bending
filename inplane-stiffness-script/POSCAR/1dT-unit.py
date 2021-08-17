import math as m
import sys
a = float(sys.argv[1])
e = float(sys.argv[4])
c = 20.0

f = open("POSCAR", 'w')
f.write("1dT-unitcell\n")
f.write("1.0\n")
f.write(str(m.sqrt(3) * a * (1.0+e)) + '\t' + str(0) + '\t' + str(0) + '\n')
f.write(str(0) + '\t' + str(a) + '\t' + str(0) + '\n')
f.write(str(0) + '\t' + str(0) + '\t' + str(c) + '\n')
f.write(sys.argv[2] + ' ' +  sys.argv[3] + '\n')
f.write(str(2) + ' ' + str(4) + '\n')
f.write('Direct\n')
f.write(str(0) + '\t' + str(0) + '\t' + str(0.5) + '\n')
f.write(str(0.3945) + '\t' + str(0.5) + '\t' + str(0.5) + '\n')
f.write(str(0.281) + '\t' + str(0) + '\t' + str(0.41353) + '\n')
f.write(str(0.618455) + '\t' + str(0) + '\t' + str(0.5661) + '\n')
f.write(str(0.113529) + '\t' + str(0.5) + '\t' + str(0.58647) + '\n')
f.write(str(0.77612) + '\t' + str(0.5) + '\t' + str(0.43388) + '\n')
f.close()
