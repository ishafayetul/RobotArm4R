import open3d as o3d
import numpy as np

class ObjectModel:
    def __init__(self,radius,x,y,z):
        self.radius=radius
        self.sphere=o3d.geometry.TriangleMesh.create_sphere(radius=self.radius)
        self.ht=np.array([
            [1,0,0,x],
            [0,1,0,y],
            [0,0,1,z],
            [0,0,0,1]
        ])
        self.sphere.transform(self.ht)
        self.sphere.paint_uniform_color([1,0,0])
        