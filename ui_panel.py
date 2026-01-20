"""
UI Panel untuk AI 3D Generator

Addon ini hanya bertindak sebagai client untuk layanan AI 3D pihak ketiga.
User harus mendaftar dan menyediakan API key sendiri.

Panel UI di 3D View sidebar untuk Text-to-3D dan Image-to-3D generation.
"""

import bpy
from bpy.types import Panel


class AI3DGeneratorPanel(Panel):
    """Panel untuk AI 3D Generator di 3D View sidebar."""
    
    bl_label = "AI 3D Generator"
    bl_idname = "VIEW3D_PT_ai3d_generator"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AI 3D Generator'
    
    def draw(self, context):
        """Draw panel UI."""
        layout = self.layout
        scene = context.scene
        
        # Quick API Setup section
        self._draw_quick_setup(layout, context)
        
        # Provider selection
        box = layout.box()
        box.label(text="Provider Selection", icon='SETTINGS')
        box.prop(scene, "ai3d_provider", expand=False)
        
        # Test connection button
        row = box.row()
        row.operator("ai3d.test_provider", icon='PLAY')
        
        # Tabs dengan panel terpisah untuk Text-to-3D dan Image-to-3D
        row = layout.row()
        row.prop(context.window_manager, 'ai3d_panel_tab', expand=True)
        
        # Tab: Text to 3D
        if context.window_manager.ai3d_panel_tab == 'TEXT':
            self._draw_text_to_3d(layout, scene)
        
        # Tab: Image to 3D
        elif context.window_manager.ai3d_panel_tab == 'IMAGE':
            self._draw_image_to_3d(layout, scene)
        
        # Status section
        self._draw_status(layout, scene)
    
    def _draw_quick_setup(self, layout, context):
        """Draw quick API setup section."""
        box = layout.box()
        box.label(text="🔑 Quick API Setup", icon='KEYFRAME_HLT')
        
        row = box.row(align=True)
        row.scale_y = 1.2
        row.operator("ai3d.open_preferences", text="⚙️ Setup API Keys", icon='PREFERENCES')
        
        # Show API key status
        try:
            prefs = context.preferences.addons['ai_3d_generator'].preferences
            provider = context.scene.ai3d_provider
            
            row = box.row()
            if provider == 'TRIPO' and prefs.tripo_api_key:
                row.label(text="✓ Tripo API configured", icon='CHECKMARK')
            elif provider == 'MESHY' and prefs.meshy_api_key:
                row.label(text="✓ Meshy API configured", icon='CHECKMARK')
            elif provider == 'MODELSLAB' and prefs.modelslab_api_key:
                row.label(text="✓ ModelsLab API configured", icon='CHECKMARK')
            else:
                row.label(text="✗ API key not set for selected provider", icon='ERROR')
        except:
            pass
    
    def _draw_text_to_3d(self, layout, scene):
        """Draw Text to 3D UI."""
        box = layout.box()
        box.label(text="Text to 3D", icon='TEXT')
        
        # Prompt input
        box.prop(scene, "ai3d_prompt", text="Prompt")
        
        # Style selection
        box.prop(scene, "ai3d_style", text="Style")
        
        # Quality slider
        box.prop(scene, "ai3d_quality", slider=True)
        
        # Output format
        box.prop(scene, "ai3d_output_format", text="Format")
        
        # Generate button
        row = box.row(align=True)
        row.scale_y = 1.5
        row.operator("ai3d.generate_text", icon='MESH_DATA')
    
    def _draw_image_to_3d(self, layout, scene):
        """Draw Image to 3D UI."""
        box = layout.box()
        box.label(text="Image to 3D", icon='IMAGE_DATA')
        
        # Image file picker
        box.prop(scene, "ai3d_image_path", text="Image")
        
        # Style selection
        box.prop(scene, "ai3d_style", text="Style")
        
        # Quality slider
        box.prop(scene, "ai3d_quality", slider=True)
        
        # Background removal checkbox
        box.prop(scene, "ai3d_background_removal")
        
        # Output format
        box.prop(scene, "ai3d_output_format", text="Format")
        
        # Generate button
        row = box.row(align=True)
        row.scale_y = 1.5
        row.operator("ai3d.generate_image", icon='MESH_DATA')
    
    def _draw_status(self, layout, scene):
        """Draw status section."""
        if scene.ai3d_current_job_id:
            box = layout.box()
            box.label(text="Generation Status", icon='PROGRESS')
            
            row = box.row()
            row.label(text=f"Job ID: {scene.ai3d_current_job_id[-12:]}", icon='INFO')
            
            row = box.row()
            row.operator("ai3d.check_status", icon='FILE_REFRESH')
            row.operator("ai3d.cancel_generation", icon='X', text="Cancel")


class AI3DGeneratorPreferencesPanel(Panel):
    """Panel untuk akses cepat ke preferences."""
    
    bl_label = "AI 3D Generator Settings"
    bl_idname = "VIEW3D_PT_ai3d_generator_settings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AI 3D Generator'
    
    def draw(self, context):
        """Draw settings panel."""
        layout = self.layout
        
        box = layout.box()
        box.label(text="API Configuration", icon='PREFERENCES')
        
        row = box.row(align=True)
        row.scale_y = 1.2
        row.operator("ai3d.open_preferences", text="Open Preferences", icon='PREFERENCES')
        
        row = box.row()
        row.label(text="Click button di atas untuk setting API keys", icon='INFO')
        row.label(text="dari Tripo, Meshy, atau ModelsLab", icon='INFO')


def register():
    """Register UI panels."""
    bpy.utils.register_class(AI3DGeneratorPanel)
    bpy.utils.register_class(AI3DGeneratorPreferencesPanel)
    
    # Add tab property untuk window manager
    from bpy.types import WindowManager
    from bpy.props import EnumProperty
    
    WindowManager.ai3d_panel_tab = EnumProperty(
        name="AI3D Tab",
        items=[
            ('TEXT', "Text to 3D", "Text to 3D generation"),
            ('IMAGE', "Image to 3D", "Image to 3D generation"),
        ],
        default='TEXT'
    )


def unregister():
    """Unregister UI panels."""
    bpy.utils.unregister_class(AI3DGeneratorPanel)
    bpy.utils.unregister_class(AI3DGeneratorPreferencesPanel)
    
    # Clean up window manager property
    from bpy.types import WindowManager
    if hasattr(WindowManager, 'ai3d_panel_tab'):
        delattr(WindowManager, 'ai3d_panel_tab')
