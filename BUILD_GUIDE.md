# Build and Distribution Guide for WinWisp

This guide explains how to build WinWisp as a standalone Windows executable and create an installer.

## Prerequisites

### 1. Python Environment
Ensure you have Python 3.8+ installed with all runtime dependencies:
```bash
pip install -r requirements.txt
```

### 2. Build Tools
Install PyInstaller for creating the executable:
```bash
pip install -r requirements-build.txt
```

### 3. Inno Setup (for installer)
Download and install Inno Setup from: https://jrsoftware.org/isdl.php

### 4. FFmpeg
WinWisp requires FFmpeg. Users will need to install it separately.
- Download from: https://ffmpeg.org/download.html
- The installer will check for FFmpeg and warn if not found

## Building the Executable

### Option 1: Using the Build Script (Recommended)

```bash
cd build
python build_exe.py
```

This will:
1. Clean previous builds
2. Run PyInstaller with optimized settings
3. Create `WinWisp.exe` in the `dist` folder
4. Include all necessary dependencies

### Option 2: Using PyInstaller Directly

```bash
pyinstaller build/winwisp.spec
```

### Option 3: Manual PyInstaller Command

```bash
pyinstaller main.py --name=WinWisp --onefile --windowed ^
    --hidden-import=whisper ^
    --hidden-import=torch ^
    --hidden-import=sounddevice ^
    --hidden-import=keyboard ^
    --hidden-import=pystray
```

## Testing the Executable

Before creating the installer, test the executable:

```bash
cd dist
WinWisp.exe
```

Check that:
- ✅ Application starts without console window
- ✅ System tray icon appears
- ✅ Hotkey works (Ctrl+Shift+Space by default)
- ✅ Recording and transcription work correctly
- ✅ GUI opens from tray menu
- ✅ Settings can be saved

## Creating the Windows Installer

### 1. Open Inno Setup
Launch Inno Setup Compiler

### 2. Open the Script
File → Open → `build/installer.iss`

### 3. Compile
Build → Compile (or press Ctrl+F9)

### 4. Output
The installer will be created in: `installer_output/WinWisp-Setup-1.0.0.exe`

## Installer Features

The installer includes:
- ✅ Installation to Program Files
- ✅ Start Menu shortcuts
- ✅ Optional Desktop icon
- ✅ Optional Windows startup entry
- ✅ FFmpeg detection and warning
- ✅ Uninstaller with option to remove user data
- ✅ Config directory in AppData
- ✅ Admin privileges for proper installation

## File Structure After Build

```
WinWisp/
├── dist/
│   └── WinWisp.exe           # Standalone executable (~500MB with Whisper model)
├── installer_output/
│   └── WinWisp-Setup-1.0.0.exe  # Windows installer
└── build_temp/               # Temporary build files (auto-deleted)
```

## Distribution

### For End Users
Distribute `WinWisp-Setup-1.0.0.exe` - this includes:
- The application executable
- README and license files
- Automatic shortcuts creation
- Proper installation/uninstallation

### For Portable Use
Distribute `WinWisp.exe` alone - users can run it directly without installation.

## User Data Locations

After installation, user data is stored in:
- **Config**: `%LOCALAPPDATA%\WinWisp\config.json`
- **Logs**: `%LOCALAPPDATA%\WinWisp\logs\`
- **Recordings**: `%LOCALAPPDATA%\WinWisp\recordings\` (if enabled)
- **Whisper Models**: `%USERPROFILE%\.cache\whisper\`

## Troubleshooting Build Issues

### Issue: "Module not found" errors
**Solution**: Add missing modules to `hiddenimports` in `winwisp.spec`

### Issue: Executable is too large
**Solution**: This is normal. The Whisper model and PyTorch are large. Expected size: 500MB-1GB

### Issue: Executable takes long to start
**Solution**: First run loads the Whisper model. Subsequent runs are faster.

### Issue: Antivirus flags the executable
**Solution**: PyInstaller executables can trigger false positives. Consider code signing or adding to whitelist.

## Code Signing (Optional)

For production releases, consider signing the executable:

1. Obtain a code signing certificate
2. Use `signtool.exe` to sign the executable:
   ```bash
   signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com dist/WinWisp.exe
   ```

## Automated Builds (CI/CD)

See `.github/workflows/build.yml` for automated building with GitHub Actions.

## Version Updates

To release a new version:
1. Update version in `build/installer.iss` (`MyAppVersion`)
2. Update version in `main.py` if applicable
3. Rebuild executable and installer
4. Tag the release in git: `git tag v1.0.0`
5. Create GitHub release with installer attached
