import os
import random
from valvebsp import Bsp
from construct.core import Int8ul
from valvebsp.structs.common import ColorRGBExp32
from valvebsp.structs.flags import dispinfo_flags8


def dispify(in_bsp, out_bsp):

    print('Loading {}'.format(os.path.abspath(in_bsp)))
    bsp = Bsp(in_bsp)

    ENT_ORIGIN = [v for k, v in bsp[0][0] if k == 'world_mins'][0]

    COLORS = {2: {'r': 130, 'g': 20, 'b': 255, 'exponent': 2},  # purple
              4: {'r': 1, 'g': 255, 'b': 20, 'exponent': 2},  # green
              8: {'r': 255, 'g': 90, 'b': 0, 'exponent': 2},  # orange
              6: {'r': 10, 'g': 20, 'b': 255, 'exponent': 2},  # blue
              10: {'r': 255, 'g': 5, 'b': 20, 'exponent': 2},  # red
              12: {'r': 255, 'g': 222, 'b': 23, 'exponent': 2},  # yellow
              14: {'r': 0, 'g': 0, 'b': 0, 'exponent': 2}}  # black

    def make_luxel(dispinfo):
        value = Int8ul.parse(dispinfo_flags8.build(dispinfo.flags))
        value -= value % 2
        return COLORS.get(value, None)

    def find_style_id(lump_faces):
        unused_styles = range(32, 64)
        for face in bsp[lump_faces]:
            for style in face.styles:
                if style in unused_styles:
                    unused_styles.remove(style)
        if len(unused_styles) >= 2:
            return unused_styles[:2]
        else:
            return None

    def insert_logic_branch():
        bsp[0].append([['origin', ENT_ORIGIN],
                       ['targetname', 'disp_vis'],
                       ['classname', 'logic_branch'],
                       ['hammerid', '-1']])
        bsp[0].append([['origin', ENT_ORIGIN],
                       ['targetname', '__disp_vis_event'],
                       ['classname', 'logic_branch_listener'],
                       ['Branch01', 'disp_vis'],
                       ['OnAllTrue', '__disp_vis_on' + ',TurnOn,,0,-1'],
                       ['OnAllTrue', '__disp_vis_off' + ',TurnOff,,0,-1'],
                       ['OnAllFalse', '__disp_vis_on' + ',TurnOff,,0,-1'],
                       ['OnAllFalse', '__disp_vis_off' + ',TurnOn,,0,-1']])

    def insert_light_with_style(name, styleid, spawnflag):
        bsp[0].append([['origin', ENT_ORIGIN],
                       ['targetname', name],
                       ['style', str(styleid)],
                       ['spawnflags', str(spawnflag)],
                       ['_zero_percent_distance', '0'],
                       ['_quadratic_attn', '1'],
                       ['_linear_attn', '0'],
                       ['_lightscaleHDR', '1'],
                       ['_lightHDR', '-1 -1 -1 1'],
                       ['_light', '0 0 0 0'],
                       ['_hardfalloff', '0'],
                       ['_fifty_percent_distance', '0'],
                       ['_distance', '0'],
                       ['_constant_attn', '0'],
                       ['classname', 'light'],
                       ['hammerid', '-1']])

    def insert_lightmaps(lump_faces, lump_lighting):
        lightofs = 0
        disp_count = 0

        if not len(bsp[lump_faces]):
            return

        for face in bsp[lump_faces]:
            # prep
            styles_count = len([x for x in face.styles if x != 255])
            luxel = make_luxel(bsp[26][face.dispinfo])
            face.lightofs += lightofs

            # check face eligibility
            if face.lightofs == -1 or \
               face.dispinfo == -1 or \
               styles_count == 4 or not luxel:
                continue

            # insert style into face
            face.styles[styles_count] = styleids[1]
            for i in range(len(face.styles)):
                if face.styles[i] == 0:
                    face.styles[i] = styleids[0]
                    break

            # insert additional lightmap
            texinfo = bsp[6][face.texinfo]
            lightmap_size = (face.lightmapTextureSizeInLuxels[0] + 1) *\
                            (face.lightmapTextureSizeInLuxels[1] + 1)
            lightmap_size *= 4 if texinfo.flags.SURF_BUMPLIGHT else 1
            lightmap = [luxel for i in range(lightmap_size)]
            lightmap_index = face.lightofs // ColorRGBExp32.sizeof()
            lightmap_index += lightmap_size * styles_count

            bsp[lump_lighting][lightmap_index:lightmap_index] = lightmap

            lightofs += lightmap_size * ColorRGBExp32.sizeof()
            disp_count += 1
        return disp_count

    styleids = find_style_id(7) or find_style_id(58)

    if not styleids:
        print('Could not tag displacements: ' +
              'too many dynamic lights are present in the map')
        return

    if insert_lightmaps(7, 8) or \
       insert_lightmaps(58, 53):
        insert_light_with_style('__disp_vis_off', styleids[0], 0)
        insert_light_with_style('__disp_vis_on', styleids[1], 1)
        insert_logic_branch()

    print('Writing {}'.format(os.path.abspath(out_bsp)))
    bsp.save(out_bsp)
