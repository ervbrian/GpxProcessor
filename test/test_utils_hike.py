import pytest

from utils.hike import Point, Segment, Hike


@pytest.fixture(scope="module")
def segment():
    point1 = Point(lat=53.32055555555556,
                   lon=-1.7297222222222221,
                   elevation=0,
                   time="2017-06-25T14:17:48+00:00",
                   heart_rate=150)

    point2 = Point(lat=53.31861111111111,
                   lon=-1.6997222222222223,
                   elevation=500,
                   time="2017-06-25T15:17:48+00:00",
                   heart_rate=165)

    point3 = Point(lat=53.41861111111111,
                   lon=-1.6947222222222223,
                   elevation=200,
                   time="2017-06-25T15:34:48+00:00",
                   heart_rate=160)

    return Segment(points=[point1, point2, point3])


@pytest.fixture(scope="module")
def hike(segment):
    list_of_segments = [segment, segment, segment, segment, segment]
    return Hike(name="Test Hike", segments=list_of_segments)


def test_segment_distance_calculation(segment):
    assert segment.distance == 13.12880768852734


def test_segment_speed_calculation(segment):
    assert segment.speed == 10.23


def test_segment_elevation_calculation(segment):
    assert segment.ascent == 500
    assert segment.descent == -300


def test_segment_duration_calculation(segment):
    assert segment.duration == 77


def test_segment_ascent_rate_calculation(segment):
    assert segment.ascent_rate == 500


def test_segment_heart_rate_calculation(segment):
    assert segment.average_heart_rate == 158


def test_hike_distance_calculation(hike):
    assert hike.distance == 65.64


def test_hike_elevation_calculation(hike):
    assert hike.ascent == 2500
    assert hike.descent == -1500


def test_hike_duration_calculation(hike):
    assert hike.duration == 385


def test_hike_speed_calculation(hike):
    assert hike.speed == 10.23


def test_hike_ascent_rate_calculation(hike):
    assert hike.ascent_rate == 500


def test_hike_heart_rate_calculation(hike):
    assert hike.average_heart_rate == 158
