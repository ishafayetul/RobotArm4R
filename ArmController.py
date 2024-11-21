import copy
import numpy as np
import json
from assets.ArmModel import ArmModel
from Kinematics.FK import homogeneousTransformationMatrix
from Kinematics.IK import inverseKinematics
from filelock import FileLock
class ArmController(ArmModel):
    def __init__(self, vis):
        super().__init__()
        self.vis = vis
        self.initialize_geometry()
        self.link1CurrentAngle = self.link2CurrentAngle = self.link3CurrentAngle = self.link4CurrentAngle = 0
        self.hasObject = False
        
    def initialize_geometry(self):
        """Initialize or reset all geometry related to the arm."""
        self.link1_original = copy.deepcopy(self.link1)
        self.link2_original = copy.deepcopy(self.link2)
        self.link3_original = copy.deepcopy(self.link3)
        self.link4_original = copy.deepcopy(self.link4)

        self.vis.add_geometry(self.basePlate)
        self.vis.add_geometry(self.link1)
        self.vis.add_geometry(self.link2)
        self.vis.add_geometry(self.link3)
        self.vis.add_geometry(self.link4)

    def view(self):
        """Set the camera view."""
        view_control = self.vis.get_view_control()
        view_control.set_front([1, 1, 1])  # Direction the camera faces
        view_control.set_lookat([0, 3, 0])  # Point the camera looks at
        view_control.set_up([0, 0.5, 0])    # Up vector for the camera
        view_control.set_zoom(0.8)          # Zoom level
    
    def reset_geometry(self):
        """Reset geometry and re-add all elements."""
        self.vis.remove_geometry(self.link1)
        self.vis.remove_geometry(self.link2)
        self.vis.remove_geometry(self.link3)
        self.vis.remove_geometry(self.link4)
        if self.hasObject:  
            #print("Removing Object")
            self.vis.remove_geometry(self.object)

        self.link1 = copy.deepcopy(self.link1_original)
        self.link2 = copy.deepcopy(self.link2_original)
        self.link3 = copy.deepcopy(self.link3_original)
        self.link4 = copy.deepcopy(self.link4_original)
        if self.hasObject:
            self.object = copy.deepcopy(self.object_original)

        self.vis.add_geometry(self.basePlate)
        self.vis.add_geometry(self.link1)
        self.vis.add_geometry(self.link2)
        self.vis.add_geometry(self.link3)
        self.vis.add_geometry(self.link4)
        if self.hasObject:
            #print("Adding Object")
            self.vis.add_geometry(self.object)

        self.view()

    def transformations(self, theta1, theta2, theta3, theta4):
        """Apply homogeneous transformations and update geometry."""
        self.ht1, self.ht2, self.ht3, self.ht4, self.eep = homogeneousTransformationMatrix(
            theta1, self.link1Length,
            theta2, self.link2Length,
            theta3, self.link3Length,
            theta4, self.link4Length
        )
        self.apply_transforms()

    def apply_transforms(self):
        """Apply transformations to all links and the object if present."""
        self.link1.transform(self.ht1)
        self.link2.transform(self.ht2)
        self.link3.transform(self.ht3)
        self.link4.transform(self.ht4)
        if self.hasObject:
            #print("Moving Object")
            self.object.transform(self.eep)
        
        self.EndEffectorPose(self.eep)
        self.update_visualization()

    def update_visualization(self):
        """Update the visualization and render changes."""
        self.vis.update_geometry(self.link1)
        self.vis.update_geometry(self.link2)
        self.vis.update_geometry(self.link3)
        self.vis.update_geometry(self.link4)
        if self.hasObject:
            #print("Updating Object")
            self.vis.update_geometry(self.object)

        self.view()
        self.vis.poll_events()
        self.vis.update_renderer()

    def moveArm(self, targetTheta1, targetTheta2, targetTheta3, targetTheta4):
        """Move arm from current position to target angles."""
        deltas = [
            (targetTheta1 - self.link1CurrentAngle, 'link1'),
            (targetTheta2 - self.link2CurrentAngle, 'link2'),
            (targetTheta3 - self.link3CurrentAngle, 'link3'),
            (targetTheta4 - self.link4CurrentAngle, 'link4')
        ]
        for delta, link in deltas:
            self.move_link(link, delta)

    def move_link(self, link, delta):
        """Move a specific link to its target angle."""
        direction = 1 if delta >= 0 else -1
        for i in np.arange(0, abs(delta), 0.5):
            self.reset_geometry()
            setattr(self, f'{link}CurrentAngle', getattr(self, f'{link}CurrentAngle') + direction * 0.5)
            self.transformations(self.link1CurrentAngle, self.link2CurrentAngle, self.link3CurrentAngle, self.link4CurrentAngle)
            self.publishArmPose()

    def setInitialPos(self, theta1, theta2, theta3, theta4):
        """Set the initial joint angles and update pose."""
        self.link1CurrentAngle = self.link1InitialAngle = theta1
        self.link2CurrentAngle = self.link2InitialAngle = theta2
        self.link3CurrentAngle = self.link3InitialAngle = theta3
        self.link4CurrentAngle = self.link4InitialAngle = theta4
        self.publishArmPose()
        self.transformations(self.link1InitialAngle, self.link2InitialAngle, self.link3InitialAngle, self.link4InitialAngle)

    def moveArmTo(self, x, y, z):
        """Move the arm to the target coordinates using inverse kinematics."""
        targetTheta1, targetTheta2, targetTheta3, targetTheta4 = inverseKinematics(
            x, y, z, self.link1Length, self.link2Length, self.link3Length, self.link4Length
        )
        #print(targetTheta1, targetTheta2, targetTheta3, targetTheta4)
        self.moveArm(targetTheta1, targetTheta2, targetTheta3, targetTheta4)

    def EndEffectorPose(self, T):
        """Calculate end effector pose (roll, pitch, yaw)."""
        R = T[:3, :3]
        self.yaw = np.degrees(np.arctan2(R[1, 0], R[0, 0]))
        self.pitch = np.degrees(np.arctan2(-R[2, 0], np.sqrt(R[2, 1]**2 + R[2, 2]**2)))
        self.roll = np.degrees(np.arctan2(R[2, 1], R[2, 2]))
        return self.roll, self.pitch, self.yaw

    def moveArmWithObject(self, x, y, z, objO,objC):
        """Move arm with object attached to the end effector."""
        #print("Object Picked Up")
        self.hasObject = True
        self.object_original = objO
        self.object = objC
        self.moveArmTo(x, y, z)
        self.hasObject = False
        return self.object,self.eep[0,3],self.eep[1,3],self.eep[2,3]

    def getCurrentJointAngles(self):
        """Return current joint angles."""
        return self.link1CurrentAngle, self.link2CurrentAngle, self.link3CurrentAngle, self.link4CurrentAngle

    def publishArmPose(self):
        """Publish the arm pose to a JSON file."""
        fileLocation = "config/ArmPose.json"
        with FileLock(fileLocation + ".lock"):
            with open(fileLocation, "r") as file:
                armData = json.load(file)

        armData["joint1"] = self.link1CurrentAngle
        armData["joint2"] = self.link2CurrentAngle
        armData["joint3"] = self.link3CurrentAngle
        armData["joint4"] = self.link4CurrentAngle
        armData["roll"] = self.roll
        armData["pitch"] = self.pitch
        armData["yaw"] = self.yaw
        armData["Ex"] = self.eep[0, 3]
        armData["Ey"] = self.eep[1, 3]
        armData["Ez"] = self.eep[2, 3]
        with FileLock(fileLocation + ".lock"):
            with open(fileLocation, "w") as file:
                json.dump(armData, file, indent=4)
