import unittest

from src.CC1TileCodes import rotate, rotate_tile, rotate_left, \
    reverse, rotate_right
from src.cc1_levelset_pb2 import CC1TileCode


class TestCC1TileCodes(unittest.TestCase):
    def test_rotate(self):
        for i, d in enumerate("NESW"):
            self.assertEqual(rotate(d, "R"), "ESWN"[i])
            self.assertEqual(rotate(d, "L"), "WNES"[i])
            self.assertEqual(rotate(d, "V"), "SWNE"[i])
        self.assertEqual(rotate("NW", "R"), "NE")
        self.assertEqual(rotate("SE", "L"), "NE")
        self.assertEqual(rotate("NW", "V"), "SE")

    def test_rotate_tile(self):
        self.assertEqual(rotate_tile(CC1TileCode.BLOB_S, "R"),
                         CC1TileCode.BLOB_W)
        self.assertEqual(rotate_tile(CC1TileCode.ICE_SE, "L"),
                         CC1TileCode.ICE_NE)
        self.assertEqual(rotate_tile(CC1TileCode.BLOCK, "V"),
                         CC1TileCode.BLOCK)

    def test_rotate_left(self):
        self.assertEqual(rotate_left(CC1TileCode.PLAYER_S),
                         CC1TileCode.PLAYER_E)

    def test_rotate_right(self):
        self.assertEqual(rotate_right(CC1TileCode.TANK_N),
                         CC1TileCode.TANK_E)

    def test_reverse(self):
        self.assertEqual(reverse(CC1TileCode.ICE_SE), CC1TileCode.ICE_NW)