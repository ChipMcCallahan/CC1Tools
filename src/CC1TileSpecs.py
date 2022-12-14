import itertools
from .cc1_levelset_pb2 import CC1TileCode, TileSpec
from . import CC1TileCodes


# Utils for CC1TileSpec proto
def of(top, bottom=CC1TileCode.FLOOR):
    tspec = TileSpec()
    tspec.top = top
    if bottom != CC1TileCode.FLOOR:
        tspec.bottom = bottom
    return tspec


def is_invalid(tspec):
    return (tspec.top not in CC1TileCodes.MOBS and
            tspec.bottom != CC1TileCode.FLOOR) or \
           tspec.top in CC1TileCodes.INVALID or \
           tspec.bottom in set().union(CC1TileCodes.INVALID,
                                       CC1TileCodes.MOBS)


def add(tspec, tcode):
    is_mob = tcode in CC1TileCodes.MOBS
    mob_here = tspec.top in CC1TileCodes.MOBS
    if is_mob:
        if not mob_here:
            tspec.bottom = tspec.top
        tspec.top = tcode
    else:
        if mob_here:
            tspec.bottom = tcode
        else:
            tspec.top = tcode


def remove(tspec, tcode):
    if tcode == CC1TileCode.FLOOR:
        return False
    elif tcode == tspec.top:
        tspec.top = tspec.bottom
        tspec.ClearField("bottom")
        return True
    elif tcode == tspec.bottom:
        tspec.ClearField("bottom")
        return True
    return False