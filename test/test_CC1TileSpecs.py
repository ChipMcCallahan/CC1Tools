import unittest

from src.CC1TileSpecs import is_invalid, of, add, remove
from src.cc1_levelset_pb2 import CC1TileCode, TileSpec


class TestCC1TileSpecs(unittest.TestCase):
    def test_of(self):
        expected = TileSpec()
        expected.top = CC1TileCode.TANK_S
        self.assertEqual(of(CC1TileCode.TANK_S), expected)

        expected.bottom = CC1TileCode.GRAVEL
        self.assertEqual(of(CC1TileCode.TANK_S, CC1TileCode.GRAVEL), expected)

    def test_is_invalid(self):
        self.assertTrue(is_invalid(of(CC1TileCode.FLOOR, CC1TileCode.WALL)))
        self.assertTrue(is_invalid(of(CC1TileCode.FLOOR, CC1TileCode.TEETH_S)))
        self.assertTrue(
            is_invalid(of(CC1TileCode.TEETH_S, CC1TileCode.TEETH_S)))
        self.assertTrue(is_invalid(of(CC1TileCode.NOT_USED_0)))
        self.assertFalse(
            is_invalid(of(CC1TileCode.TEETH_S, CC1TileCode.GRAVEL)))
        self.assertFalse(is_invalid(of(CC1TileCode.WALL)))

    def test_add(self):
        tspec = of(CC1TileCode.WALL)
        add(tspec, CC1TileCode.FIRE)
        self.assertEqual(tspec, of(CC1TileCode.FIRE))

        tspec = of(CC1TileCode.TEETH_S, CC1TileCode.GRAVEL)
        add(tspec, CC1TileCode.FIRE)
        self.assertEqual(tspec, of(CC1TileCode.TEETH_S, CC1TileCode.FIRE))

        tspec = of(CC1TileCode.TEETH_S, CC1TileCode.GRAVEL)
        add(tspec, CC1TileCode.PLAYER_S)
        self.assertEqual(tspec, of(CC1TileCode.PLAYER_S, CC1TileCode.GRAVEL))

        tspec = of(CC1TileCode.WALL)
        add(tspec, CC1TileCode.BLOCK)
        self.assertEqual(tspec, of(CC1TileCode.BLOCK, CC1TileCode.WALL))

    def test_remove(self):
        tspec = of(CC1TileCode.WALL)
        self.assertFalse(remove(tspec, CC1TileCode.BLOCK))
        self.assertEqual(tspec, of(CC1TileCode.WALL))

        tspec = of(CC1TileCode.WALL)
        self.assertTrue(remove(tspec, CC1TileCode.WALL))
        self.assertEqual(tspec, of(CC1TileCode.FLOOR))

        tspec = of(CC1TileCode.TEETH_S, CC1TileCode.WALL)
        self.assertTrue(remove(tspec, CC1TileCode.WALL))
        self.assertEqual(tspec, of(CC1TileCode.TEETH_S))

        tspec = of(CC1TileCode.TEETH_S, CC1TileCode.WALL)
        self.assertTrue(remove(tspec, CC1TileCode.TEETH_S))
        self.assertEqual(tspec, of(CC1TileCode.WALL))