import argparse

from build.utils.file_utils import *

FORMAT_STR = "{:40}, {:40}, {:40}"


def find_versions_diff(common_jars: list, jars_file_1: set, jars_file_2: set):
    versions_diff = dict()
    for jar in common_jars:
        version_1 = leave_jar_version(jars_file_1[jar])
        version_2 = leave_jar_version(jars_file_2[jar])
        if version_1 != version_2:
            versions_diff[jar] = (version_1, version_2)
    return versions_diff


def print_header():
    print(FORMAT_STR.format("jar name", "version in file 1", "version in file 2"))


parser = argparse.ArgumentParser(
    description='Compare dependencies from two different war-files')
parser.add_argument('--f1', required=True, help='File 1 path')
parser.add_argument('--f2', required=True, help='File 2 path')

args = parser.parse_args()
assert_file_exists(args.f1)
assert_file_exists(args.f2)

jars_file_1 = get_jars(args.f1)
jars_file_2 = get_jars(args.f2)

jars_file_1_set = set(jars_file_1.keys())
jars_file_2_set = set(jars_file_2.keys())

common_jars = list(jars_file_1_set.intersection(jars_file_2_set))
only_file_1 = list(jars_file_1_set - jars_file_2_set)
only_file_2 = list(jars_file_2_set - jars_file_1_set)

only_file_1.sort()
only_file_2.sort()
common_jars.sort()
print("common jars {}, only in file 1 {}, only in file 2 {}"
      .format(len(common_jars), len(only_file_1), len(only_file_2)))

versions_diff = find_versions_diff(common_jars, jars_file_1, jars_file_2)

print(os.linesep + "version difference")

print_header()
for k, v in versions_diff.items():
    print(FORMAT_STR.format(k, v[0], v[1]))

print(os.linesep + "exist only in file 1")
print_header()
for jar in only_file_1:
    print(FORMAT_STR.format(jar, leave_jar_version(jars_file_1[jar]), "-"))

print(os.linesep + "exist only in file 2")
print_header()
for jar in only_file_2:
    print(FORMAT_STR.format(jar, "-", leave_jar_version(jars_file_2[jar])))
