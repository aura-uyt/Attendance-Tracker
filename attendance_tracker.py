import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import sqlite3
from datetime import datetime
import re
import json
import csv
import logging
from pathlib import Path
from utils import (
    validate_course_code, validate_attendance_status, 
    format_timestamp, safe_percentage, get_default_font,
    sanitize_filename
)

class AttendanceTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("📊 Attendance Tracker")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Setup logging
        self.setup_logging()
        
        # Load configuration
        self.load_config()
        
        # Configure modern styling
        self.setup_styles()
        
        # Initialize database with error handling
        if not self.init_database():
            messagebox.showerror("Database Error", "Failed to initialize database. Please check permissions.")
            return
        
        # Load courses from database
        self.load_courses()
        
        # Create GUI
        self.create_widgets()
        
        # Load initial data
        self.refresh_stats()
    
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('attendance_tracker.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def load_config(self):
        """Load configuration from file"""
        config_file = Path('config.json')
        default_config = {
            'font_family': get_default_font(),
            'theme': 'light',
            'window_size': '1000x700',
            'auto_backup': True,
            'backup_interval_days': 7
        }
        
        try:
            if config_file.exists():
                with open(config_file, 'r') as f:
                    self.config = {**default_config, **json.load(f)}
            else:
                self.config = default_config
                self.save_config()
        except Exception as e:
            self.logger.error(f"Failed to load config: {e}")
            self.config = default_config
    
    def save_config(self):
        """Save configuration to file"""
        try:
            with open('config.json', 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save config: {e}")
    
    def setup_styles(self):
        """Configure modern ttk styles with cross-platform fonts"""
        style = ttk.Style()
        # Use first font from the list for compatibility
        font_name = self.config['font_family'][0] if isinstance(self.config['font_family'], (list, tuple)) else self.config['font_family']
        
        # Configure notebook style
        style.configure('Modern.TNotebook', background='#f0f0f0')
        style.configure('Modern.TNotebook.Tab', padding=[20, 10], font=(font_name, 10, 'bold'))
        
        # Configure button styles
        style.configure('Modern.TButton', 
                       font=(font_name, 10),
                       padding=[15, 8])
        
        # Configure label styles
        style.configure('Title.TLabel', 
                       font=(font_name, 16, 'bold'),
                       background='#f0f0f0',
                       foreground='#2c3e50')
        
        style.configure('Subtitle.TLabel', 
                       font=(font_name, 12),
                       background='#f0f0f0',
                       foreground='#34495e')
        
        # Configure treeview style
        style.configure('Modern.Treeview',
                       font=(font_name, 9),
                       rowheight=25)
        style.configure('Modern.Treeview.Heading',
                       font=(font_name, 10, 'bold'),
                       background='#3498db',
                       foreground='white')
        
        # Configure frame styles
        style.configure('Card.TFrame',
                       background='white',
                       relief='flat',
                       borderwidth=1)
    
    def init_database(self):
        """Initialize SQLite database with error handling"""
        try:
            self.conn = sqlite3.connect('attendance.db')
            self.cursor = self.conn.cursor()
            
            # Create tables
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS courses (
                    course_code TEXT PRIMARY KEY,
                    course_name TEXT NOT NULL
                )
            ''')
            
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    course_code TEXT,
                    date TEXT,
                    status TEXT,
                    FOREIGN KEY (course_code) REFERENCES courses (course_code)
                )
            ''')
            
            # Insert default courses if table is empty
            self.cursor.execute('SELECT COUNT(*) FROM courses')
            if self.cursor.fetchone()[0] == 0:
                self.insert_default_courses()
            
            self.conn.commit()
            self.logger.info("Database initialized successfully")
            return True
            
        except sqlite3.Error as e:
            self.logger.error(f"Database initialization failed: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error during database init: {e}")
            return False
    
    def insert_default_courses(self):
        """Insert default courses into database"""
        default_courses = {
            '16242101': 'Transforms and Vector Calculus',
            '16242102': 'Design and Analysis of Algorithms',
            '16242103': 'Database Management System',
            '16242104': 'Operating Systems',
            '16242105': 'Computer Networks',
            '16242106': 'Design and Analysis of Algorithms Lab',
            '16242107': 'Database Management System Lab',
            '16242108': 'Problem Solving Through Python Programming',
            '16242109': 'Semester Proficiency',
            '16242110': 'Macro Project-I',
            '16242111': 'Self-learning/Presentation',
            '16242112': 'Cyber Security',
            'NEC00076': 'LT Spice Tutorial for Circuit Simulation'
        }
        
        for code, name in default_courses.items():
            self.cursor.execute('''
                INSERT OR REPLACE INTO courses (course_code, course_name)
                VALUES (?, ?)
            ''', (code, name))
    
    def load_courses(self):
        """Load courses from database into memory for performance"""
        try:
            self.cursor.execute('SELECT course_code, course_name FROM courses')
            self.courses = dict(self.cursor.fetchall())
            # Create set for faster lookups
            self.course_codes = set(self.courses.keys())
            self.logger.info(f"Loaded {len(self.courses)} courses")
        except sqlite3.Error as e:
            self.logger.error(f"Failed to load courses: {e}")
            self.courses = {}
            self.course_codes = set()
    
    def create_widgets(self):
        """Create the main GUI widgets"""
        # Header
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        font_name = self.config['font_family'][0] if isinstance(self.config['font_family'], (list, tuple)) else self.config['font_family']
        title_label = tk.Label(header_frame, 
                              text="📊 Attendance Management System",
                              font=(font_name, 18, 'bold'),
                              bg='#2c3e50', fg='white')
        title_label.pack(expand=True)
        
        # Main container
        main_container = tk.Frame(self.root, bg='#f0f0f0')
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Main notebook for tabs (store as instance variable)
        self.notebook = ttk.Notebook(main_container, style='Modern.TNotebook')
        self.notebook.pack(fill='both', expand=True)
        
        # Tab 1: Upload Data
        upload_frame = ttk.Frame(self.notebook, style='Card.TFrame')
        self.notebook.add(upload_frame, text="📤 Upload Data")
        
        # Tab 2: View Statistics
        stats_frame = ttk.Frame(self.notebook, style='Card.TFrame')
        self.notebook.add(stats_frame, text="📈 Statistics")
        
        # Tab 3: Export Data
        export_frame = ttk.Frame(self.notebook, style='Card.TFrame')
        self.notebook.add(export_frame, text="📊 Export")
        
        # Upload tab widgets
        self.create_upload_widgets(upload_frame)
        
        # Statistics tab widgets
        self.create_stats_widgets(stats_frame)
        
        # Export tab widgets
        self.create_export_widgets(export_frame)
    
    def create_upload_widgets(self, parent):
        """Create widgets for the upload tab"""
        # Content container
        content_frame = tk.Frame(parent, bg='white')
        content_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Instructions
        instruction_frame = tk.Frame(content_frame, bg='white')
        instruction_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(instruction_frame, 
                 text="📝 Paste Your Daily Attendance Data", 
                 style='Title.TLabel').pack(anchor='w')
        
        ttk.Label(instruction_frame, 
                 text="Copy and paste your attendance table below, then click Upload to process", 
                 style='Subtitle.TLabel').pack(anchor='w', pady=(5, 0))
        
        # Text area container with border
        text_container = tk.Frame(content_frame, bg='#e8e8e8', relief='solid', bd=1)
        text_container.pack(fill='both', expand=True, pady=(0, 20))
        
        # Text area for pasting data
        self.text_area = scrolledtext.ScrolledText(text_container, 
                                                  height=15, 
                                                  font=('Consolas', 10),
                                                  bg='#fafafa',
                                                  relief='flat',
                                                  bd=0,
                                                  padx=10,
                                                  pady=10)
        self.text_area.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Sample text
        sample_text = """S.No.	Course Code	Course Name	attendance
1 	16242101	Transforms and Vector Calculus	Present
2 	16242103	Database Management System	Present
3 	16242104	Operating Systems	Present
4 	16242105	Computer Networks	Present
5 	16242108	Problem Solving Through Python Programming	Present"""
        
        self.text_area.insert('1.0', sample_text)
        
        # Buttons
        button_frame = tk.Frame(content_frame, bg='white')
        button_frame.pack(fill='x')
        
        # Upload button (primary)
        font_name = self.config['font_family'][0] if isinstance(self.config['font_family'], (list, tuple)) else self.config['font_family']
        upload_btn = tk.Button(button_frame, 
                              text="📤 Upload Data",
                              command=self.upload_data,
                              font=(font_name, 11, 'bold'),
                              bg='#3498db',
                              fg='white',
                              relief='flat',
                              padx=25,
                              pady=10,
                              cursor='hand2')
        upload_btn.pack(side='left', padx=(0, 10))
        
        # Clear button (secondary)
        clear_btn = tk.Button(button_frame, 
                             text="🗑️ Clear",
                             command=lambda: self.text_area.delete('1.0', 'end'),
                             font=(font_name, 11),
                             bg='#95a5a6',
                             fg='white',
                             relief='flat',
                             padx=25,
                             pady=10,
                             cursor='hand2')
        clear_btn.pack(side='left')
        
        # Fixed hover effects
        def on_enter_upload(e):
            e.widget.configure(bg='#2980b9')
        def on_leave_upload(e):
            e.widget.configure(bg='#3498db')
        def on_enter_clear(e):
            e.widget.configure(bg='#7f8c8d')
        def on_leave_clear(e):
            e.widget.configure(bg='#95a5a6')
            
        upload_btn.bind('<Enter>', on_enter_upload)
        upload_btn.bind('<Leave>', on_leave_upload)
        clear_btn.bind('<Enter>', on_enter_clear)
        clear_btn.bind('<Leave>', on_leave_clear)
    
    def create_export_widgets(self, parent):
        """Create widgets for the export tab"""
        content_frame = tk.Frame(parent, bg='white')
        content_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Header
        ttk.Label(content_frame, 
                 text="📊 Export Attendance Data", 
                 style='Title.TLabel').pack(anchor='w', pady=(0, 20))
        
        # Export buttons
        btn_frame = tk.Frame(content_frame, bg='white')
        btn_frame.pack(fill='x', pady=10)
        
        font_name = self.config['font_family'][0] if isinstance(self.config['font_family'], (list, tuple)) else self.config['font_family']
        export_csv_btn = tk.Button(btn_frame, 
                                  text="📄 Export to CSV",
                                  command=self.export_to_csv,
                                  font=(font_name, 11, 'bold'),
                                  bg='#27ae60',
                                  fg='white',
                                  relief='flat',
                                  padx=25,
                                  pady=10,
                                  cursor='hand2')
        export_csv_btn.pack(side='left', padx=(0, 10))
        
        backup_btn = tk.Button(btn_frame, 
                              text="💾 Backup Database",
                              command=self.backup_database,
                              font=(font_name, 11),
                              bg='#f39c12',
                              fg='white',
                              relief='flat',
                              padx=25,
                              pady=10,
                              cursor='hand2')
        backup_btn.pack(side='left')
    
    def create_stats_widgets(self, parent):
        """Create widgets for the statistics tab"""
        # Content container
        content_frame = tk.Frame(parent, bg='white')
        content_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Header
        header_frame = tk.Frame(content_frame, bg='white')
        header_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(header_frame, 
                 text="📈 Attendance Statistics Overview", 
                 style='Title.TLabel').pack(side='left')
        
        # Refresh button in header
        font_name = self.config['font_family'][0] if isinstance(self.config['font_family'], (list, tuple)) else self.config['font_family']
        refresh_btn = tk.Button(header_frame, 
                               text="🔄 Refresh",
                               command=self.refresh_stats,
                               font=(font_name, 10),
                               bg='#27ae60',
                               fg='white',
                               relief='flat',
                               padx=20,
                               pady=8,
                               cursor='hand2')
        refresh_btn.pack(side='right')
        
        # Hover effect for refresh button
        refresh_btn.bind('<Enter>', lambda e: e.widget.configure(bg='#229954'))
        refresh_btn.bind('<Leave>', lambda e: e.widget.configure(bg='#27ae60'))
        
        # Table container with border
        table_container = tk.Frame(content_frame, bg='#e8e8e8', relief='solid', bd=1)
        table_container.pack(fill='both', expand=True)
        
        # Treeview for displaying statistics
        columns = ('Course Code', 'Course Name', 'Present', 'Absent', 'Total', 'Percentage')
        self.stats_tree = ttk.Treeview(table_container, 
                                      columns=columns, 
                                      show='headings', 
                                      height=15,
                                      style='Modern.Treeview')
        
        # Configure columns with responsive widths
        window_width = int(self.root.winfo_width() or 1000)
        column_widths = {
            'Course Code': max(100, window_width // 10),
            'Course Name': max(300, window_width // 3),
            'Present': max(80, window_width // 12),
            'Absent': max(80, window_width // 12),
            'Total': max(80, window_width // 12),
            'Percentage': max(100, window_width // 10)
        }
        
        for col in columns:
            self.stats_tree.heading(col, text=col)
            self.stats_tree.column(col, width=column_widths.get(col, 120), anchor='center')
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(table_container, orient='vertical', command=self.stats_tree.yview)
        self.stats_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.stats_tree.pack(side='left', fill='both', expand=True, padx=2, pady=2)
        scrollbar.pack(side='right', fill='y', pady=2)
        
        # Add alternating row colors
        self.stats_tree.tag_configure('oddrow', background='#f8f9fa')
        self.stats_tree.tag_configure('evenrow', background='white')
    
    def extract_course_code(self, parts, line):
        """Extract course code from parts or line - optimized with set lookup"""
        # First check parts for exact match (O(1) lookup)
        for part in parts:
            part = part.strip()
            if part in self.course_codes:
                return part
        
        # Fallback: check if any course code is contained in the line
        for code in self.course_codes:
            if code in line:
                return code
        return None
    
    def extract_attendance_status(self, parts, line):
        """Extract attendance status from parts or line"""
        # Check parts first
        for part in parts:
            part_lower = part.strip().lower()
            if part_lower in ['present', 'absent']:
                return part_lower.title()
        
        # Check entire line
        line_lower = line.lower()
        if 'present' in line_lower:
            return 'Present'
        elif 'absent' in line_lower:
            return 'Absent'
        return 'Present'  # Default
    
    def parse_attendance_data(self, text):
        """Parse the pasted attendance data with improved performance"""
        if not text.strip():
            return []
        
        lines = text.strip().split('\n')
        data = []
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('S.No'):
                continue
                
            # Split by tab or multiple spaces
            parts = re.split(r'\t+|\s{2,}', line)
            
            # Extract course code and attendance status
            course_code = self.extract_course_code(parts, line)
            attendance_status = self.extract_attendance_status(parts, line)
            
            if course_code and course_code in self.courses:
                data.append({
                    'course_code': course_code,
                    'course_name': self.courses[course_code],
                    'attendance': attendance_status
                })
        
        return data
    
    def validate_data(self, data):
        """Validate parsed data before insertion"""
        if not data:
            return False, "No valid data found. Please check the format."
        
        invalid_courses = []
        for entry in data:
            if entry['course_code'] not in self.courses:
                invalid_courses.append(entry['course_code'])
        
        if invalid_courses:
            return False, f"Invalid course codes: {', '.join(invalid_courses)}"
        
        return True, "Data is valid"
    
    def upload_data(self):
        """Upload attendance data to database with improved error handling"""
        try:
            text = self.text_area.get('1.0', 'end')
            data = self.parse_attendance_data(text)
            
            # Validate data
            is_valid, message = self.validate_data(data)
            if not is_valid:
                messagebox.showerror("Validation Error", message)
                return
            
            # Single timestamp for consistency
            timestamp = format_timestamp()
            
            # Insert records with transaction
            self.cursor.execute('BEGIN TRANSACTION')
            for entry in data:
                self.cursor.execute('''
                    INSERT INTO attendance (course_code, date, status)
                    VALUES (?, ?, ?)
                ''', (entry['course_code'], timestamp, entry['attendance']))
            
            self.conn.commit()
            
            msg = f"Added {len(data)} attendance records for {timestamp.split()[0]}"
            messagebox.showinfo("Success", msg)
            self.text_area.delete('1.0', 'end')
            self.refresh_stats()
            self.logger.info(f"Uploaded {len(data)} records successfully")
            
        except sqlite3.Error as e:
            self.conn.rollback()
            error_msg = f"Database error: {str(e)}"
            messagebox.showerror("Database Error", error_msg)
            self.logger.error(error_msg)
        except Exception as e:
            self.conn.rollback()
            error_msg = f"Failed to upload data: {str(e)}"
            messagebox.showerror("Error", error_msg)
            self.logger.error(error_msg)
    
    def refresh_stats(self):
        """Refresh the statistics display with error handling"""
        try:
            # Clear existing data
            for item in self.stats_tree.get_children():
                self.stats_tree.delete(item)
            
            # Get statistics from database
            self.cursor.execute('''
                SELECT 
                    c.course_code,
                    c.course_name,
                    COALESCE(SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END), 0) as present,
                    COALESCE(SUM(CASE WHEN a.status = 'Absent' THEN 1 ELSE 0 END), 0) as absent,
                    COALESCE(COUNT(a.id), 0) as total
                FROM courses c
                LEFT JOIN attendance a ON c.course_code = a.course_code
                GROUP BY c.course_code, c.course_name
                ORDER BY c.course_code
            ''')
            
            results = self.cursor.fetchall()
            
            for i, row in enumerate(results):
                course_code, course_name, present, absent, total = row
                percentage = safe_percentage(present, total)
                
                # Determine row tag for alternating colors
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                
                self.stats_tree.insert('', 'end', values=(
                    course_code,
                    course_name,
                    present,
                    absent,
                    total,
                    f"{percentage:.1f}%"
                ), tags=(tag,))
                
        except sqlite3.Error as e:
            error_msg = f"Failed to refresh statistics: {e}"
            messagebox.showerror("Database Error", error_msg)
            self.logger.error(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error refreshing stats: {e}"
            messagebox.showerror("Error", error_msg)
            self.logger.error(error_msg)
    
    def export_to_csv(self):
        """Export attendance data to CSV file"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Save attendance data as CSV"
            )
            
            if not filename:
                return
            
            self.cursor.execute('''
                SELECT c.course_code, c.course_name, a.date, a.status
                FROM courses c
                LEFT JOIN attendance a ON c.course_code = a.course_code
                ORDER BY c.course_code, a.date
            ''')
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Course Code', 'Course Name', 'Date', 'Status'])
                writer.writerows(self.cursor.fetchall())
            
            messagebox.showinfo("Success", f"Data exported to {filename}")
            self.logger.info(f"Data exported to {filename}")
            
        except Exception as e:
            error_msg = f"Failed to export data: {e}"
            messagebox.showerror("Export Error", error_msg)
            self.logger.error(error_msg)
    
    def backup_database(self):
        """Create a backup of the database"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_filename = sanitize_filename(f"attendance_backup_{timestamp}.db")
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".db",
                initialvalue=backup_filename,
                filetypes=[("Database files", "*.db"), ("All files", "*.*")],
                title="Save database backup"
            )
            
            if not filename:
                return
            
            # Create backup using SQLite backup API
            backup = sqlite3.connect(filename)
            self.conn.backup(backup)
            backup.close()
            
            messagebox.showinfo("Success", f"Database backed up to {filename}")
            self.logger.info(f"Database backed up to {filename}")
            
        except Exception as e:
            error_msg = f"Failed to backup database: {e}"
            messagebox.showerror("Backup Error", error_msg)
            self.logger.error(error_msg)
    
    def __del__(self):
        """Close database connection and save config"""
        try:
            if hasattr(self, 'conn'):
                self.conn.close()
            if hasattr(self, 'config'):
                self.save_config()
        except Exception as e:
            if hasattr(self, 'logger'):
                self.logger.error(f"Error during cleanup: {e}")

def main():
    try:
        root = tk.Tk()
        app = AttendanceTracker(root)
        root.protocol("WM_DELETE_WINDOW", lambda: (app.__del__(), root.destroy()))
        root.mainloop()
    except Exception as e:
        logging.error(f"Application failed to start: {e}")
        messagebox.showerror("Startup Error", f"Failed to start application: {e}")

if __name__ == "__main__":
    main()