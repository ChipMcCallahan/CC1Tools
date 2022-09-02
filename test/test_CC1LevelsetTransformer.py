import unittest

from src.CC1LevelsetTransformer import *

class TestCC1LevelsetTransformer(unittest.TestCase):
	def test_class_construction(self):
		transformer = CC1LevelsetTransformer()
		self.assertTrue(transformer)