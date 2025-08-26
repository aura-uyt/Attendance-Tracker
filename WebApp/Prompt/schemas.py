from pydantic import BaseModel
from datetime import date
from typing import Optional

class StudentCreate(BaseModel):
    name: str
    student_id: str
    email: Optional[str] = None

class Student(BaseModel):
    id: int
    name: str
    student_id: str
    email: Optional[str] = None
    
    class Config:
        from_attributes = True

class CourseCreate(BaseModel):
    name: str
    code: str
    instructor: Optional[str] = None

class Course(BaseModel):
    id: int
    name: str
    code: str
    instructor: Optional[str] = None
    
    class Config:
        from_attributes = True

class AttendanceCreate(BaseModel):
    student_id: int
    course_id: int
    date: date
    status: str  # present, absent, late

class Attendance(BaseModel):
    id: int
    student_id: int
    course_id: int
    date: date
    status: str
    
    class Config:
        from_attributes = True