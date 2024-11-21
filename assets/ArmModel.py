import open3d as o3d
import numpy as np

class ArmModel:
    def __init__(self):
        self.link1Length=5
        self.link2Length=4
        self.link3Length=4
        self.link4Length=3

        self.basePlate=o3d.geometry.TriangleMesh.create_box(5, 0.5, 5)
        self.basePlate.translate((-2.5,0,-2.5))
        self.basePlate.paint_uniform_color([0.522, 1, 0])
        
        self.link1=o3d.geometry.TriangleMesh.create_box(1, self.link1Length, 1)
        self.link1.translate((-0.5,0,-0.5))
        self.link1.paint_uniform_color([1, 0.984, 0])
    
        self.link2=o3d.geometry.TriangleMesh.create_box(1, self.link2Length, 1)
        self.link2.translate((-0.5,0,-0.5))
        self.link2.paint_uniform_color([0.549, 0.541, 0])
        
        self.link3=o3d.geometry.TriangleMesh.create_box(1, self.link3Length, 1)
        self.link3.translate((-0.5,0,-0.5))
        self.link3.paint_uniform_color([0.341, 0.6, 0])
        
        link4 = o3d.geometry.TriangleMesh.create_box(1, self.link4Length, 1)
        endef=o3d.geometry.TriangleMesh.create_box(3,0.1,1)
        rFinger=o3d.geometry.TriangleMesh.create_box(0.1,1.5,1)
        lFinger=o3d.geometry.TriangleMesh.create_box(0.1,1.5,1)
        endef.translate((-1,self.link4Length,0))
        rFinger.translate((-1,self.link4Length,0))
        lFinger.translate((2,self.link4Length,0))
        
        self.link4=link4+endef+rFinger+lFinger
        self.link4.translate((-0.5,0,-0.5))
        self.link4.paint_uniform_color([0.812, 0.369, 0])
        
        self.link1.compute_vertex_normals()
        self.link2.compute_vertex_normals()
        self.link3.compute_vertex_normals()
        self.link4.compute_vertex_normals()
        
        
        