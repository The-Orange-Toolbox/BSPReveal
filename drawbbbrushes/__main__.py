import argparse
import traceback
from datetime import datetime

from clipify import clipify
from dispify import dispify
from triggerify import triggerify
from _constants import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Enable the visualization of blockbullet textures through r_drawclipbrushes')

    parser.add_argument('input', metavar='path', type=ascii,
                        help='The path of the BSP to modify.')

    parser.add_argument('-o', '--output', metavar='path', type=ascii, default='',
                        help='Where to save the modified bsp (overwrites the original by default)')

    parser.add_argument('-v', '--version', action='version', version=VERSION)

    args = parser.parse_args()

    print('Community Tool - {name}.exe ({date})\n'.format(name=NAME,
                                                          date=BUILD_DATE))
    in_bsp = eval(args.input)
    out_bsp = eval(args.output) or in_bsp

    try:
        initial_time = datetime.now()
        clipify(in_bsp, out_bsp)
        dispify(in_bsp, out_bsp)
        triggerify(in_bsp, out_bsp)

        elapsed_time = datetime.now() - initial_time
        elapsed_secs = elapsed_time.total_seconds()
        print('{:.1f} seconds elapsed'.format(elapsed_secs))

    except Exception as e:
        print('something went wrong')
        traceback.print_exc()
        print(e)
