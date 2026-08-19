# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src/pac-man.py'],
    pathex=[],
    binaries=[],
    datas=[('assets', 'assets')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

import os, arcade

# Affiche ce qui pose problème (à retirer une fois que ça marche)
print("=== datas liés à VERSION ===")
for d in a.datas:
    if 'VERSION' in d[0]:
        print(d)

# Retire TOUTES les entrées existantes touchant arcade/VERSION (bonnes ou mauvaises)
a.datas = [d for d in a.datas if 'arcade' + os.sep + 'VERSION' not in d[0] and 'arcade/VERSION' not in d[0]]

# Rajoute UNE seule entrée propre
arcade_version_file = os.path.join(os.path.dirname(arcade.__file__), 'VERSION')
a.datas += [('arcade/VERSION', arcade_version_file, 'DATA')]
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='pac_man',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
