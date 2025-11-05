"""
Build script for creating a standalone Windows executable
"""
import PyInstaller.__main__
import os
import shutil
from pathlib import Path

# Get the project root directory
project_root = Path(__file__).parent.parent
dist_dir = project_root / "dist"
build_dir = project_root / "build_temp"

# Clean previous builds
if dist_dir.exists():
    shutil.rmtree(dist_dir)
if build_dir.exists():
    shutil.rmtree(build_dir)

print("Building WinWisp executable...")

# PyInstaller arguments
pyinstaller_args = [
    str(project_root / "main.py"),  # Main script
    "--name=WinWisp",                # Name of the executable
    "--onefile",                      # Create a single executable file
    "--windowed",                     # No console window (GUI mode)
    "--clean",                        # Clean cache
    f"--distpath={dist_dir}",        # Output directory
    f"--workpath={build_dir}",       # Temporary build directory
    
    # Add all necessary modules
    "--hidden-import=whisper",
    "--hidden-import=torch",
    "--hidden-import=torchaudio",
    "--hidden-import=sounddevice",
    "--hidden-import=keyboard",
    "--hidden-import=pystray",
    "--hidden-import=pynput",
    "--hidden-import=tkinter",
    
    # Add icon if it exists
    # "--icon=build/app_icon.ico",
    
    # Don't include unnecessary files
    "--exclude-module=matplotlib",
    "--exclude-module=pandas",
]

# Run PyInstaller
PyInstaller.__main__.run(pyinstaller_args)

print("\n" + "="*60)
print("Build complete!")
print(f"Executable location: {dist_dir / 'WinWisp.exe'}")
print("="*60)

# Clean up build directory
if build_dir.exists():
    shutil.rmtree(build_dir)

print("\nNext steps:")
print("1. Test the executable: dist/WinWisp.exe")
print("2. Build installer: Open build/installer.iss in Inno Setup and compile")
