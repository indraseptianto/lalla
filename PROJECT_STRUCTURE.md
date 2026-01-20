# Project Structure & File Reference

## 📁 Directory Layout

```
ai_3d_generator/
│
├── 📄 Core Addon Files
│   ├── __init__.py                  # Main addon entry point & registration
│   ├── preferences.py               # Addon preferences & API key config
│   ├── ui_panel.py                 # 3D View sidebar UI panels
│   ├── operators.py                # Blender operators (generate, test, poll)
│   └── downloader.py               # Model download & import utilities
│
├── 📁 providers/                    # Provider client implementations
│   ├── __init__.py                 # Package init & exports
│   ├── base_client.py              # Abstract base class (interface)
│   ├── tripo_client.py             # Tripo 3D implementation
│   ├── meshy_client.py             # Meshy implementation
│   └── modelslab_client.py         # ModelsLab / 3D Verse implementation
│
├── 📚 Documentation
│   ├── README.md                   # Complete user documentation
│   ├── QUICKSTART.md               # 5-minute quick start guide
│   ├── INSTALL.md                  # Detailed installation & setup
│   ├── CONFIG_REFERENCE.md         # API endpoints & configuration details
│   ├── DEVELOPER_GUIDE.md          # For developers extending addon
│   ├── CHANGELOG.md                # Version history & roadmap
│   └── PROJECT_STRUCTURE.md        # This file
│
├── 🔧 Configuration
│   ├── .gitignore                  # Git ignore rules
│   └── requirements.txt            # Python dependencies (reference)
│
└── 📦 Generated at Runtime (not in repo)
    └── __pycache__/                # Python bytecode cache
```

---

## 📄 File Reference

### Core Addon Files

#### `__init__.py` (Main Entry Point)
- **Purpose**: Addon initialization, registration, properties
- **Size**: ~200 lines
- **Key Functions**:
  - `register()`: Register addon components (preferences, operators, UI)
  - `unregister()`: Cleanup on addon disable
  - `register_properties()`: Define scene properties (prompt, style, job_id, etc.)
  - `unregister_properties()`: Cleanup properties
- **Responsibilities**:
  - Define `bl_info` (addon metadata)
  - Import submodules
  - Register/unregister in correct order
  - Define scene properties for UI

#### `preferences.py` (Addon Settings)
- **Purpose**: User configuration panel for API keys
- **Size**: ~120 lines
- **Key Classes**:
  - `AI3DGeneratorPreferences(AddonPreferences)`: Main preferences class
- **Properties**:
  - Tripo: `tripo_api_key`, `tripo_base_url`
  - Meshy: `meshy_api_key`, `meshy_base_url`
  - ModelsLab: `modelslab_api_key`, `modelslab_base_url`
- **Features**:
  - Masked password input for keys
  - Custom base URL support
  - Quick links to provider docs
  - Auto-save by Blender

#### `ui_panel.py` (3D View UI)
- **Purpose**: Create sidebar panel with generation UI
- **Size**: ~150 lines
- **Key Classes**:
  - `AI3DGeneratorPanel`: Main UI panel
  - `AI3DGeneratorPreferencesPanel`: Quick access to preferences
- **Features**:
  - Provider selection dropdown
  - Tab switching (Text to 3D / Image to 3D)
  - Style & quality sliders
  - File picker for images
  - Job status display
  - Real-time feedback
- **Registered As**: `VIEW3D_PT_ai3d_generator`

#### `operators.py` (User Actions)
- **Purpose**: Execute generation, testing, polling
- **Size**: ~250 lines
- **Key Classes**:
  - `AI3DGenerateText`: Generate from text prompt
  - `AI3DGenerateImage`: Generate from image file
  - `AI3DTestProvider`: Test API connection
  - `AI3DCheckStatus`: Manual status polling
  - `AI3DCancelGeneration`: Stop active generation
- **Features**:
  - Non-blocking async operations
  - Modal handlers for polling
  - Error reporting to user
  - Auto-import on completion
- **Registered As**: 
  - `ai3d.generate_text`
  - `ai3d.generate_image`
  - `ai3d.test_provider`
  - `ai3d.check_status`
  - `ai3d.cancel_generation`

#### `downloader.py` (Model Import)
- **Purpose**: Download models from URLs, import into Blender
- **Size**: ~200 lines
- **Key Functions**:
  - `download_and_import_model()`: Main workflow
  - `download_model_file()`: HTTP download to temp
  - `_import_gltf()`, `_import_obj()`, `_import_fbx()`, `_import_stl()`: Format-specific import
- **Features**:
  - Streaming download (prevent memory bloat)
  - Format auto-detection
  - Proper error handling
  - Temp file cleanup
  - Object naming & view centering
  - Works with all Blender import operators

### Provider Clients

#### `providers/base_client.py` (Interface)
- **Purpose**: Abstract base class defining provider interface
- **Size**: ~80 lines
- **Key Class**:
  - `BaseProviderClient(ABC)`: Abstract base
- **Key Methods**:
  - `generate_text()`: Text → 3D model
  - `generate_image()`: Image → 3D model
  - `poll_status()`: Check generation status
  - `test_connection()`: Verify API key & connectivity
- **Design Pattern**: Strategy pattern + Template method

#### `providers/tripo_client.py`
- **Purpose**: Tripo 3D API implementation
- **Size**: ~180 lines
- **Base URL**: `https://platform.tripo3d.ai` (customizable)
- **API Endpoints**:
  - `POST /api/v1/generate`: Submit job
  - `GET /api/v1/jobs/{id}`: Check status
  - `GET /api/v1/user`: Test connection
- **Features**:
  - Style mapping (cartoon, realistic, clay, sci-fi)
  - Quality level support
  - Multi-format output
  - Bearer token authorization
  - Comprehensive error handling

#### `providers/meshy_client.py`
- **Purpose**: Meshy API implementation
- **Size**: ~200 lines
- **Base URL**: `https://api.meshy.ai` (customizable)
- **API Endpoints**:
  - `POST /openapi/v1/text-to-3d`: Text generation
  - `POST /openapi/v1/image-to-3d`: Image generation
  - `GET /openapi/v1/tasks/{id}`: Status check
  - `GET /openapi/v1/user/profile`: Test connection
- **Features**:
  - Multiple AI models (meshy-4, meshy-4-turbo)
  - Gaussian splatting support
  - Background removal option
  - Texture richness configuration
  - Quality/art style mapping

#### `providers/modelslab_client.py`
- **Purpose**: ModelsLab / 3D Verse API implementation
- **Size**: ~190 lines
- **Base URL**: `https://api.modelslab.com` (customizable)
- **API Endpoints**:
  - `POST /api/v1/3dverse/text-to-3d`: Text generation
  - `POST /api/v1/3dverse/image-to-3d`: Image generation
  - `GET /api/v1/3dverse/status/{id}`: Status check
  - `GET /api/v1/user/info`: Test connection
- **Features**:
  - 3D Verse format support
  - Quality level mapping
  - Multiple output formats
  - Custom endpoint support

### Documentation Files

#### `README.md` (Main Documentation)
- **Purpose**: Complete user guide
- **Length**: ~800 lines
- **Sections**:
  - Installation & system requirements
  - Setup & API key configuration
  - Feature overview & usage workflows
  - UI panel reference
  - Architecture explanation
  - Troubleshooting guide
  - Performance tips & best practices
  - FAQ

#### `QUICKSTART.md` (5-Minute Guide)
- **Purpose**: Get users generating in 5 minutes
- **Length**: ~150 lines
- **Sections**:
  - Quick install
  - API key signup
  - First generation walkthrough
  - Tips & troubleshooting
  - Next steps

#### `INSTALL.md` (Installation Guide)
- **Purpose**: Detailed step-by-step installation
- **Length**: ~300 lines
- **Sections**:
  - System requirements & prerequisites
  - Addon download & location
  - Enable in Blender
  - API key configuration per provider
  - First run verification
  - Troubleshooting
  - Uninstallation

#### `CONFIG_REFERENCE.md` (Technical Reference)
- **Purpose**: API endpoints, configuration details, comparisons
- **Length**: ~400 lines
- **Sections**:
  - Provider-specific API configuration
  - Endpoint URLs & authentication
  - Supported features matrix
  - Network & proxy settings
  - Polling strategy
  - Rate limits & pricing
  - Security best practices

#### `DEVELOPER_GUIDE.md` (Extension Guide)
- **Purpose**: For developers extending addon
- **Length**: ~500 lines
- **Sections**:
  - Architecture overview
  - Adding new providers (step-by-step)
  - UI customization
  - Debugging & testing
  - Code style guide
  - Performance optimization
  - Testing checklist

#### `CHANGELOG.md` (Version History)
- **Purpose**: Track changes & plan roadmap
- **Sections**:
  - Release notes per version
  - Added/Changed/Fixed items
  - Known limitations
  - Future roadmap
  - Contributing guidelines

#### `PROJECT_STRUCTURE.md` (This File)
- **Purpose**: File-by-file reference guide
- **Helps**: Understanding codebase organization

---

## 🔄 Module Dependencies

```
__init__.py
├── preferences.py
├── ui_panel.py
├── operators.py
│   ├── providers/base_client.py
│   ├── providers/tripo_client.py
│   ├── providers/meshy_client.py
│   ├── providers/modelslab_client.py
│   └── downloader.py
│       └── (bpy native operators)
└── providers/__init__.py
    ├── base_client.py
    ├── tripo_client.py
    ├── meshy_client.py
    └── modelslab_client.py
```

---

## 📊 Code Statistics

| File | Lines | Purpose | Complexity |
|------|-------|---------|-----------|
| `__init__.py` | ~200 | Entry point | Low |
| `preferences.py` | ~120 | API config | Low |
| `ui_panel.py` | ~150 | UI panels | Medium |
| `operators.py` | ~250 | Actions | Medium |
| `downloader.py` | ~200 | Import | Medium |
| `base_client.py` | ~80 | Interface | Low |
| `tripo_client.py` | ~180 | Tripo API | Medium |
| `meshy_client.py` | ~200 | Meshy API | Medium |
| `modelslab_client.py` | ~190 | ModelsLab API | Medium |
| **TOTAL** | **~1,570** | **Addon Core** | **Medium** |
| Documentation | ~2,500 | Guides | - |
| **TOTAL PROJECT** | **~4,000** | **Complete** | **High** |

---

## 🔐 Security Considerations by File

| File | Security Aspect |
|------|-----------------|
| `preferences.py` | API keys masked with `subtype='PASSWORD'` |
| `operators.py` | User input validation before API calls |
| `providers/*.py` | HTTPS only, SSL verification enabled |
| `downloader.py` | Temp files deleted after use |
| `.gitignore` | API keys in `.env` excluded from git |

---

## 🏗️ Design Patterns Used

### 1. Abstract Factory Pattern
```
BaseProviderClient (abstract)
├── TripoClient (concrete)
├── MeshyClient (concrete)
└── ModelsLabClient (concrete)
```

### 2. Strategy Pattern
Providers implement same interface, UI selects strategy at runtime

### 3. Observer Pattern
UI listens to scene properties, updates feedback in real-time

### 4. Singleton Pattern
One provider client instance per generation session

### 5. Template Method Pattern
Provider clients use same polling/import workflow, customize details

---

## 📈 Code Quality Metrics

- **Type Hints**: ~80% coverage
- **Docstrings**: All public functions documented
- **Error Handling**: Comprehensive try-except blocks
- **Code Reuse**: High (shared interface, utilities)
- **Modularity**: High (providers completely decoupled from UI)
- **Testability**: High (provider clients can be tested standalone)

---

## 🔄 Change Workflow

When modifying files:

1. **Update Core Addon**:
   - Modify `__init__.py`, `ui_panel.py`, `operators.py`, etc.
   - Update version in `__init__.py`
   - Test thoroughly with all providers

2. **Add Provider**:
   - Create new client in `providers/new_provider.py`
   - Extend `BaseProviderClient`
   - Add to `providers/__init__.py`
   - Update `operators.py`
   - Update `preferences.py`
   - Test with new provider

3. **Update Documentation**:
   - Update relevant `.md` files
   - Update `CHANGELOG.md`
   - Update `DEVELOPER_GUIDE.md` if new patterns
   - Ensure consistency across docs

4. **Commit to Git**:
   ```bash
   git add .
   git commit -m "Description of changes"
   git push origin branch-name
   ```

---

## 🧪 File Modification Guidelines

### DON'T Modify These Files
- `base_client.py` (abstract interface, changing breaks all providers)
- `.gitignore` (only add new patterns as needed)

### Safe to Modify
- Provider clients (isolated from each other)
- `operators.py` (safe to enhance with new operators)
- `ui_panel.py` (safe to add new UI elements)
- Documentation (always safe)

### Requires Testing
- `__init__.py` (registration order matters)
- `preferences.py` (property changes need Blender reload)
- `downloader.py` (affects import process)

---

## 📦 Distribution Files

When packaging for release:

```bash
# Create distribution ZIP
zip -r ai_3d_generator-1.0.0.zip ai_3d_generator/

# Include in ZIP:
✅ All .py files
✅ providers/ folder
✅ README.md
✅ QUICKSTART.md
✅ INSTALL.md
✅ CHANGELOG.md

❌ Don't include:
❌ __pycache__/
❌ .git/
❌ .vscode/
❌ *.blend files
❌ API keys / .env
```

---

**Project Structure Guide Version**: 1.0  
**Last Updated**: January 2026  
**For Version**: 1.0.0
