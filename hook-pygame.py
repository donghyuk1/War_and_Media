from PyInstaller.utils.hooks import copy_metadata

# Copy pygame's pyd files and font data files
datas = copy_metadata('pygame')
