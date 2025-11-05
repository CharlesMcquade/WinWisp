# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for WinWisp

block_cipher = None

a = Analysis(
    ['../main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('../README.md', '.'),
        ('../LICENSE', '.'),
        ('../ATTRIBUTION.md', '.'),
    ],
    hiddenimports=[
        'whisper',
        'torch',
        'torchaudio',
        'sounddevice',
        'scipy',
        'scipy.io.wavfile',
        'keyboard',
        'pystray',
        'pynput',
        'pynput.keyboard',
        'pyperclip',
        'tkinter',
        'PIL',
        'PIL.Image',
        'PIL.ImageDraw',
        'numpy',
        'tiktoken',
        'numba',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'pandas',
        'jupyter',
        'notebook',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='WinWisp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to False for windowed mode (no console)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='app_icon.ico' if os.path.exists('app_icon.ico') else None,
)
