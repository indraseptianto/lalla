# AI 3D Generator - Configuration Reference

## Provider API Endpoints & Configuration

### 1. Tripo 3D

**Official Website**: https://www.tripo3d.ai/

#### API Configuration
| Parameter | Value |
|-----------|-------|
| Default Base URL | `https://platform.tripo3d.ai` |
| API Key Endpoint | Dashboard → API Keys |
| Documentation | https://www.tripo3d.ai/docs |

#### Supported Models
| Model | Type | Speed | Cost |
|-------|------|-------|------|
| Tripo Text-to-3D | Text prompt → 3D | Fast | Standard |
| Tripo Image-to-3D | Single image → 3D | Fast | Standard |

#### Style Options (Internal Mapping)
```python
{
    'CARTOON': 'cartoon',
    'REALISTIC': 'realistic',
    'CLAY': 'clay',
    'SCIFI': 'sci-fi'
}
```

#### Quality Mapping
```python
Quality Slider (1-10) → Mapped to provider parameters
1-3: Low quality (faster, lower cost)
4-6: Medium quality
7-9: High quality
10: Ultra quality (slower, higher cost)
```

#### Output Formats Supported
- ✅ GLB (GLTF Binary)
- ✅ OBJ
- ✅ FBX
- ✅ STL

#### Typical Response Time
- Text-to-3D: 2-5 minutes
- Image-to-3D: 2-5 minutes
- Peak hours: Can be 10-20 minutes

#### API Key Format
- Length: 32+ characters
- Type: Alphanumeric
- Example: `trp_...` (check dashboard)

#### Common Errors & Solutions
| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid API key | Re-check key in dashboard |
| 429 Too Many Requests | Rate limited | Wait, then retry |
| 500 Server Error | Provider issue | Wait 5-10 min, try again |

---

### 2. Meshy

**Official Website**: https://www.meshy.ai/

#### API Configuration
| Parameter | Value |
|-----------|-------|
| Default Base URL | `https://api.meshy.ai` |
| API Key Endpoint | Dashboard → API Keys |
| Documentation | https://www.meshy.ai/docs |

#### Supported Models
| Model | Type | Speed | Cost |
|-------|------|-------|------|
| Text-to-3D | Text prompt → 3D | Medium | Standard |
| Image-to-3D | Single image → 3D | Fast | Standard |
| Multi-image-to-3D | Multiple images → 3D | Medium | Standard |

#### Style Options (Internal Mapping)
```python
{
    'CARTOON': 'cartoon',
    'REALISTIC': 'realistic',
    'CLAY': 'clay',
    'SCIFI': 'sci-fi'
}
```

#### Quality Mapping
```python
1-3: 'low'      → art_style parameter
4-6: 'medium'
7-9: 'high'
10: 'ultra'

Alternative via texture_richness: 'high' for GLB
```

#### Output Formats Supported
- ✅ GLB
- ✅ GLTF
- ✅ OBJ
- ✅ FBX (in some models)

#### API Parameters
- `ai_model`: Default "meshy-4" or "meshy-4-turbo"
- `model_type`: "gaussian_splatting" recommended
- `art_style`: Maps to quality
- `texture_richness`: "high" untuk better materials

#### Typical Response Time
- Text-to-3D: 3-7 minutes
- Image-to-3D: 2-5 minutes
- Multi-image: 5-10 minutes

#### API Key Format
- Length: 32+ characters
- Type: Alphanumeric
- Example: `msy_...` (check dashboard)

#### Common Errors & Solutions
| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid API key | Verify key in dashboard |
| 422 Unprocessable | Bad image format | Use PNG/JPG, min 256x256 |
| 503 Service Unavailable | Overloaded | Wait & retry later |

---

### 3. ModelsLab (3D Verse)

**Official Website**: https://www.modelslab.com/  
**3D Verse Docs**: https://docs.3dverse.io/

#### API Configuration
| Parameter | Value |
|-----------|-------|
| Default Base URL | `https://api.modelslab.com` |
| API Key Endpoint | Dashboard → API Keys |
| Documentation | https://www.modelslab.com/docs |

#### Supported Models
| Model | Type | Speed | Cost |
|-------|------|-------|------|
| Text-to-3D | Text prompt → 3D | Slow | Higher |
| Image-to-3D | Single image → 3D | Medium | Higher |

#### Style Options (Internal Mapping)
```python
{
    'CARTOON': 'cartoon',
    'REALISTIC': 'realistic',
    'CLAY': 'clay',
    'SCIFI': 'sci-fi'
}
```

#### Quality Mapping
```python
1-3: 'low'
4-6: 'medium'
7-9: 'high'
10: 'ultra'
```

#### Output Formats Supported
- ✅ GLB
- ✅ OBJ
- ✅ FBX
- ✅ STL

#### API Endpoints
```
POST /api/v1/3dverse/text-to-3d    → Text generation
POST /api/v1/3dverse/image-to-3d   → Image generation
GET  /api/v1/3dverse/status/{id}   → Check status
```

#### Typical Response Time
- Text-to-3D: 5-10 minutes
- Image-to-3D: 3-8 minutes
- Processing slower than competitors

#### API Key Format
- Length: 32+ characters
- Type: Alphanumeric
- Example: `ml_...` (check dashboard)

#### Common Errors & Solutions
| Error | Cause | Solution |
|-------|-------|----------|
| 401 Forbidden | Invalid API key | Check key validity |
| 400 Bad Request | Wrong parameter format | Verify style/quality values |
| 502 Bad Gateway | Temporary outage | Wait & retry |

---

## Provider Comparison Matrix

| Feature | Tripo | Meshy | ModelsLab |
|---------|-------|-------|-----------|
| **Text-to-3D** | ✅ | ✅ | ✅ |
| **Image-to-3D** | ✅ | ✅ | ✅ |
| **Multi-image** | ❌ | ✅ | ❌ |
| **GLB Support** | ✅ | ✅ | ✅ |
| **OBJ Support** | ✅ | ✅ | ✅ |
| **FBX Support** | ✅ | ⚠️ | ✅ |
| **STL Support** | ✅ | ❌ | ✅ |
| **Speed** | Fast | Fast-Med | Slow |
| **Quality** | Good | Very Good | Good |
| **Cost** | Standard | Standard | Higher |
| **Free Tier** | ✅ | ✅ | Limited |
| **API Docs** | Good | Good | Good |

---

## Network Configuration

### Firewall Settings

Jika addon blocked oleh firewall, ensure:

```
OUTBOUND ALLOWED TO:
- https://platform.tripo3d.ai:443
- https://api.meshy.ai:443
- https://api.modelslab.com:443

PROTOCOL: HTTPS (443)
```

### Proxy Configuration

Jika behind corporate proxy:

1. **Check Blender Proxy Settings**:
   - `Edit` → `Preferences` → `Network`
   - Configure proxy settings

2. **Test Connectivity**:
   - Open provider URL in browser through proxy
   - If works in browser, should work in addon

### SSL/TLS Certificate

- Addon uses `requests` library dengan proper SSL verification
- Jika certificate error: Check system date/time correct
- Or: Update CA certificates bundle

---

## Polling & Async Configuration

### Default Polling Strategy

```python
Polling Interval: 5-10 seconds
Max Retries: ~600 (50+ minutes)
Timeout per request: 30 seconds

Status Values:
- pending/processing → continue polling
- completed/succeeded → download & import
- failed/error → report error & stop
- unknown → retry
```

### Customization (Advanced Users)

Edit dalam `operators.py` untuk change polling:

```python
# Change interval (seconds)
POLL_INTERVAL = 5  # Default 5 seconds

# Change max polls
MAX_POLLS = 600    # Default 600 (50 minutes)
```

---

## Logging & Debugging

### Enable Console Output

**Windows**:
```
Menu: Window → Toggle System Console
```

**macOS/Linux**:
```
Run Blender from terminal:
/path/to/blender
```

### Log Locations

**Windows**:
```
%APPDATA%\Blender Foundation\Blender\[Version]\cache\
```

**macOS**:
```
~/Library/Application Support/Blender/[Version]/cache/
```

**Linux**:
```
~/.config/blender/[Version]/cache/
```

### Debug Messages

Addon logs:
- API requests (masked API key)
- Response status codes
- Download progress
- Import operations
- Error details

Check console untuk troubleshooting.

---

## Performance Optimization

### Memory Usage

| Operation | Estimated RAM |
|-----------|---------------|
| Idle addon | ~5 MB |
| Polling active | ~10 MB |
| Model download | +5-50 MB (file size) |
| Model import | +20-100 MB (rendering data) |

### Network Bandwidth

| Operation | Estimated Data |
|-----------|----------------|
| API call (text) | ~1 KB |
| API call (image) | 100 KB - 2 MB |
| Model download | 5 MB - 50 MB |
| Status polling | ~100 bytes |

### Optimization Tips

1. **Close unused addons** → saves RAM
2. **Lower quality setting** → faster processing
3. **Compress images** → faster upload
4. **Use GLB format** → optimized file size
5. **Don't run multiple** generations → conserve resources

---

## Troubleshooting Guide

### API Connection Issues

```
Problem: "Cannot connect to API"

Diagnosis:
□ Test internet: ping google.com
□ Test URL in browser
□ Check firewall rules
□ Verify proxy settings
□ Check API status page

Solutions:
1. Restart Blender
2. Restart networking
3. Try different provider
4. Wait 5-10 minutes
5. Contact provider support
```

### API Authentication Issues

```
Problem: "Invalid API key"

Diagnosis:
□ Copy key again from dashboard
□ Check no extra spaces
□ Verify key not revoked
□ Check key valid date
□ Test with curl/Postman

Solutions:
1. Generate new API key
2. Clear cached preferences
3. Restart Blender
4. Check provider status
```

### Import Issues

```
Problem: "Model failed to import"

Diagnosis:
□ Check output format correct
□ Verify file size (>1 MB)
□ Check Blender version
□ Try different format

Solutions:
1. Try GLB format (most compatible)
2. Check Blender console for errors
3. Manually import file (test)
4. Update Blender
```

---

## API Rate Limits

### Tripo
- **Limit**: Check dashboard
- **Window**: Per minute/hour
- **Action**: Queue jobs, retry with backoff

### Meshy
- **Limit**: Check dashboard
- **Window**: Per minute/hour
- **Action**: Queue jobs, retry later

### ModelsLab
- **Limit**: Check dashboard
- **Window**: Per minute/hour
- **Action**: Queue jobs, retry later

**Best Practice**: Don't spam requests, space out submissions.

---

## Pricing Reference (As of Jan 2026)

Check official pricing pages:
- **Tripo**: https://www.tripo3d.ai/pricing
- **Meshy**: https://www.meshy.ai/pricing
- **ModelsLab**: https://www.modelslab.com/pricing

⚠️ **Disclaimer**: Pricing subject to change. Verify before using.

---

## Security Best Practices

### API Key Management
- ✅ Store in Blender preferences (encrypted)
- ✅ Never hardcode in scripts
- ✅ Never commit to git/GitHub
- ❌ Don't share .blend files with keys
- ❌ Don't use same key across multiple tools

### File Security
- ✅ Download to temp folder (auto-cleaned)
- ✅ Verify file integrity after download
- ❌ Don't save model URLs permanently
- ❌ Don't pass URLs to untrusted sources

### Network Security
- ✅ All connections use HTTPS
- ✅ SSL verification enabled
- ✅ Proper error handling
- ❌ Never disable SSL verification

---

## Version Compatibility

### Blender Versions
- ✅ 3.0.0 - 3.6.x: Fully compatible
- ⚠️ 4.0.0+: Test before use (might need updates)
- ❌ 2.93.x and below: Not supported

### Python Versions
- ✅ 3.10+: Fully compatible
- ✅ 3.11+: Fully compatible

### Dependencies
- `requests`: Built-in with Blender (verified)
- `abc`: Standard library
- `tempfile`: Standard library
- `os`: Standard library

No external pip packages required!

---

**Configuration Reference Version**: 1.0  
**Last Updated**: January 2026  
**Providers Configured**: Tripo, Meshy, ModelsLab
