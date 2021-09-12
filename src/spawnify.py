def _getentval(ent, key):
    return next((v for k, v in ent if k.lower() == key), None)


def _fmt(val):
    if val % 1:
        return str(round(val, 6))
    else:
        return str(int(val))


spawn_classes = ['info_player_teamspawn', 'info_player_start']


def spawnify(bsp):
    ent_targets = []

    # find info_player_teamspawns
    for ent in bsp[0]:
        target = [v for k, v in ent if k == 'classname']
        if target and target[0] == spawn_classes:
            ent_targets.append(ent)

    # group spawns together
    groups = {}
    for ent in ent_targets:
        classn = _getentval(ent, 'classname')
        teamid = _getentval(ent, 'teamnum')
        cpoint = _getentval(ent, 'controlpoint')
        rround = _getentval(ent, 'round_redspawn')
        bround = _getentval(ent, 'round_bluespawn')
        groups.setdefault(
            (classn, teamid, cpoint, rround, bround), []).append(ent)

    # offset spawn according to group order
    for k, group in groups.items():
        for index, ent in enumerate(group):
            origin = next(x for x in ent if x[0] == 'origin')
            origin_val = [float(x) for x in origin[1].split(' ')]
            origin_val[2] += (index * 4)
            origin[1] = ' '.join([_fmt(v) for v in origin_val])

    print('{} spawns modified.'.format(len(ent_targets)))
