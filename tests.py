import unittest
import saper
from pygame.locals import *

class SaperTest(unittest.TestCase):
    def test1(self):
        tile1 = saper.tile(Rect(10, 10, 17, 17))
        tile1.x = 1
        tile1.y = 1
        saper.tiles = [tile1]
        self.assertEqual(tile1, saper.gettile(1,1))


if __name__ == "__main__":
    unittest.main()