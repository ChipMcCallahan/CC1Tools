import unittest

from src.CC1LevelImager import *

class TestCC1LevelImager(unittest.TestCase):
	def test_class_construction(self):
		imager = CC1LevelImager()
		self.assertTrue(imager)