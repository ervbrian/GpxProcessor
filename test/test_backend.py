import pytest
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker

from utils.backend import HikeDBClient, update_db, serialize_points, deserialize_points, CoordinatesDB
from utils.hike import Point


database = "sqlite://"
Base: DeclarativeMeta = declarative_base()
ENGINE = create_engine(database, echo=False)
Session = sessionmaker(bind=ENGINE)
client = HikeDBClient(engine=ENGINE, session=Session, test=True)


@pytest.mark.usefixtures("hike")
def test_update_db(hike):
    update_db(client=client, hikes=[hike])
    assert client.entry_count == 1


@pytest.mark.usefixtures("hike")
def test_coordinate_point_entry(hike):
    for point in client.show_all_points_for_hike(name=hike.name):
        assert isinstance(point, CoordinatesDB)


@pytest.mark.usefixtures("hike")
def test_hike_populated(hike):
    assert client.hike_populated(name=hike.name) == True
    assert client.hike_populated(name="undefined_hike") == False


@pytest.mark.usefixtures("hike")
def test_serialize_points(hike):
    serialized = serialize_points(hike=hike)
    assert len(serialized) == 15

    for point in serialized:
        assert isinstance(point, bytes)


@pytest.mark.usefixtures("hike")
def test_deserialize_points(hike):
    deserialized = deserialize_points(client=client, hike_name=hike.name)
    assert len(deserialized) == 15

    for point in deserialized:
        assert isinstance(point, Point)


@pytest.mark.usefixtures("hike")
def filter_populated_hikes(hike):
    new_hike = "new hike"
    assert client.filter_populated_hikes(file_list=[hike.name, new_hike]) == [new_hike]
