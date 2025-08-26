# 📊 Attendance Tracker

A modern GUI application to track and calculate your attendance percentage for academic courses. Built with Python's tkinter for a user-friendly interface and SQLite for data persistence.

## ✨ Features

- **Modern GUI Interface**: Clean, intuitive design with tabbed navigation
- **Data Import**: Paste attendance data directly from spreadsheets or text
- **Real-time Statistics**: View attendance percentages and detailed analytics
- **Course Management**: Pre-configured with common course codes and names
- **Data Persistence**: SQLite database stores all attendance records
- **Flexible Input**: Supports various text formats for attendance data
- **📊 Data Export**: Export attendance records to CSV format
- **💾 Database Backup**: Create timestamped database backups
- **⚙️ Configuration**: Customizable settings via JSON configuration
- **🔍 Data Validation**: Input validation and error handling
- **📝 Logging**: Comprehensive application logging for debugging
- **🖥️ Cross-Platform**: Works on Windows, macOS, and Linux with appropriate fonts

## 🚀 Quick Start

### Prerequisites
- Python 3.6 or higher
- No additional packages required (uses built-in modules)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/aura-uyt/Attendance-Tracker.git
   cd Attendance-Tracker
   ```

2. **Run the application**:
   ```bash
   python run.py
   ```
   
   Or directly:
   ```bash
   python attendance_tracker.py
   ```

## 📖 How to Use

### 1. Upload Attendance Data

1. **Open the Upload Data tab** (📤 Upload Data)
2. **Copy your attendance data** from any source (Excel, Google Sheets, etc.)
3. **Paste the data** into the text area
4. **Click "📤 Upload Data"** to process

**Supported Data Format**:
```
S.No.   Course Code    Course Name                              attendance
1       16242101      Transforms and Vector Calculus          Present
2       16242103      Database Management System              Present
3       16242104      Operating Systems                        Absent
```

### 2. View Statistics

1. **Switch to Statistics tab** (📈 Statistics)
2. **View attendance percentages** for each course
3. **Analyze overall attendance** trends
4. **Click Refresh** to update data

### 3. Export Data

1. **Switch to Export tab** (📊 Export)
2. **Export to CSV** - Save attendance data as spreadsheet
3. **Backup Database** - Create a backup copy of your database
4. **Choose save location** and filename

## 🎯 Pre-configured Courses

The application comes with these course codes:

| Course Code | Course Name |
|-------------|-------------|
| 16242101 | Transforms and Vector Calculus |
| 16242102 | Design and Analysis of Algorithms |
| 16242103 | Database Management System |
| 16242104 | Operating Systems |
| 16242105 | Computer Networks |
| 16242106 | Design and Analysis of Algorithms Lab |
| 16242107 | Database Management System Lab |
| 16242108 | Problem Solving Through Python Programming |
| 16242109 | Semester Proficiency |
| 16242110 | Macro Project-I |
| 16242111 | Self-learning/Presentation |
| 16242112 | Cyber Security |
| NEC00076 | LT Spice Tutorial for Circuit Simulation |

## 💾 Data Storage

- **Database**: `attendance.db` (SQLite)
- **Tables**: 
  - `courses`: Stores course codes and names
  - `attendance`: Stores daily attendance records
- **Automatic Backup**: Database persists between sessions

## 🔧 Technical Details

### File Structure
```
Attendance-Tracker/
├── attendance_tracker.py    # Main application
├── utils.py                # Utility functions
├── run.py                  # Application launcher
├── config.json             # Configuration settings
├── attendance.db           # SQLite database
├── attendance_tracker.log  # Application logs
├── test_basic.py           # Basic functionality tests
├── requirements.txt        # Dependencies (none required)
├── CHANGELOG.md           # Version history
├── README.md              # This file
└── LICENSE                # License information
```

### Dependencies
- **tkinter**: GUI framework (built-in)
- **sqlite3**: Database management (built-in)
- **datetime**: Date handling (built-in)
- **re**: Regular expressions (built-in)
- **json**: Configuration management (built-in)
- **csv**: Data export functionality (built-in)
- **logging**: Application logging (built-in)
- **pathlib**: Cross-platform file paths (built-in)

## 🎨 Interface Overview

### Upload Tab
- Large text area for pasting attendance data
- Upload and Clear buttons with hover effects
- Real-time data processing
- Comprehensive error handling and validation
- Sample data format included

### Statistics Tab
- Course-wise attendance percentages
- Overall attendance summary
- Detailed attendance records with alternating row colors
- Refresh button for real-time updates
- Responsive column widths

### Export Tab
- CSV export functionality
- Database backup with timestamps
- File save dialogs
- Progress feedback

## 🐛 Troubleshooting

**Common Issues**:

1. **Data not uploading**: Ensure data format matches the expected structure
2. **Database errors**: Check file permissions and view logs in `attendance_tracker.log`
3. **GUI not displaying**: Verify Python tkinter installation
4. **Font issues**: Application automatically selects appropriate fonts per OS
5. **Export failures**: Ensure write permissions in selected directory

**Data Format Tips**:
- Include column headers (S.No., Course Code, Course Name, attendance)
- Use "Present" or "Absent" for attendance status
- Separate columns with tabs or multiple spaces
- Course codes should match pre-configured list
- Data is validated before insertion

**Performance Tips**:
- Use the built-in validation to catch errors early
- Regular database backups are recommended
- Check logs for detailed error information
- Large datasets are now handled efficiently

## 📊 Attendance Calculation

Attendance percentage is calculated as:
```
Attendance % = (Present Days / Total Days) × 100
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. **Run tests**: `python test_basic.py`
5. Test thoroughly with the GUI
6. Update documentation if needed
7. Submit a pull request

### Development Setup
```bash
# Clone the repository
git clone <repository-url>
cd Attendance-Tracker

# Run tests
python test_basic.py

# Run the application
python run.py
```

## 📄 License

See LICENSE file for details.

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the data format requirements
3. Check the application logs (`attendance_tracker.log`)
4. Run basic tests (`python test_basic.py`)
5. Review the changelog (`CHANGELOG.md`)
6. Open an issue on the repository

## 📊 Version History

See [CHANGELOG.md](CHANGELOG.md) for detailed version history and improvements.

---

**Made with ❤️ for academic attendance tracking**
