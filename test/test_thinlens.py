#!/usr/bin/env python3

"""

"""

import unittest
import sys
sys.path.append("../rfractr")
from primitives import *
from trcutils import rad2deg, deg2rad
from math import tan, pi

def lens_power(r1, r2, n0, n1):
    """

    """
    p1 = 1/r1
    p2 = 1/r2
    return (n1-n0)*(p1-p2)/n0

class TestThinLens(unittest.TestCase):

    def setUp(self):
        pass

    def test_lens1(self):
        """
        """
        lens1 = Component(100, 5, 100, 1000, -1000, 1.5)
        line = Ray(Point(0, 10), 0)
        lens1.trace(line)
        lastseg = line.get_last_segment()
        intercept = lastseg.get_x_intercept()
        fl_measured = intercept-100

        import pdb; pdb.set_trace()
        self.assertEqual(0, 1)

if __name__ == '__main__':
    unittest.main()