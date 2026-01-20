"""
History Management untuk AI 3D Generator

Menyimpan dan mengelola history dari semua generation yang telah dilakukan.
History disimpan dalam JSON file di folder user Blender.
"""

import bpy
import json
import os
from datetime import datetime
from pathlib import Path


class GenerationHistory:
    """Manage generation history dengan persistent storage."""
    
    def __init__(self):
        """Initialize history manager."""
        self.history_file = self._get_history_file()
        self.history_data = self._load_history()
    
    def _get_history_file(self):
        """Get path ke history file."""
        config_dir = Path(bpy.utils.resource_path('USER')) / 'ai_3d_generator'
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir / 'generation_history.json'
    
    def _load_history(self):
        """Load history dari file."""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading history: {str(e)}")
                return {'generations': [], 'total_count': 0}
        return {'generations': [], 'total_count': 0}
    
    def _save_history(self):
        """Save history ke file."""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.history_data, f, indent=2)
        except Exception as e:
            print(f"Error saving history: {str(e)}")
    
    def add_generation(self, generation_info):
        """Add new generation ke history.
        
        Args:
            generation_info (dict): Information tentang generation
                - provider: Provider yang digunakan
                - type: 'text' atau 'image'
                - prompt: Text prompt (untuk text-to-3d)
                - image_path: Path ke image (untuk image-to-3d)
                - style: Style yang digunakan
                - quality: Quality level
                - format: Output format
                - job_id: Job ID dari API
                - status: Status generasi
        """
        entry = {
            'id': self.history_data['total_count'] + 1,
            'timestamp': datetime.now().isoformat(),
            'provider': generation_info.get('provider', 'Unknown'),
            'type': generation_info.get('type', 'unknown'),
            'prompt': generation_info.get('prompt', ''),
            'image_path': generation_info.get('image_path', ''),
            'style': generation_info.get('style', ''),
            'quality': generation_info.get('quality', 0),
            'format': generation_info.get('format', ''),
            'job_id': generation_info.get('job_id', ''),
            'model_url': generation_info.get('model_url', ''),
            'status': generation_info.get('status', 'pending'),
            'error': generation_info.get('error', ''),
            'imported_model_name': generation_info.get('imported_model_name', ''),
        }
        
        self.history_data['generations'].append(entry)
        self.history_data['total_count'] += 1
        self._save_history()
        
        return entry
    
    def update_generation(self, job_id, status, **kwargs):
        """Update status generasi yang existing.
        
        Args:
            job_id (str): Job ID untuk diupdate
            status (str): Status baru
            **kwargs: Field tambahan untuk diupdate
        """
        for gen in self.history_data['generations']:
            if gen['job_id'] == job_id:
                gen['status'] = status
                gen.update(kwargs)
                self._save_history()
                return gen
        return None
    
    def get_generation(self, job_id):
        """Get generasi spesifik berdasarkan job ID."""
        for gen in self.history_data['generations']:
            if gen['job_id'] == job_id:
                return gen
        return None
    
    def get_all_generations(self):
        """Get semua generations."""
        return self.history_data['generations']
    
    def get_generations_by_provider(self, provider):
        """Get generations berdasarkan provider."""
        return [g for g in self.history_data['generations'] if g['provider'] == provider]
    
    def get_generations_by_type(self, gen_type):
        """Get generations berdasarkan type (text atau image)."""
        return [g for g in self.history_data['generations'] if g['type'] == gen_type]
    
    def get_completed_generations(self):
        """Get semua completed generations."""
        return [g for g in self.history_data['generations'] if g['status'] == 'completed']
    
    def delete_generation(self, job_id):
        """Delete generation dari history."""
        self.history_data['generations'] = [
            g for g in self.history_data['generations'] if g['job_id'] != job_id
        ]
        self._save_history()
    
    def clear_history(self):
        """Clear semua history."""
        self.history_data = {'generations': [], 'total_count': 0}
        self._save_history()
    
    def get_statistics(self):
        """Get statistics dari generation history."""
        generations = self.history_data['generations']
        
        stats = {
            'total': len(generations),
            'completed': len([g for g in generations if g['status'] == 'completed']),
            'failed': len([g for g in generations if g['status'] == 'failed']),
            'pending': len([g for g in generations if g['status'] == 'pending']),
            'by_provider': {},
            'by_type': {},
            'by_style': {},
        }
        
        # Count by provider
        for gen in generations:
            provider = gen.get('provider', 'Unknown')
            stats['by_provider'][provider] = stats['by_provider'].get(provider, 0) + 1
        
        # Count by type
        for gen in generations:
            gen_type = gen.get('type', 'unknown')
            stats['by_type'][gen_type] = stats['by_type'].get(gen_type, 0) + 1
        
        # Count by style
        for gen in generations:
            style = gen.get('style', 'unknown')
            stats['by_style'][style] = stats['by_style'].get(style, 0) + 1
        
        return stats


# Global history instance
_history_instance = None


def get_history():
    """Get global history instance."""
    global _history_instance
    if _history_instance is None:
        _history_instance = GenerationHistory()
    return _history_instance
