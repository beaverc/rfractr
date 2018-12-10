from primitives import *
from trcutils import rad2deg

#
v1 = Vector(1,0.3638)
v2 = Vector(-1,0.3638)
v3 = Vector(1,-0.3638)
v4 = Vector(-1,-0.3638)

print(rad2deg(v1.angle_x()))
print(rad2deg(v2.angle_x()))
print(rad2deg(v3.angle_x()))
print(rad2deg(v4.angle_x()))

print(rad2deg(v1.angle(v2)))
print(rad2deg(v1.angle(v3)))