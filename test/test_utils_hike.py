import pytest

from utils.hike import Point, Segment, Hike


@pytest.fixture(scope="module")
def segment():
    point1 = Point(lat=53.32055555555556,
                   lon=-1.7297222222222221,
                   elevation=0,
                   time="2017-06-25T14:17:48Z")

    point2 = Point(lat=53.31861111111111,
                   lon=-1.6997222222222223,
                   elevation=500,
                   time="2017-06-25T15:17:48Z")

    return Segment(points=[point1, point2])


@pytest.fixture(scope="module")
def hike(segment):
    list_of_segments = [segment, segment, segment, segment, segment]
    return Hike(name="Test Hike", segments=list_of_segments)


def test_segment_distance_calculation(segment):
    assert segment.distance == 2.0043678382716137


def test_segment_speed_calculation(segment):
    assert segment.speed == 2.00


def test_segment_elevation_calculation(segment):
    assert segment.ascent == 500
    assert segment.descent == 0


def test_segment_duration_calculation(segment):
    assert segment.duration == 60


def test_hike_distance_calculation(hike):
    assert hike.distance == 10.02


def test_hike_elevation_calculation(hike):
    assert hike.ascent == 2500
    assert hike.descent == 0


def test_hike_duration_calculation(hike):
    assert hike.duration == 300
