from .cc1_levelset_pb2 import CC1TileCode, TileSpec
from . import CC1TileCodes, CC1TileSpecs


def add(level, pos, tcode):
    tspec = level.map[pos]
    oldspec = TileSpec()
    oldspec.CopyFrom(tspec)
    was_monster = tspec.top in CC1TileCodes.MONSTERS
    CC1TileSpecs.add(tspec, tcode)
    is_monster = tspec.top in CC1TileCodes.MONSTERS

    if was_monster and not is_monster:
        level.movement.remove(pos)
    if is_monster and not was_monster and len(level.movement) < 127:
        level.movement.append(pos)

    for code in (CC1TileCode.TRAP, CC1TileCode.TRAP_BUTTON, CC1TileCode.CLONER,
                 CC1TileCode.CLONE_BUTTON):
        if code in (oldspec.top, oldspec.bottom) and code not in (
        tspec.top, tspec.bottom):
            update_controls(level, pos, code)


def remove(level, pos, tcodes, *, keep_cloned_mobs=False):
    if isinstance(tcodes, int):
        tcodes = [tcodes]
    tspec = level.map[pos]
    removed = False
    for tcode in tcodes:
        if CC1TileSpecs.remove(tspec, tcode):
            removed = True
            if tcode in CC1TileCodes.MONSTERS and pos in level.movement:
                level.movement.remove(pos)
            elif tcode == CC1TileCode.CLONER:
                if not keep_cloned_mobs and tspec.top in CC1TileCodes.MOBS:
                    CC1TileSpecs.remove(tspec, tspec.top)
            update_controls(level, pos, tcode)
    return removed


def update_controls(level, pos, tcode):
    if tcode == CC1TileCode.TRAP:
        for k, v in tuple(level.trap_controls.items()):
            if v == pos:
                level.trap_controls.pop(k, None)
    elif tcode == CC1TileCode.TRAP_BUTTON:
        level.trap_controls.pop(pos, None)
    elif tcode == CC1TileCode.CLONER:
        for k, v in tuple(level.clone_controls.items()):
            if v == pos:
                level.clone_controls.pop(k, None)
    elif tcode == CC1TileCode.CLONE_BUTTON:
        level.clone_controls.pop(pos, None)


def is_valid(level):
    for tspec in level.map.values():
        if CC1TileSpecs.is_invalid(tspec):
            return False
    return True