import argparse
from utils import *
from maven_utils import *

DIFFERENT_PLATFORM_VERSION_STR = "different platform version"
DIFFERENT_VERSION_STR = "!!! different version"
SAME_VERSION_STR = "same version"
NOT_FOUND_STR = "not found in overlays"

VERSION_STR_TEMPLATE = " artifact {:100}, artifact_version {:15}, overlays_version {:15} line_number: {:3}"

parser = argparse.ArgumentParser(
    description='Compare overlays from Jboss/Wildfly standalone.xml and dependencies from dependency tree')
parser.add_argument('--pom', required=True, help='project pom path')
parser.add_argument('--mvn', required=True, help='maven command path')
parser.add_argument('--xml', required=True, help='jboss/wildfly standalone.xml path')
parser.add_argument('--platform_version', help='platform dependencies version')
parser.add_argument('--print_skipped',
                    type=lambda s: s.lower() == str(True).lower(),
                    default=True,
                    help='defines whether to print dependencies skipped in generate_provided_dependencies')

args = parser.parse_args()
assert_file_exists(args.pom)
assert_file_exists(args.xml)


def print_grouped_results(results, printed_head=None):
    previous_artifact = ""
    for result_tuple in results:
        message = result_tuple[0]
        artifact = result_tuple[1]
        if printed_head is None or message.startswith(printed_head):
            if artifact != previous_artifact and previous_artifact.__len__() != 0:
                print()
            previous_artifact = artifact
            print(message)


def generate_provided_dependencies(results, print_skipped):
    previous_artifact = ""
    skipped = []
    for result_tuple in results:
        message = result_tuple[0]
        artifact = result_tuple[1]
        if previous_artifact == artifact:
            continue
        else:
            previous_artifact = artifact

        if NOT_FOUND_STR in message or ":" + PROVIDED_SCOPE in message:
            skipped.append(message)
            continue
        elif (SAME_VERSION_STR in message) or (DIFFERENT_VERSION_STR in message):
            print(generate_maven_dependency_from_str(artifact))
        elif DIFFERENT_PLATFORM_VERSION_STR in message:
            print(generate_maven_dependency_from_str(artifact, "${platform.version}"))
        else:
            skipped.append(message)

    if print_skipped:
        for skip in skipped:
            print("skipped " + skip)


tree_file_path = write_maven_dependency_tree(args.mvn, args.pom, dry_run=False)
overlays = read_overlays(args.xml)

results = []
with open(tree_file_path) as fp:
    for line_number, artifact in enumerate(fp):
        artifact = artifact.strip()
        split = artifact.split(":")

        artifact_key = (split[0] + "-" + split[1]).replace(".", "-")
        artifact_version = split[3]
        overlays_version = overlays.get(artifact_key)

        if is_test_dependency(split):
            continue
        version_str = VERSION_STR_TEMPLATE.format(artifact, artifact_version, to_str(overlays_version), line_number)
        if overlays_version is None:
            results.append((NOT_FOUND_STR + version_str, artifact))
        elif overlays_version == artifact_version:
            results.append((SAME_VERSION_STR + version_str, artifact))
        elif args.platform_version is not None and args.platform_version in overlays_version:
            results.append((DIFFERENT_PLATFORM_VERSION_STR + version_str, artifact))
        else:
            results.append((DIFFERENT_VERSION_STR + version_str, artifact))
results.sort()
print_grouped_results(results, DIFFERENT_VERSION_STR)
generate_provided_dependencies(results, args.print_skipped)
