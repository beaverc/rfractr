#!/bin/env/python

"""

"""
import unittest
import sys
sys.path.append("../rfractr")
from primitives import *
from trcutils import rad2deg, deg2rad
from math import tan, pi


class TestPrimitives(unittest.TestCase):

    def setUp(self):
        pass

    def test_numbers_q1q2(self):
        """ Test angles and directions between four different vectors located in
            different quadrants
        """
        tangent = tan(deg2rad(27.5))
        v1 = Vector(1,tangent)
        v2 = Vector(-1,tangent)
        angle = v1.angle(v2)
        self.assertEqual(angle, pi-2*deg2rad(27.5))

    def test_numbers_q2q1(self):
        """ Test angles and directions between four different vectors located in
            different quadrants
        """
        tangent = tan(deg2rad(27.5))
        v1 = Vector(1,tangent)
        v2 = Vector(-1,tangent)
        angle = v2.angle(v1)
        self.assertEqual(angle, -1*(pi-2*deg2rad(27.5)))

    def test_numbers_q1q3(self):
        """ Test angles and directions between four different vectors located in
            different quadrants
        """
        tangent = tan(deg2rad(27.5))
        v1 = Vector(1,tangent)
        v3 = Vector(-1,-1*tangent)
        angle = v1.angle(v3)
        self.assertEqual(angle, pi)

    def test_strings_a_3(self):
        self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main()