import unittest
from build.utils.file_utils import *


class TestPropertyUtils(unittest.TestCase):

    def test_leave_jar_name(self):
        self.assertEqual("", leave_jar_name(""))
        self.assertEqual("logback-classic", leave_jar_name("logback-classic-1.2.3.jar"))
        self.assertEqual("logback-classic", leave_jar_name("logback-classic.jar"))
        self.assertEqual("logback-classic-api", leave_jar_name("logback-classic-api.jar"))
        self.assertEqual("discovery-out-model", leave_jar_name("discovery-out-model-0.6-SNAPSHOT.jar"))

    def test_leave_jar_version(self):
        self.assertEqual("", leave_jar_name(""))
        self.assertEqual("1.2.3", leave_jar_version("logback-classic-1.2.3.jar"))
        self.assertEqual("", leave_jar_version("logback-classic.jar"))
        self.assertEqual("", leave_jar_version("logback-classic-api.jar"))
        self.assertEqual("0.6-SNAPSHOT", leave_jar_version("discovery-out-model-0.6-SNAPSHOT.jar"))


if __name__ == '__main__':
    unittest.main()
