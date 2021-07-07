import os
import sys
import uuid
import tempfile
from zipfile import ZipFile

import shutil

from valvebsp import Bsp

TEXMAP = {
    'trigger_hurt': 'TOOLSPRO/TOOLSHURT',
    'trigger_multiple': 'TOOLSPRO/TOOLSTRIGGER',
    'trigger_capture_area': 'TOOLSPRO/TOOLSCAPTURE',
    'func_nobuild': 'TOOLSPRO/TOOLSNOBUILD',
    'func_nogrenades': 'TOOLSPRO/TOOLSNOGRENADES',
    'func_regenerate': 'TOOLSPRO/TOOLSREGENERATE',
    'func_respawnroom': 'TOOLSPRO/TOOLSRESPAWN',
}


def get_asset_paths(asset_name):
    script_dir = os.path.abspath(os.path.dirname(__file__))
    bundle_dir = getattr(sys, '_MEIPASS', script_dir)
    asset_dir = os.path.join(bundle_dir, 'assets')

    internal_path = os.path.join('/materials/toolspro/', asset_name)
    external_path = os.path.abspath(os.path.join(asset_dir, asset_name))
    return (external_path, internal_path)


def inject_pak(bsp, materials):
    materials = [m+s for m in materials for s in ['.vmt', '.vtf']]
    materials = [m.split('/')[-1].lower() for m in materials]
    zippath = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))

    with open(zippath, 'wb') as zipfile:
        zipfile.write(bsp[40])

    with ZipFile(zippath, 'a') as zipfile:
        [zipfile.write(*get_asset_paths(m)) for m in materials]

    with open(zippath, 'rb') as zipfile:
        bsp[40] = zipfile.read()


def triggerify(in_bsp, out_bsp):
    bsp = Bsp(in_bsp)

    tnameids = [x for x in range(len(bsp[43])) if
                bsp[43][x].upper() == 'TOOLS/TOOLSTRIGGER']
    tdataids = [x for x in range(len(bsp[2])) if
                bsp[2][x].nameStringTableID in tnameids]

    ent_targets = {
        'trigger_hurt': [],
        'trigger_multiple': [],
        'trigger_capture_area': [],
        'func_nobuild': [],
        'func_nogrenades': [],
        'func_regenerate': [],
        'func_respawnroom': []
    }

    for ent in bsp[0]:
        target = None
        for k, v in ent:
            if k == 'classname' and v in ent_targets.keys():
                target = v

        target = [v for k, v in ent if k == 'classname']
        if target and target[0] in ent_targets.keys():
            ent_targets[target[0]].append(ent)

    def reassign(ent_type, ents):

        # inject texture name
        tname = TEXMAP[ent_type].upper()
        tnames = [x.upper() for x in bsp[43]]
        if tname in tnames:
            tnameid = tnames.index(tname)
        else:
            bsp[44].append(bsp[44][-1] + len(bsp[43][-1]) + 1)
            bsp[43].append(tname)
            tnameid = len(bsp[43]) - 1

        # inject texture data
        tdata = [x for x in bsp[2] if x.nameStringTableID == tnameid]
        if tdata:
            tdataid = bsp[2].index(tdata)
        else:
            base_tdata = [x for x in bsp[2] if x.nameStringTableID in tdataids]
            base_tdata = base_tdata[0].copy()
            base_tdata.nameStringTableID = tnameid
            bsp[2].append(base_tdata)
            tdataid = len(bsp[2]) - 1

        # inject texture info
        tinfo_reassigns = {}

        def inject_tinfo(tinfoid):
            if tinfoid not in tinfo_reassigns.keys():
                tinfo = bsp[6][tinfoid].copy()
                tinfo.texData = tdataid
                bsp[6].append(tinfo)
                tinfo_reassigns[tinfoid] = len(bsp[6]) - 1

            return tinfo_reassigns[tinfoid]

        # find faces
        models = []
        for ent in ents:
            model = [v for k, v in ent if k == 'model']
            modelid = int(model[0][1:])
            models.append(modelid)

        faces = []
        for modelid in models:
            model = bsp[14][modelid]
            for faceid in range(model.firstface, model.firstface + model.numfaces):
                faces.append(faceid)

        # reassign face texinfo
        for faceid in faces:
            new_texinfo = inject_tinfo(bsp[7][faceid].texinfo)
            if len(bsp[7]):
                bsp[7][faceid].texinfo = new_texinfo
            if len(bsp[58]):
                bsp[58][faceid].texinfo = new_texinfo

    for ent_type, ents in ent_targets.items():
        reassign(ent_type, ents)

    materials = [TEXMAP[k] for k, v in ent_targets.items() if v]
    inject_pak(bsp, materials)

    bsp.save(out_bsp)
