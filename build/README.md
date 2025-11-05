# Build Configuration for Windows Installer

This directory contains the configuration and scripts needed to build a standalone Windows installer for WinWisp.

## Build Tools Required

1. **PyInstaller** - Creates standalone executable
2. **Inno Setup** - Creates Windows installer (.exe)

## Building the Application

### Step 1: Install Build Dependencies

```bash
pip install pyinstaller
```

### Step 2: Build the Executable

```bash
python build_exe.py
```

This will create a standalone executable in the `dist` folder.

### Step 3: Create the Installer

1. Install Inno Setup from: https://jrsoftware.org/isdl.php
2. Open `installer.iss` in Inno Setup
3. Click "Compile" to create the installer

The installer will be created in the `Output` folder.

## What Gets Built

- **Standalone Executable**: `WinWisp.exe` - No Python installation required
- **Windows Installer**: `WinWisp-Setup.exe` - Full installer with Start Menu shortcuts
- **Auto-start Support**: Option to run on Windows startup
- **System Tray Integration**: Runs in background, accessible from tray icon

## Files

- `build_exe.py` - Script to build the executable with PyInstaller
- `installer.iss` - Inno Setup configuration for the installer
- `winwisp.spec` - PyInstaller specification file
- `app_icon.ico` - Application icon (if available)
