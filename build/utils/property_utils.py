import re

COMMENT_START = "#"


class Property:

    def __init__(self, line: str = None, value: str = None, names: list = None):
        if line is None:
            self.value = value
            self.names = names
        else:
            split = line.split("=")
            self.value = re.sub("[\r\n]+", "", split[1])
            self.names = split[0].split(".")

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Property):
            return self.value == other.value and self.names == other.names
        return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def is_valid_property(line: str):
        return re.match("[^\s]+=.*", line)

    def is_comment_property(line: str):
        return line.startswith(COMMENT_START)
