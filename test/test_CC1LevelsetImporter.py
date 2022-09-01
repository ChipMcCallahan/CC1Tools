import unittest

from src.CC1LevelsetImporter import *

class TestCC1LevelsetImporter(unittest.TestCase):
	def test_class_construction(self):
		importer = CC1LevelsetImporter()
		self.assertTrue(importer)