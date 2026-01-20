"""
Tripo Client

Addon ini hanya bertindak sebagai client untuk layanan AI 3D pihak ketiga.
User harus mendaftar dan menyediakan API key sendiri.

Client untuk Tripo 3D API.
Dokumentasi: https://www.tripo3d.ai/
"""

import requests
import time
from typing import Dict, Any
from .base_client import BaseProviderClient


class TripoClient(BaseProviderClient):
    """Client untuk Tripo 3D API."""
    
    def __init__(self, api_key: str, base_url: str = "https://platform.tripo3d.ai"):
        """Initialize Tripo client."""
        super().__init__(api_key, base_url)
    
    def _get_headers(self) -> Dict[str, str]:
        """Get request headers dengan API key."""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def generate_text(self, prompt: str, style: str, quality: int, 
                     output_format: str) -> Dict[str, Any]:
        """Generate 3D model dari text prompt menggunakan Tripo API."""
        try:
            # Map style to Tripo parameter jika diperlukan
            style_mapping = {
                "cartoon": "cartoon",
                "realistic": "realistic",
                "clay": "clay",
                "sci-fi": "sci-fi"
            }
            
            payload = {
                "type": "text_to_3d",
                "prompt": prompt,
                "style": style_mapping.get(style, style),
                "quality": quality,
                "output_format": output_format
            }
            
            response = requests.post(
                f"{self.base_url}/api/v1/generate",
                json=payload,
                headers=self._get_headers(),
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            return {
                "job_id": data.get("job_id") or data.get("id"),
                "status": "pending"
            }
        
        except requests.exceptions.RequestException as e:
            return {
                "error": f"Tripo API error: {str(e)}",
                "job_id": None
            }
    
    def generate_image(self, image_path: str, style: str, quality: int, 
                      output_format: str, background_removal: bool = False) -> Dict[str, Any]:
        """Generate 3D model dari image menggunakan Tripo API."""
        try:
            with open(image_path, 'rb') as f:
                files = {'image': f}
                
                style_mapping = {
                    "cartoon": "cartoon",
                    "realistic": "realistic",
                    "clay": "clay",
                    "sci-fi": "sci-fi"
                }
                
                data = {
                    "type": "image_to_3d",
                    "style": style_mapping.get(style, style),
                    "quality": quality,
                    "output_format": output_format
                }
                
                if background_removal:
                    data["remove_background"] = True
                
                response = requests.post(
                    f"{self.base_url}/api/v1/generate",
                    data=data,
                    files=files,
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    timeout=30
                )
                response.raise_for_status()
                
                resp_data = response.json()
                return {
                    "job_id": resp_data.get("job_id") or resp_data.get("id"),
                    "status": "pending"
                }
        
        except FileNotFoundError:
            return {
                "error": f"Image file not found: {image_path}",
                "job_id": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "error": f"Tripo API error: {str(e)}",
                "job_id": None
            }
    
    def poll_status(self, job_id: str) -> Dict[str, Any]:
        """Poll status dari Tripo generation job."""
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/jobs/{job_id}",
                headers=self._get_headers(),
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            status = data.get("status", "unknown").lower()
            
            result = {
                "job_id": job_id,
                "status": status,
            }
            
            if status == "completed" or status == "succeeded":
                # Tripo returns model_url atau download_url
                model_url = data.get("model_url") or data.get("download_url")
                if model_url:
                    result["model_url"] = model_url
                result["status"] = "completed"
            elif status == "failed" or status == "error":
                result["error"] = data.get("error_message", "Unknown error")
            
            return result
        
        except requests.exceptions.RequestException as e:
            return {
                "job_id": job_id,
                "status": "error",
                "error": f"Poll error: {str(e)}"
            }
    
    def test_connection(self) -> tuple[bool, str]:
        """Test koneksi dan API key validity."""
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/user",
                headers=self._get_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                return True, "Tripo connection successful!"
            elif response.status_code == 401:
                return False, "Invalid Tripo API key"
            else:
                return False, f"Tripo API error: {response.status_code}"
        
        except requests.exceptions.ConnectionError:
            return False, f"Cannot connect to Tripo API: {self.base_url}"
        except requests.exceptions.RequestException as e:
            return False, f"Tripo connection error: {str(e)}"
