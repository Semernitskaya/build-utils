import unittest
from build.utils.property_utils import *


class TestPropertyUtils(unittest.TestCase):

    def test_is_valid_property(self):
        self.assertTrue(Property.is_valid_property("a=val"))
        self.assertTrue(Property.is_valid_property("a.b.c=val"))
        self.assertTrue(Property.is_valid_property("a=b=c"))
        self.assertTrue(Property.is_valid_property("a=#val   "))
        self.assertFalse(Property.is_valid_property("  a=val  "))
        self.assertFalse(Property.is_valid_property("a  b=val  "))

    def test_is_comment_property(self):
        self.assertTrue(Property.is_comment_property("#"))
        self.assertTrue(Property.is_comment_property("# my comment"))
        self.assertFalse(Property.is_comment_property("a.b.c=val"))

    def test_create_from_line(self):
        self.assertEqual(Property(value="val", names=["a", "b", "c"]), Property(line="a.b.c=val"))
        self.assertEqual(Property(value="", names=["a", "b", "c"]), Property(line="a.b.c="))
        self.assertEqual(Property(value="val", names=["a"]), Property(line="a=val"))


if __name__ == '__main__':
    unittest.main()
