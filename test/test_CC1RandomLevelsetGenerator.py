import unittest

from src.CC1RandomLevelsetGenerator import *

class TestCC1RandomLevelsetGenerator(unittest.TestCase):
	def test_class_construction(self):
		generator = CC1RandomLevelsetGenerator()
		self.assertTrue(generator)