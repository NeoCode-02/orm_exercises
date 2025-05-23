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

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

class StudentCourse(Base):
    __tablename__ = "student_course"
    
    student_id: Mapped[int] = mapped_column(ForeignKey("student.id"), primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("course.id"), primary_key=True)
    enrollment_date: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    grade: Mapped[Optional[str]] = mapped_column(String(2))
    
    student: Mapped["Student"] = relationship(back_populates="course_associations")
    course: Mapped["Course"] = relationship(back_populates="student_associations")

class Student(Base):
    __tablename__ = "student"
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(25), nullable=False)
    second_name: Mapped[str] = mapped_column(String(25), nullable=False)
    age: Mapped[Optional[int]] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    
    course_associations: Mapped[List["StudentCourse"]] = relationship(
        back_populates="student",
        cascade="all, delete-orphan"
    )

class Professor(Base):  
    __tablename__ = "professor"  
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(25), nullable=False)
    second_name: Mapped[str] = mapped_column(String(25), nullable=False)
    teaching_subjects: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    
    courses: Mapped[List["Course"]] = relationship(back_populates="professor")

class Category(Base):
    __tablename__ = "category"
    id: Mapped[int] = mapped_column(primary_key=True)
    category_name: Mapped[str] = mapped_column(String(25))
    price: Mapped[int] = mapped_column(Integer)
 
    courses: Mapped[List["Course"]] = relationship(back_populates="category")

class Course(Base):
    __tablename__ = "course"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    professor_id: Mapped[Optional[int]] = mapped_column(ForeignKey('professor.id'))
    professor_name: Mapped[str] = mapped_column(String(50))  
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey('category.id'))
    
    professor: Mapped[Optional["Professor"]] = relationship(back_populates="courses")
    category: Mapped[Optional["Category"]] = relationship(back_populates="courses")
    student_associations: Mapped[List["StudentCourse"]] = relationship(
        back_populates="course",
        cascade="all, delete-orphan"
    )



def perform_operations():
    with SessionLocal() as session:
        try:
            print("=== INSERTING 5 RECORDS FOR EACH MODEL ===")
            
            # Insert categories
            categories = [
                Category(category_name="Mathematics", price=100),
                Category(category_name="Science", price=120),
                Category(category_name="Computer Science", price=150),
                Category(category_name="Literature", price=80),
                Category(category_name="History", price=90)
            ]
            session.add_all(categories)
            
            # Insert professors
            professors = [
                Professor(first_name="Robert", second_name="Smith", teaching_subjects="Mathematics"),
                Professor(first_name="Sarah", second_name="Johnson", teaching_subjects="Physics"),
                Professor(first_name="James", second_name="Wilson", teaching_subjects="Computer Science"),
                Professor(first_name="Emily", second_name="Davis", teaching_subjects="Literature"),
                Professor(first_name="Thomas", second_name="Brown", teaching_subjects="History")
            ]
            session.add_all(professors)
            
            # Insert courses
            courses = [
                Course(name="Calculus I", professor=professors[0], category=categories[0],
                      professor_name=f"{professors[0].first_name} {professors[0].second_name}"),
                Course(name="Physics 101", professor=professors[1], category=categories[1],
                      professor_name=f"{professors[1].first_name} {professors[1].second_name}"),
                Course(name="Python Programming", professor=professors[2], category=categories[2],
                      professor_name=f"{professors[2].first_name} {professors[2].second_name}"),
                Course(name="Shakespeare", professor=professors[3], category=categories[3],
                      professor_name=f"{professors[3].first_name} {professors[3].second_name}"),
                Course(name="World History", professor=professors[4], category=categories[4],
                      professor_name=f"{professors[4].first_name} {professors[4].second_name}")
            ]
            session.add_all(courses)
            
            # Insert students
            students = [
                Student(first_name="Alice", second_name="Williams", age=20),
                Student(first_name="Bob", second_name="Miller", age=21),
                Student(first_name="Charlie", second_name="Davis", age=22),
                Student(first_name="Diana", second_name="Garcia", age=23),
                Student(first_name="Ethan", second_name="Martinez", age=24)
            ]
            session.add_all(students)
            
            # Enroll students in courses
            enrollments = [
                StudentCourse(student=students[0], course=courses[0], grade="A"),
                StudentCourse(student=students[0], course=courses[1], grade="B+"),
                StudentCourse(student=students[1], course=courses[0], grade="B"),
                StudentCourse(student=students[1], course=courses[2], grade="A-"),
                StudentCourse(student=students[2], course=courses[3], grade="B+"),
                StudentCourse(student=students[3], course=courses[4], grade="A"),
                StudentCourse(student=students[4], course=courses[2], grade="B")
            ]
            session.add_all(enrollments)
            
            session.commit()
            
            print("\n=== UPDATING 2 RECORDS IN EACH MODEL ===")
            
            # Update students
            students[0].age = 21
            students[1].second_name = "Smith"
            
            # Update professors
            professors[0].teaching_subjects = "Advanced Mathematics"
            professors[1].second_name = "Williams"
            
            # Update categories
            categories[0].price = 110
            categories[1].category_name = "Natural Sciences"
            
            # Update courses
            courses[0].name = "Calculus I (Honors)"
            courses[1].professor_name = "Sarah Williams"
            
            # Update enrollments
            enrollments[0].grade = "A+"
            enrollments[1].grade = "A-"
            
            session.commit()
            
            print("\n=== DELETING 1 RECORD FROM EACH MODEL ===")
            
            # Delete student (and their enrollments via cascade)
            student_to_delete = session.get(Student, students[4].id)
            if student_to_delete:
                session.delete(student_to_delete)
            
            # Delete professor (first remove from courses or set to NULL)
            professor_to_delete = session.get(Professor, professors[4].id)
            if professor_to_delete:
                for course in session.query(Course).filter_by(professor_id=professor_to_delete.id).all():
                    course.professor_id = None
                    course.professor_name = "Unassigned"
                session.delete(professor_to_delete)
            
            # Delete category (first remove from courses)
            category_to_delete = session.get(Category, categories[3].id)  # Literature
            if category_to_delete:
                for course in session.query(Course).filter_by(category_id=category_to_delete.id).all():
                    course.category_id = None
                session.delete(category_to_delete)
            
            # Delete course (and enrollments via cascade)
            course_to_delete = session.get(Course, courses[4].id)  # World History
            if course_to_delete:
                session.delete(course_to_delete)
            
            # Delete enrollment (separate from the course deletion)
            enrollment_to_delete = session.query(StudentCourse).filter_by(
                student_id=students[3].id, 
                course_id=courses[2].id
            ).first()
            if enrollment_to_delete:
                session.delete(enrollment_to_delete)
            
            session.commit()
            print("\nALL OPERATIONS COMPLETED SUCCESSFULLY!")
            
        except Exception as e:
            session.rollback()
            print(f"OPERATION FAILED: {e}")
            raise

if __name__ == "__main__":
    perform_operations()