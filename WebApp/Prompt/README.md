# Attendance Manager

FastAPI-based attendance management system for college students.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python main.py
```

3. Access the API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

- `POST /students/` - Create student
- `GET /students/` - List all students
- `POST /courses/` - Create course
- `GET /courses/` - List all courses
- `POST /attendance/` - Mark attendance
- `GET /attendance/{course_id}` - Get attendance for course

## Usage Example

```python
# Create student
{
  "name": "John Doe",
  "student_id": "ST001",
  "email": "john@example.com"
}

# Mark attendance
{
  "student_id": 1,
  "course_id": 1,
  "date": "2024-01-15",
  "status": "present"
}
```