"""
Utility functions for the Attendance Tracker application
"""

import re
from datetime import datetime
from pathlib import Path


def validate_course_code(code):
    """Validate course code format"""
    if not code or not isinstance(code, str):
        return False
    # Basic validation - alphanumeric, 6-10 characters
    return bool(re.match(r'^[A-Za-z0-9]{6,10}$', code))


def validate_attendance_status(status):
    """Validate attendance status"""
    if not status or not isinstance(status, str):
        return False
    return status.strip().lower() in ['present', 'absent']


def format_timestamp(timestamp=None):
    """Format timestamp for display"""
    if timestamp is None:
        timestamp = datetime.now()
    return timestamp.strftime('%Y-%m-%d %H:%M:%S')


def safe_percentage(numerator, denominator):
    """Safely calculate percentage avoiding division by zero"""
    if denominator == 0:
        return 0.0
    return (numerator / denominator) * 100


def ensure_directory_exists(path):
    """Ensure directory exists, create if it doesn't"""
    Path(path).parent.mkdir(parents=True, exist_ok=True)


def sanitize_filename(filename):
    """Sanitize filename for cross-platform compatibility"""
    # Remove or replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename


def get_default_font():
    """Get default font family for cross-platform compatibility"""
    import platform
    system = platform.system().lower()
    
    if system == 'windows':
        return ('Segoe UI', 'Arial', 'sans-serif')
    elif system == 'darwin':  # macOS
        return ('SF Pro Display', 'Helvetica', 'Arial', 'sans-serif')
    else:  # Linux and others
        return ('Ubuntu', 'DejaVu Sans', 'Arial', 'sans-serif')