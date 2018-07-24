#!/usr/bin/env python3
"""

"""

import tkinter as tk
import argparse
import sys

from primitives import SphericalSurface, Component, Ray, Point

class pyTrcGUI(object):
    """
    """

    def __init__(self):
        """
        """
        self.root = tk.Tk()
        self.window_width = self.root.winfo_screenwidth()
        self.window_height = self.root.winfo_screenheight()
        self.window_resize_fullscreen()

        self.frame = tk.PanedWindow(self.root, orient="vertical")
        self.frame.pack(fill=tk.BOTH, expand=1)

        self.canvas = tk.Canvas(self.frame)
        self.frame.add(self.canvas, height=self.window_height-200)
        self.entry = tk.Entry(self.frame)
        self.frame.add(self.entry, minsize=100)

        self.canvas.create_line(0, self.window_height/2, self.window_width, self.window_height/2)

    def window_resize_fullscreen(self):
        """
        """
        self.root.geometry("{0}x{1}+0+0".format(self.window_width, self.window_height))

    def conv_coord(self, p):
        """
        """
        return (p[0], (self.window_height/2)-p[1])

    def add_object(self, obj):
        """
        """
        if isinstance(obj, SphericalSurface):
            p0, p1, ang = obj.surf1.draw_curve()
            p0 = self.conv_coord(p0)
            p1 = self.conv_coord(p1)
            self.canvas.create_arc(p0[0], p0[1], p1[0], p1[1], start=ang[0], extent=ang[1], style=tk.ARC)
        elif isinstance(obj, Component):
            p0, p1, ang1 = obj.surf1.draw_curve()
            p0 = self.conv_coord(p0)
            p1 = self.conv_coord(p1)
            self.canvas.create_arc(p0[0], p0[1], p1[0], p1[1], start=ang1[0], extent=ang1[1], style=tk.ARC)
            p2, p3, ang2 = obj.surf2.draw_curve()
            p2 = self.conv_coord(p2)
            p3 = self.conv_coord(p3)
            self.canvas.create_arc(p2[0], p2[1], p3[0], p3[1], start=ang2[0], extent=ang2[1], style=tk.ARC)
            p4, p5 = obj.draw_line_upper()
            p4 = self.conv_coord(p4)
            p5 = self.conv_coord(p5)
            self.canvas.create_line(p4[0], p4[1], p5[0], p5[1])
            p6, p7 = obj.draw_line_lower()
            p6 = self.conv_coord(p6)
            p7 = self.conv_coord(p7)
            self.canvas.create_line(p6[0], p6[1], p7[0], p7[1])
        elif isinstance(obj, Ray):
            for segment in obj.get_segments():
                if not segment.end is None:
                    p0 = self.conv_coord(segment.start.get_tuple())
                    p1 = self.conv_coord(segment.end.get_tuple())
                    self.canvas.create_line(p0[0], p0[1], p1[0], p1[1], fill="red")

    def mainloop(self):
        tk.mainloop()

def main():
    trc = pyTrcGUI()
    comp1 = Component(500, 25, 100, 150, 100, 3)
    comp2 = Component(650, 30, 150, -400, -100, 3)
    trc.add_object(comp1)
    trc.add_object(comp2)

    ray1 = Ray(Point(0, 10), 0)
    ray2 = Ray(Point(0, 20), 0)
    comp1.trace(ray1)
    comp1.trace(ray2)
    trc.add_object(ray1)
    trc.add_object(ray2)

    import pdb; pdb.set_trace()
    trc.mainloop()
    return 0

if __name__ == "__main__":
    sys.exit(main())