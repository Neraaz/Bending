# This script calculates and plots the area of local charge density rho(z) with respect to 
# z
# python charge-area.py file-containing-rho(z)-vs-z-data. This input file is obtained from
# local-charge-density.py script using CHGCAR file.
import numpy as np
import sys
import matplotlib
matplotlib.use('Agg')
from scipy import interpolate
import matplotlib.pyplot as plt 
# We need inset if we need to focus on particular part of the density. Just uncomment 
# all the inset modules in the script.
#from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
#from mpl_toolkits.axes_grid1.inset_locator import mark_inset
def area(filename):
    kappa = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        for k in lines:
            if "#" in k:
                kappa.append(k.split()[0].split('#')[1])
    
    A = np.loadtxt(filename) # It should be a file with data for
    # flat as well as bent structures. Look at the 
    #print(A)
    i = np.where(A == 0.0)[0] #looking for z=0 starting point in the data to 
    # determine the number of different data points to plot.
    
    d = []
    fig, ax = plt.subplots()
    #axins = zoomed_inset_axes(ax, 2.5, loc=2)
    # Writing data for width and integral of the charge density.
    with open("Charge-area.dat", "a") as f:
        if len(i) == 1:             #If we have data for only one curvature.
            x = A[:, 0]
            y = A[:, 1]
            yint = interpolate.UnivariateSpline(x, y, k = 5, s = 0)(x)
            func = interpolate.UnivariateSpline(x, y, k = 5, s = 0)
            d = x[-1] - x[0]
            net = func.integral(0, d)
            ax.plot(x, y, 'bo', label = 'Original')
            ax.plot(x, yint, 'r', label = 'Interpolated')
            plt.savefig('area.pdf', format='pdf',bbox_inches='tight')
            plt.savefig('area.png', format='png',bbox_inches='tight')
            f.write("#" + str(d) + " " + "integral: " + str(round(net, 4)) + '\n') 
        else:
            for j in range(len(i) - 1):
                array = A[i[j]:i[j+1]]
                x = array[:, 0]
                y = array[:, 1]
                if j == 0:
                    max_index = np.where(y == np.max(y))
                    max_pos0 = x[max_index]
                    T = 0
                else:
                    max_index = np.where(y == np.max(y))
                    max_pos = x[max_index]
                    T = max_pos - max_pos0 #we are shifting the plots to the maximum of flat ribbon for better
# visualization.
                d = A[i[j+1] - 1][0]
                yint = interpolate.UnivariateSpline(x, y, k = 5, s = 0)(x)
                func = interpolate.UnivariateSpline(x, y, k = 5, s = 0)
                net = func.integral(0, d)
                #x1, x2, y1, y2 = 6, 8, 0, 0.2
                if j == 0:
                    f.write("Flat: " + " " + str(d) + " " + "integral: " + str(round(net, 4)) + " max: " + str(round(y.max(), 4)) + '\n')

                    ax.plot(x - T, y, label = 'Flat', linewidth=2.0)
                   # axins.plot(x - T, y, label = 'Flat', linewidth=2.0)
                elif 0 < j < len(i) - 2:
                    f.write("kappa: " + str(kappa[j-1]) + " " + str(d) + " " + "integral: " + str(round(net, 4)) + " max: " + str(round(y.max(), 4)) + '\n')

                    ax.plot(x - T, y, label = str(kappa[j-1]), linewidth=2.0)
                    #axins.plot(x - T, y, label = str(kappa[j-1]), linewidth=2.0)
                else:

                    ax.plot(x - T, y, label = str(kappa[j-1]), linewidth=2.0)
                   # axins.plot(x - T, y, label = str(kappa[j-1]), linewidth=2.0)
                    f.write("kappa: " + str(kappa[j-1]) + " " + str(d) + " " + "integral: " + str(round(net, 4)) + " max: " + str(round(y.max(), 4)) + '\n')
                    array2 = A[i[j+1]:]
                    x = array2[:, 0]
                    y = array2[:, 1]
                    max_index = np.where(y == np.max(y))
                    max_pos = x[max_index]
                    T0 = max_pos - max_pos0

                    ax.plot(x - T0, y, label = str(kappa[-1]), linewidth=2.0)
                   # axins.plot(x - T0, y, label = str(kappa[-1]), linewidth=2.0)
                    print(x.shape, y.shape, x[0], y[0])
                    func = interpolate.UnivariateSpline(x, y, k = 5, s = 0)
                    yint = interpolate.UnivariateSpline(x, y, k = 5, s = 0)(x)
                    
                    f.write("kappa: " + str(kappa[-1]) + " " + str(A[-1][0]) + " " + "integral: " + str(round(func.integral(0, x[-1]), 4)) + "max: " + str(y.max()) + '\n')
                    
                ax.plot(np.zeros(2) + max_pos0, np.array([0, 1.5]), 'k--', linewidth=3.0)
                #axins.set_xlim(x1, x2) # apply the x-limits
                #axins.set_ylim(y1, y2) # apply the y-limits
                plt.yticks(visible=False)
                plt.xticks(visible=False)
                ax.legend()
                #plt.title(r'$\boldsymbol{Charge density}$')
                ax.set_xlabel('z' + r'$(\AA)$', fontsize=15)
                ax.set_ylabel('Charge density ', fontsize = 20)
                ax.set_ylim(0, 1.5)
                ax.set_xlim(-2, 10)
               # mark_inset(ax, axins, loc1=2, loc2=4, fc="none", ec="0.5")
                #plt.plot(x - T, yint, 'r', label = 'Interpolated')
                plt.savefig('area.pdf', format='pdf',bbox_inches='tight')
                plt.savefig('area.png', format='png',bbox_inches='tight')

if __name__ == "__main__":
    area(sys.argv[1])
