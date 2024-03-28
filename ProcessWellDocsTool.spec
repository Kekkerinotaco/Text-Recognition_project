# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['ProcessWellDocsTool.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\python\\Lib\\site-packages\\customtkinter', 'customtkinter/')],
    hiddenimports=['tkinter', 'tkinter.filedialog', 'tkinter.font', 'darkdetect'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ProcessWellDocsTool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='C:\\MorozGY\\!_Code\\13. WellDocsParsingTool\\00.Icon\\WellIcon.ico',
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ProcessWellDocsTool',
)
