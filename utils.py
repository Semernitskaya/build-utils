import xml.etree.ElementTree as ET
from zipfile import ZipFile
import re


def to_str(s):
    return s or "None"


def read_overlays(file):
    overlays = {}
    tree = ET.parse(file)
    root = tree.getroot()
    for element in root.findall("deployment-overlays/deployment-overlay/content"):
        artifact = element.attrib['path']
        artifact = str(artifact) \
            .replace(".jar", "") \
            .replace("/WEB-INF/lib/", "")
        split = artifact.rsplit("-", 1)
        overlays[split[0]] = split[1]
    print("overlays: ", overlays)
    return overlays


def get_jars(path):
    jars = dict()
    with ZipFile(path, 'r') as zipObj:
        list_of_files = zipObj.namelist()
        path_prefix = "WEB-INF/lib/"
        for elem in list_of_files:
            if path_prefix in elem and elem != path_prefix:
                jar = elem.replace(path_prefix, "")
                jar_name = leave_jar_name(jar)
                jars[jar_name] = jar
    return jars


def leave_jar_name(jar):
    return re.sub("-\d.+", "", jar)
