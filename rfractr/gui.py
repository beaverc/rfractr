#!/usr/bin/env/python3

"""

"""

import tkinter as tk
import argparse
import sys
import math
import yaml

from primitives import SphericalSurface, PlanarSurface, Component, Ray, Point, Arrangement, RayPattern

LABEL_COMPONENTS = "components"
LABEL_RAY_PATTERN = "ray_pattern"


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
            p0, p1, ang = obj.draw_curve()
            p0 = self.conv_coord(p0)
            p1 = self.conv_coord(p1)
            self.canvas.create_arc(p0[0], p0[1], p1[0], p1[1], start=ang[0], extent=ang[1], style=tk.ARC)
        elif isinstance(obj, PlanarSurface):
            p0, p1 = obj.draw_curve()
            p0 = self.conv_coord(p0)
            p1 = self.conv_coord(p1)
            self.canvas.create_line(p0[0], p0[1], p1[0], p1[1])
        elif isinstance(obj, Component):
            if isinstance(obj.surf1, PlanarSurface):
                p0, p1 = obj.surf1.draw_curve()
                p0 = self.conv_coord(p0)
                p1 = self.conv_coord(p1)
                self.canvas.create_line(p0[0], p0[1], p1[0], p1[1])
            else:
                p0, p1, ang1 = obj.surf1.draw_curve()
                p0 = self.conv_coord(p0)
                p1 = self.conv_coord(p1)
                self.canvas.create_arc(p0[0], p0[1], p1[0], p1[1], start=ang1[0], extent=ang1[1], style=tk.ARC)
            if isinstance(obj.surf2, PlanarSurface):
                p2, p3 = obj.surf2.draw_curve()
                p2 = self.conv_coord(p2)
                p3 = self.conv_coord(p3)
                self.canvas.create_line(p2[0], p2[1], p3[0], p3[1])
            else:
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
        elif isinstance(obj, RayPattern):
            for ray in obj.rays:
                for segment in ray.get_segments():
                    if not segment.end is None:
                        p0 = self.conv_coord(segment.start.get_tuple())
                        p1 = self.conv_coord(segment.end.get_tuple())
                        self.canvas.create_line(p0[0], p0[1], p1[0], p1[1], fill="red")
        elif isinstance(obj, Arrangement):
            for comp in obj.components:
                self.add_object(comp)

    def mainloop(self):
        tk.mainloop()

def preprocess(comp):
    """
    """
    output = []
    for c in comp:
        output.append(comp[c])
    return output

def main(options):
    trc = pyTrcGUI()

    with open(options.config, "r") as fconfig:
        config = yaml.load(fconfig.read())

    if not LABEL_COMPONENTS in config:
        raise ValueError("No components specified in config file")

    components = []
    for comp in config[LABEL_COMPONENTS]:
        proc = preprocess(comp)
        components.append(Component(*proc))

    arrangement = Arrangement(*components)
    trc.add_object(arrangement)

    if LABEL_RAY_PATTERN in config:
        ray_pattern_config = config[LABEL_RAY_PATTERN]
        start = Point(ray_pattern_config["start"]["xval"], ray_pattern_config["start"]["yval"])
        stop = Point(ray_pattern_config["stop"]["xval"], ray_pattern_config["stop"]["yval"])
        count = ray_pattern_config["count"]
        ray_pattern = RayPattern(start=start, stop=stop, type=RayPattern.TYPE_PAR, count=count)
        arrangement.trace(ray_pattern)
        trc.add_object(ray_pattern)

    #comp1 = Component(500, 25, 100, math.inf, -150, 3)
    #comp2 = Component(850, 25, 100, 150, -150, 3)
    #comp2 = Component(850, 35, 150, math.inf, -100, 3)
    #arrangement = Arrangement(comp1, comp2)
    #ray_pattern = RayPattern(start=Point(0, 20), stop=Point(0, -20), type=RayPattern.TYPE_PAR, count=20)
    # ray = Ray(Point(0, -20), 0)
    #arrangement.trace(ray_pattern)
    #ray_pattern.print()
    # arrangement.trace(ray)
    #trc.add_object(ray_pattern)
    # trc.add_object(ray)
    trc.mainloop()
    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Path to arrangement configuration file")
    parser.add_argument("--print", help="Print ray data")
    options = parser.parse_args()
    sys.exit(main(options))