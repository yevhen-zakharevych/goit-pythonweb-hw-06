from sqlalchemy.orm import Session
from sqlalchemy.sql import func, desc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Student, Grade, Subject, Group, Teacher

def select_1(session: Session):
    return session.query(
        Student.name, func.avg(Grade.grade).label("average_grade")
    ).join(Grade).group_by(Student.id).order_by(desc("average_grade")).limit(5).all()

def select_2(session: Session, subject_id: int):
    return session.query(
        Student.name, func.avg(Grade.grade).label("average_grade")
    ).join(Grade).filter(Grade.subject_id == subject_id).group_by(Student.id).order_by(desc("average_grade")).first()

def select_3(session: Session, subject_id: int):
    # Average grade in each group for a specific subject
    return session.query(
        Group.name, func.avg(Grade.grade).label("average_grade")
    ).join(Student, Student.group_id == Group.id).join(Grade, Grade.student_id == Student.id).filter(Grade.subject_id == subject_id).group_by(Group.id, Group.name).all()
def select_4(session: Session):
    return session.query(func.avg(Grade.grade)).scalar()

def select_5(session: Session, teacher_id: int):
    return session.query(Subject.name).filter(Subject.teacher_id == teacher_id).all()

def select_6(session: Session, group_id: int):
    return session.query(Student.name).filter(Student.group_id == group_id).all()

def select_7(session: Session, group_id: int, subject_id: int):
    return session.query(
        Student.name, Grade.grade, Grade.date_received
    ).join(Grade).filter(Student.group_id == group_id, Grade.subject_id == subject_id).all()

def select_8(session: Session, teacher_id: int):
    return session.query(
        func.avg(Grade.grade)
    ).join(Subject).filter(Subject.teacher_id == teacher_id).scalar()

def select_9(session: Session, student_id: int):
    return session.query(Subject.name).join(Grade).filter(Grade.student_id == student_id).distinct().all()

def select_10(session: Session, student_id: int, teacher_id: int):
    return session.query(Subject.name).join(Grade).filter(
        Grade.student_id == student_id, Subject.teacher_id == teacher_id
    ).distinct().all()


if __name__ == "__main__":
    DATABASE_URL = "postgresql://postgres:1234@localhost:5432/postgres"
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    print(select_1(session))
    print(select_2(session, 1))
    print(select_3(session, 2))
    print(select_4(session))
    print(select_5(session, 1))
    print(select_6(session, 1))
    print(select_7(session, 1, 1))
    print(select_8(session, 1))
    print(select_9(session, 1))
    print(select_10(session, 1, 1))