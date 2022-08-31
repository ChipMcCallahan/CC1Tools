import unittest

from src.CC1TileSpecs import of
from src.CC1Levels import add, remove, is_valid, update_controls
from src.cc1_levelset_pb2 import CC1TileCode, Level


class TestCC1Levels(unittest.TestCase):
    def test_add(self):
        lv = Level()
        add(lv, 22, CC1TileCode.WALL)
        self.assertEqual(lv.map[22], of(CC1TileCode.WALL))

        add(lv, 22, CC1TileCode.GRAVEL)
        self.assertEqual(lv.map[22], of(CC1TileCode.GRAVEL))

        add(lv, 22, CC1TileCode.BLOB_S)
        self.assertEqual(lv.map[22], of(CC1TileCode.BLOB_S, CC1TileCode.GRAVEL))
        self.assertEqual(len(lv.movement), 1)

        add(lv, 22, CC1TileCode.WALL)
        self.assertEqual(lv.map[22], of(CC1TileCode.BLOB_S, CC1TileCode.WALL))

        add(lv, 22, CC1TileCode.BALL_S)
        self.assertEqual(lv.map[22], of(CC1TileCode.BALL_S, CC1TileCode.WALL))
        self.assertEqual(len(lv.movement), 1)

        add(lv, 22, CC1TileCode.BLOCK)
        self.assertEqual(lv.map[22], of(CC1TileCode.BLOCK, CC1TileCode.WALL))
        self.assertEqual(len(lv.movement), 0)

        add(lv, 22, CC1TileCode.BALL_S)
        self.assertEqual(lv.map[22], of(CC1TileCode.BALL_S, CC1TileCode.WALL))
        self.assertEqual(len(lv.movement), 1)

        add(lv, 22, CC1TileCode.PLAYER_S)
        self.assertEqual(lv.map[22], of(CC1TileCode.PLAYER_S, CC1TileCode.WALL))
        self.assertEqual(len(lv.movement), 0)

        add(lv, 33, CC1TileCode.TRAP_BUTTON)
        add(lv, 34, CC1TileCode.TRAP_BUTTON)
        add(lv, 35, CC1TileCode.TRAP_BUTTON)
        add(lv, 44, CC1TileCode.TRAP)
        lv.trap_controls[33] = 44
        lv.trap_controls[34] = 44
        lv.trap_controls[35] = 44
        add(lv, 34, CC1TileCode.GRAVEL)
        self.assertEqual(len(lv.trap_controls), 2)
        add(lv, 44, CC1TileCode.GRAVEL)
        self.assertEqual(len(lv.trap_controls), 0)

        add(lv, 33, CC1TileCode.CLONE_BUTTON)
        add(lv, 34, CC1TileCode.CLONE_BUTTON)
        add(lv, 35, CC1TileCode.CLONE_BUTTON)
        add(lv, 44, CC1TileCode.CLONER)
        lv.clone_controls[33] = 44
        lv.clone_controls[34] = 44
        lv.clone_controls[35] = 44
        add(lv, 34, CC1TileCode.GRAVEL)
        self.assertEqual(len(lv.clone_controls), 2)
        add(lv, 44, CC1TileCode.GRAVEL)
        self.assertEqual(len(lv.clone_controls), 0)

    def test_remove(self):
        lv = Level()
        add(lv, 22, CC1TileCode.BLOB_S)
        self.assertEqual(len(lv.movement), 1)
        remove(lv, 22, CC1TileCode.BLOB_S)
        remove(lv, 22, CC1TileCode.BLOB_S)
        self.assertEqual(lv.map[22], of(CC1TileCode.FLOOR))
        self.assertEqual(len(lv.movement), 0)

        add(lv, 22, CC1TileCode.BLOB_S)
        add(lv, 22, CC1TileCode.GRAVEL)
        remove(lv, 22, CC1TileCode.BLOB_S)
        self.assertEqual(lv.map[22], of(CC1TileCode.GRAVEL))

        add(lv, 33, CC1TileCode.TRAP_BUTTON)
        add(lv, 34, CC1TileCode.TRAP_BUTTON)
        add(lv, 35, CC1TileCode.TRAP_BUTTON)
        add(lv, 44, CC1TileCode.TRAP)
        lv.trap_controls[33] = 44
        lv.trap_controls[34] = 44
        lv.trap_controls[35] = 44
        remove(lv, 34, CC1TileCode.TRAP_BUTTON)
        self.assertEqual(len(lv.trap_controls), 2)
        remove(lv, 44, CC1TileCode.TRAP)
        self.assertEqual(len(lv.trap_controls), 0)

        add(lv, 33, CC1TileCode.CLONE_BUTTON)
        add(lv, 34, CC1TileCode.CLONE_BUTTON)
        add(lv, 35, CC1TileCode.CLONE_BUTTON)
        add(lv, 44, CC1TileCode.CLONER)
        lv.clone_controls[33] = 44
        lv.clone_controls[34] = 44
        lv.clone_controls[35] = 44
        remove(lv, 34, CC1TileCode.CLONE_BUTTON)
        self.assertEqual(len(lv.clone_controls), 2)
        remove(lv, 44, CC1TileCode.CLONER)
        self.assertEqual(len(lv.clone_controls), 0)

    def test_is_valid(self):
        lv = Level()

        lv.map[0].CopyFrom(of(CC1TileCode.WALL, CC1TileCode.FLOOR))
        self.assertTrue(is_valid(lv))

        lv.map[0].CopyFrom(of(CC1TileCode.TEETH_S, CC1TileCode.WALL))
        self.assertTrue(is_valid(lv))

        lv.map[0].CopyFrom(of(CC1TileCode.WALL, CC1TileCode.TEETH_S))
        self.assertFalse(is_valid(lv))

        lv.map[0].CopyFrom(of(CC1TileCode.FLOOR, CC1TileCode.WALL))
        self.assertFalse(is_valid(lv))

    def test_update_controls(self):
        lv = Level()
        lv.clone_controls[1] = 2
        update_controls(lv, 1, CC1TileCode.CLONE_BUTTON)
        self.assertEqual(len(lv.clone_controls), 0)

        lv = Level()
        lv.clone_controls[1] = 2
        update_controls(lv, 2, CC1TileCode.CLONER)
        self.assertEqual(len(lv.clone_controls), 0)

        lv = Level()
        lv.trap_controls[1] = 2
        update_controls(lv, 1, CC1TileCode.TRAP_BUTTON)
        self.assertEqual(len(lv.clone_controls), 0)

        lv = Level()
        lv.trap_controls[1] = 2
        update_controls(lv, 2, CC1TileCode.TRAP)
        self.assertEqual(len(lv.clone_controls), 0)