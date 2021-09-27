import os

from valvebsp.lumps import *
from totcommon.logger import stdout

def clipify(bsp):

    clip_brush_count = grate_brush_count = block_brush_count = 0

    for brush in bsp[LUMP_BRUSHES]:
        brush_side = bsp[LUMP_BRUSHSIDES][brush.firstSide]
        texinfo = bsp[LUMP_TEXINFO][brush_side.texInfo]
        texdata = bsp[LUMP_TEXDATA][texinfo.texData]
        texname = bsp[LUMP_TEXDATA_STRING_DATA][texdata.nameStringTableID]

        if brush.contents.CONTENTS_MONSTERCLIP and \
           brush.contents.CONTENTS_PLAYERCLIP:
            # Retag clip brushes as playerclip brushes
            brush.contents.CONTENTS_MONSTERCLIP = False
            clip_brush_count += 1
        elif brush.contents.CONTENTS_GRATE:
            # Retag grate solidity as clip brushes
            brush.contents.CONTENTS_MONSTERCLIP = True
            brush.contents.CONTENTS_PLAYERCLIP = True
            grate_brush_count += 1
        elif texname.startswith('TOOLS/TOOLSBLOCKBULLETS'):
            # Tag blobkbullet and npcclip brushes
            brush.contents.CONTENTS_MONSTERCLIP = True
            block_brush_count += 1

    if clip_brush_count:
        stdout('{} clip brushes modified.'.format(clip_brush_count))
    if block_brush_count:
        stdout('{} blockbullet brushes modified.'.format(block_brush_count))
    if grate_brush_count:
        stdout('{} grate brushes modified.'.format(grate_brush_count))
