# -*- mode: python -*-

block_cipher = None


a = Analysis(['E:\\WorkShop\\Python\\updata.py'],
             pathex=['C:\\Users\\xiaoniu29\\pipenv1'],
             binaries=[('scoreRecord.xlsm','.'),('xlwings.xlam','.'),],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='upScore',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          runtime_tmpdir=None,
          console=False )
