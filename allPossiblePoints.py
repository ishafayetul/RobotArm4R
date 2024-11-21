import numpy as np
import matplotlib.pyplot as plt

# Define link lengths
L1 = 5
L2 = 4
L3 = 3
L4 = 2

# Discretize joint angles (in radians)
a1_range = np.linspace(0, 2 * np.pi, 50)  # Base rotation
a2_range = np.linspace(-np.pi/2, np.pi/2, 50)  # Joint 2
a3_range = np.linspace(-np.pi/2, np.pi/2, 50)  # Joint 3
a4_range = np.linspace(-np.pi/2, np.pi/2, 50)  # Joint 4

# Initialize arrays to store workspace points
X, Y, Z = [], [], []

# Calculate end-effector positions for all combinations of joint angles
for a1 in a1_range:
    for a2 in a2_range:
        for a3 in a3_range:
            for a4 in a4_range:
                Px = np.sin(a1) * (3 * np.sin(a2 + a3) + 4 * np.sin(a2) + 2 * np.sin(a2 + a3 + a4))
                Py = 3 * np.cos(a2 + a3) + 4 * np.cos(a2) + 2 * np.cos(a2 + a3 + a4) + L1
                Pz = np.cos(a1) * (3 * np.sin(a2 + a3) + 4 * np.sin(a2) + 2 * np.sin(a2 + a3 + a4))
                
                X.append(Px)
                Y.append(Py)
                Z.append(Pz)

# Convert to numpy arrays for plotting
X = np.array(X)
Y = np.array(Y)
Z = np.array(Z)

# Plot the workspace in 3D
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X, Y, Z, s=1, c='blue', alpha=0.5)

# Set labels and title
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')
ax.set_title('Workspace of 4-DOF Robotic Arm')

plt.show()
