"""
ModelsLab Client

Addon ini hanya bertindak sebagai client untuk layanan AI 3D pihak ketiga.
User harus mendaftar dan menyediakan API key sendiri.

Client untuk ModelsLab / 3D Verse API.
Dokumentasi: https://www.modelslab.com/
"""

import requests
from typing import Dict, Any
from .base_client import BaseProviderClient


class ModelsLabClient(BaseProviderClient):
    """Client untuk ModelsLab / 3D Verse API."""
    
    def __init__(self, api_key: str, base_url: str = "https://api.modelslab.com"):
        """Initialize ModelsLab client."""
        super().__init__(api_key, base_url)
    
    def _get_headers(self) -> Dict[str, str]:
        """Get request headers dengan API key."""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def generate_text(self, prompt: str, style: str, quality: int, 
                     output_format: str) -> Dict[str, Any]:
        """Generate 3D model dari text prompt menggunakan ModelsLab API."""
        try:
            # Map style untuk ModelsLab
            style_mapping = {
                "cartoon": "cartoon",
                "realistic": "realistic",
                "clay": "clay",
                "sci-fi": "sci-fi"
            }
            
            # Map quality level
            quality_mapping = {
                1: "low", 2: "low", 3: "low",
                4: "medium", 5: "medium", 6: "medium",
                7: "high", 8: "high", 9: "high", 10: "ultra"
            }
            
            payload = {
                "prompt": prompt,
                "style": style_mapping.get(style, style),
                "quality": quality_mapping.get(quality, "medium"),
                "output_format": output_format
            }
            
            response = requests.post(
                f"{self.base_url}/api/v1/3dverse/text-to-3d",
                json=payload,
                headers=self._get_headers(),
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            
            return {
                "job_id": data.get("id") or data.get("job_id") or data.get("task_id"),
                "status": "pending"
            }
        
        except requests.exceptions.RequestException as e:
            return {
                "error": f"ModelsLab API error: {str(e)}",
                "job_id": None
            }
    
    def generate_image(self, image_path: str, style: str, quality: int, 
                      output_format: str, background_removal: bool = False) -> Dict[str, Any]:
        """Generate 3D model dari image menggunakan ModelsLab API."""
        try:
            with open(image_path, 'rb') as f:
                files = {'image': f}
                
                style_mapping = {
                    "cartoon": "cartoon",
                    "realistic": "realistic",
                    "clay": "clay",
                    "sci-fi": "sci-fi"
                }
                
                quality_mapping = {
                    1: "low", 2: "low", 3: "low",
                    4: "medium", 5: "medium", 6: "medium",
                    7: "high", 8: "high", 9: "high", 10: "ultra"
                }
                
                data = {
                    "style": style_mapping.get(style, style),
                    "quality": quality_mapping.get(quality, "medium"),
                    "output_format": output_format
                }
                
                if background_removal:
                    data["remove_background"] = "true"
                
                response = requests.post(
                    f"{self.base_url}/api/v1/3dverse/image-to-3d",
                    data=data,
                    files=files,
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    timeout=30
                )
                response.raise_for_status()
                
                resp_data = response.json()
                
                return {
                    "job_id": resp_data.get("id") or resp_data.get("job_id") or resp_data.get("task_id"),
                    "status": "pending"
                }
        
        except FileNotFoundError:
            return {
                "error": f"Image file not found: {image_path}",
                "job_id": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "error": f"ModelsLab API error: {str(e)}",
                "job_id": None
            }
    
    def poll_status(self, job_id: str) -> Dict[str, Any]:
        """Poll status dari ModelsLab generation job."""
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/3dverse/status/{job_id}",
                headers=self._get_headers(),
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            status = data.get("status", "unknown").lower()
            
            poll_result = {
                "job_id": job_id,
                "status": status,
            }
            
            if status == "completed" or status == "succeeded":
                model_url = data.get("model_url") or data.get("output_url")
                if model_url:
                    poll_result["model_url"] = model_url
                poll_result["status"] = "completed"
            elif status == "failed" or status == "error":
                poll_result["error"] = data.get("error_message", "Unknown error")
            
            return poll_result
        
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
                f"{self.base_url}/api/v1/user/info",
                headers=self._get_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                return True, "ModelsLab connection successful!"
            elif response.status_code == 401:
                return False, "Invalid ModelsLab API key"
            else:
                return False, f"ModelsLab API error: {response.status_code}"
        
        except requests.exceptions.ConnectionError:
            return False, f"Cannot connect to ModelsLab API: {self.base_url}"
        except requests.exceptions.RequestException as e:
            return False, f"ModelsLab connection error: {str(e)}"
