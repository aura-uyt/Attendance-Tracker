import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sqlite3
from datetime import datetime
import re

class AttendanceTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("📊 Attendance Tracker")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Configure modern styling
        self.setup_styles()
        
        # Predefined courses
        self.courses = {
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
        
        # Initialize database
        self.init_database()
        
        # Create GUI
        self.create_widgets()
        
        # Load initial data
        self.refresh_stats()
    
    def setup_styles(self):
        """Configure modern ttk styles"""
        style = ttk.Style()
        
        # Configure notebook style
        style.configure('Modern.TNotebook', background='#f0f0f0')
        style.configure('Modern.TNotebook.Tab', padding=[20, 10], font=('Segoe UI', 10, 'bold'))
        
        # Configure button styles
        style.configure('Modern.TButton', 
                       font=('Segoe UI', 10),
                       padding=[15, 8])
        
        # Configure label styles
        style.configure('Title.TLabel', 
                       font=('Segoe UI', 16, 'bold'),
                       background='#f0f0f0',
                       foreground='#2c3e50')
        
        style.configure('Subtitle.TLabel', 
                       font=('Segoe UI', 12),
                       background='#f0f0f0',
                       foreground='#34495e')
        
        # Configure treeview style
        style.configure('Modern.Treeview',
                       font=('Segoe UI', 9),
                       rowheight=25)
        style.configure('Modern.Treeview.Heading',
                       font=('Segoe UI', 10, 'bold'),
                       background='#3498db',
                       foreground='white')
        
        # Configure frame styles
        style.configure('Card.TFrame',
                       background='white',
                       relief='flat',
                       borderwidth=1)
    
    def init_database(self):
        """Initialize SQLite database"""
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
        
        # Insert all predefined courses
        for code, name in self.courses.items():
            self.cursor.execute('''
                INSERT OR REPLACE INTO courses (course_code, course_name)
                VALUES (?, ?)
            ''', (code, name))
        
        self.conn.commit()
    
    def create_widgets(self):
        """Create the main GUI widgets"""
        # Header
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, 
                              text="📊 Attendance Management System",
                              font=('Segoe UI', 18, 'bold'),
                              bg='#2c3e50', fg='white')
        title_label.pack(expand=True)
        
        # Main container
        main_container = tk.Frame(self.root, bg='#f0f0f0')
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Main notebook for tabs
        notebook = ttk.Notebook(main_container, style='Modern.TNotebook')
        notebook.pack(fill='both', expand=True)
        
        # Tab 1: Upload Data
        upload_frame = ttk.Frame(notebook, style='Card.TFrame')
        notebook.add(upload_frame, text="📤 Upload Data")
        
        # Tab 2: View Statistics
        stats_frame = ttk.Frame(notebook, style='Card.TFrame')
        notebook.add(stats_frame, text="📈 Statistics")
        
        # Upload tab widgets
        self.create_upload_widgets(upload_frame)
        
        # Statistics tab widgets
        self.create_stats_widgets(stats_frame)
    
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
        upload_btn = tk.Button(button_frame, 
                              text="📤 Upload Data",
                              command=self.upload_data,
                              font=('Segoe UI', 11, 'bold'),
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
                             font=('Segoe UI', 11),
                             bg='#95a5a6',
                             fg='white',
                             relief='flat',
                             padx=25,
                             pady=10,
                             cursor='hand2')
        clear_btn.pack(side='left')
        
        # Hover effects
        def on_enter(e, color):
            e.widget.configure(bg=color)
        def on_leave(e, color):
            e.widget.configure(bg=color)
            
        upload_btn.bind('<Enter>', lambda e: on_enter(e, '#2980b9'))
        upload_btn.bind('<Leave>', lambda e: on_leave(e, '#3498db'))
        clear_btn.bind('<Enter>', lambda e: on_enter(e, '#7f8c8d'))
        clear_btn.bind('<Leave>', lambda e: on_leave(e, '#95a5a6'))
    
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
        refresh_btn = tk.Button(header_frame, 
                               text="🔄 Refresh",
                               command=self.refresh_stats,
                               font=('Segoe UI', 10),
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
        
        # Configure columns with better widths
        column_widths = {'Course Code': 100, 'Course Name': 300, 'Present': 80, 
                        'Absent': 80, 'Total': 80, 'Percentage': 100}
        
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
    
    def parse_attendance_data(self, text):
        """Parse the pasted attendance data"""
        lines = text.strip().split('\n')
        data = []
        
        for line in lines:
            if line.strip() and not line.startswith('S.No'):
                # Split by tab or multiple spaces
                parts = re.split(r'\t+|\s{2,}', line.strip())
                
                # Look for course code in the line
                course_code = None
                attendance_status = None
                
                # Find course code from our predefined list
                for part in parts:
                    part = part.strip()
                    if part in self.courses:
                        course_code = part
                    elif part.lower() in ['present', 'absent']:
                        attendance_status = part.title()
                
                # Also check if any part contains a known course code
                if not course_code:
                    for known_code in self.courses.keys():
                        if known_code in line:
                            course_code = known_code
                            break
                
                # Extract attendance status if not found
                if not attendance_status:
                    if 'present' in line.lower():
                        attendance_status = 'Present'
                    elif 'absent' in line.lower():
                        attendance_status = 'Absent'
                    else:
                        attendance_status = 'Present'  # Default to present
                
                if course_code:
                    data.append({
                        'course_code': course_code,
                        'course_name': self.courses[course_code],
                        'attendance': attendance_status
                    })
        
        return data
    
    def upload_data(self):
        """Upload attendance data to database"""
        text = self.text_area.get('1.0', 'end')
        data = self.parse_attendance_data(text)
        
        if not data:
            messagebox.showerror("Error", "No valid data found. Please check the format.")
            return
        
        try:
            today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Always insert new records (each upload represents new classes)
            for entry in data:
                self.cursor.execute('''
                    INSERT INTO attendance (course_code, date, status)
                    VALUES (?, ?, ?)
                ''', (entry['course_code'], today, entry['attendance']))
            
            self.conn.commit()
            
            msg = f"Added {len(data)} new attendance records for {datetime.now().strftime('%Y-%m-%d')}"
            messagebox.showinfo("Success", msg)
            self.text_area.delete('1.0', 'end')
            self.refresh_stats()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to upload data: {str(e)}")
    
    def refresh_stats(self):
        """Refresh the statistics display"""
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
            if total > 0:
                percentage = (present / total) * 100
            else:
                percentage = 0
            
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
    
    def __del__(self):
        """Close database connection"""
        if hasattr(self, 'conn'):
            self.conn.close()

def main():
    root = tk.Tk()
    app = AttendanceTracker(root)
    root.mainloop()

if __name__ == "__main__":
    main()