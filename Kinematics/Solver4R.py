import numpy as np
from scipy.optimize import fsolve

# Constants
def Solver4R(x,y,z,l1,l2,l3,l4):
    # Function to solve
    def equations(variables):
        a1, a2, a3, a4 = variables
        eq1 = np.tan(np.radians(a1)) - (x / z)
        eq2 = a2 + a3 + a4 - 180
        eq3 = l2 * np.cos(np.radians(a2)) - l3 * np.cos(np.radians(a4)) - (y + l4 - l1)
        eq4 = l3 * np.sin(np.radians(a4)) + l2 * np.sin(np.radians(a2)) - ((z / np.cos(np.radians(a1))) + l4)
        return [eq1, eq2, eq3, eq4]

    initial_guess = [0, 0, 0, 0]
    solution = fsolve(equations, initial_guess)
    a1, a2, a3, a4 = solution
    return a1, a2, a3, a4
