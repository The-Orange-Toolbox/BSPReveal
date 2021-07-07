import os

from valvebsp import *
from valvebsp.lumps import *


def clipify(in_bsp, out_bsp):

    print('Loading {}'.format(os.path.abspath(in_bsp)))
    bsp = Bsp(in_bsp)
    brush_count = 0

    for brush in bsp[LUMP_BRUSHES]:
        brush_side = bsp[LUMP_BRUSHSIDES][brush.firstSide]
        texinfo = bsp[LUMP_TEXINFO][brush_side.texInfo]
        texdata = bsp[LUMP_TEXDATA][texinfo.texData]
        texname = bsp[LUMP_TEXDATA_STRING_DATA][texdata.nameStringTableID]

        if brush.contents.CONTENTS_GRATE:
            brush.contents.CONTENTS_MONSTERCLIP = True
            brush.contents.CONTENTS_PLAYERCLIP = True
            brush_count += 1

        elif texname.startswith('TOOLS/TOOLSBLOCKBULLETS'):
            brush.contents.CONTENTS_MONSTERCLIP = True
            brush_count += 1

    print('{} blockbullet brushes modified'.format(brush_count))

    # cleanup
    del bsp[LUMP_BRUSHSIDES]
    del bsp[LUMP_TEXINFO]
    del bsp[LUMP_TEXDATA]
    del bsp[LUMP_TEXDATA_STRING_DATA]

    print('Writing {}'.format(os.path.abspath(out_bsp)))
    bsp.save(out_bsp)
