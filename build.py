from sys import platform
import glob

from totcommon.builder import builder
from src._constants import VERSION, NAME, ORGNAME, URL

assets = []
delimiter = ';' if platform == "win32" else ':'

for asset_path in glob.glob('src/assets/*'):
    assets.append('--add-data')
    assets.append(asset_path + delimiter + 'assets')

builder(NAME, ORGNAME, URL, VERSION, assets)
