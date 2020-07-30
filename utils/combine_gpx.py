import xml.etree.ElementTree as ET
from os import PathLike
from typing import List
from xml.etree.ElementTree import ElementTree

from utils.namespaces import TRK_ELEMENT


class CombineGpx:
    def __init__(self, gpx_files: List[PathLike]):
        self.gpx_files = gpx_files
        self.roots = self.get_roots()
        self.combined = self.combine()

    def get_roots(self) -> List[ElementTree]:
        return [ET.parse(filename).getroot() for filename in self.gpx_files]

    def _combine_tracks(self, first: ElementTree, second: ElementTree):
        """
        Append trk of first root to the second root
        """
        first.append(second.find(TRK_ELEMENT))
        self.roots[0] = first

    def combine(self) -> ElementTree:
        for root in self.roots[1:]:
            self._combine_tracks(self.roots[0], root)
        return ET.tostring(self.roots[0], encoding="utf-8")

    def write_to_file(self, filename):
        with open(filename, "w") as f:
            f.write(self.combined.decode("utf-8"))
