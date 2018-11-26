from primitives import Vector
import sys

def test_angles():
    # Rotate clockwise by 90 deg
    v1 = Vector(0, 1)
    v2 = Vector(1, 0)
    angle = v1.angle(v2)

    print("v1 angle to x-axis: {}".format(v1.angle_x()))
    print("v2 angle to x-axis: {}".format(v2.angle_x()))
    print(angle)

    # Rotate couter-clockwise by 90 deg
    v1 = Vector(1, 0)
    v2 = Vector(0, 1)
    print(angle)

    return 0

if __name__ == "__main__":
    sys.exit(test_angles())