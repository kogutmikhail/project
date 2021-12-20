import unittest
from unittest.mock import patch
import saper
import pygame

class SaperTest(unittest.TestCase):

    @patch('pygame.key.get_pressed')
    def setup(self, test_patch):
        test_patch.return_value = 'win_test'
        self.assertEqual(saper.lose(), 'win_test')


if __name__ == "__main__":
    unittest.main()