import pytest
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker

from utils.backend import HikeDBClient, update_db, serialize_points, deserialize_points, CoordinatesDB
from utils.hike import Point, Segment, Hike


database = "sqlite://"
Base: DeclarativeMeta = declarative_base()
ENGINE = create_engine(database, echo=False)
Session = sessionmaker(bind=ENGINE)
client = HikeDBClient(engine=ENGINE, session=Session, test=True)


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


def test_update_db(hike):
    update_db(client=client, hikes=[hike])
    assert client.entry_count == 1


def test_coordinate_point_entry(hike):
    for point in client.show_all_points_for_hike(name=hike.name):
        assert isinstance(point, CoordinatesDB)


def test_hike_populated(hike):
    assert client.hike_populated(name=hike.name) == True
    assert client.hike_populated(name="undefined_hike") == False


def test_serialize_points(hike):
    serialized = serialize_points(hike=hike)
    assert len(serialized) == 15

    for point in serialized:
        assert isinstance(point, bytes)


def test_deserialize_points(hike):
    deserialized = deserialize_points(client=client, hike_name=hike.name)
    assert len(deserialized) == 15

    for point in deserialized:
        assert isinstance(point, Point)


def filter_populated_hikes(hike):
    new_hike = "new hike"
    assert client.filter_populated_hikes(file_list=[hike.name, new_hike]) == [new_hike]
