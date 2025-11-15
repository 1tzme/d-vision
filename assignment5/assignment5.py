import open3d as o3d
import numpy as np
import copy

# ========================================
# CONFIGURATION: Set model path here
# ========================================
MODEL_PATH = "models/model.ply"
# recommended to use .ply format

def print_separator(step_number, step_name):
    """Print separator between steps"""
    print("\n" + "="*80)
    print(f"  STEP {step_number}: {step_name}")
    print("="*80)


def print_mesh_info(mesh, step_name="Mesh"):
    """Print mesh information"""
    bbox = mesh.get_axis_aligned_bounding_box()
    extent = bbox.get_extent()
    print(f"\n{step_name}:")
    print(f"  Number of vertices: {len(mesh.vertices)}")
    print(f"  Number of triangles: {len(mesh.triangles)}")
    print(f"  Bounding box size: X={extent[0]:.4f}, Y={extent[1]:.4f}, Z={extent[2]:.4f}")
    print(f"  Has vertex colors: {'Yes' if mesh.has_vertex_colors() else 'No'}")
    print(f"  Has vertex normals: {'Yes' if mesh.has_vertex_normals() else 'No'}")


def print_pointcloud_info(pcd, step_name="Point Cloud"):
    """Print point cloud information"""
    print(f"\n{step_name}:")
    print(f"  Number of points: {len(pcd.points)}")
    print(f"  Has colors: {'Yes' if pcd.has_colors() else 'No'}")
    print(f"  Has normals: {'Yes' if pcd.has_normals() else 'No'}")


def print_voxel_info(voxel_grid, step_name="Voxel Grid"):
    """Print voxel grid information"""
    print(f"\n{step_name}:")
    voxels = voxel_grid.get_voxels()
    print(f"  Number of voxels: {len(voxels)}")
    print(f"  Voxel size: {voxel_grid.voxel_size}")


# ========================================
# STEP 1: Loading and Visualization
# ========================================
def step1_load_and_visualize():
    print_separator(1, "Loading and Visualization")
    
    mesh = o3d.io.read_triangle_mesh(MODEL_PATH)
    
    if len(mesh.triangles) == 0:
        print("\nNote: Model has no triangles. Loading as point cloud...")
        pcd_direct = o3d.io.read_point_cloud(MODEL_PATH)
        
        if len(pcd_direct.points) > 0:
            print("Creating mesh from point cloud...")
            pcd_direct.estimate_normals()
            mesh, _ = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd_direct, depth=8)
            mesh.compute_vertex_normals()
        else:
            raise RuntimeError(f"Could not load model from {MODEL_PATH}. Check file path!")
    else:
        if not mesh.has_vertex_normals():
            mesh.compute_vertex_normals()
    
    print("\nModel loaded successfully!")
    print_mesh_info(mesh, "Original Model")
    
    print("\n>>> Opening visualization window...")
    print(">>> Close window to continue")
    o3d.visualization.draw_geometries([mesh], 
                                      window_name="Step 1: Original Model",
                                      width=1024, height=768)
    
    return mesh


# ========================================
# STEP 2: Conversion to Point Cloud
# ========================================
def step2_convert_to_pointcloud(mesh):
    print_separator(2, "Conversion to Point Cloud")
    
    pcd = mesh.sample_points_uniformly(number_of_points=10000)
    
    print("\nConverted to point cloud!")
    print_pointcloud_info(pcd, "Point Cloud")
    
    print("\n>>> Opening visualization window...")
    print(">>> Close window to continue")
    o3d.visualization.draw_geometries([pcd], 
                                      window_name="Step 2: Point Cloud",
                                      width=1024, height=768)
    
    return pcd


# ========================================
# STEP 3: Surface Reconstruction
# ========================================
def step3_surface_reconstruction(pcd):
    print_separator(3, "Surface Reconstruction from Point Cloud")
    
    print("\nEstimating normals...")
    pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(
        radius=0.1, max_nn=30))
    pcd.orient_normals_consistent_tangent_plane(k=15)
    
    print("Performing Poisson reconstruction...")
    mesh_recon, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
        pcd, depth=9)
    
    print("Removing artifacts...")
    vertices_to_remove = densities < np.quantile(densities, 0.05)
    mesh_recon.remove_vertices_by_mask(vertices_to_remove)
    
    bbox = pcd.get_axis_aligned_bounding_box()
    mesh_cropped = mesh_recon.crop(bbox)
    mesh_cropped.compute_vertex_normals()
    
    print_mesh_info(mesh_cropped, "Reconstructed Surface")
    
    print("\n>>> Opening visualization window...")
    print(">>> Close window to continue")
    o3d.visualization.draw_geometries([mesh_cropped], 
                                      window_name="Step 3: Reconstructed Surface",
                                      width=1024, height=768)
    
    return mesh_cropped


# ========================================
# STEP 4: Voxelization
# ========================================
def step4_voxelization(pcd):
    print_separator(4, "Voxelization")
    
    # Adaptive voxel size based on model dimensions
    bbox = pcd.get_axis_aligned_bounding_box()
    extent = bbox.get_extent()
    max_dimension = max(extent)
    
    # Use 1/100 of the largest dimension for good detail
    voxel_size = max_dimension / 100.0
    
    print(f"\nModel bounding box extent: {extent}")
    print(f"Max dimension: {max_dimension:.4f}")
    print(f"Auto-calculated voxel size: {voxel_size:.6f}")
    print(f"Creating voxel grid...")
    
    voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(pcd, voxel_size=voxel_size)
    
    print_voxel_info(voxel_grid, "Voxel Grid")
    
    print("\n>>> Opening visualization window...")
    print(">>> Close window to continue")
    o3d.visualization.draw_geometries([voxel_grid],
                                      window_name="Step 4: Voxelization",
                                      width=1024, height=768)
    
    return voxel_grid


# ========================================
# STEP 5: Adding a Plane
# ========================================
def step5_add_plane(pcd):
    print_separator(5, "Adding a Plane")
    
    center = pcd.get_center()
    extent = pcd.get_max_bound() - pcd.get_min_bound()
    
    plane_height = extent[1] * 1.5
    plane_depth = extent[2] * 1.5
    
    plane = o3d.geometry.TriangleMesh.create_box(
        width=0.002,
        height=plane_height, 
        depth=plane_depth)
    
    plane_center = center.copy()
    plane_center[0] = center[0]
    
    plane.translate(plane_center - plane.get_center())
    plane.paint_uniform_color([1.0, 0.3, 0.0])
    plane.compute_vertex_normals()
    
    pcd_with_plane = copy.deepcopy(pcd)
    
    print(f"\nPlane created: 0.002 x {plane_height:.3f} x {plane_depth:.3f}")
    print(f"Position (center): {plane_center}")
    
    print("\n>>> Opening visualization window...")
    print(">>> Close window to continue")
    o3d.visualization.draw_geometries([pcd_with_plane, plane], 
                                      window_name="Step 5: Object with Plane",
                                      width=1024, height=768)
    
    return center


# ========================================
# STEP 6: Surface Clipping
# ========================================
def step6_surface_clipping(pcd, plane_center):
    print_separator(6, "Surface Clipping")
    
    points = np.asarray(pcd.points)
    
    plane_normal = np.array([1, 0, 0])
    plane_point = plane_center
    
    distances = np.dot(points - plane_point, plane_normal)
    mask = distances < 0
    
    pcd_clipped = o3d.geometry.PointCloud()
    pcd_clipped.points = o3d.utility.Vector3dVector(points[mask])
    
    if pcd.has_colors():
        colors = np.asarray(pcd.colors)
        pcd_clipped.colors = o3d.utility.Vector3dVector(colors[mask])
    
    if pcd.has_normals():
        normals = np.asarray(pcd.normals)
        pcd_clipped.normals = o3d.utility.Vector3dVector(normals[mask])
    
    print_pointcloud_info(pcd_clipped, "Clipped Point Cloud")
    print(f"  Points removed: {len(pcd.points) - len(pcd_clipped.points)}")
    print(f"  Points remaining: {len(pcd_clipped.points)}")
    
    print("\n>>> Opening visualization window...")
    print(">>> Close window to continue")
    o3d.visualization.draw_geometries([pcd_clipped], 
                                      window_name="Step 6: Clipped Point Cloud",
                                      width=1024, height=768)
    
    return pcd_clipped


# ========================================
# STEP 7: Color and Extremes
# ========================================
def step7_color_and_extremes(pcd_clipped):
    print_separator(7, "Color and Extremes")
    
    points = np.asarray(pcd_clipped.points)
    
    axis = 2  # 0=X, 1=Y, 2=Z
    axis_name = ['X', 'Y', 'Z'][axis]
    
    min_value = points[:, axis].min()
    max_value = points[:, axis].max()
    
    min_idx = np.argmin(points[:, axis])
    max_idx = np.argmax(points[:, axis])
    min_point = points[min_idx]
    max_point = points[max_idx]
    
    print(f"\nApplying color gradient along {axis_name}-axis...")
    print(f"  Minimum: {min_value:.4f} at {min_point}")
    print(f"  Maximum: {max_value:.4f} at {max_point}")
    
    normalized = (points[:, axis] - min_value) / (max_value - min_value)
    colors = np.zeros((len(points), 3))
    colors[:, 0] = normalized
    colors[:, 2] = 1 - normalized
    
    pcd_colored = copy.deepcopy(pcd_clipped)
    pcd_colored.colors = o3d.utility.Vector3dVector(colors)
    
    sphere_min = o3d.geometry.TriangleMesh.create_sphere(radius=0.01)
    sphere_min.translate(min_point)
    sphere_min.paint_uniform_color([0, 1, 0])
    sphere_min.compute_vertex_normals()
    
    sphere_max = o3d.geometry.TriangleMesh.create_sphere(radius=0.01)
    sphere_max.translate(max_point)
    sphere_max.paint_uniform_color([1, 1, 0])
    sphere_max.compute_vertex_normals()
    
    print(f"\nGradient applied! Colors: blue (min) to red (max)")
    print(f"Extremes highlighted: green (min), yellow (max)")
    
    print("\n>>> Opening visualization window...")
    print(">>> Close window to finish")
    o3d.visualization.draw_geometries([pcd_colored, sphere_min, sphere_max], 
                                      window_name="Step 7: Color Gradient & Extremes",
                                      width=1024, height=768)
    
    return pcd_colored


# ========================================
# MAIN FUNCTION
# ========================================
def main():
    print("\n" + "="*80)
    print("  ASSIGNMENT 5 - 3D VISUALIZATION WITH OPEN3D")
    print("="*80)
    print(f"\nModel path: {MODEL_PATH}")
    print("\nNote: Visualization window will open after each step.")
    print("Close the window to proceed to the next step.\n")
    
    input("Press Enter to start...")
    
    # Step 1: Load and visualize
    mesh = step1_load_and_visualize()
    
    # Step 2: Convert to point cloud
    pcd = step2_convert_to_pointcloud(mesh)
    
    # Step 3: Surface reconstruction
    step3_surface_reconstruction(pcd)
    
    # Step 4: Voxelization
    step4_voxelization(pcd)
    
    # Step 5: Add plane
    plane_center = step5_add_plane(pcd)
    
    # Step 6: Clipping
    pcd_clipped = step6_surface_clipping(pcd, plane_center)
    
    # Step 7: Color and extremes
    step7_color_and_extremes(pcd_clipped)
    
    print("\n" + "="*80)
    print("\nSummary:")
    print("✓ Step 1: Loaded and visualized 3D model")
    print("✓ Step 2: Converted to point cloud")
    print("✓ Step 3: Reconstructed surface using Poisson")
    print("✓ Step 4: Created voxel grid")
    print("✓ Step 5: Added plane to scene")
    print("✓ Step 6: Clipped surface (removed right half)")
    print("✓ Step 7: Applied color gradient and highlighted extremes")
    print("\nAll steps completed")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
