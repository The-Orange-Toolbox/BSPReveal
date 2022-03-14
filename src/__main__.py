import os
import argparse
import traceback
from datetime import datetime

from valvebsp import Bsp

from totcommon.executable import TOTExecutable
from totcommon.logger import stdout

from clipify import clipify
from dispify import dispify
from spawnify import spawnify
from triggerify import triggerify

from _constants import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Reveal various BSP elements previously unable to be visualised.')

    parser.add_argument('input', metavar='path', type=ascii,
                        help='The path of the BSP to modify.')

    parser.add_argument('-o', '--output', metavar='path', type=ascii, default='',
                        help='Where to save the modified bsp (overwrites the original if not specified)')

    parser.add_argument('-v', '--version', action='version', version=VERSION)

    parser.add_argument('-a', '--all', action='store_true',
                        help='Runs all operations (clip, disp, spawn, trigger)')

    parser.add_argument('-c', '--clip', action='store_true',
                        help='Runs clip operations for "r_drawclipbrushes 2"')

    parser.add_argument('-d', '--disp', action='store_true',
                        help='Runs disp operations for "ent_fire vis_disp toggle"')

    parser.add_argument('-s', '--spawn', action='store_true',
                        help='Runs spawn operations for "map_showspawnpoints"')

    parser.add_argument('--spawn-delta', type=int, default=4,
                        help='The height delta to be added between spawns')

    parser.add_argument('-t', '--trigger', action='store_true',
                        help='Runs trigger operations for "showtriggers_toggle"')

    args = parser.parse_args()

    with TOTExecutable(NAME, ORGNAME, URL, VERSION, BUILD_DATE):

        in_bsp = eval(args.input)
        out_bsp = eval(args.output) or in_bsp

        stdout('Loading {}'.format(os.path.abspath(in_bsp)))
        bsp = Bsp(in_bsp)

        specified = args.all or args.clip or args.disp or args.spawn or args.trigger

        if not specified or args.all or args.clip:
            clipify(bsp)
        if not specified or args.all or args.disp:
            dispify(bsp)
        if not specified or args.all or args.spawn:
            spawnify(bsp, args.spawn_delta)
        if not specified or args.all or args.trigger:
            triggerify(bsp)

        stdout('Writing {}'.format(os.path.abspath(out_bsp)))
        bsp.save(out_bsp)
