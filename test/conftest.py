import pytest

from utils.hike import Point, Segment, Hike


@pytest.fixture(scope="session")
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


@pytest.fixture(scope="session")
def hike(segment):
    list_of_segments = [segment, segment, segment, segment, segment]
    return Hike(name="Test Hike", segments=list_of_segments)
