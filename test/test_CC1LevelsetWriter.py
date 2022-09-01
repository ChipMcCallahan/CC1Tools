import unittest

from src.CC1LevelsetWriter import *

class TestCC1LevelsetWriter(unittest.TestCase):
	def test_class_construction(self):
		Writer = CC1LevelsetWriter()
		self.assertTrue(Writer)