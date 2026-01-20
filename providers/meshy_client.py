"""
Meshy Client

Addon ini hanya bertindak sebagai client untuk layanan AI 3D pihak ketiga.
User harus mendaftar dan menyediakan API key sendiri.

Client untuk Meshy API.
Dokumentasi: https://www.meshy.ai/
"""

import requests
from typing import Dict, Any
from .base_client import BaseProviderClient


class MeshyClient(BaseProviderClient):
    """Client untuk Meshy API."""
    
    def __init__(self, api_key: str, base_url: str = "https://api.meshy.ai"):
        """Initialize Meshy client."""
        super().__init__(api_key, base_url)
    
    def _get_headers(self) -> Dict[str, str]:
        """Get request headers dengan API key."""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def generate_text(self, prompt: str, style: str, quality: int, 
                     output_format: str) -> Dict[str, Any]:
        """Generate 3D model dari text prompt menggunakan Meshy API."""
        try:
            # Map style ke Meshy parameter
            style_mapping = {
                "cartoon": "cartoon",
                "realistic": "realistic",
                "clay": "clay",
                "sci-fi": "sci-fi"
            }
            
            # Map quality (1-10) to art_style atau quality parameter
            quality_mapping = {
                1: "low", 2: "low", 3: "low",
                4: "medium", 5: "medium", 6: "medium",
                7: "high", 8: "high", 9: "high", 10: "ultra"
            }
            
            payload = {
                "object_prompt": prompt,
                "style": style_mapping.get(style, style),
                "model_type": "gaussian_splatting",
                "art_style": quality_mapping.get(quality, "medium"),
                "negative_prompt": "",
                "ai_model": "meshy-4"
            }
            
            # Map output format
            if output_format.lower() in ["glb", "gltf"]:
                payload["texture_richness"] = "high"
            
            response = requests.post(
                f"{self.base_url}/openapi/v1/text-to-3d",
                json=payload,
                headers=self._get_headers(),
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            result = data.get("result", {})
            
            return {
                "job_id": result.get("id"),
                "status": "pending"
            }
        
        except requests.exceptions.RequestException as e:
            return {
                "error": f"Meshy API error: {str(e)}",
                "job_id": None
            }
    
    def generate_image(self, image_path: str, style: str, quality: int, 
                      output_format: str, background_removal: bool = False) -> Dict[str, Any]:
        """Generate 3D model dari image menggunakan Meshy API."""
        try:
            with open(image_path, 'rb') as f:
                files = {'image_file': f}
                
                style_mapping = {
                    "cartoon": "cartoon",
                    "realistic": "realistic",
                    "clay": "clay",
                    "sci-fi": "sci-fi"
                }
                
                data = {
                    "object_prompt": "",
                    "style": style_mapping.get(style, style),
                    "ai_model": "meshy-4-turbo",
                }
                
                if background_removal:
                    data["background_removal"] = "true"
                
                response = requests.post(
                    f"{self.base_url}/openapi/v1/image-to-3d",
                    data=data,
                    files=files,
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    timeout=30
                )
                response.raise_for_status()
                
                resp_data = response.json()
                result = resp_data.get("result", {})
                
                return {
                    "job_id": result.get("id"),
                    "status": "pending"
                }
        
        except FileNotFoundError:
            return {
                "error": f"Image file not found: {image_path}",
                "job_id": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "error": f"Meshy API error: {str(e)}",
                "job_id": None
            }
    
    def poll_status(self, job_id: str) -> Dict[str, Any]:
        """Poll status dari Meshy generation job."""
        try:
            response = requests.get(
                f"{self.base_url}/openapi/v1/tasks/{job_id}",
                headers=self._get_headers(),
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            result = data.get("result", {})
            status = result.get("status", "unknown").lower()
            
            poll_result = {
                "job_id": job_id,
                "status": status,
            }
            
            if status == "completed":
                model_urls = result.get("model_urls", [])
                if model_urls:
                    # Pilih format yang tersedia (preferensi: glb, obj, fbx)
                    for model_url in model_urls:
                        if "glb" in model_url.lower() or "gltf" in model_url.lower():
                            poll_result["model_url"] = model_url
                            break
                    else:
                        # Jika tidak ada glb, gunakan yang pertama
                        poll_result["model_url"] = model_urls[0]
            elif status == "failed" or status == "error":
                poll_result["error"] = result.get("error_message", "Unknown error")
            
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
                f"{self.base_url}/openapi/v1/user/profile",
                headers=self._get_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                return True, "Meshy connection successful!"
            elif response.status_code == 401:
                return False, "Invalid Meshy API key"
            else:
                return False, f"Meshy API error: {response.status_code}"
        
        except requests.exceptions.ConnectionError:
            return False, f"Cannot connect to Meshy API: {self.base_url}"
        except requests.exceptions.RequestException as e:
            return False, f"Meshy connection error: {str(e)}"
