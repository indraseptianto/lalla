# Blender 5.0 Compatibility Guide

## Overview

AI 3D Generator addon is now fully compatible with Blender 5.0 (and later versions). This document outlines the changes made and important information for users upgrading to Blender 5.0.

## What Changed in Blender 5.0

### Context.Preferences Read-Only Issue

**Problem**: In Blender 5.0+, accessing `context.preferences` in certain execution contexts (particularly during modal operator execution) may result in a read-only attribute error:
```
AttributeError: bpy_struct: attribute "preferences" from "Context" is read-only
```

**Solution**: The addon now implements a fallback mechanism that handles both standard contexts and Blender 5.0's modal contexts.

## Implementation Details

### 1. Enhanced Preferences Access

The `get_provider_client()` function now includes error handling:

```python
def get_provider_client(context):
    """Get current provider client instance.
    
    Compatible with Blender 5.0+ where preferences may be read-only in certain contexts.
    """
    try:
        # Try standard access first (works in most contexts)
        prefs = context.preferences.addons['ai_3d_generator'].preferences
    except (AttributeError, RuntimeError):
        # Fallback for Blender 5.0+ modal contexts
        import bpy
        try:
            addon_prefs = bpy.context.preferences.addons.get('ai_3d_generator')
            if addon_prefs:
                prefs = addon_prefs.preferences
            else:
                return None
        except Exception:
            return None
```

### 2. Modal Operator Context Handling

Operators that use modal handlers (like `AI3DGenerateText` and `AI3DGenerateImage`) now safely access preferences:

```python
try:
    prefs = context.preferences.addons['ai_3d_generator'].preferences
except (AttributeError, RuntimeError):
    # Fallback for Blender 5.0+ modal contexts
    import bpy
    addon_prefs = bpy.context.preferences.addons.get('ai_3d_generator')
    if addon_prefs:
        prefs = addon_prefs.preferences
```

## Tested Compatibility

- ✅ Blender 3.0 - 4.x (Original version)
- ✅ Blender 5.0+ (With compatibility enhancements)

## Known Issues & Workarounds

### Issue: "Cannot access addon preferences" error

**Cause**: In rare edge cases, preferences may not be fully initialized when addon starts.

**Workaround**: 
1. Restart Blender
2. Ensure addon is enabled in preferences
3. Configure API keys before generating models

### Issue: Job polling stops unexpectedly

**Cause**: Modal context changes in Blender 5.0 may affect timer events.

**Workaround**: 
1. Use "Check Status" button to manually poll job status
2. Job ID is preserved in scene properties, so you can check status even after restarting

## API Key Configuration in Blender 5.0

Configuration steps remain unchanged:

1. Open Blender Edit → Preferences
2. Go to Add-ons section
3. Search for "AI 3D Generator"
4. Expand the addon entry
5. Configure API keys for desired provider:
   - **Tripo 3D**: Get key from https://www.tripo3d.ai/
   - **Meshy**: Get key from https://www.meshy.ai/
   - **ModelsLab**: Get key from https://www.modelslab.com/

## Blender Version Information

### Version Detection

The addon dynamically handles API differences between Blender versions:

```
- Blender < 3.0: Not supported
- Blender 3.0 - 4.x: Full compatibility (no special handling needed)
- Blender 5.0+: Enhanced compatibility (automatic fallback mechanisms)
```

### Addon Info

Current addon metadata:
```python
bl_info = {
    "name": "AI 3D Generator",
    "author": "AI 3D Generator Team",
    "description": "Unified client untuk AI 3D generation (Tripo, Meshy, ModelsLab)",
    "blender": (3, 0, 0),  # Minimum version
    "version": (1, 0, 1),  # Version with B5.0 support
    "location": "View3D > Sidebar > AI 3D Generator",
    "category": "Import-Export"
}
```

## Troubleshooting

### Steps to diagnose compatibility issues:

1. **Check Blender Version**: Help → About Blender
2. **Verify Addon is Enabled**: Edit → Preferences → Add-ons (search for "AI 3D")
3. **Check Console for Errors**: Window → Toggle System Console (Windows) or check terminal output
4. **Test Provider**: Click "Test Provider" button in UI panel
5. **Review Error Reports**: Check Blender's Report Output for detailed error messages

### Debug Mode

To enable more verbose logging, add this to Blender's startup script:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Migration from Older Versions

If upgrading from an older addon version:

1. Uninstall old version
2. Install new version
3. Restart Blender
4. Re-configure API keys (preferences may be reset)
5. Test provider connection before generating models

## Performance Considerations

Blender 5.0 has improved performance, but model generation still depends on:
- Internet connection speed
- API provider response time
- Model complexity and output quality settings

## Future Compatibility

The addon's compatibility layer is designed to:
- Gracefully handle API changes in future Blender versions
- Maintain backward compatibility with Blender 3.0+
- Use non-deprecated APIs where possible

## Support & Bug Reports

For issues related to Blender 5.0 compatibility:

1. Include your Blender version (Help → About Blender)
2. Provide addon version from preferences
3. Share error messages from Report Output
4. Include reproduction steps

## Related Documentation

- [Blender 5.0 Release Notes](https://www.blender.org/download/releases/5-0/)
- [Blender Python API](https://docs.blender.org/api/current/)
- [AI 3D Generator Developer Guide](./DEVELOPER_GUIDE.md)
- [Installation Guide](./INSTALL.md)

---

**Last Updated**: 2026-01-20  
**Addon Version**: 1.0.1  
**Blender Support**: 3.0 - 5.0+
