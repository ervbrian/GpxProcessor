import pickle

from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta  # type: ignore
from sqlalchemy import create_engine, Column, Integer, String, Float, Binary, LargeBinary  # type: ignore
from sqlalchemy.orm import sessionmaker  # type: ignore
from sqlalchemy.orm.query import Query  # type: ignore
from typing import Any, List

from utils.hike import Hike, Point  # type: ignore


database = "sqlite:///data/HikeDB.db"
Base: DeclarativeMeta = declarative_base()
ENGINE = create_engine(database, echo=False)
Session = sessionmaker(bind=ENGINE)


def serialize_points(hike: Hike) -> List[bytes]:
    serialized: List[bytes] = []
    for segment in hike.segments:
        serialized.extend([pickle.dumps(point) for point in segment.points])

    return serialized


def update_db(client, hikes: List[Hike]) -> None:
    """ Add a list of hike statistics to database

    :param client: HikeDBClient session object
    :param hikes: list of Hike objects
    :return: None
    """

    obj_list = []
    for hike in hikes:
        obj_list.append(HikeDB(name=hike.name,
                               distance=hike.distance,
                               ascent=hike.ascent,
                               descent=hike.descent,
                               duration=hike.duration,
                               speed=hike.speed,
                               ascent_rate=hike.ascent_rate,
                               average_heart_rate=hike.average_heart_rate))

        obj_list.extend([CoordinatesDB(point=point, hike_name=hike.name) for point in serialize_points(hike)])

    client.add_all(obj_list)


class HikeDB(Base):
    """ Model used to populate database with hikes table schema
    """
    __tablename__ = 'hikes'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    distance = Column(Float)
    ascent = Column(Float)
    descent = Column(Float)
    duration = Column(Float)
    speed = Column(Float)
    ascent_rate = Column(Float)
    average_heart_rate = Column(Integer)


class CoordinatesDB(Base):
    """ Model used to populate database with coordinates table schema
    """
    __tablename__ = 'coordinates'

    id = Column(Integer, primary_key=True)
    hike_name = Column(String)
    point = Column(LargeBinary)


class HikeDBClient:
    """ Wrapper used to populate HikeDB tables.
    Tables are used to generate HTML report on hike statistics.
    """

    def __init__(self, engine=None, session=None, test=False):
        if test:
            Base.metadata.create_all(engine)
            self.session = session()
        else:
            Base.metadata.create_all(ENGINE)
            self.session = Session()

    @property
    def entry_count(self) -> Any:
        return self.show_all_hikes().count()

    def add_all(self, hike_list: List[HikeDB]):
        self.session.add_all(hike_list)
        self.session.commit()

    def show_all_hikes(self) -> Query:
        return self.session.query(HikeDB).order_by(HikeDB.name.desc())

    def show_all_points_for_hike(self, name: str) -> Query:
        return self.session.query(CoordinatesDB).filter_by(hike_name=name)

    def hike_populated(self, name: str) -> bool:
        return self.session.query(HikeDB).filter_by(name=name).scalar() is not None

    def filter_populated_hikes(self, file_list: List[str]) -> List[str]:
        return [filename for filename in file_list if not self.hike_populated(filename)]


def deserialize_points(client: HikeDBClient, hike_name: str) -> List[Point]:
    return [pickle.loads(point.point) for point in client.show_all_points_for_hike(hike_name)]
