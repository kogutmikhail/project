import unittest
from unittest.mock import patch
import saper

class SaperTest(unittest.TestCase):
    def test1(self):
        tile1 = saper.tile(1,1)
        self.assertEqual(tile1, saper.gettile(1,1))


if __name__ == "__main__":
    unittest.main()