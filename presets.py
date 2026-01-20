"""
Presets Management untuk AI 3D Generator

Menyimpan dan mengelola presets generation yang dapat digunakan kembali.
Presets disimpan dalam JSON file.
"""

import bpy
import json
from pathlib import Path


class PresetsManager:
    """Manage generation presets dengan persistent storage."""
    
    def __init__(self):
        """Initialize presets manager."""
        self.presets_file = self._get_presets_file()
        self.presets_data = self._load_presets()
    
    def _get_presets_file(self):
        """Get path ke presets file."""
        config_dir = Path(bpy.utils.resource_path('USER')) / 'ai_3d_generator'
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir / 'generation_presets.json'
    
    def _load_presets(self):
        """Load presets dari file."""
        if self.presets_file.exists():
            try:
                with open(self.presets_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading presets: {str(e)}")
                return {'text_presets': [], 'image_presets': []}
        return {'text_presets': [], 'image_presets': []}
    
    def _save_presets(self):
        """Save presets ke file."""
        try:
            with open(self.presets_file, 'w') as f:
                json.dump(self.presets_data, f, indent=2)
        except Exception as e:
            print(f"Error saving presets: {str(e)}")
    
    def create_text_preset(self, name, prompt, style, quality, output_format):
        """Create text-to-3D preset.
        
        Args:
            name (str): Nama preset
            prompt (str): Default prompt
            style (str): Default style
            quality (int): Default quality
            output_format (str): Default format
        
        Returns:
            dict: Preset yang dibuat
        """
        preset = {
            'name': name,
            'type': 'text',
            'prompt': prompt,
            'style': style,
            'quality': quality,
            'output_format': output_format,
        }
        
        self.presets_data['text_presets'].append(preset)
        self._save_presets()
        return preset
    
    def create_image_preset(self, name, style, quality, output_format, background_removal):
        """Create image-to-3D preset.
        
        Args:
            name (str): Nama preset
            style (str): Default style
            quality (int): Default quality
            output_format (str): Default format
            background_removal (bool): Default background removal
        
        Returns:
            dict: Preset yang dibuat
        """
        preset = {
            'name': name,
            'type': 'image',
            'style': style,
            'quality': quality,
            'output_format': output_format,
            'background_removal': background_removal,
        }
        
        self.presets_data['image_presets'].append(preset)
        self._save_presets()
        return preset
    
    def get_text_presets(self):
        """Get semua text presets."""
        return self.presets_data['text_presets']
    
    def get_image_presets(self):
        """Get semua image presets."""
        return self.presets_data['image_presets']
    
    def get_preset_by_name(self, name, preset_type='text'):
        """Get preset berdasarkan nama.
        
        Args:
            name (str): Nama preset
            preset_type (str): 'text' atau 'image'
        
        Returns:
            dict: Preset jika ditemukan, None jika tidak
        """
        presets = self.presets_data['text_presets'] if preset_type == 'text' else self.presets_data['image_presets']
        for preset in presets:
            if preset['name'] == name:
                return preset
        return None
    
    def update_preset(self, name, updates, preset_type='text'):
        """Update preset yang existing.
        
        Args:
            name (str): Nama preset
            updates (dict): Field untuk diupdate
            preset_type (str): 'text' atau 'image'
        
        Returns:
            dict: Preset yang diupdate
        """
        presets = self.presets_data['text_presets'] if preset_type == 'text' else self.presets_data['image_presets']
        for preset in presets:
            if preset['name'] == name:
                preset.update(updates)
                self._save_presets()
                return preset
        return None
    
    def delete_preset(self, name, preset_type='text'):
        """Delete preset.
        
        Args:
            name (str): Nama preset
            preset_type (str): 'text' atau 'image'
        """
        if preset_type == 'text':
            self.presets_data['text_presets'] = [
                p for p in self.presets_data['text_presets'] if p['name'] != name
            ]
        else:
            self.presets_data['image_presets'] = [
                p for p in self.presets_data['image_presets'] if p['name'] != name
            ]
        self._save_presets()
    
    def duplicate_preset(self, name, new_name, preset_type='text'):
        """Duplicate preset dengan nama baru.
        
        Args:
            name (str): Nama preset original
            new_name (str): Nama preset baru
            preset_type (str): 'text' atau 'image'
        
        Returns:
            dict: Preset yang diduplicate
        """
        original = self.get_preset_by_name(name, preset_type)
        if not original:
            return None
        
        new_preset = original.copy()
        new_preset['name'] = new_name
        
        presets = self.presets_data['text_presets'] if preset_type == 'text' else self.presets_data['image_presets']
        presets.append(new_preset)
        self._save_presets()
        
        return new_preset
    
    def export_presets(self, filepath):
        """Export presets ke file.
        
        Args:
            filepath (str): Path ke file untuk export
        """
        try:
            with open(filepath, 'w') as f:
                json.dump(self.presets_data, f, indent=2)
        except Exception as e:
            print(f"Error exporting presets: {str(e)}")
    
    def import_presets(self, filepath, merge=True):
        """Import presets dari file.
        
        Args:
            filepath (str): Path ke file untuk import
            merge (bool): Merge dengan existing presets atau replace
        """
        try:
            with open(filepath, 'r') as f:
                imported = json.load(f)
            
            if merge:
                self.presets_data['text_presets'].extend(imported.get('text_presets', []))
                self.presets_data['image_presets'].extend(imported.get('image_presets', []))
            else:
                self.presets_data = imported
            
            self._save_presets()
        except Exception as e:
            print(f"Error importing presets: {str(e)}")


# Global presets instance
_presets_instance = None


def get_presets():
    """Get global presets instance."""
    global _presets_instance
    if _presets_instance is None:
        _presets_instance = PresetsManager()
    return _presets_instance
