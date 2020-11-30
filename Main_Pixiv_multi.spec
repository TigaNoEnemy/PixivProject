# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['./Main_Pixiv.py'],
             pathex=['.'],
             binaries=[],
             datas=[('./browsers.json', './cloudscraper/user_agent'), ('./RES/关于.png', './Pixiv_Widget/RES'), ('./RES/timeout_pic', './Pixiv_Widget/RES'), ('./RES/注销-p.png', './Pixiv_Widget/RES'), ('./RES/no_h', './Pixiv_Widget/RES'), ('./RES/男女-p.png', './Pixiv_Widget/RES'), ('./RES/正常-p.png', './Pixiv_Widget/RES'), ('./RES/下载-p.png', './Pixiv_Widget/RES'), ('./RES/搜索-p.png', './Pixiv_Widget/RES'), ('./RES/pixiv.ico', './Pixiv_Widget/RES'), ('./RES/login_gif', './Pixiv_Widget/RES'), ('./RES/DOWNLOAD_TIPS.png', './Pixiv_Widget/RES'), ('./RES/exit.png', './Pixiv_Widget/RES'), ('./RES/设置-p.png', './Pixiv_Widget/RES')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['pytz', 'psutil', 'PIL','PyQt5.QtWebChannel','PyQt5.QtMultimedia','PyQt5.QtQuick','PyQt5.QtLocation','PyQt5.QtWebSockets','PyQt5.QtSvg','PyQt5.QtNetwork','PyQt5.QtNfc','PyQt5.QtNetworkAuth','PyQt5.QtSerialPort','PyQt5.QtBluetooth','PyQt5.QtQuickWidgets','PyQt5.QtPositioning','PyQt5.QtQuick3D','PyQt5.QtSql','PyQt5.QtTextToSpeech','PyQt5.QtOpenGL','PyQt5.QtX11Extras','PyQt5.QtXml','PyQt5.QtXmlPatterns','PyQt5.QtDBus','PyQt5.QtHelp','PyQt5.QtMultimediaWidgets','PyQt5.QtPrintSupport','PyQt5.QtTest','PyQt5.QtDesigner','PyQt5.QtRemoteObjects','PyQt5.QtQml','PyQt5.QtSensors'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Main_Pixiv',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          icon='pixiv.ico' )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Main_Pixiv')
