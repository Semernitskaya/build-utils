import argparse
import shutil

from utils import *


def include_dir(dir, dir_path):
    # skip .git etc
    if dir.startswith("."):
        return False
    # include only maven modules
    for file in os.listdir(dir_path):
        if file == "pom.xml":
            return True
    return False


def include_file(file):
    return ".git" not in file


parser = argparse.ArgumentParser(
    description='Copy Maven-project sources to the target directory, ignore target-directories, idea-configs etc')
parser.add_argument('--source', required=True, help='Source directory path')
parser.add_argument('--target', required=True, help='Target directory path')

args = parser.parse_args()
assert_dir_exists(args.source)

source_path = args.source
dest_path = args.target
if os.path.exists(dest_path):
    shutil.rmtree(dest_path)
    print('Dir {} was removed'.format(dest_path))

ignore = shutil.ignore_patterns('*.iml', '.git*', "target/")

for file in os.listdir(source_path):
    file_source_path = os.path.join(source_path, file)
    print("File ", file_source_path, file)
    if os.path.isfile(file_source_path):
        if include_file(file):
            shutil.copy2(file_source_path, dest_path)
    else:
        if include_dir(file, file_source_path):
            file_dest_path = os.path.join(dest_path, file)
            print("Copying directory ", file_source_path)
            shutil.copytree(file_source_path, file_dest_path, ignore=ignore)
        else:
            print("Skipping directory ", file_source_path)
