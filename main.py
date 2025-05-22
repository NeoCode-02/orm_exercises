from sqlalchemy import create_engine, String, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from datetime import datetime
from typing import Optional, List
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env")
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

class Base(DeclarativeBase):
    pass

class Student(Base):
    __tablename__ = "student"
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(25), nullable=False)
    second_name: Mapped[str] = mapped_column(String(25), nullable=False)
    age: Mapped[Optional[int]] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    def __repr__(self):
        return f"Student(id={self.id}, first_name={self.first_name}, second_name={self.second_name})"

class Professor(Base):  
    __tablename__ = "professor"  
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(25), nullable=False)
    second_name: Mapped[str] = mapped_column(String(25), nullable=False)
    teaching_subjects: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    
    courses: Mapped[List["Course"]] = relationship(back_populates="professor")

    def __repr__(self):
        return f"Professor(id={self.id}, first_name={self.first_name}, second_name={self.second_name})"

class Course(Base):
    __tablename__ = "course"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    professor_id: Mapped[Optional[int]] = mapped_column(ForeignKey('professor.id'))
    professor_name: Mapped[str] = mapped_column(String(50))  
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey('category.id'))
    
    professor: Mapped[Optional[Professor]] = relationship(back_populates="courses")
    # category: Mapped[Optional[Category]] = relationship(back_populates="courses")
    
    def __repr__(self):
        return f"Course(id={self.id}, name={self.name})"

class Category(Base):
    __tablename__ = "category"
    id: Mapped[int] = mapped_column(primary_key=True)
    category_name: Mapped[str] = mapped_column(String(25))
    price: Mapped[int] = mapped_column(Integer)
 
    courses: Mapped[List["Course"]] = relationship(back_populates="category")
    def __repr__(self):
        return f"Category(id={self.id}, category_name={self.category_name}, price={self.price})"
    

def insert_sample_data():
    with SessionLocal() as session:
        # Check if data already exists
        if session.query(Student).count() > 0:
            print("Sample data already exists. Skipping insertion.")
            return

        # Insert students
        students = [
            Student(first_name="John", second_name="Doe", age=20),
            Student(first_name="Jane", second_name="Smith", age=21),
            Student(first_name="Michael", second_name="Johnson", age=22),
            Student(first_name="Emily", second_name="Williams", age=19),
            Student(first_name="David", second_name="Brown", age=20)
        ]
        session.add_all(students)

        # Insert professors
        professors = [
            Professor(first_name="Robert", second_name="Sam", teaching_subjects="Mathematics"),
            Professor(first_name="Sarah", second_name="Davis", teaching_subjects="Physics"),
            Professor(first_name="James", second_name="Wilson", teaching_subjects="Computer Science"),
            Professor(first_name="Jennifer", second_name="Taylor", teaching_subjects="Biology"),
            Professor(first_name="Thomas", second_name="Anderson", teaching_subjects="History")
        ]
        session.add_all(professors)

        # Insert courses
        courses = [
            Course(name="Introduction to Calculus", professor_name="Robert Sam"),
            Course(name="Physics 101", professor_name="Sarah Davis"),
            Course(name="Computer Programming", professor_name="James Wilson"),
            Course(name="Biology Fundamentals", professor_name="Jennifer Taylor"),
            Course(name="World History", professor_name="Thomas Anderson")
        ]
        session.add_all(courses)

        # Insert categories
        categories = [
            Category(category_name="Mathematics", price=100),
            Category(category_name="Science", price=120),
            Category(category_name="Technology", price=150),
            Category(category_name="Humanities", price=80),
            Category(category_name="Social Sciences", price=90)
        ]
        session.add_all(categories)

        session.commit()
        print("Successfully inserted sample data!")

def update_records():
    with SessionLocal() as session:
        # Update 2 students
        student1 = session.query(Student).filter_by(first_name="John").first()
        if student1:
            student1.age = 21
            student1.second_name = "Updated"

        student2 = session.query(Student).filter_by(first_name="Jane").first()
        if student2:
            student2.age = 22
            student2.first_name = "Janet"

        # Update 2 professors
        prof1 = session.query(Professor).filter_by(first_name="Robert").first()
        if prof1:
            prof1.teaching_subjects = "Advanced Mathematics"

        prof2 = session.query(Professor).filter_by(first_name="Sarah").first()
        if prof2:
            prof2.teaching_subjects = "Advanced Physics"

        # Update 2 courses
        course1 = session.query(Course).filter_by(name="Introduction to Calculus").first()
        if course1:
            course1.name = "Advanced Calculus"

        course2 = session.query(Course).filter_by(name="Physics 101").first()
        if course2:
            course2.name = "Advanced Physics"

        # Update 2 categories
        cat1 = session.query(Category).filter_by(category_name="Mathematics").first()
        if cat1:
            cat1.price = 150

        cat2 = session.query(Category).filter_by(category_name="Science").first()
        if cat2:
            cat2.price = 180

        session.commit()
        print("Successfully updated records!")

def delete_records():
    with SessionLocal() as session:
        # Delete 1 student
        student = session.query(Student).filter_by(first_name="Michael").first()
        if student:
            session.delete(student)

        # Delete 1 professor
        professor = session.query(Professor).filter_by(first_name="James").first()
        if professor:
            session.delete(professor)

        # Delete 1 course
        course = session.query(Course).filter_by(name="Computer Programming").first()
        if course:
            session.delete(course)

        # Delete 1 category
        category = session.query(Category).filter_by(category_name="Technology").first()
        if category:
            session.delete(category)

        session.commit()
        print("Successfully deleted records!")

def view_all_data():
    with SessionLocal() as session:
        print("\nStudents:")
        for student in session.query(Student).all():
            print(student)

        print("\nProfessors:")
        for professor in session.query(Professor).all():
            print(professor)

        print("\nCourses:")
        for course in session.query(Course).all():
            print(course)

        print("\nCategories:")
        for category in session.query(Category).all():
            print(category)

if __name__ == "__main__":
    # First, insert the sample data
    insert_sample_data()
    
    # View initial data
    print("\nInitial data:")
    view_all_data()
    
    # Update records
    update_records()
    
    # View data after updates
    print("\nData after updates:")
    view_all_data()
    
    # Delete records
    delete_records()
    
    # View final data
    print("\nFinal data after deletions:")
    view_all_data()



