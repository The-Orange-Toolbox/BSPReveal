import PyInstaller.__main__
import datetime

exename = 'drawbbbrushes'
builddate = datetime.datetime.now().strftime('%b %d %Y')
version = "1.0"

# Write version info into _constants.py resource file
with open('drawbbbrushes/_constants.py', 'w') as f:
    f.write("NAME = \"{}\"\n".format(exename))
    f.write("VERSION = \"{}\"\n".format(version))
    f.write("BUILD_DATE = \"{}\"\n".format(builddate))

PyInstaller.__main__.run([
    'drawbbbrushes\__main__.py',
    '-F',
    '-p', 'drawbbbrushes',
    '-n', exename,
    '--add-data',
    'drawbbbrushes//assets//toolstrigger.vmt;assets',
    '--add-data',
    'drawbbbrushes//assets//toolstrigger.vtf;assets'
])
