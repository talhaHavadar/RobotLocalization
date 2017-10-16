"""
MIT License

Copyright (c) 2017 Talha Can Havadar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from robot_localization.utils.vector import Vector2D

REPR_3D = 0
REPR_2D = 1
REPR_UNKNOWN = -1

class Point(object):
    """
    A Point interface to provide essential functionalities
    and modularity to module
    """

    def get_position(self):
        """
        Returns the all axis together as tuple
        """
        raise NotImplementedError

    def get_x_axis(self):
        """
        Returns the x axis
        """
        raise NotImplementedError

    def get_y_axis(self):
        """
        Returns the y axis
        """
        raise NotImplementedError

    def get_z_axis(self):
        """
        Returns the z axis
        """
        raise NotImplementedError

    def set_x_axis(self, x_axis):
        """
        Sets the x axis
        """
        raise NotImplementedError

    def set_y_axis(self, y_axis):
        """
        Sets the y axis
        """
        raise NotImplementedError

    def set_z_axis(self, z_axis):
        """
        Sets the z axis
        """
        raise NotImplementedError

#pylint: disable=W0223
class Point2D(Point):
    """
    A representation of Point interface with 2 axis
    """
    def __init__(self, x_, y_):
        super().__init__()
        self.x_axis = x_
        self.y_axis = y_

    def __eq__(self, other):
        """Overrides the default behaviour"""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        """Overrides the default behaviour"""
        return not self.__eq__(other)

    def get_position(self):
        """
        Returns (x, y)
        """
        return (self.x_axis, self.y_axis)

    def get_x_axis(self):
        """
        Returns the x axis
        """
        return self.x_axis

    def get_y_axis(self):
        """
        Returns the y axis
        """
        return self.y_axis

    def set_x_axis(self, x_axis):
        """
        Sets the x axis
        """
        self.x_axis = x_axis

    def set_y_axis(self, y_axis):
        """
        Sets the y axis
        """
        self.y_axis = y_axis

class Point3D(Point2D):
    """
    A representation of Point interface with 3 axis
    """
    def __init__(self, x_, y_, z_):
        super().__init__(x_, y_)
        self.z_axis = z_

    def __eq__(self, other):
        """Overrides the default behaviour"""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        """Overrides the default behaviour"""
        return not self.__eq__(other)

    def get_position(self):
        """
        Returns (x, y, z)
        """
        return (self.x_axis, self.y_axis, self.z_axis)

    def get_z_axis(self):
        """
        Returns the z axis
        """
        return self.z_axis

    def set_z_axis(self, z_axis):
        """
        Sets the z axis
        """
        self.z_axis = z_axis

class Pose(object):
    """
    Holds the position and the orientation of the robot
    """
    def __init__(self, position: Point, orientation):
        self.position = position
        self.orientation = orientation


    def move(self, vector: Vector2D):
        if self.get_representation_type() == REPR_2D:
            assert isinstance(vector, Vector2D)
            assert vector.start_point.get_position() == (0, 0)
            e_xy = vector.end_point.get_position()
            new_xy = tuple(map(sum, zip(e_xy, self.get_position())))
            self.set_position(Point2D(*new_xy))
        else:
            raise NotImplementedError

    def set_orientation(self, orientation):
        """
        Sets the orientation
        """
        self.orientation = orientation

    def set_position(self, position: Point):
        """
        Sets the position
        """
        self.position = position

    def get_position(self):
        """
        Returns the position as a tuple (x, y) for 2D point (x, y, z) for 3D point
        """
        return self.position.get_position()

    def get_orientation(self):
        """
        Returns the orientation
        """
        return self.orientation

    def get_representation_type(self):
        """
        Returns the representation type of the pose.
        REPR_2D, REPR_2D or REPR_UNKNOWN according to point type
        """
        if isinstance(self.position, Point3D):
            return REPR_3D
        elif isinstance(self.position, Point2D):
            return REPR_2D
        else:
            return REPR_UNKNOWN
