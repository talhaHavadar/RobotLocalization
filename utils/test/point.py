#pylint: disable-all
import unittest
from robot_localization.utils.point import Point2D, Point3D

class TestPoint(unittest.TestCase):

    def test_Point2D(self):
        print("\n[!] Point2D testing..")
        p = Point2D(5, 4)
        self.assertEqual(p.get_x_axis(), 5)
        self.assertEqual(p.get_y_axis(), 4)
        with self.assertRaises(NotImplementedError):
            p.get_z_axis()
            p.set_z_axis()
        self.assertEqual(p.get_position(), (5, 4))
        p.set_x_axis(0); self.assertEqual(p.get_x_axis(), 0)
        p.set_y_axis(0); self.assertEqual(p.get_y_axis(), 0)
        self.assertEqual(p.get_position(), (0, 0))
        print("[*] Test done")

    def test_Point3D(self):
        print("\n[!] Point3D testing..")
        p = Point3D(5, 4, 2)
        self.assertEqual(p.get_x_axis(), 5)
        self.assertEqual(p.get_y_axis(), 4)
        self.assertEqual(p.get_z_axis(), 2)
        self.assertEqual(p.get_position(), (5, 4, 2))
        p.set_x_axis(0); self.assertEqual(p.get_x_axis(), 0)
        p.set_y_axis(0); self.assertEqual(p.get_y_axis(), 0)
        p.set_z_axis(0); self.assertEqual(p.get_z_axis(), 0)
        self.assertEqual(p.get_position(), (0, 0, 0))
        print("[*] Test done")


if __name__ == '__main__':
    unittest.main()
