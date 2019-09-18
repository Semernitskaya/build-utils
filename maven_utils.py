import os

PROVIDED_SCOPE = "provided"


def generate_maven_dependency_from_str(artifact_str, version=None, scope=PROVIDED_SCOPE):
    split = artifact_str.split(":")
    if version is None:
        version = split[3]
    return generate_maven_dependency(split[0], split[1], version, scope)


def generate_maven_dependency(group_id, artifact_id, version, scope=PROVIDED_SCOPE):
    return """          <dependency>
                <groupId>{}</groupId>
                <artifactId>{}</artifactId>
                <version>{}</version>
                <scope>{}</scope>
            </dependency>""".format(group_id, artifact_id, version, scope)


def is_test_dependency(split: []):
    return split.__len__() >= 5 and split[4] == "test"


def write_maven_dependency_tree(mvn_path, project_pom_path, tree_file_path="/tmp/dependencies.txt", dry_run=True):
    if os.path.exists(tree_file_path):
        os.remove(tree_file_path)
        print('File {} was removed'.format(tree_file_path))
    cmd = "{} dependency:tree " \
          "-DoutputFile={} " \
          "-Dtokens=whitespace " \
          "-DappendOutput=true " \
          "-P discovery " \
          "-f {}".format(mvn_path, tree_file_path, project_pom_path)
    print(cmd)
    if not dry_run:
        os.system(cmd)
    return tree_file_path
