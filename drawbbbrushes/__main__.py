import argparse
import traceback

from clipify import clipify

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Enable the visualization of blockbullet textures through r_drawclipbrushes')

    parser.add_argument('input', metavar='path', type=ascii,
                        help='The path of the BSP to modify.')

    parser.add_argument('-o', '--output', metavar='path', type=ascii, default='',
                        help='Where to save the modified bsp (overwrites the original by default)')

    args = parser.parse_args()
    in_bsp = eval(args.input)
    out_bsp = eval(args.output) or in_bsp

    try:
        clipify(in_bsp, out_bsp)
        print('completed')

    except Exception as e:
        print('something went wrong')
        traceback.print_exc()
        print(e)
