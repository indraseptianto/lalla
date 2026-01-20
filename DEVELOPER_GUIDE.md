# AI 3D Generator - Developer Guide

## 📚 For Developers: Extending & Contributing

This guide helps developers who want to:
- Extend addon dengan provider baru
- Modify UI/operators
- Fix bugs
- Contribute improvements

---

## 🏗️ Architecture Overview

### Module Structure

```
ai_3d_generator/
├── __init__.py                 # Main addon entry point
├── preferences.py              # Preferences UI & config
├── ui_panel.py                 # 3D View panel UI
├── operators.py                # Blender operators
├── downloader.py               # Model download & import
└── providers/
    ├── __init__.py             # Package init & exports
    ├── base_client.py          # Abstract base class
    ├── tripo_client.py         # Tripo implementation
    ├── meshy_client.py         # Meshy implementation
    └── modelslab_client.py     # ModelsLab implementation
```

### Data Flow

```
User Input (UI)
    ↓
Operator (operators.py)
    ↓
Provider Client (providers/*.py)
    ↓
API Request (requests library)
    ↓
API Response
    ↓
Polling / Job Tracking
    ↓
Download (downloader.py)
    ↓
Import (Blender native operators)
    ↓
Object in Scene
```

---

## 🔌 Adding a New Provider

### Step 1: Create New Client Class

Create file: `providers/new_provider_client.py`

```python
"""
New Provider Client

Example of new AI 3D provider integration.
"""

import requests
from typing import Dict, Any
from .base_client import BaseProviderClient


class NewProviderClient(BaseProviderClient):
    """Client untuk New Provider API."""
    
    def __init__(self, api_key: str, base_url: str = "https://api.newprovider.com"):
        """Initialize new provider client."""
        super().__init__(api_key, base_url)
    
    def _get_headers(self) -> Dict[str, str]:
        """Get request headers dengan API key."""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def generate_text(self, prompt: str, style: str, quality: int, 
                     output_format: str) -> Dict[str, Any]:
        """Generate 3D model dari text prompt."""
        try:
            # Map style untuk provider
            style_mapping = {
                "cartoon": "cartoon",
                "realistic": "realistic",
                "clay": "clay",
                "sci-fi": "sci-fi"
            }
            
            payload = {
                "prompt": prompt,
                "style": style_mapping.get(style, style),
                "quality": quality,
                "format": output_format
            }
            
            response = requests.post(
                f"{self.base_url}/v1/generate/text",
                json=payload,
                headers=self._get_headers(),
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            return {
                "job_id": data.get("id"),
                "status": "pending"
            }
        
        except requests.exceptions.RequestException as e:
            return {
                "error": f"NewProvider API error: {str(e)}",
                "job_id": None
            }
    
    def generate_image(self, image_path: str, style: str, quality: int, 
                      output_format: str, background_removal: bool = False) -> Dict[str, Any]:
        """Generate 3D model dari image."""
        try:
            with open(image_path, 'rb') as f:
                files = {'image': f}
                
                data = {
                    "style": style,
                    "quality": quality,
                    "format": output_format
                }
                
                if background_removal:
                    data["remove_bg"] = True
                
                response = requests.post(
                    f"{self.base_url}/v1/generate/image",
                    data=data,
                    files=files,
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    timeout=30
                )
                response.raise_for_status()
                
                resp_data = response.json()
                return {
                    "job_id": resp_data.get("id"),
                    "status": "pending"
                }
        
        except FileNotFoundError:
            return {"error": f"Image file not found: {image_path}", "job_id": None}
        except requests.exceptions.RequestException as e:
            return {"error": f"NewProvider API error: {str(e)}", "job_id": None}
    
    def poll_status(self, job_id: str) -> Dict[str, Any]:
        """Poll status dari generation job."""
        try:
            response = requests.get(
                f"{self.base_url}/v1/status/{job_id}",
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
            
            if status == "completed":
                model_url = data.get("model_url")
                if model_url:
                    result["model_url"] = model_url
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
                f"{self.base_url}/v1/user/info",
                headers=self._get_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                return True, "NewProvider connection successful!"
            elif response.status_code == 401:
                return False, "Invalid NewProvider API key"
            else:
                return False, f"NewProvider API error: {response.status_code}"
        
        except requests.exceptions.ConnectionError:
            return False, f"Cannot connect to NewProvider API: {self.base_url}"
        except requests.exceptions.RequestException as e:
            return False, f"NewProvider connection error: {str(e)}"
```

### Step 2: Update providers/__init__.py

Add import:

```python
from .new_provider_client import NewProviderClient

__all__ = [
    'BaseProviderClient',
    'TripoClient',
    'MeshyClient',
    'ModelsLabClient',
    'NewProviderClient',  # Add this
]
```

### Step 3: Add to preferences.py

Add properties untuk new provider:

```python
# New Provider settings
newprovider_api_key: StringProperty(
    name="API Key",
    description="New Provider API Key",
    subtype='PASSWORD'
)

newprovider_base_url: StringProperty(
    name="Base URL",
    description="New Provider API Base URL",
    default="https://api.newprovider.com"
)
```

Add UI:

```python
# New Provider section
box_newprovider = layout.box()
row = box_newprovider.row()
row.label(text="NEW PROVIDER", icon='SETTINGS')

box_newprovider.prop(self, "newprovider_api_key")
box_newprovider.prop(self, "newprovider_base_url")

row = box_newprovider.row(align=True)
row.operator("wm.url_open", text="Open NewProvider Docs", icon='WORLD').url = "https://www.newprovider.com/docs"
```

### Step 4: Add to __init__.py

Update enum:

```python
Scene.ai3d_provider = EnumProperty(
    name="Provider",
    description="Pilih AI 3D provider",
    items=[
        ('TRIPO', "Tripo 3D", "Tripo 3D service"),
        ('MESHY', "Meshy", "Meshy service"),
        ('MODELSLAB', "ModelsLab", "ModelsLab / 3D Verse service"),
        ('NEWPROVIDER', "New Provider", "New Provider service"),  # Add this
    ],
    default='TRIPO'
)
```

### Step 5: Update operators.py

Update `get_provider_client()`:

```python
def get_provider_client(context):
    """Get current provider client instance."""
    prefs = context.preferences.addons['ai_3d_generator'].preferences
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
    elif provider == 'NEWPROVIDER':  # Add this
        api_key = prefs.newprovider_api_key
        base_url = prefs.newprovider_base_url
        from .providers import NewProviderClient  # Import
        return NewProviderClient(api_key, base_url)
    
    return None
```

### Step 6: Test

```python
# Test new provider
from providers import NewProviderClient

client = NewProviderClient(
    api_key="test_key_here",
    base_url="https://api.newprovider.com"
)

# Test connection
success, msg = client.test_connection()
print(f"Connection: {success} - {msg}")

# Test text generation
result = client.generate_text("red ball", "realistic", 7, "glb")
print(f"Job ID: {result.get('job_id')}")
```

---

## 🎨 Customizing UI

### Add New UI Element to Panel

Edit `ui_panel.py`:

```python
def _draw_text_to_3d(self, layout, scene):
    """Draw Text to 3D UI."""
    box = layout.box()
    box.label(text="Text to 3D", icon='TEXT')
    
    # Existing properties...
    box.prop(scene, "ai3d_prompt", text="Prompt")
    
    # Add new property
    box.prop(scene, "ai3d_custom_setting", text="Custom Setting")
    
    # Generate button
    row = box.row(align=True)
    row.scale_y = 1.5
    row.operator("ai3d.generate_text", icon='MESH_DATA')
```

### Define New Scene Property

Edit `__init__.py`:

```python
def register_properties():
    """Register custom scene properties."""
    # ... existing properties ...
    
    # Add new custom property
    Scene.ai3d_custom_setting = StringProperty(
        name="Custom Setting",
        description="Custom setting description",
        default="default_value"
    )
```

### Add New Tab to Panel

```python
# In ui_panel.py, register() function:

WindowManager.ai3d_panel_tab = EnumProperty(
    name="AI3D Tab",
    items=[
        ('TEXT', "Text to 3D", "Text to 3D generation"),
        ('IMAGE', "Image to 3D", "Image to 3D generation"),
        ('ADVANCED', "Advanced", "Advanced options"),  # New tab
    ],
    default='TEXT'
)

# In draw() method:
if context.window_manager.ai3d_panel_tab == 'ADVANCED':
    self._draw_advanced_options(layout, scene)

# Add method:
def _draw_advanced_options(self, layout, scene):
    """Draw advanced options tab."""
    box = layout.box()
    # ... UI elements ...
```

---

## 🐛 Debugging & Testing

### Enable Debug Output

```python
# In operators.py
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Usage:
logger.debug(f"Job ID: {job_id}")
logger.info(f"Status: {status}")
logger.error(f"Error: {error}")
```

### Test Provider Client Directly

```python
# Test script (can run in Blender Python console)
import sys
sys.path.append(r"C:\path\to\addon\folder")

from providers import TripoClient

client = TripoClient("your_api_key")

# Test connection
success, msg = client.test_connection()
print(f"Success: {success}, Message: {msg}")

# Test text generation
result = client.generate_text("red cube", "realistic", 7, "glb")
print(f"Result: {result}")

# Test status polling
if result.get('job_id'):
    status = client.poll_status(result['job_id'])
    print(f"Status: {status}")
```

### Logging Requests

```python
# In provider client
import logging
import requests

logging.basicConfig(level=logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True
```

### Error Handling Best Practices

```python
try:
    response = requests.post(url, json=payload, timeout=30)
    response.raise_for_status()  # Raise on 4xx/5xx
    
    data = response.json()
    
    # Validate response structure
    if not data.get('id'):
        raise ValueError("Missing 'id' in response")
    
    return {"job_id": data['id'], "status": "pending"}

except requests.exceptions.Timeout:
    return {"error": "Request timeout", "job_id": None}

except requests.exceptions.HTTPError as e:
    if e.response.status_code == 401:
        return {"error": "Invalid API key", "job_id": None}
    else:
        return {"error": f"HTTP {e.response.status_code}", "job_id": None}

except requests.exceptions.RequestException as e:
    return {"error": f"Network error: {str(e)}", "job_id": None}

except (ValueError, KeyError) as e:
    return {"error": f"Invalid response format: {str(e)}", "job_id": None}
```

---

## 📋 Code Style Guide

### Python Style

Follow PEP 8:
- Line length: Max 100 characters
- Indentation: 4 spaces
- Naming: snake_case untuk functions/variables, PascalCase untuk classes

```python
# ✅ Good
def get_provider_client(context):
    """Get provider client based on scene settings."""
    prefs = context.preferences.addons['ai_3d_generator'].preferences
    return create_client(prefs)

# ❌ Bad
def GetProviderClient(c):
    p = c.preferences.addons['ai_3d_generator'].preferences
    return c
```

### Docstrings

Use Google-style docstrings:

```python
def generate_text(self, prompt: str, style: str) -> Dict[str, Any]:
    """
    Generate 3D model dari text prompt.
    
    Args:
        prompt: Text description of the object
        style: Visual style (cartoon, realistic, etc)
    
    Returns:
        Dict dengan keys 'job_id' dan 'status'
    
    Raises:
        RequestException: Jika API call gagal
    """
    pass
```

### Type Hints

Gunakan type hints:

```python
# ✅ Good
def poll_status(self, job_id: str) -> Dict[str, Any]:
    pass

# ❌ Bad
def poll_status(self, job_id):
    pass
```

### Error Messages

User-friendly error messages:

```python
# ✅ Good
return {"error": "Invalid API key - check Preferences > Add-ons"}

# ❌ Bad
return {"error": "401"}
```

---

## 🔄 Testing Checklist

Before submitting changes:

- [ ] Code follows style guide
- [ ] All functions have docstrings
- [ ] Type hints untuk all function signatures
- [ ] Error handling comprehensive
- [ ] Tested dengan multiple providers
- [ ] UI responsive (no freezing)
- [ ] Preferences save/load correctly
- [ ] No hardcoded paths
- [ ] No debug prints (use logging)
- [ ] Comments untuk complex logic
- [ ] Clean up temp files
- [ ] Handle network errors gracefully

---

## 🚀 Performance Optimization

### API Request Optimization

```python
# ✅ Good - reuse session
session = requests.Session()
response = session.post(url, json=payload, timeout=30)

# ❌ Bad - create new connection each time
response = requests.post(url, json=payload)
```

### Memory Management

```python
# ✅ Good - stream large files
response = requests.get(url, stream=True)
with open(filepath, 'wb') as f:
    for chunk in response.iter_content(chunk_size=8192):
        f.write(chunk)

# ❌ Bad - load entire file to memory
response = requests.get(url)
content = response.content  # All in memory
```

### Async Polling

```python
# ✅ Good - non-blocking with timer
def _poll_periodic(context):
    """Poll status every few seconds (non-blocking)."""
    if not context.scene.ai3d_current_job_id:
        return None  # Remove timer
    
    # Do poll here
    return 5  # Call again in 5 seconds

wm.modal_handler_add(self)

# ❌ Bad - blocking loop
while True:
    status = client.poll_status(job_id)
    time.sleep(5)  # Blocks UI!
```

---

## 📦 Distribution & Packaging

### Create Release

1. Update version di `__init__.py`
2. Update CHANGELOG
3. Test thoroughly
4. Tag release: `git tag v1.0.1`
5. Create GitHub release

### Addon Packaging

```bash
# Create zip for distribution
zip -r ai_3d_generator-1.0.1.zip ai_3d_generator/
```

### README.md in Release

Include:
- Installation instructions
- Quick start guide
- Known issues
- Changelog

---

## 🔗 API Integration Patterns

### Standard Response Format

```python
# Success response
{
    "job_id": "unique_job_id",
    "status": "pending|completed|failed",
    "model_url": "https://...",  # Only if completed
    "error": None
}

# Error response
{
    "job_id": None,
    "status": "failed",
    "error": "Human-readable error message"
}
```

### Polling Strategy

```python
POLLING_INTERVAL = 5  # seconds
MAX_POLLS = 600       # ~50 minutes

STATUS_PENDING = ['pending', 'processing', 'queued']
STATUS_COMPLETED = ['completed', 'succeeded', 'done']
STATUS_FAILED = ['failed', 'error', 'cancelled']

def should_continue_polling(status):
    return status.lower() in STATUS_PENDING
```

---

## 💡 Best Practices

### API Design
- Always check `response.status_code` before parsing JSON
- Use timeout on all requests (prevent hanging)
- Handle partial/incomplete responses
- Implement exponential backoff for retries

### UI Design
- Keep UI responsive (use non-blocking operations)
- Provide clear feedback to user
- Show progress/status updates
- Allow cancellation of operations
- Don't assume file paths (use file dialogs)

### Error Handling
- Log errors for debugging
- Show user-friendly messages
- Don't expose internal details
- Handle network errors gracefully
- Provide recovery options

### Testing
- Test with invalid API keys
- Test with no internet connection
- Test with corrupt files
- Test with extreme values
- Test with rapid successive calls

---

## 📚 References

### Blender API
- https://docs.blender.org/api/current/
- https://docs.blender.org/api/current/bpy_types.html

### Python
- https://peps.python.org/pep-0008/ (Style Guide)
- https://peps.python.org/pep-0257/ (Docstrings)
- https://docs.python.org/3/library/requests/ (Requests)

### Providers
- https://www.tripo3d.ai/docs
- https://www.meshy.ai/docs
- https://www.modelslab.com/docs

---

**Developer Guide Version**: 1.0  
**Last Updated**: January 2026  
**Target Audience**: Developers & Contributors
