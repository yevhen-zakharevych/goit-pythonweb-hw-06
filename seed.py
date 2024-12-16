import random
from faker import Faker
from datetime import date, timedelta
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base, Student, Group, Teacher, Subject, Grade

DATABASE_URL = "postgresql://postgres:1234@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()


def random_date(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)


def seed_database():
    try:
        groups = [Group(name=f"Group {i}") for i in range(1, 4)]
        session.add_all(groups)
        session.commit()

        teachers = [Teacher(name=fake.name()) for _ in range(3)]
        session.add_all(teachers)
        session.commit()

        subjects = [Subject(name=fake.word().capitalize(), teacher_id=random.choice(teachers).id) for _ in range(5)]
        session.add_all(subjects)
        session.commit()

        students = [
            Student(name=fake.name(), group_id=random.choice(groups).id) for _ in range(30)
        ]
        session.add_all(students)
        session.commit()

        grades = []
        for student in students:
            for subject in subjects:
                for _ in range(random.randint(5, 20)):
                    grades.append(
                        Grade(
                            student_id=student.id,
                            subject_id=subject.id,
                            grade=round(random.uniform(60, 100), 2),
                            date_received=random_date(date(2024, 1, 1), date(2024, 12, 31)),
                        )
                    )
        session.add_all(grades)
        session.commit()

        print("Database seeded successfully!")

    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    seed_database()
