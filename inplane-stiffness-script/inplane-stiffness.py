# Once we have Energy-1T and lattice-con-1T files,
# python Y-and-poisson.py Energy-1T lattice-cont-1T will create plots with in-plane stiffness
import numpy as np
import matplotlib
matplotlib.use('Agg')
import numpy.polynomial.polynomial as poly
import matplotlib.pyplot as plt
import sys



def parse_input(inputfile):
    with open(inputfile, 'r') as f:
        lines = f.readlines()
    header = lines[0]
    l = len(lines[1:])
    line1 = lines[1:]
    data = {}
    list1 = []
    for i in range(l/4):
        list2 = []
        for j in range(4*i, 4*i + 4):
            list2.append(line1[j].split()[1:])
        list1.append(list2)
  #  print(list1, l)
    i = 0

        
    while i < (l / 4):
        data[line1[4*i].split()[0]] = list1[i]
        i += 1
    
    return header, data

header, data = parse_input(sys.argv[1]) #data is a dictionary with key as TMD and values have list with sublist of strain and energy. For inplane stiffness only ion are allowed to relax, keeping 
# strained x, unstrained y, and unstrained z axis fixed.
header1, data1 = parse_input(sys.argv[2])#data1 is a dictionary with key as TMD and values have list with "strain a0 b0 a b". Poisson's ratio can be calculated as -(b-b0)/(a-a0). But the
#other direction (y) should be relaxed if x direction is strained. atoms can be relaxed in all 3 direction but strained x axis and unstrained z axis is fixed.
# Here we do not compute poisson ratio. We only extract a0 and b0 for Area of unstrained systems.

for i in data.keys():
    x = []
    y = []
    a0 = float(data1[i][1][1])
    b0 = float(data1[i][1][3])
    
    for j in range(len(data[i])):
        x.append(float(data[i][j][0]))
        y.append(float(data[i][j][1]))
# Starting plot
    plt.plot(x, y, "o", alpha=0.4)
    coefs = poly.polyfit(x, y, 3)
    x_new = np.linspace(x[1], x[-1], len(x)*10)
    ffit = poly.Polynomial(coefs)
    plt.plot(x_new, ffit(x_new))
    plt.xlabel('Strain (z)', fontsize=8)
    plt.ylabel('Energy (eV)', fontsize=8)
    #plt.ylim(min(y)-0.001, max(y)+0.001)
    plt.xticks([-0.01, -0.005, 0.005, 0.01])
    print(max(y))
    plt.text(0, max(y), i, fontsize=8)
    
    plt.title('quadratic coeff: ' + str(coefs[2]) + ' A: ' + str(a0*b0) + ' Inplane stiffness: ' + str(coefs[2] * 2.0 * 16 / (a0 * b0)), fontsize=6)
    #plt.title(i + ': ' + str(coefs[0]) + ' + ' + str(coefs[1]) + 'x + ' + str(coefs[2]) + 'x**2 + ' + str(coefs[3]) + 'x**3', fontsize=6)
    plt.savefig(i + '.png')
    plt.show()
