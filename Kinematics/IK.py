import sympy as sp
from .Solver4R import Solver4R
def rotationMatrix(theta, axis, link): 
    if axis == "y":
        return sp.Matrix([
            [sp.cos(theta), 0, sp.sin(theta), 0],
            [0, 1, 0, link],
            [-sp.sin(theta), 0, sp.cos(theta), 0],
            [0, 0, 0, 1],
        ])
    elif axis == "x":
        return sp.Matrix([
            [1, 0, 0, 0],
            [0, sp.cos(theta), -sp.sin(theta), link],
            [0, sp.sin(theta), sp.cos(theta), 0],
            [0, 0, 0, 1],
        ])
    return sp.eye(4)

def inverseKinematics(x, y, z, l1, l2, l3, l4):
    # Define the joint variables (a1, a2, a3, a4)
    a1, a2, a3, a4 = sp.symbols('a1 a2 a3 a4')
    
    # Define the rotation matrices for each joint
    h1 = rotationMatrix(a1, axis="y", link=0)
    h2 = rotationMatrix(a2, axis="x", link=l1)
    h3 = rotationMatrix(a3, axis="x", link=l2)
    h4 = rotationMatrix(a4, axis="x", link=l3)
    h5 = rotationMatrix(0, axis="x", link=l4)
    
    # Forward kinematics
    ht = h1 * h2 * h3 * h4 * h5

    return Solver4R(x, y, z, l1, l2, l3, l4)

'''
The homogeneous transformation matrix HT is:
[ cos(a1), sin(a1)*sin(a2 + a3 + a4), sin(a1)*cos(a2 + a3 + a4), sin(a1)*(3*sin(a2 + a3) + 4*sin(a2) + 2*sin(a2 + a3 + a4))]
[       0,         cos(a2 + a3 + a4),        -sin(a2 + a3 + a4),       3*cos(a2 + a3) + 4*cos(a2) + 2*cos(a2 + a3 + a4) + 5]
[-sin(a1), cos(a1)*sin(a2 + a3 + a4), cos(a1)*cos(a2 + a3 + a4), cos(a1)*(3*sin(a2 + a3) + 4*sin(a2) + 2*sin(a2 + a3 + a4))]
[       0,                         0,                         0,                                                          1]
'''