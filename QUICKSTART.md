# AI 3D Generator - Quick Start Guide

Mulai generate 3D models dalam 5 menit! 🚀

---

## ⚡ Instalasi Cepat (2 menit)

### 1. Download Addon
```bash
# Clone dari GitHub atau download ZIP
git clone https://github.com/youruser/ai_3d_generator.git
```

### 2. Copy ke Blender

**Windows**:
```
Copy folder ke:
C:\Users\YourName\AppData\Roaming\Blender Foundation\Blender\3.x\scripts\addons\
```

**macOS**:
```
Copy folder ke:
~/Library/Application Support/Blender/3.x/scripts/addons/
```

**Linux**:
```
Copy folder ke:
~/.config/blender/3.x/scripts/addons/
```

### 3. Enable di Blender
1. Open Blender
2. `Edit` → `Preferences` → `Add-ons`
3. Search: "AI 3D Generator"
4. Click checkbox ☑️ to enable
5. Done!

---

## 🔑 Setup API Keys (2 menit)

### Quick Signup

Choose at least ONE provider:

| Provider | Signup | Free? |
|----------|--------|-------|
| [Tripo 3D](https://www.tripo3d.ai/) | 30 sec | ✅ Limited free |
| [Meshy](https://www.meshy.ai/) | 30 sec | ✅ Limited free |
| [ModelsLab](https://www.modelslab.com/) | 30 sec | ✅ Very limited |

### Add API Key to Blender

1. Open Blender Preferences
2. `Add-ons` → `AI 3D Generator` (expand)
3. Paste your API key:
   ```
   API Key: [paste_here]
   ```
4. Done! (Auto-saved)

### Test Connection

1. Open 3D View (press `N` for sidebar)
2. Find "AI 3D Generator" panel
3. Click "Test Provider" button
4. Should see ✅ "Connection successful!"

---

## 🎨 First Generation (1 minute)

### Text to 3D

1. **Open 3D View Sidebar** (press `N`)
2. **Find "AI 3D Generator"** panel (right side)
3. **Make sure "Text to 3D" tab selected**
4. **Type Prompt**:
   ```
   Example: "red ceramic vase with flower pattern"
   ```
5. **Set Quality**: Slide to 7 (good balance)
6. **Click "Generate from Text"**
7. **Wait 2-5 minutes**
8. ✅ **Model imports automatically!**

### Image to 3D

1. **Select "Image to 3D" tab**
2. **Click file picker** → select an image
3. **Set Quality**: 7
4. **Click "Generate from Image"**
5. **Wait 2-5 minutes**
6. ✅ **Model imports!**

---

## 💡 Pro Tips

### For Better Text Results
- ✅ Be specific: "blue ceramic vase" NOT "vase"
- ✅ Include materials: "ceramic", "metal", "plastic"
- ✅ Include style: "realistic", "cartoon", "clay"
- ✅ Add details: "with flower pattern", "glossy finish"

**Example Good Prompts**:
- "Red ceramic vase with glossy glaze"
- "Wooden chair in cartoon style"
- "Metal cube with sci-fi design"

### For Better Image Results
- ✅ Clear subject with good lighting
- ✅ Remove clutter/complex backgrounds
- ✅ Enable "Background Removal" if needed
- ✅ Size: 512x512 - 2048x2048 optimal

### Quality Settings
- **Quality 5**: Fast preview (1-2 min) ⚡
- **Quality 7**: Good balance (2-5 min) ⭐ Recommended
- **Quality 10**: Maximum detail (5-10 min) ⚙️

### Format Selection
- **GLB**: Best for Blender (preserves materials) ⭐ Recommended
- **OBJ**: Geometry only (no materials)
- **FBX**: Good for rigged/animated models
- **STL**: For 3D printing

---

## 🆘 Troubleshooting

### Problem: Connection error
```
Solution:
1. Check internet connection
2. Verify API key copied correctly
3. Try opening provider URL in browser
4. Restart Blender
```

### Problem: Generation timeout
```
Solution:
1. Wait longer (30+ minutes sometimes)
2. Lower quality setting
3. Simplify prompt
4. Try different provider
```

### Problem: Model fails to import
```
Solution:
1. Try GLB format
2. Check file size > 1 MB
3. Scale object (press S, type 2, Enter)
4. Manually import file to test
```

### Problem: API key rejected
```
Solution:
1. Recopy API key from dashboard
2. Check no extra spaces
3. Verify key not expired
4. Generate new key in provider dashboard
```

---

## 📖 Learn More

- **Full Docs**: [README.md](README.md)
- **Installation Guide**: [INSTALL.md](INSTALL.md)
- **Configuration**: [CONFIG_REFERENCE.md](CONFIG_REFERENCE.md)
- **For Developers**: [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)

---

## 🎯 Next Steps

1. ✅ Try text-to-3D generation
2. ✅ Try image-to-3D generation
3. ✅ Compare providers (which you prefer)
4. ✅ Optimize prompts for better results
5. ✅ Combine with Blender materials/rendering

---

## ⚠️ Important Notes

- **Cost**: First provider signup usually includes free credits
- **Processing Time**: Dependent on provider queue (peak hours slower)
- **File Size**: Downloaded models can be 5-50 MB
- **Storage**: Temporary files auto-deleted after import
- **No Local Processing**: All AI processing happens on provider servers

---

## 🚀 You're Ready!

```
1. ✅ Addon installed
2. ✅ API key configured
3. ✅ Connection tested
4. ✅ First generation done

Enjoy generating 3D models! 🎉
```

---

**Quick Start Version**: 1.0  
**Time to First Generation**: ~5 minutes  
**Blender Target**: 3.0.0+
