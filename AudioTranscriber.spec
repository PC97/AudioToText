# -*- mode: python ; coding: utf-8 -*-

import vosk

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
    (vosk.__path__[0], 'vosk'),
    ('models/vosk-model-small-en-us-0.15', 'models/vosk-model-small-en-us-0.15'),
    ('ffmpeg.exe', '.'),
    ('ffplay.exe', '.'),
    ('ffprobe.exe', '.')
    ],
    hiddenimports=['pydub.utils'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AudioTranscriber',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
