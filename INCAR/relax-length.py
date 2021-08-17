#python relax-length.py CONTCAR 1H (or 1T or 1dT). This simply calculate the width of the ribbon. metal - metal distances along 2 edges.
import sys

f = open(sys.argv[1], 'r')
line = f.readlines()
f.close()
N = int(line[6].split()[0])
factor = max(float(line[2].split()[0]), float(line[3].split()[1]), float(line[4].split()[2]))
if sys.argv[2] == '1H':
    print(line[5].split()[0]+line[5].split()[1] + '\t' + str(factor*(float(line[8+N-1].split()[0])-float(line[8].split()[0]))) + '\n')
else:
    print(line[5].split()[0]+line[5].split()[1] + '\t' + str(factor*(float(line[8+N-1].split()[1])-float(line[8].split()[1])))+ '\n')
