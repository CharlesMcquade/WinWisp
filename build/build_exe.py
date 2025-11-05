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
def remove_readonly(func, path, _):
    """Clear the readonly bit and retry"""
    os.chmod(path, 0o777)
    func(path)

try:
    if dist_dir.exists():
        shutil.rmtree(dist_dir, onerror=remove_readonly)
except Exception as e:
    print(f"Warning: Could not remove dist directory: {e}")
    print("Continuing anyway - PyInstaller will overwrite files...")

try:
    if build_dir.exists():
        shutil.rmtree(build_dir, onerror=remove_readonly)
except Exception as e:
    print(f"Warning: Could not remove build_temp directory: {e}")
    print("Continuing anyway...")

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
    "--exclude-module=IPython",
    "--exclude-module=jupyter",
    "--exclude-module=notebook",
    "--exclude-module=pytest",
    "--exclude-module=sphinx",
    "--exclude-module=PIL.ImageQt",  # Qt support in PIL
    "--exclude-module=PIL.ImageTk",  # Tk is included separately
    
    # Exclude unused torch modules (big savings)
    "--exclude-module=torchvision",
    "--exclude-module=torchaudio.datasets",
    "--exclude-module=torchaudio.models",
    "--exclude-module=torch.distributions",
    "--exclude-module=torch.autograd.profiler",
    "--exclude-module=torch.utils.tensorboard",
    
    # Exclude transformers extras we don't need
    "--exclude-module=transformers.modeling_tf_utils",
    "--exclude-module=transformers.modeling_flax_utils",
    
    # Exclude dev/test dependencies
    "--exclude-module=setuptools",
    "--exclude-module=wheel",
    "--exclude-module=pip",
    
    # Exclude data science stack
    "--exclude-module=scipy.spatial.distance",
    "--exclude-module=scipy.stats",
    "--exclude-module=scipy.optimize",
    "--exclude-module=scipy.integrate",
    
    # Exclude image processing we don't use
    "--exclude-module=cv2.dnn",
    "--exclude-module=cv2.face",
    "--exclude-module=skimage",
    
    # Exclude audio processing we don't use
    "--exclude-module=librosa",
    "--exclude-module=pydub.effects",
    
    # Exclude NLP libraries we don't need
    "--exclude-module=nltk",
    "--exclude-module=spacy",
    
    # Compression settings for better size
    "--strip",  # Strip debug symbols (Windows)
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
