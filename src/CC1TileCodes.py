from src.cc1_levelset_pb2 import CC1TileCode

# Utils for CC1TileCode enum
ALL = frozenset(CC1TileCode.values())
ICE = frozenset(CC1TileCode.Value(s) for s in
                ("ICE", "ICE_NW", "ICE_NE", "ICE_SW", "ICE_SE"))
FORCES = frozenset(CC1TileCode.Value(s) for s in
                   ("FORCE_N", "FORCE_E", "FORCE_S", "FORCE_W", "FORCE_RANDOM"))
WALLS = frozenset(CC1TileCode.Value(s) for s in
                  ("WALL", "INV_WALL_PERM", "INV_WALL_APP", "BLUE_WALL_REAL"))
PANELS = frozenset(CC1TileCode.Value(s) for s in
                   ("PANEL_SE", "PANEL_N", "PANEL_E", "PANEL_S", "PANEL_W"))
CLONE_BLOCKS = frozenset(CC1TileCode.Value(s) for s in
                         tuple(f"CLONE_BLOCK_{d}" for d in "NESW"))
BLOCKS = CLONE_BLOCKS.union(frozenset(((CC1TileCode.BLOCK,))))
PLAYERS = frozenset(
    CC1TileCode.Value(s) for s in tuple(f"PLAYER_{d}" for d in "NESW"))
ANTS = frozenset(
    CC1TileCode.Value(s) for s in tuple(f"ANT_{d}" for d in "NESW"))
PARAMECIA = frozenset(CC1TileCode.Value(s) for s in
                      tuple(f"PARAMECIUM_{d}" for d in "NESW"))
GLIDERS = frozenset(
    CC1TileCode.Value(s) for s in tuple(f"GLIDER_{d}" for d in "NESW"))
FIREBALLS = frozenset(CC1TileCode.Value(s) for s in
                      tuple(f"FIREBALL_{d}" for d in "NESW"))
TANKS = frozenset(
    CC1TileCode.Value(s) for s in tuple(f"TANK_{d}" for d in "NESW"))
BALLS = frozenset(
    CC1TileCode.Value(s) for s in tuple(f"BALL_{d}" for d in "NESW"))
WALKERS = frozenset(
    CC1TileCode.Value(s) for s in tuple(f"WALKER_{d}" for d in "NESW"))
TEETH = frozenset(
    CC1TileCode.Value(s) for s in tuple(f"TEETH_{d}" for d in "NESW"))
BLOBS = frozenset(
    CC1TileCode.Value(s) for s in tuple(f"BLOB_{d}" for d in "NESW"))
MONSTERS = frozenset().union(ANTS, PARAMECIA, GLIDERS, FIREBALLS, TANKS, BALLS,
                             WALKERS, TEETH, BLOBS)
ENTITIES = frozenset().union(MONSTERS, BLOCKS, PLAYERS)
NONENTITIES = ALL.difference(ENTITIES)
DOORS = frozenset(CC1TileCode.Value(s) for s in
                  tuple(
                      f"{c}_DOOR" for c in ("RED", "BLUE", "YELLOW", "GREEN")))
KEYS = frozenset(CC1TileCode.Value(s) for s in
                 tuple(f"{c}_KEY" for c in ("RED", "BLUE", "YELLOW", "GREEN")))
BOOTS = frozenset(CC1TileCode.Value(s) for s in
                  ("FLIPPERS", "FIRE_BOOTS", "SKATES", "SUCTION_BOOTS"))
PICKUPS = frozenset().union(KEYS, BOOTS, frozenset((CC1TileCode.CHIP,)))
BUTTONS = frozenset(CC1TileCode.Value(s) for s in
                    ("GREEN_BUTTON", "TRAP_BUTTON", "CLONE_BUTTON",
                     "TANK_BUTTON"))
INVALID = frozenset((
    CC1TileCode.NOT_USED_0,
    CC1TileCode.DROWN_CHIP,
    CC1TileCode.BURNED_CHIP0,
    CC1TileCode.BURNED_CHIP1,
    CC1TileCode.NOT_USED_1,
    CC1TileCode.NOT_USED_2,
    CC1TileCode.NOT_USED_3,
    CC1TileCode.CHIP_EXIT,
    CC1TileCode.UNUSED_EXIT_0,
    CC1TileCode.UNUSED_EXIT_1,
    CC1TileCode.CHIP_SWIMMING_N,
    CC1TileCode.CHIP_SWIMMING_E,
    CC1TileCode.CHIP_SWIMMING_S,
    CC1TileCode.CHIP_SWIMMING_W
))


# Rotate letter string e.g. "N", "SE" by letter d where d = "R" for right,
# "L" for left, "V" for reverse
def rotate(letters, d):
    if len(letters) == 1:
        return "NESW"[("NESW".index(letters) + "_RVL".index(d)) % 4]
    elif len(letters) == 2:
        corners = {"NE": "NW", "NW": "SW", "SW": "SE", "SE": "NE"}
        passes = "_LVR".index(d)
        for _ in range(passes):
            letters = corners[letters]
        return letters
    else:
        raise Exception(f"Cannot rotate {letters}.")


# Rotate Tile code e.g. PLAYER_N by letter d where d = "R" for right,
# "L" for left, "V" for reverse
def rotate_tile(tile_code, d):
    name = CC1TileCode.Name(tile_code)
    if name[-2] == "_":
        return CC1TileCode.Value(name[:-1] + rotate(name[-1], d))
    elif name[-3] == "_" and tile_code not in PANELS:
        return CC1TileCode.Value(name[:-2] + rotate(name[-2:], d))
    else:
        return tile_code


def rotate_left(tile_code):
    return rotate_tile(tile_code, "L")


def reverse(tile_code):
    return rotate_tile(tile_code, "V")


def rotate_right(tile_code):
    return rotate_tile(tile_code, "R")