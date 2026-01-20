# AI 3D Generator - Blender Add-on

**Unified AI 3D Generation Client untuk Blender 3.x**

Addon ini menyediakan interface yang konsisten dan user-friendly untuk mengakses multiple AI 3D generation services (Tripo, Meshy, dan ModelsLab) langsung dari Blender.

⚠️ **Disclaimer**: Addon ini hanya bertindak sebagai **client** untuk layanan AI pihak ketiga. Addon **tidak** melakukan pemrosesan AI secara lokal. User **wajib** mendaftar dan menyediakan API key sendiri dari masing-masing provider.

---

## 📋 Daftar Isi

- [Instalasi](#instalasi)
- [Setup Awal](#setup-awal)
- [Fitur Utama](#fitur-utama)
- [User Interface](#user-interface)
- [Arsitektur Kode](#arsitektur-kode)
- [Panduan Penggunaan](#panduan-penggunaan)
- [Troubleshooting](#troubleshooting)

---

## 🔧 Instalasi

### Persyaratan Sistem
- **Blender**: 3.0.0 atau lebih tinggi
- **Python**: 3.10+ (included dengan Blender)
- **Dependencies**: `requests` (biasanya sudah ada di Blender)

### Langkah-Langkah Instalasi

1. **Copy addon folder** ke Blender add-ons directory:
   - **Windows**: `C:\Users\[YourUsername]\AppData\Roaming\Blender Foundation\Blender\[Version]\scripts\addons\`
   - **macOS**: `~/Library/Application Support/Blender/[Version]/scripts/addons/`
   - **Linux**: `~/.config/blender/[Version]/scripts/addons/`

   Nama folder harus: `ai_3d_generator`

2. **Buka Blender** dan masuk ke:
   - Menu: `Edit` → `Preferences`
   - Panel: `Add-ons`
   - Cari: "AI 3D Generator"
   - **Enable** checkbox addon

3. **Konfigurasi API Keys** (lihat bagian Setup Awal)

---

## 🚀 Setup Awal

### 1. Dapatkan API Keys

#### Tripo 3D
- Visit: https://www.tripo3d.ai/
- Sign up dan create account
- Dapatkan API key dari dashboard
- (Optional) Catat custom Base URL jika ada

#### Meshy
- Visit: https://www.meshy.ai/
- Sign up dan create account
- Dapatkan API key dari dashboard
- (Optional) Catat custom Base URL

#### ModelsLab / 3D Verse
- Visit: https://www.modelslab.com/
- Sign up dan create account
- Dapatkan API key dari dashboard
- (Optional) Catat custom Base URL

### 2. Konfigurasi di Blender

1. **Buka Addon Preferences**:
   - `Edit` → `Preferences` → `Add-ons` → `AI 3D Generator`

2. **Masukkan API Keys**:
   - Untuk setiap provider yang ingin digunakan, masukkan:
     - API Key (masked untuk keamanan)
     - Base URL (optional, sudah ada default)
   
3. **Test Connection**:
   - Klik button "Open [Provider] Docs" untuk verifikasi URL
   - Atau gunakan "Test Provider" button di 3D View panel

---

## ✨ Fitur Utama

### 1. Text to 3D Generation

**Input**:
- Text prompt deskriptif (misal: "red cube made of clay")
- Style selection (Cartoon, Realistic, Clay, Sci-Fi)
- Quality/Detail level (1-10)
- Output format (GLB, OBJ, FBX, STL)

**Output**:
- Model 3D otomatis di-import ke scene
- Ditempatkan di 3D Cursor position
- Named: `{provider}_{prompt_preview}`

### 2. Image to 3D Generation

**Input**:
- Single image file (PNG, JPG)
- Style selection
- Quality/Detail level
- Background removal option (jika provider support)
- Output format

**Output**:
- Model 3D hasil dari image di-import ke scene
- Sama naming convention seperti text mode

### 3. Provider Management

- **One-click Provider Selection**: Dropdown di main panel
- **Test Connection**: Verify API key & network connectivity
- **Quick Documentation Access**: Buttons ke official docs
- **Flexible Configuration**: Custom base URLs supported

### 4. Job Tracking

- Real-time job status monitoring
- Job ID tracking
- Auto-polling completion status
- Cancel generation anytime

---

## 🎨 User Interface

### Panel Location
**View3D** → **Sidebar (N-Panel)** → **AI 3D Generator**

### Panel Sections

#### 1. Provider Selection
```
[Provider Dropdown: Tripo / Meshy / ModelsLab]
[Test Provider Button]
```

#### 2. Text to 3D Tab
```
Prompt:        [Multiline Text Input]
Style:         [Dropdown: Cartoon, Realistic, Clay, Sci-Fi]
Quality:       [Slider: 1-10]
Format:        [Dropdown: GLB, OBJ, FBX, STL]
[Generate from Text Button]
```

#### 3. Image to 3D Tab
```
Image:         [File Picker]
Style:         [Dropdown: Cartoon, Realistic, Clay, Sci-Fi]
Quality:       [Slider: 1-10]
BG Removal:    [Checkbox]
Format:        [Dropdown: GLB, OBJ, FBX, STL]
[Generate from Image Button]
```

#### 4. Generation Status
```
Job ID: [Last 12 chars of ID]
[Check Status Button] [Cancel Button]
```

---

## 🏗️ Arsitektur Kode

### Struktur File

```
ai_3d_generator/
├── __init__.py           # Main addon file, registration, properties
├── preferences.py         # API preferences panel
├── ui_panel.py           # UI panels untuk 3D View sidebar
├── operators.py          # Blender operators (generate, test, poll)
├── downloader.py         # Model download & import utilities
└── providers/
    ├── __init__.py
    ├── base_client.py     # Abstract base class
    ├── tripo_client.py    # Tripo API client
    ├── meshy_client.py    # Meshy API client
    └── modelslab_client.py # ModelsLab API client
```

### Design Patterns

#### 1. Abstract Base Class Pattern
```python
class BaseProviderClient(ABC):
    @abstractmethod
    def generate_text(self, ...): pass
    
    @abstractmethod
    def generate_image(self, ...): pass
    
    @abstractmethod
    def poll_status(self, ...): pass
```

**Benefit**: UI & operators tidak perlu tahu detail setiap provider

#### 2. Provider Abstraction
- `TripoClient(BaseProviderClient)`
- `MeshyClient(BaseProviderClient)`
- `ModelsLabClient(BaseProviderClient)`

Setiap provider implement endpoint-specific logic, style mapping, dll.

#### 3. Async Job + Polling
```
1. Call generate_*() → get job_id
2. Store job_id di scene property
3. Poll status setiap interval
4. Saat completed → download & import
```

#### 4. Modular Import System
- Download model ke temp folder
- Import berdasarkan format (GLB, OBJ, FBX, STL)
- Auto-cleanup temp files

---

## 📖 Panduan Penggunaan

### Workflow Text to 3D

1. **Buka 3D View Sidebar**:
   - Tekan `N` atau menu: `View` → `Toggle Sidebar`

2. **Pilih Tab "Text to 3D"**

3. **Masukkan Detail**:
   - **Prompt**: Deskripsi yang detail dan jelas
     - ✅ Good: "Red ceramic vase with flower pattern"
     - ❌ Bad: "vase"
   - **Style**: Pilih style visual yang diinginkan
   - **Quality**: Slider untuk detail level (7-8 umumnya cukup)
   - **Format**: GLB recommended untuk Blender

4. **Klik "Generate from Text"**

5. **Monitor Progress**:
   - Lihat Job ID yang muncul
   - Klik "Check Status" untuk manual poll
   - Processing bisa 2-10 menit (tergantung provider & queue)

6. **Model Imported**:
   - Otomatis di-import saat completed
   - Positioned di 3D Cursor
   - Siap untuk edit/render

### Workflow Image to 3D

1. **Persiapan Image**:
   - Format: PNG or JPG
   - Clear subject, good lighting
   - Size: 512x512 - 2048x2048 optimal

2. **Buka Tab "Image to 3D"**

3. **Select Image**:
   - Klik file picker button
   - Pilih image dari disk

4. **Konfigurasi**:
   - **Style**: Untuk texture/material guidance
   - **Quality**: Detail level
   - **BG Removal**: Enable jika image punya background kompleks
   - **Format**: GLB recommended

5. **Klik "Generate from Image"**

6. **Wait & Import**:
   - Same process seperti text-to-3D
   - Hasil biasanya lebih detail dari text

### API Key Setup

1. **Buka Preferences**:
   - `Edit` → `Preferences` → `Add-ons`
   - Cari "AI 3D Generator"
   - Click expand icon

2. **Setiap Provider**:
   - Paste API key (akan di-mask)
   - (Optional) Ubah base URL jika custom
   - Klik "Open [Provider] Docs" untuk verify

3. **Test Connection**:
   - Di main panel, klik "Test Provider"
   - Akan show success/error message

---

## 🔄 Async Polling Mechanism

Model generation berjalan asynchronously di server provider. Addon menggunakan polling untuk check status:

```
User clicks "Generate"
    ↓
API call → job_id returned
    ↓
Store job_id di scene.ai3d_current_job_id
    ↓
Modal operator start polling (bpy.app.timers)
    ↓
Poll every 5-10 seconds:
  - GET /status/{job_id}
  - If "completed": download & import
  - If "pending": continue polling
  - If "failed": show error
    ↓
Model imported, cancel polling
```

**Keuntungan**:
- User bisa continue bekerja di Blender saat waiting
- Tidak block UI
- Auto-retry network errors

---

## 📥 Model Download & Import

### Supported Formats

| Format | Import Operator | Best For |
|--------|-----------------|----------|
| GLB | `bpy.ops.import_scene.gltf` | Recommended - preserves materials |
| OBJ | `bpy.ops.import_scene.obj` | Geometry only |
| FBX | `bpy.ops.import_scene.fbx` | Rigged models |
| STL | `bpy.ops.import_mesh.stl` | 3D printing |

### Import Process

1. **Download** model file dari provider URL
2. **Save** to temp folder (`%TEMP%` on Windows)
3. **Import** using Blender's native operators
4. **Cleanup** delete temp file
5. **Rename** object to `{provider}_{name}`
6. **View** center 3D view pada object

---

## ⚙️ Custom Configuration

### Change Base URLs

Jika provider menggunakan custom domain:

1. Buka Preferences
2. Expand provider section
3. Edit "Base URL" field
4. Ensure format: `https://api.example.com` (no trailing slash)

### Style Mapping

Setiap provider memiliki internal style parameter yang berbeda. Addon melakukan mapping otomatis:

```python
style_mapping = {
    'CARTOON': 'cartoon',    # User selection → provider param
    'REALISTIC': 'realistic',
    'CLAY': 'clay',
    'SCIFI': 'sci-fi',
}
```

Jika provider tidak support style tertentu, akan default ke 'realistic'.

### Quality Mapping

Addon normalize quality 1-10 ke provider-specific values:

```python
quality_mapping = {
    1-3: 'low',
    4-6: 'medium',
    7-9: 'high',
    10: 'ultra'
}
```

---

## 🐛 Troubleshooting

### Problem: "Invalid API Key"

**Solution**:
1. Verify API key copied correctly (no extra spaces)
2. Check API key valid di provider's dashboard
3. Ensure API key bukan expired/revoked
4. Try "Test Provider" button untuk detailed error

### Problem: "Cannot Connect to API"

**Solution**:
1. Check internet connection
2. Verify Base URL correct (try opening in browser)
3. Check firewall/proxy settings
4. Try different provider (rule out local network issue)

### Problem: "Download Failed"

**Solution**:
1. Model URL might be expired (job_id stale)
2. Try "Check Status" again
3. Re-generate model baru
4. Check if model file size reasonable (>1MB)

### Problem: "Import Failed" or Model Not Appearing

**Solution**:
1. Check output format matches file (GLB/OBJ/FBX/STL)
2. Ensure 3D Cursor di center scene
3. Try scaling model: select → `S` → `2` → `Enter`
4. Check if imported dengan extreme scale/location
5. Try different format (GLB most compatible)

### Problem: Generation Stuck/Timeout

**Solution**:
1. Click "Check Status" to manually poll
2. Provider might be overloaded (common during peak hours)
3. Cancel & retry later
4. Try smaller prompt atau lower quality setting

### Problem: Preferences Not Saving

**Solution**:
1. Blender preferences auto-save on exit
2. Make sure using Edit > Preferences (not user preferences)
3. Addon harus enabled saat konfigurasi
4. Restart Blender jika issue persists

---

## 📊 Performance Tips

### For Faster Results

1. **Optimize Prompts**:
   - Be specific & descriptive
   - Include style/material hints
   - Avoid overly complex descriptions

2. **Choose Appropriate Quality**:
   - Quality 7-8: Good balance speed/detail
   - Quality 10: Highest detail (slower)
   - Quality 5: Quick previews

3. **Select Best Format**:
   - GLB: Fastest (binary, optimized)
   - OBJ: Slower but universal
   - FBX: Good for rigged models
   - STL: Only for 3D printing

4. **Image Preparation**:
   - 1024x1024: Sweet spot (fast, good detail)
   - Crop close to subject
   - Avoid cluttered backgrounds
   - Good lighting in image

### For Higher Quality

1. **Use Detailed Prompts**:
   - Include materials: "ceramic", "metal", etc.
   - Specify style: "realistic", "cartoon", etc.
   - Add details: "with intricate patterns"

2. **Better Images**:
   - Higher resolution (up to 2048x2048)
   - Multiple angles if multi-view supported
   - Remove background
   - Professional lighting

3. **Quality Setting**:
   - Set to 9-10 untuk maximum detail
   - Accept longer processing time

---

## 🔐 Security Notes

### API Key Protection

- API keys stored di Blender preferences (encrypted by Blender)
- Never commit API keys to version control
- Never share .blend files containing API key prefs
- Reset API keys in provider dashboard if compromised

### Network Security

- All requests use HTTPS
- Provider URLs must use `https://` prefix
- Addon uses `requests` library with proper SSL verification

### Data Privacy

- Generated models processed by provider's servers
- Check provider's privacy policy for data retention
- Downloaded models saved only to temp folder
- Temp files auto-deleted after import

---

## 📝 API Reference (For Developers)

### Instantiate Provider

```python
from providers import TripoClient, MeshyClient, ModelsLabClient

# Tripo
client = TripoClient(api_key="your_key", base_url="https://platform.tripo3d.ai")

# Meshy
client = MeshyClient(api_key="your_key", base_url="https://api.meshy.ai")

# ModelsLab
client = ModelsLabClient(api_key="your_key", base_url="https://api.modelslab.com")
```

### Generate Methods

```python
# Text to 3D
result = client.generate_text(
    prompt="red cube",
    style="realistic",
    quality=7,
    output_format="glb"
)
# Returns: {"job_id": "xxx", "status": "pending"}

# Image to 3D
result = client.generate_image(
    image_path="/path/to/image.png",
    style="realistic",
    quality=7,
    output_format="glb",
    background_removal=True
)
# Returns: {"job_id": "xxx", "status": "pending"}
```

### Poll Status

```python
result = client.poll_status("job_id_here")
# Returns: {"status": "completed", "model_url": "https://..."}
#       or {"status": "pending", "job_id": "..."}
#       or {"status": "failed", "error": "message"}
```

### Test Connection

```python
success, message = client.test_connection()
# Returns: (True, "Connection successful!")
#       or (False, "Invalid API key")
```

---

## 🤝 Contributing

Untuk menambah provider baru:

1. Extend `BaseProviderClient`
2. Implement: `generate_text()`, `generate_image()`, `poll_status()`, `test_connection()`
3. Add client ke `providers/__init__.py`
4. Add enum option di `__init__.py` preferences
5. Test dengan existing UI/operators

---

## 📄 License

Addon ini dibuat sebagai tool utility. Setiap provider memiliki Terms of Service sendiri - pastikan comply dengan ketentuan mereka.

---

## 📞 Support

### Quick Help
- 🔍 Check preferences API keys valid
- 🌐 Test internet connection
- 🔄 Try "Test Provider" button
- ⏱️ Wait for queue (popular times slower)

### Common Issues
- See [Troubleshooting](#troubleshooting) section above

### Provider Support
- Tripo: https://www.tripo3d.ai/help
- Meshy: https://www.meshy.ai/support
- ModelsLab: https://www.modelslab.com/help

---

**Version**: 1.0.0  
**Last Updated**: January 2026  
**Blender Target**: 3.0.0+
