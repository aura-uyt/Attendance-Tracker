#!/usr/bin/env python3
"""
Basic functionality test for Attendance Tracker
"""

import sqlite3
import tempfile
import os
from datetime import datetime
from utils import validate_course_code, validate_attendance_status, safe_percentage


def test_utilities():
    """Test utility functions"""
    print("Testing utility functions...")
    
    # Test course code validation
    assert validate_course_code("16242101") == True
    assert validate_course_code("NEC00076") == True
    assert validate_course_code("short") == False  # Too short
    assert validate_course_code("") == False
    
    # Test attendance status validation
    assert validate_attendance_status("Present") == True
    assert validate_attendance_status("Absent") == True
    assert validate_attendance_status("invalid") == False
    
    # Test safe percentage calculation
    assert safe_percentage(50, 100) == 50.0
    assert safe_percentage(0, 0) == 0.0
    assert safe_percentage(3, 4) == 75.0
    
    print("✓ Utility functions working correctly")


def test_database_operations():
    """Test database operations"""
    print("Testing database operations...")
    
    # Create temporary database
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        # Test database creation
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS courses (
                course_code TEXT PRIMARY KEY,
                course_name TEXT NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_code TEXT,
                date TEXT,
                status TEXT,
                FOREIGN KEY (course_code) REFERENCES courses (course_code)
            )
        ''')
        
        # Insert test data
        cursor.execute("INSERT INTO courses VALUES (?, ?)", ("TEST101", "Test Course"))
        cursor.execute("INSERT INTO attendance VALUES (?, ?, ?, ?)", 
                      (None, "TEST101", datetime.now().isoformat(), "Present"))
        
        conn.commit()
        
        # Test query
        cursor.execute("SELECT COUNT(*) FROM courses")
        course_count = cursor.fetchone()[0]
        assert course_count == 1
        
        cursor.execute("SELECT COUNT(*) FROM attendance")
        attendance_count = cursor.fetchone()[0]
        assert attendance_count == 1
        
        conn.close()
        print("✓ Database operations working correctly")
        
    finally:
        # Cleanup
        if os.path.exists(db_path):
            os.unlink(db_path)


def main():
    """Run all tests"""
    print("Running basic functionality tests...\n")
    
    try:
        test_utilities()
        test_database_operations()
        print("\n🎉 All tests passed! Application is ready to use.")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())