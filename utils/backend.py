from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta  # type: ignore
from sqlalchemy import create_engine, Column, Integer, String, Float  # type: ignore
from sqlalchemy.orm import sessionmaker  # type: ignore
from sqlalchemy.orm.query import Query  # type: ignore
from typing import Any, List

from utils.hike import Hike  # type: ignore


database = "sqlite:///data/HikeDB.db"
Base: DeclarativeMeta = declarative_base()
engine = create_engine(database, echo=False)
Session = sessionmaker(bind=engine)


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


class HikeDBClient:
    """ Wrapper used to populate HikeDB tables.
    Tables are used to generate HTML report on hike statistics.
    """

    def __init__(self):
        Base.metadata.create_all(engine)
        self.session = Session()

    @property
    def entry_count(self) -> Any:
        return self.show_all_hikes().count()

    def add_all(self, hike_list: List[HikeDB]):
        self.session.add_all(hike_list)
        self.session.commit()

    def show_all_hikes(self) -> Query:
        return self.session.query(HikeDB).order_by(HikeDB.name.desc())

    def hike_populated(self, name: str) -> bool:
        return self.session.query(HikeDB).filter_by(name=name).scalar() is not None

    def filter_populated_hikes(self, file_list: List[str]) -> List[str]:
        return [filename for filename in file_list if not self.hike_populated(filename)]
