from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.schemas.course import CourseCreate
from app.models.base import Course

def get_course(db: Session, course_id: int):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

def get_courses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Course).offset(skip).limit(limit).all()

def create_course(db: Session, course: CourseCreate):
    db_course = Course(
        title=course.title,
        description=course.description
    )
    db.add(db_course)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Course already exists or data conflict")
    db.refresh(db_course)
    return db_course

def delete_course(db: Session, course_id: int):
    course = get_course(db, course_id)
    db.delete(course)
    db.commit()
    return course

def update_course(db: Session, course_id: int, new_data: dict):
    course = get_course(db, course_id)
    for key, value in new_data.items():
        setattr(course, key, value)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Update failed due to data conflict")
    db.refresh(course)
    return course
