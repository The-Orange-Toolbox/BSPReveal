import os
import argparse
import traceback
from datetime import datetime

from valvebsp import Bsp

from totcommon.logger import print_header, stdout
from totcommon.updater import check_updates
from totcommon.reporter import ErrorReporter
from totcommon.stopwatch import StopWatch

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

    args = parser.parse_args()

    print_header(ORGNAME, NAME, BUILD_DATE)
    check_updates(NAME, VERSION, URL)

    in_bsp = eval(args.input)
    out_bsp = eval(args.output) or in_bsp

    with ErrorReporter(NAME, URL), StopWatch():
        stdout('Loading {}'.format(os.path.abspath(in_bsp)))
        bsp = Bsp(in_bsp)

        clipify(bsp)
        dispify(bsp)
        spawnify(bsp)
        triggerify(bsp)

        stdout('Writing {}'.format(os.path.abspath(out_bsp)))
        bsp.save(out_bsp)

