"""
Base Provider Client

Addon ini hanya bertindak sebagai client untuk layanan AI 3D pihak ketiga.
User harus mendaftar dan menyediakan API key sendiri.

Abstract base class untuk semua provider (Tripo, Meshy, ModelsLab).
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any


class BaseProviderClient(ABC):
    """Abstract base class untuk AI 3D provider clients."""
    
    def __init__(self, api_key: str, base_url: str):
        """
        Initialize provider client.
        
        Args:
            api_key: API key untuk provider
            base_url: Base URL untuk API provider
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
    
    @abstractmethod
    def generate_text(self, prompt: str, style: str, quality: int, 
                     output_format: str) -> Dict[str, Any]:
        """
        Generate 3D model dari text prompt.
        
        Returns:
            Dict dengan minimal kunci 'job_id' atau 'task_id'
        """
        pass
    
    @abstractmethod
    def generate_image(self, image_path: str, style: str, quality: int, 
                      output_format: str, background_removal: bool = False) -> Dict[str, Any]:
        """
        Generate 3D model dari image.
        
        Returns:
            Dict dengan minimal kunci 'job_id' atau 'task_id'
        """
        pass
    
    @abstractmethod
    def poll_status(self, job_id: str) -> Dict[str, Any]:
        """
        Poll status dari generation job.
        
        Returns:
            Dict dengan kunci 'status' (pending/completed/failed) dan 'model_url' jika completed
        """
        pass
    
    @abstractmethod
    def test_connection(self) -> tuple[bool, str]:
        """
        Test koneksi dan API key validity.
        
        Returns:
            Tuple (success: bool, message: str)
        """
        pass
