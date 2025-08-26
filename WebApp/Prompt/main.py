from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import database
import schemas

app = FastAPI(title="Attendance Manager", version="1.0.0")

# Students
@app.post("/students/", response_model=schemas.Student)
def create_student(student: schemas.StudentCreate, db: Session = Depends(database.get_db)):
    db_student = database.Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@app.get("/students/", response_model=List[schemas.Student])
def get_students(db: Session = Depends(database.get_db)):
    return db.query(database.Student).all()

# Courses
@app.post("/courses/", response_model=schemas.Course)
def create_course(course: schemas.CourseCreate, db: Session = Depends(database.get_db)):
    db_course = database.Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@app.get("/courses/", response_model=List[schemas.Course])
def get_courses(db: Session = Depends(database.get_db)):
    return db.query(database.Course).all()

# Attendance
@app.post("/attendance/", response_model=schemas.Attendance)
def mark_attendance(attendance: schemas.AttendanceCreate, db: Session = Depends(database.get_db)):
    # Check if attendance already exists
    existing = db.query(database.Attendance).filter(
        database.Attendance.student_id == attendance.student_id,
        database.Attendance.course_id == attendance.course_id,
        database.Attendance.date == attendance.date
    ).first()
    
    if existing:
        existing.status = attendance.status
        db.commit()
        db.refresh(existing)
        return existing
    
    db_attendance = database.Attendance(**attendance.dict())
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance

@app.get("/attendance/{course_id}", response_model=List[schemas.Attendance])
def get_attendance(course_id: int, db: Session = Depends(database.get_db)):
    return db.query(database.Attendance).filter(database.Attendance.course_id == course_id).all()

@app.get("/")
def root():
    return {"message": "Attendance Manager API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)