"""
Batch Generation Manager untuk AI 3D Generator

Mengelola batch generation dengan queue system dan progress tracking.
"""

import bpy
import json
from pathlib import Path
from datetime import datetime


class BatchJob:
    """Representasi satu batch job."""
    
    def __init__(self, job_id, name, generation_configs):
        """Initialize batch job.
        
        Args:
            job_id (str): Unique ID untuk batch job
            name (str): Nama batch job
            generation_configs (list): List of generation configs
        """
        self.job_id = job_id
        self.name = name
        self.generation_configs = generation_configs
        self.created_at = datetime.now().isoformat()
        self.status = 'pending'  # pending, running, completed, failed
        self.total_items = len(generation_configs)
        self.completed_items = 0
        self.failed_items = 0
        self.item_statuses = []  # List of individual item statuses
    
    def to_dict(self):
        """Convert ke dictionary."""
        return {
            'job_id': self.job_id,
            'name': self.name,
            'generation_configs': self.generation_configs,
            'created_at': self.created_at,
            'status': self.status,
            'total_items': self.total_items,
            'completed_items': self.completed_items,
            'failed_items': self.failed_items,
            'item_statuses': self.item_statuses,
        }
    
    @staticmethod
    def from_dict(data):
        """Create dari dictionary."""
        batch = BatchJob(data['job_id'], data['name'], data['generation_configs'])
        batch.created_at = data['created_at']
        batch.status = data['status']
        batch.completed_items = data['completed_items']
        batch.failed_items = data['failed_items']
        batch.item_statuses = data['item_statuses']
        return batch


class BatchGenerator:
    """Manage batch generation dengan persistent storage."""
    
    def __init__(self):
        """Initialize batch generator."""
        self.jobs_file = self._get_jobs_file()
        self.jobs_data = self._load_jobs()
        self.current_batch = None
    
    def _get_jobs_file(self):
        """Get path ke jobs file."""
        config_dir = Path(bpy.utils.resource_path('USER')) / 'ai_3d_generator'
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir / 'batch_jobs.json'
    
    def _load_jobs(self):
        """Load jobs dari file."""
        if self.jobs_file.exists():
            try:
                with open(self.jobs_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading batch jobs: {str(e)}")
                return {'jobs': []}
        return {'jobs': []}
    
    def _save_jobs(self):
        """Save jobs ke file."""
        try:
            with open(self.jobs_file, 'w') as f:
                json.dump(self.jobs_data, f, indent=2)
        except Exception as e:
            print(f"Error saving batch jobs: {str(e)}")
    
    def create_batch(self, name, generation_configs):
        """Create batch job baru.
        
        Args:
            name (str): Nama batch job
            generation_configs (list): List dari generation configs
                Setiap config memiliki:
                - provider: Provider untuk generasi
                - type: 'text' atau 'image'
                - prompt: Text prompt (untuk text-to-3d)
                - image_path: Path ke image (untuk image-to-3d)
                - style: Style
                - quality: Quality level
                - format: Output format
        
        Returns:
            BatchJob: Batch job yang dibuat
        """
        job_id = f"batch_{int(datetime.now().timestamp())}"
        batch = BatchJob(job_id, name, generation_configs)
        
        self.jobs_data['jobs'].append(batch.to_dict())
        self._save_jobs()
        self.current_batch = batch
        
        return batch
    
    def get_batch(self, job_id):
        """Get batch job berdasarkan ID."""
        for job_data in self.jobs_data['jobs']:
            if job_data['job_id'] == job_id:
                return BatchJob.from_dict(job_data)
        return None
    
    def get_all_batches(self):
        """Get semua batch jobs."""
        return [BatchJob.from_dict(j) for j in self.jobs_data['jobs']]
    
    def update_batch_status(self, job_id, status, completed=None, failed=None):
        """Update status batch job.
        
        Args:
            job_id (str): Job ID
            status (str): Status baru
            completed (int): Total completed items
            failed (int): Total failed items
        """
        for job_data in self.jobs_data['jobs']:
            if job_data['job_id'] == job_id:
                job_data['status'] = status
                if completed is not None:
                    job_data['completed_items'] = completed
                if failed is not None:
                    job_data['failed_items'] = failed
                self._save_jobs()
                return
    
    def update_item_status(self, job_id, item_index, item_status):
        """Update status satu item dalam batch.
        
        Args:
            job_id (str): Job ID
            item_index (int): Index item dalam batch
            item_status (dict): Status item dengan format:
                - job_id: API job ID
                - status: current status
                - error: error message jika ada
                - model_url: URL model jika completed
        """
        for job_data in self.jobs_data['jobs']:
            if job_data['job_id'] == job_id:
                # Ensure item_statuses list cukup besar
                while len(job_data['item_statuses']) <= item_index:
                    job_data['item_statuses'].append(None)
                
                job_data['item_statuses'][item_index] = item_status
                self._save_jobs()
                return
    
    def delete_batch(self, job_id):
        """Delete batch job."""
        self.jobs_data['jobs'] = [
            j for j in self.jobs_data['jobs'] if j['job_id'] != job_id
        ]
        self._save_jobs()
        if self.current_batch and self.current_batch.job_id == job_id:
            self.current_batch = None
    
    def get_batch_progress(self, job_id):
        """Get progress dari batch job.
        
        Returns:
            dict: Progress dengan format:
                - total: Total items
                - completed: Completed items
                - failed: Failed items
                - pending: Pending items
                - progress_percent: Percentage (0-100)
        """
        batch = self.get_batch(job_id)
        if not batch:
            return None
        
        completed = batch.completed_items
        failed = batch.failed_items
        total = batch.total_items
        pending = total - completed - failed
        
        progress_percent = int((completed + failed) / total * 100) if total > 0 else 0
        
        return {
            'total': total,
            'completed': completed,
            'failed': failed,
            'pending': pending,
            'progress_percent': progress_percent,
        }
    
    def add_to_batch(self, job_id, generation_config):
        """Add item ke existing batch.
        
        Args:
            job_id (str): Batch job ID
            generation_config (dict): Generation config untuk ditambah
        """
        batch = self.get_batch(job_id)
        if batch:
            batch.generation_configs.append(generation_config)
            batch.total_items = len(batch.generation_configs)
            
            for job_data in self.jobs_data['jobs']:
                if job_data['job_id'] == job_id:
                    job_data['generation_configs'].append(generation_config)
                    job_data['total_items'] = len(job_data['generation_configs'])
            
            self._save_jobs()
    
    def get_pending_items(self, job_id):
        """Get pending items dari batch.
        
        Returns:
            list: List of (index, config) tuple untuk items yang belum processed
        """
        batch = self.get_batch(job_id)
        if not batch:
            return []
        
        pending = []
        for i, status in enumerate(batch.item_statuses):
            if status is None:
                pending.append((i, batch.generation_configs[i]))
        
        return pending


# Global batch generator instance
_batch_generator_instance = None


def get_batch_generator():
    """Get global batch generator instance."""
    global _batch_generator_instance
    if _batch_generator_instance is None:
        _batch_generator_instance = BatchGenerator()
    return _batch_generator_instance
