# AI 3D Generator - Panduan Instalasi & Setup

## 📋 Daftar Isi
1. [System Requirements](#system-requirements)
2. [Pre-Installation Checklist](#pre-installation-checklist)
3. [Installation Steps](#installation-steps)
4. [Initial Configuration](#initial-configuration)
5. [First Run](#first-run)
6. [Verification](#verification)

---

## ✅ System Requirements

### Minimum Requirements
- **Blender**: 3.0.0 atau lebih tinggi
- **Python**: 3.10+ (included dengan Blender)
- **RAM**: 4GB minimal
- **Disk Space**: 500MB free space
- **Network**: Stable internet connection (untuk API calls)

### Optional
- **GPU**: NVIDIA/AMD GPU untuk faster preview (tidak required)

### Supported Operating Systems
- ✅ Windows 10/11
- ✅ macOS 10.13+
- ✅ Linux (Ubuntu 18.04+, Fedora 28+)

### Browser (untuk API key registration)
- Chrome, Firefox, Safari, Edge (any modern browser)

---

## 🔍 Pre-Installation Checklist

Sebelum install, pastikan:

- [ ] Blender 3.0+ sudah installed
- [ ] Blender dapat run properly
- [ ] Internet connection stabil
- [ ] Akses ke terminal/command prompt
- [ ] Tidak ada conflicting addons (optional untuk dicheck)

### Test Blender Installation

**Windows**:
```powershell
# Check Blender version
cd "C:\Program Files\Blender Foundation\Blender 3.x"
blender --version
```

**macOS/Linux**:
```bash
blender --version
```

Expected output: `Blender 3.x.x ...`

---

## 📥 Installation Steps

### Step 1: Download Addon

Pilih salah satu method:

#### Option A: Download dari GitHub (Recommended)
```bash
# Gunakan git clone
git clone https://github.com/youruser/ai_3d_generator.git ai_3d_generator

# Atau download ZIP dan extract
# https://github.com/youruser/ai_3d_generator/archive/refs/heads/main.zip
```

#### Option B: Manual Copy
Jika sudah punya folder addon, copy ke location berikut:

### Step 2: Locate Blender Add-ons Directory

**Windows**:
```
C:\Users\[YourUsername]\AppData\Roaming\Blender Foundation\Blender\3.x\scripts\addons\
```

Shortcut: `Shift + Windows` → Type `%appdata%` → Navigate ke folder

**macOS**:
```
~/Library/Application Support/Blender/3.x/scripts/addons/
```

**Linux**:
```
~/.config/blender/3.x/scripts/addons/
```

### Step 3: Copy Addon Folder

Copy entire `ai_3d_generator` folder ke addons directory:

**Result folder structure**:
```
addons/
  ├── ai_3d_generator/
  │   ├── __init__.py
  │   ├── preferences.py
  │   ├── ui_panel.py
  │   ├── operators.py
  │   ├── downloader.py
  │   ├── README.md
  │   └── providers/
  │       ├── __init__.py
  │       ├── base_client.py
  │       ├── tripo_client.py
  │       ├── meshy_client.py
  │       └── modelslab_client.py
  └── [other addons...]
```

### Step 4: Enable Addon di Blender

1. **Open Blender**

2. **Go to Preferences**:
   - Menu: `Edit` → `Preferences`
   - Atau shortcut: `Alt + ,`

3. **Go to Add-ons**:
   - Click tab: `Add-ons` (left sidebar)

4. **Search Addon**:
   - Search box (top right): Type `"AI 3D Generator"`

5. **Enable Addon**:
   - Find entry: "AI 3D Generator" → Click checkbox ☑️
   - Status akan change to "Enabled"

6. **Close Preferences** (optional):
   - Blender auto-saves addon state

### Step 5: Verify Installation

Cek addon berhasil installed:

1. **Open 3D View** (if not already)
   - Workspace: `Layout`

2. **Toggle Sidebar**:
   - Press `N` key
   - Atau: Menu `View` → `Toggle Sidebar`

3. **Check Panel**:
   - Right sidebar → Look for tab labeled **"AI 3D Generator"**
   - Harus ada sections: Provider Selection, Test Provider button

✅ **Jika panel terlihat**, installation successful!

---

## ⚙️ Initial Configuration

### Prerequisite: Get API Keys

Sebelum konfigurasi, daftar dan dapatkan API keys dari:

#### 1. Tripo 3D
- **Website**: https://www.tripo3d.ai/
- **Sign up**: Click "Sign Up"
- **Get API Key**:
  1. Login ke dashboard
  2. Settings → API Keys
  3. Create new API key
  4. Copy key (save somewhere secure)
- **Optional - Custom URL**: Note custom endpoint jika ada

#### 2. Meshy
- **Website**: https://www.meshy.ai/
- **Sign up**: Click "Get Started"
- **Get API Key**:
  1. Login ke dashboard
  2. Account → API Keys
  3. Generate API key
  4. Copy & save
- **Optional - Custom URL**: Check dashboard untuk custom endpoints

#### 3. ModelsLab (3D Verse)
- **Website**: https://www.modelslab.com/
- **Sign up**: Click "Sign Up"
- **Get API Key**:
  1. Login ke account
  2. Account Settings → API Keys
  3. Create new key
  4. Copy key
- **Optional - Custom URL**: Document jika using custom 3D Verse endpoint

### Configure in Blender

1. **Open Preferences**:
   - `Edit` → `Preferences` (or `Alt + ,`)

2. **Go to Add-ons**:
   - Click `Add-ons` tab

3. **Find AI 3D Generator**:
   - Search: `"AI 3D Generator"`
   - Click expand arrow pada addon

4. **Configure Each Provider** (optional - only configure yang akan digunakan):

#### For Tripo:
```
✓ Tripo API Key:    [paste_your_tripo_key_here]
✓ Tripo Base URL:   https://platform.tripo3d.ai  ← default
```

#### For Meshy:
```
✓ Meshy API Key:    [paste_your_meshy_key_here]
✓ Meshy Base URL:   https://api.meshy.ai  ← default
```

#### For ModelsLab:
```
✓ ModelsLab API Key:    [paste_your_modelslab_key_here]
✓ ModelsLab Base URL:   https://api.modelslab.com  ← default
```

5. **Save Configuration**:
   - Blender auto-saves
   - Close Preferences window

---

## 🚀 First Run

### Test Configuration

1. **Open 3D View** dengan addon UI (toggle sidebar dengan `N`)

2. **Go to 3D View Sidebar**:
   - Panel: "AI 3D Generator"
   - Provider dropdown (should show "Tripo", "Meshy", "ModelsLab")

3. **Select a Provider** you configured:
   - Click dropdown → select provider

4. **Click "Test Provider"**:
   - Button di bawah provider dropdown
   - Tunggu 2-5 detik untuk response

5. **Check Result**:
   - ✅ Success message → "Connection successful!"
   - ❌ Error message → check API key & URL

### Troubleshoot First Run Issues

#### Issue: Addon not appearing di Add-ons list

**Solution**:
1. Check folder name exactly: `ai_3d_generator` (lowercase)
2. Ensure in correct addons directory (see Step 2)
3. Restart Blender completely
4. If still not showing: Check Blender console for error messages

#### Issue: "Invalid API key" error

**Solution**:
1. Copy API key lagi dari provider dashboard
2. Paste carefully (no extra spaces before/after)
3. Verify API key belum expired/revoked
4. Test dengan curl atau Postman (technical users)

#### Issue: "Cannot connect to API"

**Solution**:
1. Check internet connection (open provider website)
2. Verify base URL correct (try opening in browser)
3. Check firewall/proxy (corporate networks mungkin block)
4. Try different provider (rule out local issue)

#### Issue: Sidebar panel not showing

**Solution**:
1. Press `N` to toggle sidebar (atau `View` → `Toggle Sidebar`)
2. Check right side panel tabs
3. Look for "AI 3D Generator" tab
4. If not there: Addon may not be enabled (go back to Preferences)

---

## ✔️ Verification

Setelah installation & configuration, verify:

### Checklist

- [ ] Blender version 3.0+
- [ ] Addon enabled di Preferences
- [ ] All 3 folders exist: `providers/`, docs, etc.
- [ ] "AI 3D Generator" tab visible di 3D View sidebar
- [ ] Provider dropdown shows all options
- [ ] "Test Provider" button returns success message
- [ ] Can type prompt di Text to 3D tab
- [ ] Can select image di Image to 3D tab
- [ ] Output format dropdown has options (GLB, OBJ, FBX, STL)

### Quick Functionality Test

**Text to 3D Test**:
```
1. Set Provider: Tripo
2. Type Prompt: "small red ball"
3. Set Quality: 7
4. Click "Generate from Text"
5. Should see: Job ID message
6. Wait 2-5 minutes for model
7. Should auto-import when complete
```

**Image to 3D Test**:
```
1. Set Provider: Meshy
2. Select any image: Any simple PNG/JPG
3. Set Quality: 7
4. Click "Generate from Image"
5. Should see: Job ID message
6. Wait 2-5 minutes for model
7. Should auto-import when complete
```

---

## 📚 Next Steps

After successful installation:

1. **Read Full Documentation**: See [README.md](README.md)
2. **Learn UI**: Familiarize dengan panel layout & options
3. **Try First Generation**: Follow workflow di documentation
4. **Explore Providers**: Test each provider untuk comparison
5. **Optimize Prompts**: Learn best practices untuk better results

---

## 🔧 Uninstallation

Jika perlu uninstall:

### Option 1: Disable via Blender UI
1. `Edit` → `Preferences` → `Add-ons`
2. Find "AI 3D Generator"
3. Click checkbox to disable ☐
4. Click "Remove" button (jika visible)

### Option 2: Manual Removal
1. Delete folder: `[addon_directory]/ai_3d_generator/`
2. Restart Blender

### Important
- Preferences auto-saved → konfigurasi disimpan di `.blend` file jika ada
- Jika perlu remove completely: Delete preferences juga

---

## 💡 Tips & Tricks

### Installation Tips
- Install addon di default location (recommended)
- Jangan install di `scripts/startup/` (reserved untuk scripts)
- Keep addon folder structure intact (jangan rearrange files)

### Performance Tips
- Restart Blender after installation (fresh load)
- Disable other addons jika ada issue (test compatibility)
- Use latest Blender version untuk compatibility

### Troubleshooting Tips
- Keep error messages/console output (for debugging)
- Test internet connection separately
- Check provider status pages (sometimes down for maintenance)
- Try different provider jika satu down

---

## ❓ FAQ

**Q: Apakah addon illegal?**
A: Tidak. Addon adalah client yang authorized untuk use provider APIs dengan API keys legitimate.

**Q: Apakah gratis?**
A: Addon sendiri gratis. Tetapi provider services (Tripo, Meshy, ModelsLab) mungkin berbayar - check pricing di website mereka.

**Q: Bisa offline?**
A: Tidak, addon memerlukan internet connection untuk API calls.

**Q: Bisa use tanpa Blender?**
A: Provider clients bisa di-import sebagai library Python, tapi addon memerlukan Blender.

**Q: Bagaimana kalau API key terekspos?**
A: Immediately revoke di provider dashboard, generate new key.

**Q: Compatible dengan versi Blender lebih lama?**
A: Addon requires Blender 3.0+ (uses features tidak available di 2.9x).

---

## 📞 Support

Jika encounter issues:

1. **Check Documentation**: Read README.md
2. **Check Troubleshooting**: See section di top
3. **Test Provider Connection**: Use "Test Provider" button
4. **Check Console**: View → Toggle System Console (see error details)
5. **Provider Support**: Contact provider directly jika API issue

---

**Installation Guide Version**: 1.0  
**Last Updated**: January 2026  
**Target Blender**: 3.0.0+
