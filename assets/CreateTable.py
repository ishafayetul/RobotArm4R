import open3d as o3d

class CreateTable: 
    def __init__(self,height,width,length,vis):
        self.vis=vis
        self.width=width
        self.height=height
        self.depth=length
        self.table=self.drawTable()
        self.vis.add_geometry(self.table)
        
    def drawTable(self):
        topSurface=o3d.geometry.TriangleMesh.create_box(self.width, 1,self.depth)
        topSurface.translate((0,0,0),relative=False)
        
        leg=[]
        for i in range(4):
            leg.append(o3d.geometry.TriangleMesh.create_box(1,self.height,1))
            
        leg[0].translate((-self.width/2,-self.height,-self.depth/2))
        leg[1].translate((self.width/2-1,-self.height,-self.depth/2))
        leg[2].translate((-self.width/2,-self.height,self.depth/2-1))
        leg[3].translate((self.width/2-1,-self.height,self.depth/2-1))
        
        table=topSurface+leg[0]+leg[1]+leg[2]+leg[3]
        table.paint_uniform_color([0.133,0.529,0.502])
        return table
    
    def viewTable(self,vis):
        vis.add_geometry(self.table)
        return vis