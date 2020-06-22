import os
import xml.etree.ElementTree as ET

from cached_property import cached_property

from utils.hike import Point, Segment, Hike

GPX_NAMESPACE = "{http://www.topografix.com/GPX/1/1}"
TRK_ELEMENT = f"{GPX_NAMESPACE}trk"
TRKSEG_ELEMENT = f"{GPX_NAMESPACE}trkseg"
TRKPT_ELEMENT = f"{GPX_NAMESPACE}trkpt"
ELE_ELEMENT = f"{GPX_NAMESPACE}ele"
TIME_ELEMENT = f"{GPX_NAMESPACE}time"
LAT = "lat"
LON = "lon"


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
    def import_gpx(filename):
        return ET.parse(filename)

    def _populate_coordinates(self):
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
                    points.append(Point(lat=lat, lon=lon, elevation=elevation, time=time))

        return points

    @cached_property
    def segment(self):
        return Segment(points=self.coordinates)

    @cached_property
    def hike(self):
        return Hike(name=self.name, segments=[self.segment])
