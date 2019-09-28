import argparse
from typing import Dict, Any

from utils import *

YAML_EXTENSION = ".yaml"

COMMENT_START = "#"


class Property:

    def __init__(self, value, names: list):
        self.value = value
        self.names = names

    def __init__(self, line: str):
        split = line.split("=")
        self.value = re.sub("[\r\n]+", "", split[1])
        self.names = split[0].split(".")

    def is_valid_property(line: str):
        return re.match("[^\s]+=.*", line)

    def is_comment_property(line: str):
        return line.startswith(COMMENT_START)


class Node:
    sub_nodes: Dict[Any, Any]

    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.sub_nodes = dict()

    def add_prop(self, prop: Property):
        self.add(prop.value, prop.names)

    def add(self, value, names: list):
        if names.__len__() == 0:
            self.value = value
        else:
            sub_node = self.sub_nodes.get(names[0])
            if sub_node is None:
                sub_node = Node(names[0])
                self.sub_nodes[names[0]] = sub_node
            sub_node.add(value, names[1:])

    def is_root(self):
        return self.key is None

    def print_as_yaml(self, offset: int, file):
        offset_str = "  " * offset
        if self.sub_nodes.__len__() == 0:
            print((offset_str + "{}: {}").format(self.key, self.value), file=file)
        else:
            if not self.is_root():
                print((offset_str + "{}:").format(self.key), file=file)
                offset = offset + 1
            for node in self.sub_nodes.values():
                node.print_as_yaml(offset, file)


parser = argparse.ArgumentParser(
    description='Convert properties-file to yaml-file')
parser.add_argument('--f', required=True, help='Properties file path')

args = parser.parse_args()
properties_file = args.f
name, extension = os.path.splitext(properties_file)
yaml_file = name + YAML_EXTENSION

root_node = Node()
with open(properties_file) as fp:
    for line_number, line in enumerate(fp):
        if line.strip().__len__() == 0 or Property.is_comment_property(line):
            continue
        elif Property.is_valid_property(line):
            root_node.add_prop(Property(line))
        else:
            print("Incorrect property, skipped, line number {}, line [{}]".format(line_number, line))

with open(yaml_file, 'w') as f:
    root_node.print_as_yaml(0, f)
