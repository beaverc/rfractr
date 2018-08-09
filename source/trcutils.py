#!/usr/bin/env/python3

"""

"""

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