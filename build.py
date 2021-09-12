import PyInstaller.__main__
import datetime
import glob
from sys import platform

orgname = 'The Orange Toolbox'
exename = 'BSPReveal'
builddate = datetime.datetime.now().strftime('%b %d %Y')
version = "1.0"

# Write version info into _constants.py resource file
with open('src/_constants.py', 'w') as f:
    f.write("ORGNAME = \"{}\"\n".format(orgname))
    f.write("NAME = \"{}\"\n".format(exename))
    f.write("VERSION = \"{}\"\n".format(version))
    f.write("BUILD_DATE = \"{}\"\n".format(builddate))

args = ['src/__main__.py',
        '-p', 'src',
        '-n', exename,
        '-F']

# Adding assets
assets = []
delimiter = ';' if platform == "win32" else ':'

for asset_path in glob.glob('src/assets/*'):
    assets.append('--add-data')
    assets.append(asset_path + delimiter + 'assets')

# Build!
PyInstaller.__main__.run(args + assets)
