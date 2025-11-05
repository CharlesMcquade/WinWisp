# Changelog

All notable changes to WinWisp will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Windows installer (.exe) for easy installation
- Standalone executable distribution
- Auto-update functionality
- Additional language support configurations
- Custom themes for GUI

## [1.0.0] - 2025-11-04

### Added
- Initial release of WinWisp (rebranded from WindowsWhisper)
- Global hotkey support (Ctrl+Shift+Space by default)
- Automatic text pasting at cursor location
- System tray integration with menu
- Configurable Whisper model selection (tiny, base, small, medium, large)
- Settings GUI for customization
- Speech-to-text using OpenAI's Whisper model
- Support for multiple languages
- Clipboard copy functionality
- Recording status indicators
- Visual and audio feedback during recording
- Configuration persistence in %LOCALAPPDATA%\WinWisp
- Logging system for debugging
- PyInstaller build configuration for standalone executables
- Inno Setup installer script
- Comprehensive build documentation

### Technical
- Python 3.8+ compatibility
- Uses sounddevice for audio recording
- PyTorch and Whisper integration
- Cross-compatible with Windows 10/11
- AppData storage for user configuration
- Background model loading for faster startup

### Documentation
- Complete README with installation instructions
- BUILD_GUIDE.md for developers
- ATTRIBUTION.md for proper OpenAI Whisper credits
- MIT License

---

## Version History

- **1.0.0** (2025-11-04) - Initial public release
