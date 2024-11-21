import tkinter as tk
import json
from Environment import Environment
from filelock import FileLock

class ControlPanel:
    def __init__(self):
        # Initialize the window, labels, buttons, and start periodic updates
        self.setWindow()
        self.setLabels()
        self.setButtons()
        self.update_angles_periodically()
        self.playFlag = False
        self.resetFlag = False
        self.command_path = "config/Command.json"
        self.armPose_path = "config/ArmPose.json"
        self.command_locker = "config/Command.json.lock"
        self.armPose_locker = "config/ArmPose.json.lock"
        
        # Lock and read the current command, setting initial play/reset states
        with FileLock(self.command_locker):
            with open('config/Command.json', 'r') as file:
                cmd = json.load(file)
        cmd["play"] = 1
        cmd["reset"] = 1
        with FileLock(self.command_locker):
            with open('config/Command.json', 'w') as file:
                json.dump(cmd, file, indent=4)

    def update_angles(self):
        # Read the current arm pose and update the labels with the joint angles and roll/pitch/yaw values
        with FileLock("config/ArmPose.json.lock"):
            with open('config/ArmPose.json', 'r') as file:
                armPose = json.load(file)
        self.angle1_value.config(text=f"Angle1: {armPose['joint1']}°")
        self.angle2_value.config(text=f"Angle2: {armPose['joint2']}°")
        self.angle3_value.config(text=f"Angle3: {armPose['joint3']}°")
        self.angle4_value.config(text=f"Angle4: {armPose['joint4']}°")
        self.roll_label.config(text=f"Roll: {armPose['roll']:.2f}°")
        self.pitch_label.config(text=f"Pitch: {armPose['pitch']:.2f}°")
        self.yaw_label.config(text=f"Yaw: {armPose['yaw']:.2f}°")

    def setWindow(self):
        # Create the main window with a title and fixed size
        self.root = tk.Tk()
        self.root.title("Robot Arm Controller")
        self.root.geometry("400x200")
        self.root.resizable(False, False)

    def setLabels(self):
        # Set up the labels for displaying roll, pitch, yaw, and joint angles
        self.rpy_frame = tk.Frame(self.root)
        self.rpy_frame.pack()
        self.roll_label = tk.Label(self.rpy_frame, text="Roll: 0°", font=("Arial", 14))
        self.roll_label.pack(side="left", padx=0)
        self.pitch_label = tk.Label(self.rpy_frame, text="Pitch: 0°", font=("Arial", 14))
        self.pitch_label.pack(side="left", padx=0)
        self.yaw_label = tk.Label(self.rpy_frame, text="Yaw: 0°", font=("Arial", 14))
        self.yaw_label.pack(side="left", padx=0)

        self.angle_frame = tk.Frame(self.root)
        self.angle_frame.pack()
        self.angle1_value = tk.Label(self.angle_frame, text="Angle1: 0°", font=("Arial", 14))
        self.angle1_value.pack()
        self.angle2_value = tk.Label(self.angle_frame, text="Angle2: 0°", font=("Arial", 14))
        self.angle2_value.pack()
        self.angle3_value = tk.Label(self.angle_frame, text="Angle3: 0°", font=("Arial", 14))
        self.angle3_value.pack()
        self.angle4_value = tk.Label(self.angle_frame, text="Angle4: 0°", font=("Arial", 14))
        self.angle4_value.pack()

    def setButtons(self):
        # Set up the "Play" and "Reset" buttons with their respective commands
        self.play_button = tk.Button(self.root, text="Play", font=("Arial", 14), width=13, command=self.playButton)
        self.play_button.pack(side="left", padx=0)
        self.reset_button = tk.Button(self.root, text="Reset", font=("Arial", 14), width=13, command=self.resetButton)
        self.reset_button.pack(side="right", padx=0)

    def playButton(self, event=None):
        # Toggle the play state and update the button text
        with FileLock(self.command_locker):
            with open("config/Command.json", "r") as file:
                status = json.load(file)
        if(self.playFlag):
            self.play_button.config(text="Pause")
            self.playFlag = False
            status["play"] = -1
        else:
            self.play_button.config(text="Play")
            self.playFlag = True
            status["play"] = 1
        with FileLock(self.command_locker):
            with open("config/Command.json", "w") as file:
                json.dump(status, file, indent=4)

    def resetButton(self, event=None):
        # Toggle the reset state and update the button text
        with FileLock(self.command_locker):
            with open("config/Command.json", "r") as file:
                status = json.load(file)
        if(self.resetFlag):
            self.reset_button.config(text="Done!!")
            self.resetFlag = False
            status["reset"] = -1
        else:
            self.reset_button.config(text="Reset")
            self.resetFlag = True
            status["reset"] = 1
        with FileLock(self.command_locker):
            with open("config/Command.json", "w") as file:
                json.dump(status, file, indent=4)

    def update_angles_periodically(self):
        # Periodically update the angles every 500 ms
        self.update_angles()
        self.root.after(500, self.update_angles_periodically)

    def run(self):
        # Start the Tkinter event loop to run the GUI
        self.root.mainloop()
