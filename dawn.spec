from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT

# Collect JSON presets from dawn.presets
datas = collect_data_files('dawn', include_py_files=False) + [('dawn/presets', 'dawn/presets')]

a = Analysis(
    ['dawn/cli.py'],
    pathex=['.'],
    binaries=[],
    datas=datas,
    hiddenimports=['dawn.presets'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[]
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='dawn',
    debug=False,
    console=True,
    icon=None,
    onefile=True
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='dawn'
)