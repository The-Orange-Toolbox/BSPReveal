from totcommon.logger import stdout


def _getentval(ent, key):
    return next((v for k, v in ent if k.lower() == key), None)


def _fmt(val):
    if val % 1:
        return str(round(val, 6))
    else:
        return str(int(val))


spawn_classes = ['info_player_teamspawn', 'info_player_start']


def spawnify(bsp, delta=4):
    ent_targets = []
    spawn_count = 0

    # find info_player_teamspawns
    for ent in bsp[0]:
        target = [v for k, v in ent if k == 'classname']
        if target and target[0] in spawn_classes:
            ent_targets.append(ent)

    # group spawns together
    groups = {}
    for ent in ent_targets:
        classn = _getentval(ent, 'classname')
        targetn = _getentval(ent, 'targetname')
        teamid = _getentval(ent, 'teamnum')
        cpoint = _getentval(ent, 'controlpoint')
        rround = _getentval(ent, 'round_redspawn')
        bround = _getentval(ent, 'round_bluespawn')
        zvalue = [float(x) for x in _getentval(ent, 'origin').split(' ')][2]
        groups.setdefault(
            (classn, targetn, teamid, cpoint, rround, bround, zvalue), []).append(ent)

    # offset spawn according to group order
    for k, group in groups.items():
        for index, ent in enumerate(group):
            origin = next(x for x in ent if x[0] == 'origin')
            origin_val = [float(x) for x in origin[1].split(' ')]
            origin_val[2] += (index * delta)
            if index > 0:
                spawn_count += 1
            origin[1] = ' '.join([_fmt(v) for v in origin_val])

    if spawn_count:
        stdout('{} spawns modified.'.format(spawn_count))
