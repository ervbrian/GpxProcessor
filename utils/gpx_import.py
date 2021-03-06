import os
import xml.etree.ElementTree as ET

from cached_property import cached_property
from xml.etree.cElementTree import Element
from os import PathLike
from typing import List

from utils.exceptions import ParseError
from utils.hike import Point, Segment, Hike
from utils.namespaces import TRK_ELEMENT, TRKSEG_ELEMENT, TRKPT_ELEMENT, ELE_ELEMENT, TIME_ELEMENT, EXTENSIONS_ELEMENT, GARMIN_EXTENSIONS_ELEMENT


LAT = "lat"
LON = "lon"
HR = "hr"


class GpxImport:
    """
    Class used to parse GPX files and import coordinate point details.
    Point, Segment and Hike objects are generated based on imported coordinates.
    """

    def __init__(self, filename):
        self.tree = self.import_gpx(filename)
        self.name = os.path.basename(filename)
        self.coordinates = self._populate_coordinates()

    @staticmethod
    def import_gpx(filename: PathLike):
        try:
            return ET.parse(filename)
        except Exception as e:
            raise ParseError(f"GPX file {filename} could not be parsed. {e}")

    def fetch_heart_rate_extension(self, trkpt: Element) -> int:
        try:
            for gpx_extension in trkpt.findall(EXTENSIONS_ELEMENT):
                for garmin_extension in gpx_extension.findall(f"{GARMIN_EXTENSIONS_ELEMENT}TrackPointExtension"):
                    heart_rate = garmin_extension.find(f"{GARMIN_EXTENSIONS_ELEMENT}hr").text
        except AttributeError:  # heart rate extension not present
            heart_rate = 0

        return int(heart_rate)

    def _populate_coordinates(self) -> List[Point]:
        """
        Walk XML tree and fetch coordinate details logged as trkpt elements.
        Create Point object for each coordinate and append to coordinates list.
        """
        points = []
        for trk in self.tree.findall(TRK_ELEMENT):
            for trkseg in trk.findall(TRKSEG_ELEMENT):
                for trkpt in trkseg.findall(TRKPT_ELEMENT):
                    lat = float(trkpt.attrib.get(LAT))
                    lon = float(trkpt.attrib.get(LON))
                    elevation = float(trkpt.find(ELE_ELEMENT).text)
                    time = trkpt.find(TIME_ELEMENT).text.replace("Z", "+00:00")
                    heart_rate = self.fetch_heart_rate_extension(trkpt)
                    points.append(Point(lat=lat, lon=lon, elevation=elevation, time=time, heart_rate=heart_rate))

        return points

    @cached_property
    def segment(self):
        return Segment(points=self.coordinates)

    @cached_property
    def hike(self):
        return Hike(name=self.name, segments=[self.segment])
