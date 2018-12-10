#!/usr/bin/env/python3

"""

"""

from math import pi

def myrange(start, end, step):
    vals = []
    curr = start
    while curr <= end:
        vals.append(float(curr))
        curr += step
    return vals

def rad2deg(rad):
    return 180*rad/pi

def deg2rad(deg):
    return pi*deg/180

def sign(val):
    if val>=0:
        return 1
    else:
        return -1