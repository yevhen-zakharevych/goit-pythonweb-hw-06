from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Group, Teacher, Subject, Student, Grade
import logging


logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

DATABASE_URL = "postgresql://postgres:1234@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


if __name__ == "__main__":
    try:
        with engine.connect() as connection:
            print("Connected to PostgreSQL!")

            all_students = session.query(Student).all()
            for s in all_students:
                print(f"Student: {s.name}, Group ID: {s.group_id}")

    except Exception as e:
        print(f"Error connecting to the database: {e}")
