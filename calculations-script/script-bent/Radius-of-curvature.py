from sympy import sin
from sympy.abc import x
from sympy import nsolve
import sys

#distance between 2 metallic edge atoms
d0 = float(sys.argv[1]) #Flat nanoribbons 
d  = float(sys.argv[2]) #bent nanoribbons
kappa = nsolve(sin(d0*x/2.0)-(d*x/2.0), 0.05)

# determining bending curvature from our relax structures.
print(1/kappa)
