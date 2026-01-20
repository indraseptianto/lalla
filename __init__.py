"""
AI 3D Generator - Blender Add-on

Addon ini hanya bertindak sebagai client untuk layanan AI 3D pihak ketiga.
User harus mendaftar dan menyediakan API key sendiri.

Unified client untuk beberapa layanan AI 3D generation:
- Tripo 3D
- Meshy
- ModelsLab / 3D Verse

Addon menyediakan UI konsisten untuk Text-to-3D dan Image-to-3D generation.
"""

bl_info = {
    "name": "AI 3D Generator",
    "author": "Palawa Kampa",
    "description": "Unified client untuk AI 3D generation (Tripo, Meshy, ModelsLab)",
    "blender": (3, 0, 0),
    "version": (1, 0, 0),
    "location": "View3D > Sidebar > AI 3D Generator",
    "warning": "",
    "doc_url": "",
    "tracker_url": "",
    "category": "Import-Export"
}

import bpy
from bpy.types import Scene
from bpy.props import StringProperty, IntProperty, BoolProperty, EnumProperty, PointerProperty

from . import preferences
from . import ui_panel
from . import operators


# Register order matters
def register():
    """Register addon."""
    # Register preferences first
    preferences.register()
    
    # Register custom properties
    register_properties()
    
    # Register operators
    operators.register()
    
    # Register UI panels
    ui_panel.register()
    
    print("AI 3D Generator addon registered successfully!")


def unregister():
    """Unregister addon."""
    ui_panel.unregister()
    operators.unregister()
    unregister_properties()
    preferences.unregister()
    
    print("AI 3D Generator addon unregistered!")


def register_properties():
    """Register custom scene properties."""
    # Provider selection
    Scene.ai3d_provider = EnumProperty(
        name="Provider",
        description="Pilih AI 3D provider",
        items=[
            ('TRIPO', "Tripo 3D", "Tripo 3D service"),
            ('MESHY', "Meshy", "Meshy service"),
            ('MODELSLAB', "ModelsLab", "ModelsLab / 3D Verse service"),
        ],
        default='TRIPO'
    )
    
    # Text to 3D properties
    Scene.ai3d_prompt = StringProperty(
        name="Prompt",
        description="Deskripsi object yang ingin dibuat",
        default=""
    )
    
    Scene.ai3d_style = EnumProperty(
        name="Style",
        description="Pilih style generasi model",
        items=[
            ('CARTOON', "Cartoon", "Cartoon style"),
            ('REALISTIC', "Realistic", "Realistic style"),
            ('CLAY', "Clay", "Clay style"),
            ('SCIFI', "Sci-Fi", "Science fiction style"),
        ],
        default='REALISTIC'
    )
    
    Scene.ai3d_quality = IntProperty(
        name="Quality/Detail",
        description="Tingkat detail model (1-10)",
        default=7,
        min=1,
        max=10
    )
    
    Scene.ai3d_output_format = EnumProperty(
        name="Output Format",
        description="Format file model output",
        items=[
            ('GLB', "GLB (Binary)", "GLB format"),
            ('OBJ', "OBJ", "OBJ format"),
            ('FBX', "FBX", "FBX format"),
            ('STL', "STL", "STL format"),
        ],
        default='GLB'
    )
    
    # Image to 3D properties
    Scene.ai3d_image_path = StringProperty(
        name="Image Path",
        description="Path ke image untuk generasi",
        default="",
        subtype='FILE_PATH'
    )
    
    Scene.ai3d_background_removal = BoolProperty(
        name="Background Removal",
        description="Hapus background dari image (jika provider mendukung)",
        default=False
    )
    
    # Generation tracking
    Scene.ai3d_current_job_id = StringProperty(
        name="Current Job ID",
        description="ID job yang sedang berjalan",
        default=""
    )
    
    Scene.ai3d_generation_type = StringProperty(
        name="Generation Type",
        description="Tipe generasi terakhir (text atau image)",
        default=""
    )


def unregister_properties():
    """Unregister custom properties."""
    props = [
        'ai3d_provider',
        'ai3d_prompt',
        'ai3d_style',
        'ai3d_quality',
        'ai3d_output_format',
        'ai3d_image_path',
        'ai3d_background_removal',
        'ai3d_current_job_id',
        'ai3d_generation_type',
    ]
    
    for prop in props:
        if hasattr(Scene, prop):
            delattr(Scene, prop)


if __name__ == "__main__":
    register()
