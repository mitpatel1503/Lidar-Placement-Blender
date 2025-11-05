
import urdfpy
import numpy as np
import os
import sys
import blender_utils 

np.float = float    
np.int = int   
np.object = object    
np.bool = bool


def load_and_verify_urdf(path, package_dirs=None):
    """Reads the URDF, verifies its data, and returns the urdfpy object."""
    print(f"\n Starting URDF Read Process")
    if not os.path.exists(path):
        print(f"ERROR: URDF file not found at: {path}")
        sys.exit(1)
        
    try:
        model = urdfpy.URDF.load(path)
        _ = model.visual_geometry_fk(cfg={}) 
        print(f"SUCCESS: Data read for {model.name} passed. {len(model.links)} links found.")
        return model
    except Exception as e:
        print(f"ERROR: Failed to parse URDF data. Error: {e}")
        sys.exit(1)

def link_positions(model_data, base_position=(0, 0, 0)):
    """
    Calculates the world pose for every link, offset by a given base position.
    """
    cfg = {}  # Empty config means zero joint angles
    relative_poses = model_data.link_fk(cfg=cfg)
    base_translation_matrix = np.identity(4)
    base_translation_matrix[:3, 3] = base_position
    
    world_poses = {}
    print("WORLD POSES (Offset by Base Position) ")
    for link_object, matrix_np in relative_poses.items():
        world_matrix = base_translation_matrix @ matrix_np
        world_poses[link_object.name] = world_matrix
        
        location = world_matrix[:3, 3]
        print(f"\n--- Link: {link_object.name} ---")
        print(f"  Location (XYZ): {np.around(location, 4)} (meters)")
        
    print("\nKinematic calculation complete.")
    return world_poses

def get_link_position(all_poses_dict, link_name):
    """
    Retrieves a specific link's XYZ position from a pre-calculated poses dictionary.
    """
    pose_matrix = all_poses_dict.get(link_name)
    if pose_matrix is not None:
        location_xyz = pose_matrix[:3, 3]
        return location_xyz
    else:
        print(f" Link '{link_name}' not found in the provided pose data.")
        return None

def find_closest_link(target_pos, all_link_poses):
    """Finds the link in a pose dictionary closest to a target XYZ position."""
    if target_pos is None or not all_link_poses:
        return None, float('inf')

    closest_link_name = None
    min_distance = float('inf') 

    for link_name, pose_matrix in all_link_poses.items():
        link_pos = pose_matrix[:3, 3]
        distance = np.linalg.norm(target_pos - link_pos)
        
        if distance < min_distance:
            min_distance = distance
            closest_link_name = link_name
            
    return closest_link_name, min_distance

