from ControlPanel import ControlPanel
from Environment import Environment
import threading
import time
import json
def runRobot():
    env=Environment()
    while(True):
        time.sleep(1)
        with open('config/Command.json', 'r') as file:
            cmd = json.load(file)
        if(cmd['play']*-1 == 1):
            #env.pickNplaceObject((-4.7289, 3, -3.49922), (3.6742, 5, 3.6742))
            #time.sleep(2)
            env.pickNplaceObject((6, 3, 4.5), (3.6742, 5, 3.6742))
            time.sleep(2)
            env.pickNplaceObject((-3, 3, 4.5), (3.6742, 5, 3.6742))
            time.sleep(2)
            env.pickNplaceObject((7, 3, 3), (3.6742, 5, 3.6742))
            time.sleep(2)
        if (cmd['reset']*-1==1):
            env.resetScene()
    env.run()

if __name__ == "__main__":
    panel = ControlPanel()
    robot_thread = threading.Thread(target=runRobot, daemon=True)
    robot_thread.start()
    # Start the Tkinter event loop
    panel.run()
