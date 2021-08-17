# This script creates a rectangular 1H monolayers
# python 1H-unit.py Mo S (for MoS2)
# Developed by Niraj K. Nepal, Ph.D.
# To obtain nanoribbon for different 1H TMD, simply change lattice constant, and S-S vertical distance (thickness).
#
import math as m
import sys
a = float(input("import lattice constant: "))
c = float(input("provide cell height (c): "))
t = float(input("provide thickness of layer: "))

f = open("1H-unitcell-{}{}2.vasp".format(sys.argv[1], sys.argv[2]), 'w')
f.write("1H-unitcell\n")
f.write("1.0\n")
f.write(str(a) + '\t' + str(0) + '\t' + str(0) + '\n')
f.write(str(0) + '\t' + str(m.sqrt(3) * a) + '\t' + str(0) + '\n')
f.write(str(0) + '\t' + str(0) + '\t' + str(c) + '\n')
f.write(sys.argv[1] + '\t' +  sys.argv[2] + '\n')
f.write(str(2) + '\t' + str(4) + '\n')
f.write('Direct\n')
f.write(str(0.5) + '\t' + str(1 / 6.0) + '\t' + str(0.25) + '\n')
f.write(str(0) + '\t' + str( 2 / 3.0) + '\t' + str(0.25) + '\n')
f.write(str(0.5) + '\t' + str(5 / 6.0) + '\t' + str(0.25 + (t / (2.0 * c))) + '\n')
f.write(str(0) + '\t' + str(1 / 3.0) + '\t' + str(0.25 + (t / (2.0 * c))) + '\n')
f.write(str(0) + '\t' + str(1 / 3.0) + '\t' + str(0.25 - (t / (2.0 * c))) + '\n')
f.write(str(0.5) + '\t' + str(5 / 6.0) + '\t' + str(0.25 - (t / (2.0 * c))) + '\n')

f.close()


