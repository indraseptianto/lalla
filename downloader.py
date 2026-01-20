"""
Model Downloader dan Importer

Addon ini hanya bertindak sebagai client untuk layanan AI 3D pihak ketiga.
User harus mendaftar dan menyediakan API key sendiri.

Utility untuk download model dari provider dan import ke Blender.
"""

import bpy
import os
import tempfile
import requests
from pathlib import Path


def download_and_import_model(model_url: str, import_type: str, object_name: str):
    """
    Download model dari URL dan import ke Blender scene.
    
    Args:
        model_url: URL model file
        import_type: Tipe import (glb, obj, fbx, stl)
        object_name: Nama object di Blender scene
    """
    if not model_url:
        raise ValueError("Model URL is empty")
    
    # Download model file
    temp_path = download_model_file(model_url, import_type)
    
    if not temp_path or not os.path.exists(temp_path):
        raise RuntimeError("Failed to download model file")
    
    # Import berdasarkan format
    try:
        if import_type.lower() in ['glb', 'gltf']:
            _import_gltf(temp_path, object_name)
        elif import_type.lower() == 'obj':
            _import_obj(temp_path, object_name)
        elif import_type.lower() == 'fbx':
            _import_fbx(temp_path, object_name)
        elif import_type.lower() == 'stl':
            _import_stl(temp_path, object_name)
        else:
            raise ValueError(f"Unsupported format: {import_type}")
    finally:
        # Cleanup temp file
        try:
            os.remove(temp_path)
        except:
            pass


def download_model_file(model_url: str, file_type: str = None) -> str:
    """
    Download model file dari URL ke temp folder.
    
    Returns:
        Path ke file yang di-download
    """
    try:
        # Determine file extension
        if file_type:
            ext = f".{file_type.lower()}"
        else:
            # Try to get from URL
            if ".glb" in model_url:
                ext = ".glb"
            elif ".obj" in model_url:
                ext = ".obj"
            elif ".fbx" in model_url:
                ext = ".fbx"
            elif ".stl" in model_url:
                ext = ".stl"
            else:
                ext = ".glb"  # default
        
        # Download file
        response = requests.get(model_url, timeout=300, stream=True)
        response.raise_for_status()
        
        # Save to temp file
        temp_dir = tempfile.gettempdir()
        temp_file = os.path.join(temp_dir, f"ai3d_model_{id(model_url)}{ext}")
        
        with open(temp_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        print(f"Model downloaded to: {temp_file}")
        return temp_file
    
    except requests.exceptions.RequestException as e:
        print(f"Download error: {str(e)}")
        raise
    except Exception as e:
        print(f"Error downloading model: {str(e)}")
        raise


def _import_gltf(filepath: str, object_name: str):
    """Import GLTF/GLB file ke Blender."""
    try:
        # Clear selection
        bpy.ops.object.select_all(action='DESELECT')
        
        # Import model
        bpy.ops.import_scene.gltf(filepath=filepath)
        
        # Rename imported objects
        # Biasanya GLTF import mengimpor dengan nama default
        # Cari object yang baru di-select
        for obj in bpy.context.selected_objects:
            if obj.type in ['MESH', 'ARMATURE']:
                obj.name = object_name
                break
        
        # Center view pada object
        bpy.ops.view3d.view_all()
        
        print(f"Imported GLTF/GLB as: {object_name}")
    
    except Exception as e:
        print(f"GLTF import error: {str(e)}")
        raise


def _import_obj(filepath: str, object_name: str):
    """Import OBJ file ke Blender."""
    try:
        # Clear selection
        bpy.ops.object.select_all(action='DESELECT')
        
        # Import model
        bpy.ops.import_scene.obj(filepath=filepath)
        
        # Rename imported object
        for obj in bpy.context.selected_objects:
            if obj.type == 'MESH':
                obj.name = object_name
                break
        
        # Center view pada object
        bpy.ops.view3d.view_all()
        
        print(f"Imported OBJ as: {object_name}")
    
    except Exception as e:
        print(f"OBJ import error: {str(e)}")
        raise


def _import_fbx(filepath: str, object_name: str):
    """Import FBX file ke Blender."""
    try:
        # Clear selection
        bpy.ops.object.select_all(action='DESELECT')
        
        # Import model
        bpy.ops.import_scene.fbx(filepath=filepath)
        
        # Rename imported object
        for obj in bpy.context.selected_objects:
            if obj.type in ['MESH', 'ARMATURE']:
                obj.name = object_name
                break
        
        # Center view pada object
        bpy.ops.view3d.view_all()
        
        print(f"Imported FBX as: {object_name}")
    
    except Exception as e:
        print(f"FBX import error: {str(e)}")
        raise


def _import_stl(filepath: str, object_name: str):
    """Import STL file ke Blender."""
    try:
        # Clear selection
        bpy.ops.object.select_all(action='DESELECT')
        
        # Import model
        bpy.ops.import_mesh.stl(filepath=filepath)
        
        # Rename imported object
        for obj in bpy.context.selected_objects:
            if obj.type == 'MESH':
                obj.name = object_name
                break
        
        # Center view pada object
        bpy.ops.view3d.view_all()
        
        print(f"Imported STL as: {object_name}")
    
    except Exception as e:
        print(f"STL import error: {str(e)}")
        raise
