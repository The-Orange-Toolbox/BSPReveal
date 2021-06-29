from valvebsp import *
from valvebsp.lumps import *


def clipify(in_bsp, out_bsp):
    bsp = Bsp(in_bsp)

    for brush in bsp[LUMP_BRUSHES]:
        brush_side = bsp[LUMP_BRUSHSIDES][brush.firstSide]
        texinfo = bsp[LUMP_TEXINFO][brush_side.texInfo]
        texdata = bsp[LUMP_TEXDATA][texinfo.texData]
        texname = bsp[LUMP_TEXDATA_STRING_DATA][texdata.nameStringTableID]

        if texname.startswith('TOOLS/TOOLSBLOCKBULLETS'):
            brush.contents.CONTENTS_MONSTERCLIP = True

    bsp.save(out_bsp)
