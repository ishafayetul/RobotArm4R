import numpy as np
import open3d as o3d

def computeOBBVertices(cube):
    # Compute the oriented bounding box (OBB)
    obb = cube.get_oriented_bounding_box()
    center = obb.center
    rotation = obb.R
    extent = obb.extent

    # Compute the 8 vertices of the OBB
    vertices = []
    for sign in np.array([[1, 1, 1], [1, 1, -1], [1, -1, 1], [1, -1, -1],
                          [-1, 1, 1], [-1, 1, -1], [-1, -1, 1], [-1, -1, -1]]):
        vertex = center + np.dot(rotation, sign * extent)
        vertices.append(vertex)
    return np.array(vertices)

def checkCollision(cube1, cube2):
    # Get the vertices of the two cubes
    vertices1 = computeOBBVertices(cube1)
    vertices2 = computeOBBVertices(cube2)

    # Get the rotation matrices of the cubes
    obb1 = cube1.get_oriented_bounding_box()
    obb2 = cube2.get_oriented_bounding_box()
    rotation1 = obb1.R
    rotation2 = obb2.R

    # Get the axes of the OBBs (each OBB has its own coordinate system)
    axes1 = [rotation1[:, i] for i in range(3)]
    axes2 = [rotation2[:, i] for i in range(3)]
    
    # Combine axes from both OBBs
    axes = axes1 + axes2

    # Check for separation along each axis using the projection of the OBBs onto the axes
    for axis in axes:
        # Project both OBBs onto the axis
        projection1 = np.dot(vertices1, axis)
        projection2 = np.dot(vertices2, axis)

        # Find the min and max projections for both OBBs
        min_proj1, max_proj1 = np.min(projection1), np.max(projection1)
        min_proj2, max_proj2 = np.min(projection2), np.max(projection2)

        # Check for overlap between the projections
        if max_proj1 < min_proj2 or max_proj2 < min_proj1:
            return False  # No overlap along this axis, no collision

    return True  # Overlap along all axes, collision detected

