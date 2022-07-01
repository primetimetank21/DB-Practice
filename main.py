"""
This script serves as practice with SQLAlchemy
"""
import os
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData
import names

# import uuid


def main() -> None:
    """
    Drives the script
    """
    cur_dir = os.path.abspath(os.path.curdir)
    db_path = os.path.join(cur_dir, "students.db")
    engine = create_engine(f"sqlite:///{db_path}", echo=True)
    conn = engine.connect()

    meta = MetaData()

    students = Table(
        "students",
        meta,
        Column("id", Integer, primary_key=True),
        Column("name", String),
        Column("lastname", String),
    )
    meta.create_all(bind=engine)

    for _ in range(5):
        name = names.get_first_name()
        last_name = names.get_last_name()
        query = students.insert().values(name=name, lastname=last_name)
        conn.execute(query)

    query = students.select().where(students.c.id <= 10)
    result = conn.execute(query)

    for student in result:
        print(student)


if __name__ == "__main__":
    main()
