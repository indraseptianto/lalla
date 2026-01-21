"""
Operators untuk AI 3D Generator

Addon ini hanya bertindak sebagai client untuk layanan AI 3D pihak ketiga.
User harus mendaftar dan menyediakan API key sendiri.

Operators untuk generate text-to-3D, image-to-3D, test connection, dan polling status.
"""

import bpy
from bpy.types import Operator
from bpy.props import StringProperty
import os
import tempfile

from .providers import TripoClient, MeshyClient, ModelsLabClient
from .downloader import download_and_import_model


def get_provider_client(context):
    """Get current provider client instance.
    
    Compatible with Blender 5.0+ where preferences may be read-only in certain contexts.
    """
    try:
        # Try to get preferences - works in most contexts
        prefs = context.preferences.addons['ai_3d_generator'].preferences
    except (AttributeError, RuntimeError):
        # Fallback for Blender 5.0+ modal contexts where preferences are read-only
        # In this case, we'll get addon from bpy directly
        import bpy
        try:
            addon_prefs = bpy.context.preferences.addons.get('ai_3d_generator')
            if addon_prefs:
                prefs = addon_prefs.preferences
            else:
                return None
        except Exception:
            return None
    
    provider = context.scene.ai3d_provider
    
    if provider == 'TRIPO':
        api_key = prefs.tripo_api_key
        base_url = prefs.tripo_base_url
        return TripoClient(api_key, base_url)
    elif provider == 'MESHY':
        api_key = prefs.meshy_api_key
        base_url = prefs.meshy_base_url
        return MeshyClient(api_key, base_url)
    elif provider == 'MODELSLAB':
        api_key = prefs.modelslab_api_key
        base_url = prefs.modelslab_base_url
        return ModelsLabClient(api_key, base_url)
    
    return None


class AI3DGenerateText(Operator):
    """Generate 3D model dari text prompt."""
    
    bl_idname = "ai3d.generate_text"
    bl_label = "Generate from Text"
    bl_description = "Mulai generasi 3D model dari text prompt"
    
    def execute(self, context):
        """Execute text-to-3D generation."""
        scene = context.scene
        
        # Validate input
        if not scene.ai3d_prompt.strip():
            self.report({'ERROR'}, "Please enter a prompt")
            return {'FINISHED'}
        
        # Get provider client
        client = get_provider_client(context)
        if not client:
            self.report({'ERROR'}, "Provider not configured")
            return {'FINISHED'}
        
        # Check API key
        try:
            prefs = context.preferences.addons['ai_3d_generator'].preferences
        except (AttributeError, RuntimeError):
            # Fallback for Blender 5.0+ modal contexts
            import bpy
            addon_prefs = bpy.context.preferences.addons.get('ai_3d_generator')
            if addon_prefs:
                prefs = addon_prefs.preferences
            else:
                self.report({'ERROR'}, "Cannot access addon preferences")
                return {'FINISHED'}
        
        if not client.api_key:
            self.report({'ERROR'}, "API key not set in preferences")
            return {'FINISHED'}
        
        # Map style
        style_map = {
            'CARTOON': 'cartoon',
            'REALISTIC': 'realistic',
            'CLAY': 'clay',
            'SCIFI': 'sci-fi',
        }
        style = style_map.get(scene.ai3d_style, 'realistic')
        
        # Map format
        format_map = {
            'GLB': 'glb',
            'OBJ': 'obj',
            'FBX': 'fbx',
            'STL': 'stl',
        }
        output_format = format_map.get(scene.ai3d_output_format, 'glb')
        
        # Call API
        result = client.generate_text(
            prompt=scene.ai3d_prompt,
            style=style,
            quality=scene.ai3d_quality,
            output_format=output_format
        )
        
        # Handle result
        if 'error' in result and result['error']:
            self.report({'ERROR'}, result['error'])
            return {'FINISHED'}
        
        if not result.get('job_id'):
            self.report({'ERROR'}, "Failed to get job ID from API")
            return {'FINISHED'}
        
        # Store job info
        scene.ai3d_current_job_id = result['job_id']
        scene.ai3d_generation_type = 'text'
        
        self.report({'INFO'}, f"Generation started (Job ID: {result['job_id'][-12:]})")
        
        # Start polling
        wm = context.window_manager
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}
    
    def modal(self, context, event):
        """Modal for polling status."""
        if event.type == 'TIMER':
            return self._poll_status(context)
        return {'PASS_THROUGH'}
    
    def _poll_status(self, context):
        """Poll generation status."""
        scene = context.scene
        job_id = scene.ai3d_current_job_id
        
        if not job_id:
            return {'FINISHED'}
        
        client = get_provider_client(context)
        result = client.poll_status(job_id)
        
        status = result.get('status', 'unknown')
        
        if status == 'completed':
            model_url = result.get('model_url')
            if model_url:
                # Download and import
                self._download_and_import(context, model_url)
            return {'FINISHED'}
        elif status == 'failed' or status == 'error':
            error = result.get('error', 'Unknown error')
            print(f"Generation failed: {error}")
            return {'FINISHED'}
        
        # Continue polling
        return {'PASS_THROUGH'}
    
    def _download_and_import(self, context, model_url):
        """Download model and import to Blender."""
        try:
            scene = context.scene
            prompt = scene.ai3d_prompt[:20].replace(' ', '_')
            provider = scene.ai3d_provider.lower()
            
            format_ext = {
                'GLB': '.glb',
                'OBJ': '.obj',
                'FBX': '.fbx',
                'STL': '.stl',
            }
            ext = format_ext.get(scene.ai3d_output_format, '.glb')
            
            download_and_import_model(
                model_url=model_url,
                import_type=scene.ai3d_output_format.lower(),
                object_name=f"{provider}_{prompt}"
            )
            
            print(f"Model imported successfully")
        except Exception as e:
            print(f"Import failed: {str(e)}")


class AI3DGenerateImage(Operator):
    """Generate 3D model dari image."""
    
    bl_idname = "ai3d.generate_image"
    bl_label = "Generate from Image"
    bl_description = "Mulai generasi 3D model dari image"
    
    def execute(self, context):
        """Execute image-to-3D generation."""
        scene = context.scene
        
        # Validate input
        if not scene.ai3d_image_path or not os.path.exists(scene.ai3d_image_path):
            self.report({'ERROR'}, "Please select a valid image file")
            return {'FINISHED'}
        
        # Get provider client
        client = get_provider_client(context)
        if not client:
            self.report({'ERROR'}, "Provider not configured")
            return {'FINISHED'}
        
        # Check API key
        if not client.api_key:
            self.report({'ERROR'}, "API key not set in preferences")
            return {'FINISHED'}
        
        # Map style
        style_map = {
            'CARTOON': 'cartoon',
            'REALISTIC': 'realistic',
            'CLAY': 'clay',
            'SCIFI': 'sci-fi',
        }
        style = style_map.get(scene.ai3d_style, 'realistic')
        
        # Map format
        format_map = {
            'GLB': 'glb',
            'OBJ': 'obj',
            'FBX': 'fbx',
            'STL': 'stl',
        }
        output_format = format_map.get(scene.ai3d_output_format, 'glb')
        
        # Call API
        result = client.generate_image(
            image_path=scene.ai3d_image_path,
            style=style,
            quality=scene.ai3d_quality,
            output_format=output_format,
            background_removal=scene.ai3d_background_removal
        )
        
        # Handle result
        if 'error' in result and result['error']:
            self.report({'ERROR'}, result['error'])
            return {'FINISHED'}
        
        if not result.get('job_id'):
            self.report({'ERROR'}, "Failed to get job ID from API")
            return {'FINISHED'}
        
        # Store job info
        scene.ai3d_current_job_id = result['job_id']
        scene.ai3d_generation_type = 'image'
        
        self.report({'INFO'}, f"Generation started (Job ID: {result['job_id'][-12:]})")
        
        # Start polling
        wm = context.window_manager
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}
    
    def modal(self, context, event):
        """Modal for polling status."""
        if event.type == 'TIMER':
            return self._poll_status(context)
        return {'PASS_THROUGH'}
    
    def _poll_status(self, context):
        """Poll generation status."""
        scene = context.scene
        job_id = scene.ai3d_current_job_id
        
        if not job_id:
            return {'FINISHED'}
        
        client = get_provider_client(context)
        result = client.poll_status(job_id)
        
        status = result.get('status', 'unknown')
        
        if status == 'completed':
            model_url = result.get('model_url')
            if model_url:
                # Download and import
                self._download_and_import(context, model_url)
            return {'FINISHED'}
        elif status == 'failed' or status == 'error':
            error = result.get('error', 'Unknown error')
            print(f"Generation failed: {error}")
            return {'FINISHED'}
        
        # Continue polling
        return {'PASS_THROUGH'}
    
    def _download_and_import(self, context, model_url):
        """Download model and import to Blender."""
        try:
            scene = context.scene
            image_name = os.path.splitext(os.path.basename(scene.ai3d_image_path))[0][:20]
            provider = scene.ai3d_provider.lower()
            
            download_and_import_model(
                model_url=model_url,
                import_type=scene.ai3d_output_format.lower(),
                object_name=f"{provider}_{image_name}"
            )
            
            print(f"Model imported successfully")
        except Exception as e:
            print(f"Import failed: {str(e)}")


class AI3DTestProvider(Operator):
    """Test API connection dan validity."""
    
    bl_idname = "ai3d.test_provider"
    bl_label = "Test Provider"
    bl_description = "Test API connection dan API key"
    
    def execute(self, context):
        """Execute connection test."""
        client = get_provider_client(context)
        if not client:
            self.report({'ERROR'}, "Provider not configured")
            return {'FINISHED'}
        
        if not client.api_key:
            self.report({'ERROR'}, "API key not set in preferences")
            return {'FINISHED'}
        
        success, message = client.test_connection()
        
        if success:
            self.report({'INFO'}, message)
        else:
            self.report({'ERROR'}, message)
        
        return {'FINISHED'}


class AI3DCheckStatus(Operator):
    """Check status generasi yang sedang berjalan."""
    
    bl_idname = "ai3d.check_status"
    bl_label = "Check Status"
    bl_description = "Check status generasi saat ini"
    
    def execute(self, context):
        """Execute status check."""
        scene = context.scene
        job_id = scene.ai3d_current_job_id
        
        if not job_id:
            self.report({'WARNING'}, "No active generation job")
            return {'FINISHED'}
        
        client = get_provider_client(context)
        if not client:
            self.report({'ERROR'}, "Provider not configured")
            return {'FINISHED'}
        
        result = client.poll_status(job_id)
        status = result.get('status', 'unknown')
        
        if status == 'completed':
            self.report({'INFO'}, "Generation completed! Importing model...")
            model_url = result.get('model_url')
            if model_url:
                self._download_and_import(context, model_url)
        elif status == 'pending' or status == 'processing':
            self.report({'INFO'}, f"Generation in progress... ({status})")
        elif status == 'failed' or status == 'error':
            error = result.get('error', 'Unknown error')
            self.report({'ERROR'}, f"Generation failed: {error}")
        else:
            self.report({'INFO'}, f"Status: {status}")
        
        return {'FINISHED'}
    
    def _download_and_import(self, context, model_url):
        """Download model and import to Blender."""
        try:
            scene = context.scene
            
            if scene.ai3d_generation_type == 'text':
                name = scene.ai3d_prompt[:20].replace(' ', '_')
            else:
                name = os.path.splitext(os.path.basename(scene.ai3d_image_path))[0][:20]
            
            provider = scene.ai3d_provider.lower()
            
            download_and_import_model(
                model_url=model_url,
                import_type=scene.ai3d_output_format.lower(),
                object_name=f"{provider}_{name}"
            )
            
            print(f"Model imported successfully")
        except Exception as e:
            print(f"Import failed: {str(e)}")


class AI3DCancelGeneration(Operator):
    """Cancel generasi yang sedang berjalan."""
    
    bl_idname = "ai3d.cancel_generation"
    bl_label = "Cancel Generation"
    bl_description = "Cancel generasi yang sedang berjalan"
    
    def execute(self, context):
        """Execute cancel."""
        scene = context.scene
        scene.ai3d_current_job_id = ""
        scene.ai3d_generation_type = ""
        
        self.report({'INFO'}, "Generation cancelled")
        return {'FINISHED'}


class AI3DOpenPreferences(Operator):
    """Open addon preferences window."""
    
    bl_idname = "ai3d.open_preferences"
    bl_label = "Open Preferences"
    bl_description = "Open AI 3D Generator addon preferences"
    
    def execute(self, context):
        """Execute opening preferences."""
        try:
            # Buka preferences window
            bpy.ops.screen.userpref_show('INVOKE_DEFAULT')
            return {'FINISHED'}
        except RuntimeError:
            # Fallback: gunakan invoke sebagai gantinya
            try:
                bpy.ops.preferences.addon_show('INVOKE_DEFAULT', module="ai_3d_generator")
                return {'FINISHED'}
            except Exception as e:
                self.report({'ERROR'}, f"Could not open preferences: {str(e)}")
                return {'FINISHED'}


class AI3DValidateAPIKey(Operator):
    """Validate API key dengan server provider."""
    
    bl_idname = "ai3d.validate_api_key"
    bl_label = "Validate API Key"
    bl_description = "Validate API key dengan provider server"
    
    provider: StringProperty(default="TRIPO")
    
    def execute(self, context):
        """Execute API key validation."""
        try:
            prefs = context.preferences.addons['ai_3d_generator'].preferences
        except (AttributeError, RuntimeError):
            # Fallback
            import bpy
            addon_prefs = bpy.context.preferences.addons.get('ai_3d_generator')
            if addon_prefs:
                prefs = addon_prefs.preferences
            else:
                self.report({'ERROR'}, "Cannot access addon preferences")
                return {'FINISHED'}
        
        # Get provider and API key
        provider = self.provider
        
        if provider == 'TRIPO':
            api_key = prefs.tripo_api_key
            base_url = prefs.tripo_base_url
            client = TripoClient(api_key, base_url)
        elif provider == 'MESHY':
            api_key = prefs.meshy_api_key
            base_url = prefs.meshy_base_url
            client = MeshyClient(api_key, base_url)
        elif provider == 'MODELSLAB':
            api_key = prefs.modelslab_api_key
            base_url = prefs.modelslab_base_url
            client = ModelsLabClient(api_key, base_url)
        else:
            self.report({'ERROR'}, "Unknown provider")
            return {'FINISHED'}
        
        # Check if API key is set
        if not api_key or not api_key.strip():
            self.report({'ERROR'}, f"{provider}: API key not set")
            return {'FINISHED'}
        
        # Validate API key
        is_valid, message = client.validate_api_key()
        
        if is_valid:
            self.report({'INFO'}, f"{provider}: {message}")
        else:
            self.report({'ERROR'}, f"{provider}: {message}")
        
        return {'FINISHED'}


def register():
    """Register operators."""
    bpy.utils.register_class(AI3DGenerateText)
    bpy.utils.register_class(AI3DGenerateImage)
    bpy.utils.register_class(AI3DTestProvider)
    bpy.utils.register_class(AI3DCheckStatus)
    bpy.utils.register_class(AI3DCancelGeneration)
    bpy.utils.register_class(AI3DOpenPreferences)
    bpy.utils.register_class(AI3DValidateAPIKey)


def unregister():
    """Unregister operators."""
    bpy.utils.unregister_class(AI3DGenerateText)
    bpy.utils.unregister_class(AI3DGenerateImage)
    bpy.utils.unregister_class(AI3DTestProvider)
    bpy.utils.unregister_class(AI3DCheckStatus)
    bpy.utils.unregister_class(AI3DCancelGeneration)
    bpy.utils.unregister_class(AI3DOpenPreferences)
    bpy.utils.unregister_class(AI3DValidateAPIKey)
