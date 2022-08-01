import PyInstaller.__main__
import datetime
import glob
import os
import re
from sys import platform
from shutil import copy, make_archive

orgName = 'The Orange Toolbox'
url = 'https://github.com/The-Orange-Toolbox/BSPReveal'
exeName = 'BSPReveal'
builddate = datetime.datetime.now().strftime('%b %d %Y')
version = "1.3.1"
distDir = './dist/' + exeName + '-v' + str(version)
exeDir = distDir + '/' + exeName
iconPath = './icon/icon.ico'

# Write version info into _constants.py resource file
with open('src/_constants.py', 'w') as f:
    f.write("ORGNAME = \"{}\"\n".format(orgName))
    f.write("NAME = \"{}\"\n".format(exeName))
    f.write("VERSION = \"{}\"\n".format(version))
    f.write("BUILD_DATE = \"{}\"\n".format(builddate))
    f.write("URL = \"{}\"\n".format(url))

args = ['src/__main__.py',
        '-p', 'src',
        '-n', exeName,
        '-F',
        '--distpath', exeDir,
        '--icon', iconPath]

# Adding assets
assets = []
delimiter = ';' if platform == "win32" else ':'

for asset_path in glob.glob('src/assets/*'):
    assets.append('--add-data')
    assets.append(asset_path + delimiter + 'assets')

# Build!
PyInstaller.__main__.run(args + assets)

# Copy other bundle files
copy('./plugins/compilepal/meta.json', exeDir)
copy('./plugins/compilepal/parameters.json', exeDir)

# Edit README.md to produce a readme.txt
f = open('./README.md')
re_omit = r'<!--- start txt omit -->.*<!--- end txt omit -->'
readmetxt = re.sub(re_omit, '', f.read(), flags=re.S)
f.close()

f = open(distDir + '/readme.txt', "w+")
f.seek(0)
f.write(readmetxt)
f.truncate()
f.close()

# Zip the package
try:
    os.remove(distDir + '.zip')
except OSError:
    pass
make_archive(distDir, 'zip', distDir)
