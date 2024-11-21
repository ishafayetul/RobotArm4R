

#from RotationMatrix import rotationMatrix
import numpy as np

def rotationMatrix(theta, axis, link): 
    theta = np.radians(theta)
    if axis == "y":
        return np.array([
            [np.cos(theta), 0, np.sin(theta), 0],
            [0, 1, 0, link],
            [-np.sin(theta), 0, np.cos(theta), 0],
            [0, 0, 0, 1],
        ])
    elif axis == "x":
        return np.array([
            [1, 0, 0, 0],
            [0, np.cos(theta), -np.sin(theta), link],
            [0, np.sin(theta), np.cos(theta), 0],
            [0, 0, 0, 1],
        ])
    return np.eye(4)

def homogeneousTransformationMatrix(a1,l1, a2,l2, a3,l3, a4,l4):
    ht1 = rotationMatrix(a1, axis="y", link=0)
    ht2 = ht1 @ rotationMatrix(a2, axis="x", link=l1)
    ht3 = ht2 @ rotationMatrix(a3, axis="x", link=l2)
    ht4 = ht3 @ rotationMatrix(a4, axis="x", link=l3)
    ht5 = ht4 @ rotationMatrix(0, axis="x", link=l4)
    return ht1, ht2, ht3, ht4, ht5