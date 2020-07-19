from cached_property import cached_property
from datetime import datetime
from math import sin, cos, sqrt, radians, asin
from typing import List


class Point:
    """ Class used to store coordinate point details
    """

    def __init__(self, lat: float, lon: float, elevation: float, time: str, heart_rate: int):
        self.lat = lat
        self.lon = lon
        self.elevation = elevation
        self.time = time
        self.distance_from_start = 0
        self.heart_rate = heart_rate

    def update_distance_from_start(self, distance: float):
        self.distance_from_start = distance


class Segment:
    """ Class used to group Points objects.
    Distance, ascent, descent, duration and speed calculations are made here.
    """

    def __init__(self, points: List[Point]):
        self.points = points
        self.distance = 0
        self.ascent = 0
        self.descent = 0
        self.ascent_rates = []
        self._calc_statistics()

    @cached_property
    def point_count(self):
        return len(self.points)

    @cached_property
    def duration(self):
        start = self.points[0].time
        end = self.points[-1].time
        elapsed = datetime.fromisoformat(end) - datetime.fromisoformat(start)
        return round(elapsed.seconds / 60)  # convert to minutes

    @cached_property
    def speed(self):
        return round(self.distance / self.duration * 60, 2)

    @cached_property
    def ascent_rate(self):
        average_rate = sum(self.ascent_rates) / len(self.ascent_rates)
        return round(average_rate, 2)

    @cached_property
    def average_heart_rate(self):
        heart_rates = []
        for point in self.points:
            heart_rates.append(point.heart_rate)
        average_rate = sum(heart_rates) / self.point_count

        return round(average_rate)

    def _calc_distance_between_points(self, point_a: Point, point_b: Point) -> None:
        # https://www.geeksforgeeks.org/program-distance-two-points-earth/
        # radians converts from degrees to radians.
        lon1 = radians(point_a.lon)
        lon2 = radians(point_b.lon)
        lat1 = radians(point_a.lat)
        lat2 = radians(point_b.lat)

        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2

        c = 2 * asin(sqrt(a))

        # Radius of earth in kilometers
        r = 6371

        # add result to distance
        self.distance += (c * r)

    def _calc_ascent_rate_between_points(self, point_a: Point, point_b: Point, elevation_delta: float) -> None:
        start = point_a.time
        end = point_b.time
        elapsed = datetime.fromisoformat(end) - datetime.fromisoformat(start)
        rate = elevation_delta / elapsed.seconds * 3600

        self.ascent_rates.append(rate)

    def _calc_elevation_change_between_points(self, point_a: Point, point_b: Point) -> None:
        if point_b.elevation == point_a.elevation:
            return

        elevation_delta = point_b.elevation - point_a.elevation
        if point_b.elevation > point_a.elevation:
            self.ascent += elevation_delta
            self._calc_ascent_rate_between_points(point_a, point_b, elevation_delta)
        else:
            self.descent += elevation_delta

    def _calc_statistics(self) -> None:
        for i in range(self.point_count - 1):
            self.points[i].update_distance_from_start(self.distance)
            self._calc_distance_between_points(self.points[i], self.points[i+1])
            self._calc_elevation_change_between_points(self.points[i], self.points[i+1])


class Hike:
    """ Class used to group Segments.
    Distance, ascent, descent, duration and speed values for Segments are combined
    to calculate an average for the entire hike.
    """

    def __init__(self, name: str, segments: List[Segment]):
        self.name = name
        self.segments = segments

    @cached_property
    def segment_count(self):
        return len(self.segments)

    @cached_property
    def distance(self):
        return round(sum([segment.distance for segment in self.segments]), 2)

    @cached_property
    def ascent(self):
        return round(sum([segment.ascent for segment in self.segments]), 2)

    @cached_property
    def descent(self):
        return round(sum([segment.descent for segment in self.segments]), 2)

    @cached_property
    def duration(self):
        return sum([segment.duration for segment in self.segments])

    @cached_property
    def speed(self):
        return sum([segment.speed for segment in self.segments]) / self.segment_count

    @cached_property
    def ascent_rate(self):
        average_rate = sum([segment.ascent_rate for segment in self.segments]) / self.segment_count
        return round(average_rate, 2)

    @cached_property
    def average_heart_rate(self):
        average_rate = sum(segment.average_heart_rate for segment in self.segments) / self.segment_count
        return round(average_rate)
