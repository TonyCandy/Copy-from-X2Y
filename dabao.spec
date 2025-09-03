# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['从X复制到Y.py'],
             pathex=['e:\\AI\\AI编程-从X复制到Y'],
             binaries=[],
             datas=[('icon_rc.py', '.')],
             hiddenimports=['PIL', 'PIL.Image', 'PIL.ImageTk'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='文件复制移动工具',
          debug=False,
          bootloader_ignore_signals=False,
          strip=True,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          optimize=2,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )

a = Analysis(['从X复制到Y.py'],
             pathex=['e:\\AI\\AI编程-从X复制到Y'],
             binaries=[],
             datas=[('app.ico', '.')],  # 将app.ico复制到输出目录
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='文件复制移动工具',
          debug=False,
          bootloader_ignore_signals=False,
          strip=True,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          windowed=True,
          icon='app.ico',
          optimize=2)