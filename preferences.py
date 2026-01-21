"""
Addon Preferences Panel

Addon ini hanya bertindak sebagai client untuk layanan AI 3D pihak ketiga.
User harus mendaftar dan menyediakan API key sendiri.

Panel preferensi untuk konfigurasi API keys dan URLs provider.
"""

import bpy
import webbrowser
from bpy.types import AddonPreferences
from bpy.props import StringProperty, BoolProperty, EnumProperty


class AI3DGeneratorPreferences(AddonPreferences):
    """Preferences panel untuk AI 3D Generator addon."""
    
    bl_idname = "ai_3d_generator"
    
    # Active provider tab selection
    active_provider: EnumProperty(
        name="Provider",
        description="Select API provider to configure",
        items=[
            ('TRIPO', "Tripo 3D", "Tripo AI 3D generation service", 'SETTINGS', 0),
            ('MESHY', "Meshy", "Meshy AI 3D generation service", 'SETTINGS', 1),
            ('MODELSLAB', "ModelsLab", "ModelsLab 3D Verse service", 'SETTINGS', 2),
        ],
        default='TRIPO'
    )
    
    # Tripo settings
    tripo_api_key: StringProperty(
        name="API Key",
        description="Tripo API Key (get from https://www.tripo3d.ai/)",
        subtype='PASSWORD'
    )
    
    tripo_base_url: StringProperty(
        name="Base URL",
        description="Tripo API Base URL",
        default="https://platform.tripo3d.ai"
    )
    
    # Meshy settings
    meshy_api_key: StringProperty(
        name="API Key",
        description="Meshy API Key (get from https://www.meshy.ai/)",
        subtype='PASSWORD'
    )
    
    meshy_base_url: StringProperty(
        name="Base URL",
        description="Meshy API Base URL",
        default="https://api.meshy.ai"
    )
    
    # ModelsLab settings
    modelslab_api_key: StringProperty(
        name="API Key",
        description="ModelsLab API Key (get from https://www.modelslab.com/)",
        subtype='PASSWORD'
    )
    
    modelslab_base_url: StringProperty(
        name="Base URL",
        description="ModelsLab / 3D Verse API Base URL",
        default="https://api.modelslab.com"
    )
    
    def draw(self, context):
        """Draw preferences panel."""
        layout = self.layout
        
        # Header
        box_header = layout.box()
        row = box_header.row()
        row.label(text="AI 3D Generator - API Configuration", icon='WORLD')
        
        # Provider tabs
        row = layout.row(align=True)
        row.label(text="Select Provider:", icon='SETTINGS')
        
        row = layout.row(align=True)
        for provider, label, desc, icon, _ in [
            ('TRIPO', "🟦 Tripo 3D", "Configure Tripo API", 'SETTINGS', 0),
            ('MESHY', "🟩 Meshy", "Configure Meshy API", 'SETTINGS', 1),
            ('MODELSLAB', "🟨 ModelsLab", "Configure ModelsLab API", 'SETTINGS', 2),
        ]:
            row.prop_enum(self, "active_provider", provider, text=label, icon='SETTINGS')
        
        # Draw selected provider configuration
        box_provider = layout.box()
        
        if self.active_provider == 'TRIPO':
            self._draw_tripo_config(box_provider, context)
        elif self.active_provider == 'MESHY':
            self._draw_meshy_config(box_provider, context)
        elif self.active_provider == 'MODELSLAB':
            self._draw_modelslab_config(box_provider, context)
    
    def _draw_tripo_config(self, box, context):
        """Draw Tripo configuration."""
        row = box.row()
        row.label(text="TRIPO 3D Configuration", icon='SETTINGS')
        
        # Info
        row = box.row()
        row.label(text="Get your API Key from: https://www.tripo3d.ai/", icon='INFO')
        
        # API Key field
        row = box.row(align=True)
        row.label(text="API Key:", icon='LOCKED')
        row.prop(self, "tripo_api_key", text="")
        
        # Sync button
        row = box.row(align=True)
        row.scale_y = 1.2
        op = row.operator("ai3d.validate_api_key", text="🔄 Sinkronisasi API", icon='FILE_REFRESH')
        op.provider = "TRIPO"
        
        # Base URL
        row = box.row()
        row.prop(self, "tripo_base_url")
        
        # Link buttons
        row = box.row(align=True)
        row.operator("wm.url_open", text="📖 API Documentation", icon='WORLD').url = "https://www.tripo3d.ai/docs"
        row.operator("wm.url_open", text="🌐 Get API Key", icon='WORLD').url = "https://www.tripo3d.ai/signup"
        
        # Status
        row = box.row()
        if self.tripo_api_key:
            row.label(text="✓ API Key configured", icon='CHECKMARK')
        else:
            row.label(text="✗ API Key not set", icon='ERROR')
    
    def _draw_meshy_config(self, box, context):
        """Draw Meshy configuration."""
        row = box.row()
        row.label(text="MESHY Configuration", icon='SETTINGS')
        
        # Info
        row = box.row()
        row.label(text="Get your API Key from: https://www.meshy.ai/", icon='INFO')
        
        # API Key field
        row = box.row(align=True)
        row.label(text="API Key:", icon='LOCKED')
        row.prop(self, "meshy_api_key", text="")
        
        # Sync button
        row = box.row(align=True)
        row.scale_y = 1.2
        op = row.operator("ai3d.validate_api_key", text="🔄 Sinkronisasi API", icon='FILE_REFRESH')
        op.provider = "MESHY"
        
        # Base URL
        row = box.row()
        row.prop(self, "meshy_base_url")
        
        # Link buttons
        row = box.row(align=True)
        row.operator("wm.url_open", text="📖 API Documentation", icon='WORLD').url = "https://www.meshy.ai/docs"
        row.operator("wm.url_open", text="🌐 Get API Key", icon='WORLD').url = "https://www.meshy.ai/signup"
        
        # Status
        row = box.row()
        if self.meshy_api_key:
            row.label(text="✓ API Key configured", icon='CHECKMARK')
        else:
            row.label(text="✗ API Key not set", icon='ERROR')
    
    def _draw_modelslab_config(self, box, context):
        """Draw ModelsLab configuration."""
        row = box.row()
        row.label(text="MODELSLAB / 3D VERSE Configuration", icon='SETTINGS')
        
        # Info
        row = box.row()
        row.label(text="Get your API Key from: https://www.modelslab.com/", icon='INFO')
        
        # API Key field
        row = box.row(align=True)
        row.label(text="API Key:", icon='LOCKED')
        row.prop(self, "modelslab_api_key", text="")
        
        # Sync button
        row = box.row(align=True)
        row.scale_y = 1.2
        op = row.operator("ai3d.validate_api_key", text="🔄 Sinkronisasi API", icon='FILE_REFRESH')
        op.provider = "MODELSLAB"
        
        # Base URL
        row = box.row()
        row.prop(self, "modelslab_base_url")
        
        # Link buttons
        row = box.row(align=True)
        row.operator("wm.url_open", text="📖 API Documentation", icon='WORLD').url = "https://www.modelslab.com/docs"
        row.operator("wm.url_open", text="🌐 Get API Key", icon='WORLD').url = "https://www.modelslab.com/signup"
        
        # Status
        row = box.row()
        if self.modelslab_api_key:
            row.label(text="✓ API Key configured", icon='CHECKMARK')
        else:
            row.label(text="✗ API Key not set", icon='ERROR')


def register():
    """Register preferences class."""
    bpy.utils.register_class(AI3DGeneratorPreferences)


def unregister():
    """Unregister preferences class."""
    bpy.utils.unregister_class(AI3DGeneratorPreferences)
