# CHANGELOG - AI 3D Generator

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.1] - 2026-01-20

### Blender 5.0 Compatibility Update ✨

**Fixes**:
- 🔧 Fixed `AttributeError: context.preferences read-only` error in Blender 5.0+
- 🔧 Added fallback mechanism for preferences access in modal operator contexts
- 🔧 Enhanced error handling for Blender 5.0's stricter context requirements

**Improvements**:
- 📚 Added comprehensive Blender 5.0 Compatibility Guide
- ✅ Verified compatibility with Blender 5.0+ while maintaining backward compatibility
- 🛡️ Improved exception handling in provider client initialization

**Documentation**:
- 📖 New: `BLENDER_5_COMPATIBILITY.md` - Complete guide for Blender 5.0 users
- 📝 Updated: Preferences access with error handling and fallback strategies
- 🔍 Added: Troubleshooting section for common Blender 5.0 issues

**Blender Version Support**:
- ✅ Blender 3.0 - 4.x (Original)
- ✅ Blender 5.0+ (New - with enhanced compatibility layer)

---

## [1.0.0] - 2026-01-20

### Initial Release ✨

**Major Features**:
- ✅ Unified client untuk 3 providers: Tripo, Meshy, ModelsLab
- ✅ Text-to-3D generation dengan consistent UI
- ✅ Image-to-3D generation dengan background removal option
- ✅ Async job polling dengan non-blocking modal
- ✅ Automatic model download & import ke Blender scene
- ✅ Multi-format support: GLB, OBJ, FBX, STL

**UI Features**:
- ✅ 3D View sidebar panel dengan tabbed interface
- ✅ Provider selection dropdown
- ✅ Style customization (Cartoon, Realistic, Clay, Sci-Fi)
- ✅ Quality/Detail slider (1-10)
- ✅ Output format selection
- ✅ Job status tracking dengan Check Status button
- ✅ Real-time generation status feedback

**Provider Support**:
- ✅ **Tripo 3D**
  - Text-to-3D via API v1
  - Image-to-3D support
  - Style mapping (cartoon, realistic, clay, sci-fi)
  - Quality mapping (low, medium, high, ultra)
  - Test connection endpoint
  
- ✅ **Meshy**
  - Text-to-3D via openapi/v1/text-to-3d
  - Image-to-3D via openapi/v1/image-to-3d
  - AI model selection (meshy-4, meshy-4-turbo)
  - Gaussian splatting model type
  - Background removal support
  - Profile info endpoint for testing
  
- ✅ **ModelsLab (3D Verse)**
  - Text-to-3D via 3dverse endpoint
  - Image-to-3D via 3dverse endpoint
  - Quality-based art style mapping
  - Format conversion support

**Preferences**:
- ✅ API key configuration per provider
- ✅ Custom base URL support
- ✅ Quick links ke documentation
- ✅ Password field untuk API key security
- ✅ Auto-save preferences

**Architecture**:
- ✅ Abstract base class design (BaseProviderClient)
- ✅ Provider-agnostic operators & UI
- ✅ Modular download & import system
- ✅ Proper error handling & user feedback
- ✅ Async/await pattern dengan Blender timers

**Download & Import**:
- ✅ Auto model download ke temp folder
- ✅ Format-specific import operators
  - GLTF/GLB: `bpy.ops.import_scene.gltf`
  - OBJ: `bpy.ops.import_scene.obj`
  - FBX: `bpy.ops.import_scene.fbx`
  - STL: `bpy.ops.import_mesh.stl`
- ✅ Auto-cleanup temp files
- ✅ Object naming convention: `{provider}_{name}`
- ✅ Auto center view pada imported model

**Documentation**:
- ✅ Comprehensive README.md (user guide)
- ✅ INSTALL.md (installation & setup)
- ✅ QUICKSTART.md (5-minute quick start)
- ✅ CONFIG_REFERENCE.md (API & configuration details)
- ✅ DEVELOPER_GUIDE.md (extending & contributing)
- ✅ Inline code documentation & docstrings

**Testing & Quality**:
- ✅ Type hints throughout codebase
- ✅ Error handling untuk network issues
- ✅ Graceful degradation
- ✅ User-friendly error messages
- ✅ Security: Masked API keys, HTTPS only

**Compatibility**:
- ✅ Blender 3.0.0 - 3.6.x (tested)
- ✅ Python 3.10+
- ✅ Windows, macOS, Linux
- ✅ No external pip dependencies

### Known Limitations

- Async polling happens via Blender timer (not true async)
- No real-time progress updates during provider processing
- Single image only (no multi-view for Meshy yet)
- No built-in prompt optimization/suggestions
- No job history/tracking across sessions
- Temp files deleted even if import fails

### Future Roadmap

**Planned for 1.1.0**:
- [ ] Add more providers (Blockade, DreamFusion, etc.)
- [ ] Multi-image support (Meshy multi-view)
- [ ] Job history panel
- [ ] Prompt templates & suggestions
- [ ] Material assignment from metadata
- [ ] Batch generation queue
- [ ] Generation settings presets
- [ ] Webhook-based completion (real async)

**Planned for 1.2.0**:
- [ ] Web UI dashboard
- [ ] API rate limit tracking
- [ ] Advanced settings per provider
- [ ] Custom style/quality profiles
- [ ] Model preview before import
- [ ] Post-processing tools (cleanup, retopo)
- [ ] Texture baking
- [ ] Export presets (game engine, 3D print)

**Planned for 2.0.0**:
- [ ] Blender 4.0+ native async
- [ ] Cloud storage integration
- [ ] Collaborative features
- [ ] Advanced AI parameter tuning
- [ ] Model variations & iterations

---

## [Unreleased]

### Added
- (None yet)

### Changed
- (None yet)

### Deprecated
- (None yet)

### Removed
- (None yet)

### Fixed
- (None yet)

### Security
- (None yet)

---

## How to Release

1. Update version in `__init__.py` (bl_info['version'])
2. Update this CHANGELOG.md
3. Create git tag: `git tag v1.0.0`
4. Push tag: `git push origin v1.0.0`
5. Create GitHub release with changelog
6. Package as ZIP: `zip -r ai_3d_generator-1.0.0.zip ai_3d_generator/`

---

## Version History Summary

| Version | Release Date | Status | Notes |
|---------|------------|--------|-------|
| 1.0.0 | 2026-01-20 | ✅ Released | Initial stable release |

---

## Contributing

### To Report Issues
1. Check existing issues first
2. Provide detailed reproduction steps
3. Include Blender version & OS
4. Include error messages/logs

### To Contribute Code
1. Fork repository
2. Create feature branch
3. Follow code style guide (PEP 8)
4. Test thoroughly
5. Submit pull request with description

---

**CHANGELOG Version**: 1.0  
**Last Updated**: January 2026  
**Maintainer**: AI 3D Generator Team
