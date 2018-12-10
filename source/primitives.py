#!/usr/bin/env/python3

"""

"""

from math import sqrt, tan, atan, cos, acos, sin, asin, pi, inf
from trcutils import myrange, rad2deg, deg2rad, sign

def tabular_print(*args, width=80):
    """Print data as a table
    """
    cols = len(args)
    colw = width//cols

    # Pad or truncate depending on length
    rowstring = ""
    for arg in args:
        if len(arg) == colw:
            temp = arg
        elif len(arg) > colw:
            temp = arg[0:colw]
        else:
            diff = colw - len(arg)
            temp = arg
            temp += "".join(" " for i in range(diff))
        rowstring += temp

    print(rowstring)

class Vector(object):
    """
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        if not isinstance(other, Vector):
            raise TypeError("Expecting a vector for vector addition")
        return Vector(self.x+other.x, self.y+other.y)

    def __mul__(self, other):
        if not (isinstance(other, float) or isinstance(other, int)):
            raise TypeError("Expecting an int or a float for scalar multiplication")
        return Vector(self.x*other, self.y*other)

    def dot(self, other):
        if not isinstance(other, Vector):
            raise TypeError("Expecting a vector for dot product")
        return self.x*other.x+self.y*other.y

    def mag(self):
        return sqrt(self.x**2+self.y**2)

    def angle(self, other):
        v1_anglex = self.angle_x()
        v2_anglex = other.angle_x()

        if (v1_anglex>=0 and v2_anglex>=0) or (v1_anglex<=0 and v2_anglex<=0):
            return v2_anglex-v1_anglex
        elif (v1_anglex>0 and v2_anglex<0) or (v1_anglex<0 and v2_anglex>0):
            v1_negativex = v1_anglex-pi
            # Return the closest angle between the two vectors
            if v2_anglex<=v1_negativex:
                return v2_anglex+v1_anglex+pi
            else:
                return v2_anglex-v1_anglex

    def angle_x(self):
        angle_tan = self.y/self.x
        if self.x>=0:
            return atan(angle_tan)
        else:
            return atan(angle_tan)+sign(self.y)*pi

    # def angle_y(self):
    #     y_axis = Vector(0, self.y)
    #     return self.angle(y_axis)

    def extend(self, distance):
        angle_x = self.angle(Vector(self.x, 0))
        self.x += distance*cos(angle_x)
        self.y += distance*sin(angle_x)

class SphericalSurface(object):
    """A spherical optical surface
    """

    def __init__(self, pos, r, aperture, index):
        """
        """
        # Evaluate radius
        if r == 0:
            raise ValueError("Radius must be a nonzero number")

        #
        self.pos_x = pos
        self.ctr_x = pos + r
        self.r = r
        self.ap = aperture

        # Get thickness
        self.thick = abs(self.r) - self.circle_x(self.ap/2)[0]
        if self.r>0:
            self.x_apt = self.thick + self.pos_x
        else:
            self.x_apt = self.pos_x - self.thick

    def circle(self, x):
        """
        """
        try:
            res = sqrt(self.r**2-(x-self.ctr_x)**2)
            return res, -1*res
        except ValueError:
            return None, None

    def in_circle(self, x, y):
        """
        """
        r_calc = (x-self.ctr_x)**2 + y**2
        if r_calc>self.r**2:
            return False
        else:
            return True

    def circle_x(self, y):
        """
        """
        try:
            res = sqrt(self.r**2-y**2)
            return res, -1*res
        except ValueError:
            return None, None

    def get_intersection(self, segment):
        """
        """
        x_dist = self.x_apt - segment.start.x
        h_apt = segment.start.y+tan(segment.angle)*x_dist

        if h_apt>self.ap/2 or h_apt<(-1)*self.ap/2:
            return None

        x_test = self.x_apt
        y_test = h_apt

        STEP = 0.001
        if self.r > 0:
            STEP = -STEP

        while True:
            if not self.in_circle(x_test, y_test):
                break
            x_test += STEP*cos(segment.angle)
            y_test += STEP*sin(segment.angle)

        return Point(x_test, y_test)

    def get_refraction(self, segment, intersect, index):
        """
        """
        # Check if surface is concave or convex
        concave = self.ctr_x<intersect.x

        # Angle between surface normal (v) and incident ray (u)
        v = Vector(intersect.x-self.ctr_x, intersect.y)
        u = Vector(segment.start.x-intersect.x, segment.start.y-intersect.y)

        angle = v.angle(u)
        if concave:
            angle -= pi

        n1 = 1
        n2 = index

        sine = n1*sin(angle)/n2
        angle2 = asin(sine)

        if concave:
            angle2 -= v.angle_x()
        else:
            angle2 -= (pi-v.angle_x())

        return Segment(start=intersect, angle=angle2)

    def draw_curve(self):
        """
        """
        half_angle = asin((self.ap/2)/abs(self.r))
        if self.r > 0:
            start = 180-rad2deg(half_angle)
            extent = 2*rad2deg(half_angle)
        else:
            start = -rad2deg(half_angle)
            extent = 2*rad2deg(half_angle)
        return (self.pos_x, self.r), (self.ctr_x+self.r, -1*self.r), (start, extent)

    def trace(self, ray):
        """
        """
        segment = ray.get_last_segment()
        if segment:
            intersection = self.get_intersection(segment)
            if intersection is None:
                segment.out_of_range = True
            else:
                refraction = self.get_refraction(segment, intersection, 1.5)
                ray.add_segment(refraction)

class PlanarSurface(object):
    """A planar optical surface
    """

    def __init__(self, pos, aperture, index):
        """
        """
        self.pos_x = pos
        self.ap = aperture

    def get_intersection(self, segment):
        """
        """
        x_dist = self.pos_x-segment.start.x
        h_apt = segment.start.y+tan(segment.angle)*x_dist

        if h_apt>self.ap/2 or h_apt<(-1)*self.ap/2:
            return None

        return Point(self.pos_x, h_apt)

    def get_refraction(self, segment, intersect, index):
        """
        """
        n1 = 1
        n2 = index

        sine = n1*sin(segment.angle)/n2
        angle2 = asin(sine)

        return Segment(start=intersect, angle=angle2)

    def draw_curve(self):
        """
        """
        return (self.pos_x, self.ap/2), (self.pos_x, -1*self.ap/2)

    def trace(self, ray):
        """
        """
        segment = ray.get_last_segment()
        if segment:
            intersection = self.get_intersection(segment)
            if intersection is None:
                segment.out_of_range = True
            else:
                refraction = self.get_refraction(segment, intersection, 1.5)
                ray.add_segment(refraction)

class Component(object):
    """An optical component consisting of an entry and exit surface (spherical
       or planar)
    """

    def __init__(self, pos, spacing, aperture, radius1, radius2, index):
        """
        """
        self.index = index
        if radius1=="INF":
            self.surf1 = PlanarSurface(pos, aperture, index)
        else:
            self.surf1 = SphericalSurface(pos, radius1, aperture, index)
        if radius2=="INF":
            self.surf2 = PlanarSurface(pos+spacing, aperture, index)
        else:
            self.surf2 = SphericalSurface(pos+spacing, radius2, aperture, index)

    def draw_line_upper(self):
        """Draw the top connecting line between two surfaces
        """
        if isinstance(self.surf1, PlanarSurface):
            x_start = self.surf1.pos_x
        else:
            if self.surf1.r > 0:
                x_start = self.surf1.pos_x+self.surf1.thick
            else:
                x_start = self.surf1.pos_x-self.surf1.thick
        if isinstance(self.surf2, PlanarSurface):
            x_stop = self.surf2.pos_x
        else:
            if self.surf2.r > 0:
                x_stop = self.surf2.pos_x+self.surf2.thick
            else:
                x_stop = self.surf2.pos_x-self.surf2.thick
        return (x_start, self.surf1.ap/2), (x_stop, self.surf1.ap/2)

    def draw_line_lower(self):
        """Draw the bottom connecting line between two surfaces
        """
        if isinstance(self.surf1, PlanarSurface):
            x_start = self.surf1.pos_x
        else:
            if self.surf1.r > 0:
                x_start = self.surf1.pos_x+self.surf1.thick
            else:
                x_start = self.surf1.pos_x-self.surf1.thick
        if isinstance(self.surf2, PlanarSurface):
            x_stop = self.surf2.pos_x
        else:
            if self.surf2.r > 0:
                x_stop = self.surf2.pos_x+self.surf2.thick
            else:
                x_stop = self.surf2.pos_x-self.surf2.thick
        return (x_start, -1*self.surf1.ap/2), (x_stop, -1*self.surf1.ap/2)

    def trace(self, ray):
        """
        """
        self.surf1.trace(ray)
        self.surf2.trace(ray)

class Ray(object):
    """Representation of an entire ray consisting of several segments
    """

    def __init__(self, start, angle):
        """
        """
        self.__segments = [Segment(start=start, angle=angle)]

    def add_segment(self, newseg):
        """
        """
        if len(self.__segments)>0:
            self.__segments[-1].update(end=newseg.start)
        self.__segments.append(newseg)

    def get_last_segment(self):
        """
        """
        if len(self.__segments) > 0:
            return self.__segments[-1]
        else:
            return None

    def get_segments(self):
        """
        """
        return self.__segments

    def print(self):
        """Prints out the segments from start to end for debug purposes
        """
        print("".join("#" for i in range(80)))
        print("".join("#" for i in range(80)))
        tabular_print("START", "END", "ANGLE")
        for i in range(len(self.__segments)):
            seg = self.__segments[i]
            start = "{:.4f},{:.4f}".format(seg.start.x, seg.start.y) if not seg.start is None else str(seg.start)
            end = "{:.4f},{:.4f}".format(seg.end.x, seg.end.y) if not seg.end is None else str(seg.end)
            angle = "{:.4f}".format(seg.angle) if not seg.angle is None else str(seg.angle)
            tabular_print(start, end, angle)

class Segment(object):
    """Representation of a single segment in a ray's path
    """
    RESOLVED = 0
    UNRESOLVED = 1

    def __init__(self, **kwargs):
        """
        """

        if "start" in kwargs and "angle" in kwargs:
            self.type = Segment.UNRESOLVED
            self.start = kwargs["start"]
            self.angle = kwargs["angle"]
            self.end = None
        elif "start" in kwargs and "end" in kwargs:
            self.type = Segment.RESOLVED
            self.start = kwargs["start"]
            self.end = kwargs["end"]
            self.angle = Vector((self.end.x-self.start.x), (self.end.y-self.start.y)).angle_x()
        else:
            ValueError("Invalid arguments")

        if "out_of_range" in kwargs:
            self.out_of_range = kwargs["out_of_range"]
        else:
            self.out_of_range = False

    def update(self, **kwargs):
        """
        """
        if "start" in kwargs:
            self.start = kwargs["start"]
            if self.type==Segment.RESOLVED:
                self.angle = Vector((self.end.x-self.start.x), (self.end.y-self.start.y)).angle_x()
        if "end" in kwargs:
            self.end = kwargs["end"]
            self.angle = Vector((self.end.x-self.start.x), (self.end.y-self.start.y)).angle_x()
            if self.type==Segment.UNRESOLVED:
                self.type = Segment.RESOLVED
        if "angle" in kwargs:
            if self.type==Segment.UNRESOLVED:
                self.angle = Vector((self.end.x-self.start.x), (self.end.y-self.start.y)).angle_x()

class Point(object):
    """
    """

    def __init__(self, x, y):
        """
        """
        self.x = x
        self.y = y

    def get_tuple(self):
        """
        """
        return (self.x, self.y)

class Arrangement(object):
    """
    """

    def __init__(self, *args, index=1.0):
        """
        """
        self.components = []
        for arg in args:
            self.add_component(arg)

    def add_component(self, component):
        """
        """
        if not isinstance(component, Component):
            raise ValueError("Expecting type Component")
        self.components.append(component)

    def trace(self, obj):
        """
        """
        if isinstance(obj, Ray):
            for comp in self.components:
                comp.trace(obj)
        elif isinstance(obj, RayPattern):
            for ray in obj.rays:
                for comp in self.components:
                    comp.trace(ray)

class RayPattern(object):
    """
    """
    TYPE_FAN = 0
    TYPE_PAR = 1

    def __init__(self, **kwargs):
        """
        """
        self.rays = []
        if not "type" in kwargs:
            raise ValueError("Expecting option 'type'")
        if not "start" in kwargs:
            raise ValueError("Expecting option 'start'")
        else:
            start = kwargs["start"]
        if kwargs["type"]==RayPattern.TYPE_PAR:
            if not "stop" in kwargs:
                raise ValueError("Expecting option 'stop'")
            else:
                stop = kwargs["stop"]
            if not "count" in kwargs:
                raise ValueError("Expecting option 'count'")
            else:
                count = kwargs["count"]
            step = (stop.y-start.y)/(count-1)
            new_y = start.y
            for i in range(count):
                self.rays.append(Ray(Point(start.x, new_y), 0))
                new_y += step
        else:
            raise ValueError("Invalid RayPattern type")

    def print(self):
        for ray in self.rays:
            ray.print()
