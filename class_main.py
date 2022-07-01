"""
This script does ...
"""
import os
from dataclasses import dataclass
from random import randint, choice
from sqlalchemy import Column, Integer, Boolean, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import names

cur_dir = os.path.abspath(os.path.curdir)
db_path = f'sqlite:///{os.path.join(cur_dir, "animals.db")}'
engine = create_engine(db_path)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


@dataclass
class Pet(Base):
    """
    Pet objects to be held in the database
    """

    __tablename__ = "pets"
    id: int = Column("id", Integer, primary_key=True)  # pylint: disable=invalid-name
    name: str = Column("name", String)
    age: int = Column("age", Integer)


@dataclass
class WildAnimal(Base):
    """
    Wild animal objects to be held in the database
    """

    __tablename__ = "wild_animals"
    id: int = Column("id", Integer, primary_key=True)  # pylint: disable=invalid-name
    species: str = Column("species", String)
    endangered: bool = Column("endangered", Boolean)


def main() -> None:
    """
    Driver code
    """

    # conn = engine.connect()

    pets = []
    for _ in range(10):
        pets.append(Pet(name=names.get_first_name(), age=randint(1, 15)))
    session.add_all(pets)
    print(session.new)
    session.rollback()
    session.commit()

    result = session.query(Pet).all()
    print("All:")
    for pet in result:
        print(pet)

    old_pets = session.query(Pet).filter(Pet.age >= 5)
    print("Old:")
    for pet in old_pets:
        print(pet)

    wild_animals = []
    for _ in range(15):
        species = choice(["boar", "frog", "horse", "rabit"])
        endangered = choice([True, False])
        wild_animals.append(WildAnimal(species=species, endangered=endangered))

    session.add_all(wild_animals)
    session.commit()

    print("Wild animals:")
    all_wild_animals = session.query(WildAnimal).all()
    for animal in all_wild_animals:
        print(animal)


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    main()
