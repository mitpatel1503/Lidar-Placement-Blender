#
# FILE: lidar_utils.py
#
import bpy
import addon_utils
import range_scanner

def enable_scanner_addon():
    """Enables the Range Scanner add-on."""
    try:
        # Check if it's not already enabled before trying to enable it
        if not addon_utils.check("range_scanner")[1]:
             bpy.ops.preferences.addon_enable(module="range_scanner")
        print("Range Scanner add-on is enabled.")
    except Exception as e:
        print(f"Warning: Could not enable add-on. May already be enabled. {e}")

def run_detailed_rotating_scan(scanner_name, output_dir, output_filename, export=True, add_mesh_to_scene=True):
    scanner_obj = bpy.data.objects.get(scanner_name)
    if not scanner_obj:
        print(f" ERROR: Scanner object named '{scanner_name}' not found")
        return    
    range_scanner.ui.user_interface.scan_rotating(
        bpy.context, 

        scannerObject=scanner_obj,

        # Your specific scan parameters ---
        xStepDegree=0.4, fovX=360.0, yStepDegree=0.33, fovY=270.0, rotationsPerSecond=20,
        reflectivityLower=1.0, distanceLower=0.0, reflectivityUpper=1.0, distanceUpper=99999.9, maxReflectionDepth=10,
        
        # Animation and Noise ---
        enableAnimation=False, frameStart=1, frameEnd=1, frameStep=1, frameRate=1,
        addNoise=False, noiseType='gaussian', mu=0.0, sigma=0.01, noiseAbsoluteOffset=0.0, noiseRelativeOffset=0.0, 
        simulateRain=False, rainfallRate=0.0, 

        # Output and Visualization ---
        addMesh=add_mesh_to_scene,

        # Export Formats ---
        exportLAS=False, 
        exportHDF=False, 
        exportCSV=export,
        exportPLY= False,
        exportSingleFrames=False,
        
        # File Paths ---
        dataFilePath=output_dir, 
        dataFileName=output_filename,
        
        # Debugging ---
        debugLines=False, debugOutput=False, outputProgress=True, measureTime=False, singleRay=False, destinationObject=None, targetObject=None
    )
    
    print("scan complete.")