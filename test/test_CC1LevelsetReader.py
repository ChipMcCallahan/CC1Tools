import unittest

from src.CC1LevelsetReader import *

class TestCC1LevelsetReader(unittest.TestCase):
	def test_class_construction(self):
		reader = CC1LevelsetReader()
		self.assertTrue(reader)