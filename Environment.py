from assets.CreateTable import CreateTable
from ArmController import ArmController
import open3d as o3d
import json
from CollisionDetection import checkCollision
import copy
from filelock import FileLock
class Environment():
    def __init__(self):
        # Initializes the 3D visualization window and creates the scene
        self.vis = o3d.visualization.Visualizer()
        self.vis.create_window()
        self.createScene()
        self.view()
    def view(self):
        """Set the camera view."""
        view_control = self.vis.get_view_control()
        view_control.set_front([1, 1, 1])  # Direction the camera faces
        view_control.set_lookat([0, 3, 0])  # Point the camera looks at
        view_control.set_up([0, 0.5, 0])    # Up vector for the camera
        view_control.set_zoom(0.8)          # Zoom level
        
    def addTable(self):
        # Loads table data from a JSON file and adds the table to the scene
        with open('config/table.json', 'r') as file:
            tableData = json.load(file)
        self.table = CreateTable(tableData['height'], tableData['width'], tableData['length'], self.vis)
    
    def addArm(self):
        # Initializes the arm controller and adds the robotic arm to the scene
        self.arm = ArmController(self.vis)
        
    def addObject(self):
        # Adds a spherical object to the scene with a specified radius and color, then places it at two locations
        self.objectRadius = 1.5
        self.object = o3d.geometry.TriangleMesh.create_sphere(self.objectRadius)
        self.object.paint_uniform_color([1, 0, 0])  # Red color
        self.object.translate((0, self.objectRadius, 0))
        self.objectCopy = copy.deepcopy(self.object)
        
        # Second object placement at a different location
        self.objectX = 0
        self.objectY = 3
        self.objectZ = 6
        self.objectCopy.translate((self.objectX, 0, self.objectZ))
        
        # Adds the object copy to the visualization
        self.vis.add_geometry(self.objectCopy)
    
    def addFrame(self):
        # Creates and adds a coordinate frame to the scene for reference
        self.frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=5, origin=[0, 0, 0])
        self.frame.translate((-self.table.width/2, 2, -self.table.depth/2))
        self.vis.add_geometry(self.frame)
        
    def createScene(self):
        # Initializes the full scene with table, arm, object, and reference frame
        self.addTable()
        self.addArm()
        self.addObject()
        self.addFrame()
        
        # Set the initial joint angles of the arm
        self.setArmJointAngles([0, 45, 45,45])
        
    def resetScene(self):
        # Clears the current scene and creates a new one
        self.vis.clear_geometries()
        self.vis.update_renderer()
        self.createScene()
    
    def setArmJointAngles(self, angles):
        # Sets the robot arm's joint angles
        angle1, angle2, angle3,angle4 = angles
        self.arm.moveArm(angle1, angle2, angle3,angle4)
    
    def getArmJointAngles(self):
        # Returns the current joint angles of the robotic arm
        return self.arm.getCurrentJointAngles()
    
    def moveArmToGoal(self, goal):
        # Moves the robotic arm to the specified goal coordinates (x, y, z)
        x, y, z = goal
        self.arm.moveArmTo(x, y, z)
    
    def pickNplaceObject(self, placeLocation, restLocation):
        # Simulates a pick-and-place operation with the robot arm:
        # - Move the arm to the goal position above the object
        # - Pick up the object if no collision is detected
        # - Move the arm to a resting position after placing the object
        goal = self.objectX, self.objectY, self.objectZ  # Position of the object
        self.moveArmToGoal(goal)
        
        # Check for potential collision between arm and object
        if checkCollision(self.arm.link4, self.objectCopy):
            self.vis.remove_geometry(self.objectCopy)  # Remove object before picking it up
            
            # Move the arm and pick up the object by linking it with the end effector
            self.objectCopy, self.objectX, self.objectY, self.objectZ = self.arm.moveArmWithObject(
                placeLocation[0], placeLocation[1], placeLocation[2], self.object, self.objectCopy
            )
            self.vis.update_geometry(self.objectCopy)
            
            # Move the arm to the resting position after placing the object
            self.moveArmToGoal(restLocation)
            
            # Detach the object from the arm once it is placed
            self.arm.hasObject = False
            self.vis.update_geometry(self.objectCopy)

    def run(self):
        # Main loop for running the visualization
        self.vis.poll_events()
        self.vis.update_renderer()
        self.vis.run()
