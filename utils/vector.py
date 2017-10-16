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

from robot_localization.utils.point import Point2D, Point
from math import sqrt

class Vector(object):
    """
    A Vector interface to provide essential functionalities
    and modularity to module
    """

    def get_start_point(self) -> Point:
        """
        Returns start point of the vector 
        """
        raise NotImplementedError

    def get_end_point(self) -> Point:
        """
        Returns end point of the vector
        """
        raise NotImplementedError

    def get_magnitude(self) -> float:
        """
        Returns the magnitude of the vector
        """
        raise NotImplementedError

class Vector2D(object):

    def __init__(self, start_point=Point2D(0, 0), end_point=Point2D(0, 0)):
        self.start_point = start_point
        self.end_point = end_point

    def get_start_point(self) -> Point2D:
        """
        Returns start point of the vector as Point2D instance
        """
        return self.start_point

    def get_end_point(self) -> Point2D:
        """
        Returns end point of the vector as Point2D instance
        """
        return self.end_point

    def get_magnitude(self) -> float:
        """
        Returns the magnitude of the vector
        """
        x_1, y_1 = self.get_start_point().get_position()
        x_2, y_2 = self.get_end_point().get_position()
        return sqrt(((x_2 - x_1) ** 2) + ((y_2 - y_1) ** 2))

UP = Vector2D(end_point=Point2D(1, 0))
DOWN = Vector2D(end_point=Point2D(-1, 0))
LEFT = Vector2D(end_point=Point2D(0, -1))
RIGHT = Vector2D(end_point=Point2D(0, 1))
