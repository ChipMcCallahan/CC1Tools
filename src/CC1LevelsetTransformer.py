from .cc1_levelset_pb2 import CC1TileCode, Levelset, Level
from . import CC1TileCodes, CC1Levels

class CC1LevelsetTransformer:
    def transform(self, levels, old, new):
        if isinstance(levels, Levelset):
            levels = levels.levels
        if isinstance(levels, Level):
            levels = [levels]
        if isinstance(old, int):
            old = [old]
        for level in levels:
            for pos, tspec in level.map.items():
                if CC1Levels.remove(level, pos, old):
                    CC1Levels.add(level, pos, new)
                elif CC1TileCode.FLOOR in old: # since FLOOR is default, it doesn't ever get removed
                    if tspec.top == CC1TileCode.FLOOR or (tspec.top in CC1TileCodes.MOBS and tspec.bottom == CC1TileCode.FLOOR):
                        CC1Levels.add(level, pos, new)
    
    def keep(self, levels, old):
        if isinstance(old, int):
            old = set((old,))
        old = set(old)
        self.transform(levels, CC1TileCodes.ALL.difference(old), CC1TileCode.FLOOR)
    
    def walls_of(self, levels, walls=CC1TileCodes.WALLS.union(CC1TileCodes.PANELS)):
        return self.keep(levels, walls)
    
    def mobs_of(self, levels, mobs=CC1TileCodes.MOBS, *, keep_cloners=True):
        if keep_cloners:
            mobs = mobs.union(set((CC1TileCode.CLONER,)))
        return self.keep(levels, mobs)
    
    # old can be multiple mob types. new must be exactly one mob for each direction.
    def mob_switcher(self, levels, old, new):
        for d in "NESW":
            targets = set(tuple(mob for mob in old if CC1TileCode.Name(mob).endswith(f"_{d}")))
            replace = tuple(mob for mob in new if CC1TileCode.Name(mob).endswith(f"_{d}"))
            self.transform(levels, targets, replace[0])
