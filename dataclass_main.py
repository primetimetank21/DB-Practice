"""
This script practices using SQLAlchemy with dataclasses
"""
from dataclasses import dataclass, field
import os
import random
from typing import Any
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


@dataclass
class DataBase:
    """
    base: Base
    name: str
    engine: Engine
    session: Session
    """

    name: str = field(repr=True)
    engine: Any = field(init=False, repr=False)
    session: Any = field(init=False, repr=False)
    path: str = field(init=False, repr=False)
    base: Any = field(default=declarative_base(), repr=False)
    cur_dir: str = field(default=os.path.abspath(os.path.curdir), repr=False)

    def __post_init__(self) -> None:
        self.path = os.path.join(self.cur_dir, self.name)
        self.engine = create_engine(f"sqlite:///{self.path}")
        Session = sessionmaker(bind=self.engine)  # pylint: disable=invalid-name
        self.session = Session()

    def instantiate_db(self) -> None:
        """
        Create database
        """
        self.base.metadata.create_all(bind=self.engine)


@dataclass
class Vehicle(DataBase.base):
    """
    id: int
    model: str
    year: int
    """

    __tablename__ = "vehicles"
    id: int = Column("id", Integer, primary_key=True)  # pylint: disable=invalid-name
    model: str = Column("model", String)
    year: int = Column("year", Integer)


@dataclass
class Boat(DataBase.base):
    """
    id: int
    model: str
    year: int
    """

    __tablename__ = "boats"
    id: int = Column("id", Integer, primary_key=True)  # pylint: disable=invalid-name
    model: str = Column("model", String)
    year: int = Column("year", Integer)


def main() -> None:
    """
    Driver code for script
    """
    db = DataBase("vehicles.db")  # pylint: disable=invalid-name
    print(db)
    db.instantiate_db()

    vehicles = [
        Vehicle(model="Ferrari", year=random.randint(1970, 2022)),
        Vehicle(model="Harley", year=random.randint(1970, 2022)),
        Vehicle(model="Tesla", year=random.randint(1970, 2022)),
        Vehicle(model="Honda", year=random.randint(1970, 2022)),
    ]

    db.session.add_all(vehicles)
    db.session.commit()

    vehicle_query = db.session.query(Vehicle).all()

    for vehicle in vehicle_query:
        print(vehicle)

    boats = [
        Boat(model="boat1", year=random.randint(1970, 2022)),
        Boat(model="boat2", year=random.randint(1970, 2022)),
        Boat(model="boat3", year=random.randint(1970, 2022)),
        Boat(model="boat4", year=random.randint(1970, 2022)),
    ]

    db.session.add_all(boats)
    db.session.commit()

    boat_query = db.session.query(Boat).all()

    for boat in boat_query:
        print(boat)


if __name__ == "__main__":
    main()
