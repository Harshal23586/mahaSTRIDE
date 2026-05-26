import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
import json
from hashlib import sha256
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="mahaSTRIDE Project Tracker",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #e0e0e0;
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .info-card {
        background-color: #d1ecf1;
        border-left: 4px solid #17a2b8;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .success-card {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .warning-card {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .admin-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .projectlead-card {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .sangam-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .stButton > button {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 5px;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .storage-status {
        font-size: 0.8rem;
        padding: 0.2rem 0.5rem;
        border-radius: 5px;
        display: inline-block;
    }
    .storage-connected {
        background-color: #d4edda;
        color: #155724;
    }
    .assignment-card {
        background-color: #f8f9fa;
        border-left: 4px solid #1e3c72;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    .daily-routine {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 10px;
        font-family: monospace;
    }
    .default-task-card {
        background-color: #e8f8f5;
        border-left: 4px solid #27ae60;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# User credentials
USERS = {
    "admin@mahastride.com": {
        "password": sha256("Admin@2026".encode()).hexdigest(),
        "role": "admin",
        "name": "Admin"
    },
    "projectlead@mahastride.com": {
        "password": sha256("ProjectLead@2026".encode()).hexdigest(),
        "role": "project_lead",
        "name": "Dr. Harshal Kotwal"
    },
    "sneha@mu.edu": {
        "password": sha256("Sneha@2026".encode()).hexdigest(),
        "role": "coordinator",
        "name": "Ms Sneha",
        "university": "MU"
    },
    "shubham@mu.edu": {
        "password": sha256("Shubham@2026".encode()).hexdigest(),
        "role": "coordinator",
        "name": "Shubham",
        "university": "MU"
    },
    "jagan@sspu.edu": {
        "password": sha256("Jagan@2026".encode()).hexdigest(),
        "role": "coordinator",
        "name": "Mr Jagan",
        "university": "SSPU"
    },
    "vaibhav@coep.edu": {
        "password": sha256("Vaibhav@2026".encode()).hexdigest(),
        "role": "coordinator",
        "name": "Mr Vaibhav",
        "university": "COEP"
    },
    "pratham@au.edu": {
        "password": sha256("Pratham@2026".encode()).hexdigest(),
        "role": "coordinator",
        "name": "Mr Pratham",
        "university": "AU"
    },
    "anjali@nu.edu": {
        "password": sha256("Anjali@2026".encode()).hexdigest(),
        "role": "coordinator",
        "name": "Ms Anjali",
        "university": "NU"
    },
    "nitish@kbcnmu.edu": {
        "password": sha256("Nitish@2026".encode()).hexdigest(),
        "role": "coordinator",
        "name": "Mr Nitish",
        "university": "KBCNMU"
    },
    "atharv@bamu.edu": {
        "password": sha256("Atharv@2026".encode()).hexdigest(),
        "role": "coordinator",
        "name": "Mr Atharv",
        "university": "BAMU"
    }
}

# University details - Updated with correct names, without registrar and VC
UNIVERSITIES = {
    "MU": {
        "name": "University of Mumbai",
        "coordinators": ["Ms Sneha", "Shubham"],
        "nodal_officer": "Dr. Varsha Kelkar Mane",
        "registrar": "_________",
        "vc": "_________"
    },
    "SSPU": {
        "name": "Savitribai Phule Pune University",
        "coordinators": ["Mr Jagan"],
        "nodal_officer": "Prof. Vinayak Joshi",
        "registrar": "_________",
        "vc": "_________"
    },
    "COEP": {
        "name": "College of Engineering Pune Technological University (COEP)",
        "coordinators": ["Mr Vaibhav"],
        "nodal_officer": "Dr. Uttam Chaskar",
        "registrar": "_________",
        "vc": "_________"
    },
    "AU": {
        "name": "Sant Gadge Baba Amravati University",
        "coordinators": ["Mr Pratham"],
        "nodal_officer": "Dr. A. B. Naik",
        "registrar": "_________",
        "vc": "_________"
    },
    "NU": {
        "name": "Rashtrasant Tukadoji Maharaj Nagpur University",
        "coordinators": ["Ms Anjali"],
        "nodal_officer": "Prof. Nandkishor Karade",
        "registrar": "_________",
        "vc": "_________"
    },
    "KBCNMU": {
        "name": "Kavayitri Bahinabai Chaudhari North Maharashtra University, Jalgaon",
        "coordinators": ["Mr Nitish"],
        "nodal_officer": "Prof. Sameer Narkhede",
        "registrar": "_________",
        "vc": "_________"
    },
    "BAMU": {
        "name": "Dr. Babasaheb Ambedkar Marathwada University, Aurangabad",
        "coordinators": ["Mr Atharv"],
        "nodal_officer": "Prof. G.D. Khedkar",
        "registrar": "_________",
        "vc": "_________"
    }
}

# MITRA Officials
MITRA_OFFICIALS = {
    "project_director": "Shri Aman Mittal, Project Director, MahaSTRIDE",
    "jt_ceo": "Jt. CEO, MITRA",
    "addl_chief_secretary": "Addl. Chief Secretary, Higher and Technical Education Department",
    "secretary_governor": "Secretary to Hon. Governor Maharashtra"
}

# ICARE Officials
ICARE_OFFICIALS = {
    "project_head": "Shri Karthick Sridhar, Project Head, ICARE Pvt. Ltd.",
    "data_analyst_lead": "Data Analytics and Dashboard Specialist, ICARE"
}

# Daily Work Routine
DAILY_ROUTINE = """
| Time | Activity |
|------|----------|
| 10:00 AM | Report to university / IQAC cell |
| 10:00-10:30 AM | Prepare for daily stand-up; review pending tasks |
| 10:30-11:00 AM | **Daily stand-up with ICARE Team Only** |
| 11:00 AM-1:00 PM | Data collection / meetings with departments |
| 1:00-2:00 PM | Lunch |
| 2:00-5:30 PM | Data validation, gap analysis, documentation |
| 5:30-6:00 PM | Update daily tracker; email summary to ICARE Project Head |
| 6:00 PM | Departure |
"""

WORKING_HOURS = "10:00 AM - 6:00 PM"
PROJECT_START_DATE = datetime(2026, 5, 7)
PROJECT_DURATION_YEARS = 2
PROJECT_END_DATE = datetime(2028, 5, 6)

# Data file paths
PROGRESS_DATA_FILE = "coordinator_progress_data.json"
ASSIGNMENTS_DATA_FILE = "assignments_data.json"
CUSTOM_TASKS_DATA_FILE = "custom_tasks_data.json"
ATTENDANCE_DATA_FILE = "attendance_data.json"

def hash_password(password):
    return sha256(password.encode()).hexdigest()

def authenticate_user(email, password):
    if email in USERS:
        if USERS[email]["password"] == hash_password(password):
            return True, USERS[email]["role"], USERS[email]["name"], USERS[email].get("university", None)
    return False, None, None, None

def create_initial_progress_data():
    data = {}
    for uni_code in UNIVERSITIES.keys():
        data[uni_code] = {}
    return data

def create_initial_assignments_data():
    return {"assignments": [], "submissions": {}}

def create_initial_custom_tasks_data():
    return {"date_specific_tasks": {}}

def create_initial_attendance_data():
    data = {}
    for uni_code in UNIVERSITIES.keys():
        data[uni_code] = {}
    return data

def load_progress_data():
    try:
        if os.path.exists(PROGRESS_DATA_FILE):
            with open(PROGRESS_DATA_FILE, 'r') as f:
                data = json.load(f)
                if all(uni_code in data for uni_code in UNIVERSITIES.keys()):
                    return data
                else:
                    return create_initial_progress_data()
        else:
            return create_initial_progress_data()
    except Exception as e:
        st.error(f"Error loading progress data: {e}")
        return create_initial_progress_data()

def save_progress_data(data):
    try:
        with open(PROGRESS_DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving progress data: {e}")
        return False

def load_assignments_data():
    try:
        if os.path.exists(ASSIGNMENTS_DATA_FILE):
            with open(ASSIGNMENTS_DATA_FILE, 'r') as f:
                return json.load(f)
        else:
            return create_initial_assignments_data()
    except Exception as e:
        st.error(f"Error loading assignments data: {e}")
        return create_initial_assignments_data()

def save_assignments_data(data):
    try:
        with open(ASSIGNMENTS_DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving assignments data: {e}")
        return False

def load_custom_tasks_data():
    try:
        if os.path.exists(CUSTOM_TASKS_DATA_FILE):
            with open(CUSTOM_TASKS_DATA_FILE, 'r') as f:
                return json.load(f)
        else:
            return create_initial_custom_tasks_data()
    except Exception as e:
        st.error(f"Error loading custom tasks data: {e}")
        return create_initial_custom_tasks_data()

def save_custom_tasks_data(data):
    try:
        with open(CUSTOM_TASKS_DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving custom tasks data: {e}")
        return False

def load_attendance_data():
    try:
        if os.path.exists(ATTENDANCE_DATA_FILE):
            with open(ATTENDANCE_DATA_FILE, 'r') as f:
                data = json.load(f)
                if all(uni_code in data for uni_code in UNIVERSITIES.keys()):
                    return data
                else:
                    return create_initial_attendance_data()
        else:
            return create_initial_attendance_data()
    except Exception as e:
        st.error(f"Error loading attendance data: {e}")
        return create_initial_attendance_data()

def save_attendance_data(data):
    try:
        with open(ATTENDANCE_DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving attendance data: {e}")
        return False

def add_custom_task_for_date(date_str, task_category, task_name, description, deliverables, added_by):
    custom_tasks = load_custom_tasks_data()
    custom_tasks["date_specific_tasks"][date_str] = {
        "task_category": task_category, "task": task_name, "description": description,
        "deliverables": deliverables, "added_by": added_by, "added_at": datetime.now().isoformat()
    }
    return save_custom_tasks_data(custom_tasks)

def get_plan_for_date(date_str):
    custom_tasks = load_custom_tasks_data()
    if date_str in custom_tasks["date_specific_tasks"]:
        return custom_tasks["date_specific_tasks"][date_str]
    return None

def log_daily_entry(university_code, date, task_category, task_name, description, deliverables, status, hours_spent, remarks, swapped_from_default, edited_task, updated_by):
    data = load_progress_data()
    if university_code not in data:
        data[university_code] = {}
    
    data[university_code][date] = {
        "date": date, "task_category": task_category, "task_name": task_name,
        "description": description, "deliverables": deliverables, "status": status,
        "hours_spent": hours_spent, "remarks": remarks, "swapped_from_default": swapped_from_default,
        "edited_task": edited_task, "updated_at": datetime.now().isoformat(), "updated_by": updated_by
    }
    return save_progress_data(data)

def get_university_entries(university_code):
    data = load_progress_data()
    if university_code not in data:
        return pd.DataFrame()
    
    records = []
    for date, entry in data[university_code].items():
        records.append({
            "Date": date, "Task Category": entry.get("task_category", ""), "Task": entry.get("task_name", ""),
            "Description": entry.get("description", ""), "Deliverables": entry.get("deliverables", ""),
            "Status": entry.get("status", "").upper(), "Hours Spent": entry.get("hours_spent", 0),
            "Swapped": "✅" if entry.get("swapped_from_default", False) else "❌",
            "Edited": "✅" if entry.get("edited_task", False) else "❌",
            "Remarks": entry.get("remarks", ""), "Updated At": entry.get("updated_at", "")[:16] if entry.get("updated_at") else "",
            "Updated By": entry.get("updated_by", "")
        })
    return pd.DataFrame(records).sort_values("Date", ascending=False)

def get_monthly_summary(university_code, year, month):
    data = load_progress_data()
    if university_code not in data:
        return []
    
    month_str = f"{year}-{month:02d}"
    monthly_entries = []
    
    for date, entry in data[university_code].items():
        if date.startswith(month_str):
            monthly_entries.append({
                "date": date, "task_category": entry.get("task_category", ""), "task_name": entry.get("task_name", ""),
                "description": entry.get("description", ""), "deliverables": entry.get("deliverables", ""),
                "status": entry.get("status", ""), "hours_spent": entry.get("hours_spent", 0)
            })
    return monthly_entries

def get_daily_progress_data():
    """Get daily progress data for all universities"""
    data = load_progress_data()
    daily_records = []
    
    for uni_code, entries in data.items():
        uni_name = UNIVERSITIES[uni_code]["name"]
        for date, entry in entries.items():
            daily_records.append({
                "Date": date, "University": uni_name, "University Code": uni_code,
                "Task": entry.get("task_name", ""), "Category": entry.get("task_category", ""),
                "Status": entry.get("status", ""), "Hours": entry.get("hours_spent", 0)
            })
    
    df = pd.DataFrame(daily_records)
    if not df.empty:
        df["Date"] = pd.to_datetime(df["Date"])
    return df

def get_weekly_progress_data():
    """Get weekly aggregated progress data"""
    df = get_daily_progress_data()
    if df.empty:
        return pd.DataFrame()
    
    df["Week"] = df["Date"].dt.isocalendar().week
    df["Year"] = df["Date"].dt.year
    df["Week_Start"] = df["Date"] - pd.to_timedelta(df["Date"].dt.dayofweek, unit='d')
    
    weekly = df.groupby(["Year", "Week", "Week_Start", "University"]).agg({
        "Hours": "sum",
        "Task": "count"
    }).reset_index()
    weekly.columns = ["Year", "Week", "Week_Start", "University", "Total Hours", "Tasks Completed"]
    
    return weekly

def get_monthly_progress_data():
    """Get monthly aggregated progress data"""
    df = get_daily_progress_data()
    if df.empty:
        return pd.DataFrame()
    
    df["Month"] = df["Date"].dt.month
    df["Year"] = df["Date"].dt.year
    df["Month_Name"] = df["Date"].dt.strftime("%B %Y")
    
    monthly = df.groupby(["Year", "Month", "Month_Name", "University"]).agg({
        "Hours": "sum",
        "Task": "count"
    }).reset_index()
    monthly.columns = ["Year", "Month", "Month_Name", "University", "Total Hours", "Tasks Completed"]
    
    return monthly

def create_assignment(title, description, due_date, assigned_universities, created_by):
    assignments_data = load_assignments_data()
    assignment_id = f"ASSIGN_{len(assignments_data['assignments']) + 1}_{int(datetime.now().timestamp())}"
    
    new_assignment = {
        "id": assignment_id, "title": title, "description": description, "due_date": due_date,
        "assigned_universities": assigned_universities, "created_by": created_by,
        "created_at": datetime.now().isoformat(), "status": "active"
    }
    
    assignments_data["assignments"].append(new_assignment)
    
    if assignment_id not in assignments_data["submissions"]:
        assignments_data["submissions"][assignment_id] = {}
        for uni_code in assigned_universities:
            assignments_data["submissions"][assignment_id][uni_code] = {
                "status": "pending", "completed_at": None, "remarks": "", "completed_by": None
            }
    
    save_assignments_data(assignments_data)
    return assignment_id

def get_university_assignments(university_code):
    assignments_data = load_assignments_data()
    university_assignments = []
    
    for assignment in assignments_data["assignments"]:
        if assignment["status"] == "active" and university_code in assignment["assigned_universities"]:
            submission = assignments_data["submissions"].get(assignment["id"], {}).get(university_code, {})
            assignment_copy = assignment.copy()
            assignment_copy["submission_status"] = submission.get("status", "pending")
            assignment_copy["submission_remarks"] = submission.get("remarks", "")
            university_assignments.append(assignment_copy)
    
    return university_assignments

def update_assignment_submission(assignment_id, university_code, status, remarks, completed_by):
    assignments_data = load_assignments_data()
    
    if assignment_id in assignments_data["submissions"]:
        if university_code in assignments_data["submissions"][assignment_id]:
            assignments_data["submissions"][assignment_id][university_code] = {
                "status": status, "completed_at": datetime.now().isoformat() if status == "completed" else None,
                "remarks": remarks, "completed_by": completed_by
            }
            return save_assignments_data(assignments_data)
    return False

def create_mpr_word_document(university_code, year, month, coordinator_name):
    """Generate MPR in Word format - Ready for MITRA submission"""
    university = UNIVERSITIES[university_code]
    monthly_entries = get_monthly_summary(university_code, year, month)
    
    doc = Document()
    
    for section in doc.sections:
        section.top_margin = Inches(0.5)
        section.bottom_margin = Inches(0.5)
        section.left_margin = Inches(0.7)
        section.right_margin = Inches(0.7)
    
    # Confidential Header
    header_para = doc.add_paragraph()
    header_para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = header_para.add_run("Confidential")
    run.bold = True
    run.font.size = Pt(10)
    
    doc.add_paragraph()
    
    # MITRA Header
    mitra_header = doc.add_paragraph()
    mitra_header.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = mitra_header.add_run("Maharashtra Institution for Transformation (MITRA)")
    run.bold = True
    run.font.size = Pt(12)
    
    address = doc.add_paragraph()
    address.alignment = WD_ALIGN_PARAGRAPH.CENTER
    address.add_run("5th Floor, Nirmal, Nariman Point, Mumbai-400021")
    address.add_run("\nOffice Tel. No. 022 69979440 | Email: pmu.mahastride@mahamitra.org")
    
    doc.add_paragraph()
    
    # Title
    title = doc.add_heading("MONTHLY PROGRESS REPORT", 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    period_end = datetime(year, month, 1).replace(day=30 if month in [4,6,9,11] else 31)
    subtitle = doc.add_paragraph(f"(From 01-{month:02d}-{year} to {period_end.strftime('%d')}-{month:02d}-{year})")
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_paragraph()
    
    # Client Information
    doc.add_heading("1. CLIENT INFORMATION", level=1)
    info_table = doc.add_table(rows=7, cols=2)
    info_table.style = 'Table Grid'
    info_data = [
        ("Client Name", "Maharashtra Institution for Transformation (MITRA)"),
        ("Project Name", "Comprehensive Data Collection, Advanced Analytics, and Development of Performance Improvement Framework for Maharashtra State Universities under MahaSTRIDE operations"),
        ("University / Division", university["name"]),
        ("Reporting Month", f"{datetime(year, month, 1).strftime('%B %Y')}"),
        ("Report Date", datetime.now().strftime("%d-%m-%Y")),
        ("Prepared By", coordinator_name),
        ("Designation", "Institutional Coordinator cum Research & Innovation Officer")
    ]
    for i, (label, value) in enumerate(info_data):
        info_table.rows[i].cells[0].text = label
        info_table.rows[i].cells[1].text = value
        info_table.rows[i].cells[0].paragraphs[0].runs[0].bold = True
    
    doc.add_paragraph()
    
    # Project Team Deployment
    doc.add_heading("2. PROJECT TEAM DEPLOYMENT", level=1)
    
    team_table = doc.add_table(rows=3, cols=6)
    team_table.style = 'Table Grid'
    headers = ["Sr. No.", "Name", "Profile", "Location", "Present Days", "Remarks"]
    
    header_row = team_table.rows[0].cells
    for i, header in enumerate(headers):
        header_row[i].text = header
        header_row[i].paragraphs[0].runs[0].bold = True
    
    total_present = len(monthly_entries)
    team_data = [
        ("1", coordinator_name, "Institutional Coordinator", university["name"], str(total_present), "Present all working days"),
        ("2", "Support Staff", "Data Entry Operator", university["name"], str(total_present), "Present all working days")
    ]
    for i, row_data in enumerate(team_data):
        row_cells = team_table.rows[i + 1].cells
        for j, cell_data in enumerate(row_data):
            row_cells[j].text = cell_data
    
    doc.add_paragraph()
    
    # Monthly Activities
    doc.add_heading("3. MONTHLY ACTIVITIES UNDERTAKEN", level=1)
    
    if monthly_entries:
        for entry in monthly_entries[:15]:
            doc.add_paragraph(f"• {entry['date']}: {entry['task_name']} - {entry['description'][:100]}", style='List Bullet')
    else:
        doc.add_paragraph("No activities logged for this period.", style='List Bullet')
    
    doc.add_paragraph()
    
    # Major Deliverables
    doc.add_heading("4. MAJOR DELIVERABLES", level=1)
    
    if monthly_entries:
        for entry in monthly_entries:
            if entry.get('deliverables'):
                doc.add_paragraph(f"• {entry['date']}: {entry['deliverables'][:100]}", style='List Bullet')
    else:
        doc.add_paragraph("No deliverables reported for this period.", style='List Bullet')
    
    doc.add_paragraph()
    
    # Meetings Conducted
    doc.add_heading("5. MEETINGS CONDUCTED", level=1)
    doc.add_paragraph("• Daily stand-up meetings with ICARE Team (10:30-11:00 AM)")
    doc.add_paragraph(f"• Weekly review meeting with Nodal Officer: {university['nodal_officer']}")
    doc.add_paragraph("• Monthly coordination meeting with MITRA PMU")
    doc.add_paragraph("• Department-wise data collection meetings")
    
    doc.add_paragraph()
    
    # Risks and Issues
    doc.add_heading("6. RISKS AND ISSUES", level=1)
    doc.add_paragraph("• Timely data availability from certain departments remains a challenge")
    doc.add_paragraph("• Digitization of legacy data requires additional resources")
    doc.add_paragraph("• Coordination with multiple stakeholders requires proactive follow-ups")
    
    doc.add_paragraph()
    
    # Attendance Summary
    doc.add_heading("7. ATTENDANCE SUMMARY", level=1)
    
    att_table = doc.add_table(rows=4, cols=3)
    att_table.style = 'Table Grid'
    att_headers = ["Particulars", "Days", "Remarks"]
    for i, header in enumerate(att_headers):
        att_table.rows[0].cells[i].text = header
        att_table.rows[0].cells[i].paragraphs[0].runs[0].bold = True
    
    working_days = len(set(entry["date"] for entry in monthly_entries))
    att_table.rows[1].cells[0].text = "Total Working Days"
    att_table.rows[1].cells[1].text = str(working_days)
    att_table.rows[1].cells[2].text = "As per monthly calendar"
    
    att_table.rows[2].cells[0].text = "Present Days"
    att_table.rows[2].cells[1].text = str(working_days)
    att_table.rows[2].cells[2].text = "Full attendance maintained"
    
    att_table.rows[3].cells[0].text = "Leave / Absent"
    att_table.rows[3].cells[1].text = "0"
    att_table.rows[3].cells[2].text = "No leave taken"
    
    doc.add_paragraph()
    
    # Status of Initiatives
    doc.add_heading("8. STATUS OF INITIATIVES", level=1)
    doc.add_paragraph("1. Finalisation of Annual Action Plan: In Progress")
    doc.add_paragraph("2. Data Collection Framework: Implemented")
    doc.add_paragraph("3. Stakeholder Engagement: Ongoing")
    doc.add_paragraph("4. NIRF Data Compilation: In Progress")
    
    doc.add_paragraph()
    
    # Signatures Section - As per SOP
    doc.add_heading("9. APPROVALS AND SIGNATURES", level=1)
    
    sig_table = doc.add_table(rows=7, cols=2)
    sig_table.style = 'Table Grid'
    
    signatures = [
        ("Prepared by:", f"{coordinator_name}\n(Institutional Coordinator)"),
        ("Verified by:", f"{university['nodal_officer']}\n(Nodal Officer, IQAC Coordinator)"),
        ("Approved by:", f"{university['registrar']}\n(Registrar)"),
        ("Copy to:", f"{university['vc']}\n(Hon. Vice Chancellor)"),
        ("Reviewed by:", f"{ICARE_OFFICIALS['project_head']}\n(Project Head, ICARE Pvt. Ltd.)"),
        ("Approved by:", f"{MITRA_OFFICIALS['project_director']}\n(Project Director, MahaSTRIDE)"),
        ("Copy for information:", f"{MITRA_OFFICIALS['addl_chief_secretary']}\n{university['nodal_officer']}")
    ]
    
    for i, (role, name) in enumerate(signatures):
        sig_table.rows[i].cells[0].text = role
        sig_table.rows[i].cells[1].text = name
        sig_table.rows[i].cells[0].paragraphs[0].runs[0].bold = True
    
    doc.add_paragraph()
    
    # Footer
    footer = doc.add_paragraph()
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = footer.add_run("This report is submitted as per SOP Section 2 - Monthly Progress Report (MPR)")
    run.font.size = Pt(9)
    run.italic = True
    
    doc_bytes = BytesIO()
    doc.save(doc_bytes)
    doc_bytes.seek(0)
    return doc_bytes

def create_consolidated_mpr(year, month):
    """Generate consolidated MPR for all universities"""
    doc = Document()
    
    for section in doc.sections:
        section.top_margin = Inches(0.5)
        section.bottom_margin = Inches(0.5)
        section.left_margin = Inches(0.7)
        section.right_margin = Inches(0.7)
    
    # Confidential Header
    header_para = doc.add_paragraph()
    header_para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = header_para.add_run("Confidential")
    run.bold = True
    run.font.size = Pt(10)
    
    doc.add_paragraph()
    
    # MITRA Header
    mitra_header = doc.add_paragraph()
    mitra_header.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = mitra_header.add_run("Maharashtra Institution for Transformation (MITRA)")
    run.bold = True
    run.font.size = Pt(12)
    
    doc.add_paragraph()
    
    # Title
    title = doc.add_heading("CONSOLIDATED MONTHLY PROGRESS REPORT", 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    subtitle = doc.add_paragraph(f"All Maharashtra State Universities\nReporting Period: {datetime(year, month, 1).strftime('%B %Y')}")
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_paragraph()
    
    # Client Information
    doc.add_heading("1. CLIENT INFORMATION", level=1)
    info_table = doc.add_table(rows=6, cols=2)
    info_table.style = 'Table Grid'
    info_data = [
        ("Client Name", "Maharashtra Institution for Transformation (MITRA)"),
        ("Project Name", "Comprehensive Data Collection, Advanced Analytics, and Development of Performance Improvement Framework for Maharashtra State Universities"),
        ("Reporting Month", f"{datetime(year, month, 1).strftime('%B %Y')}"),
        ("Report Date", datetime.now().strftime("%d-%m-%Y")),
        ("Prepared By", ICARE_OFFICIALS["project_head"]),
        ("Submitted To", "PMU, MahaSTRIDE, MITRA")
    ]
    for i, (label, value) in enumerate(info_data):
        info_table.rows[i].cells[0].text = label
        info_table.rows[i].cells[1].text = value
        info_table.rows[i].cells[0].paragraphs[0].runs[0].bold = True
    
    doc.add_paragraph()
    
    # University-wise Progress Summary
    doc.add_heading("2. UNIVERSITY-WISE PROGRESS SUMMARY", level=1)
    
    summary_data = []
    for uni_code, uni_info in UNIVERSITIES.items():
        entries = get_monthly_summary(uni_code, year, month)
        tasks_completed = sum(1 for e in entries if e.get("status") == "completed")
        total_hours = sum(e.get("hours_spent", 0) for e in entries)
        summary_data.append({
            "University": uni_info["name"][:40], "Days Logged": len(entries),
            "Tasks Completed": tasks_completed, "Total Hours": total_hours,
            "Nodal Officer": uni_info["nodal_officer"]
        })
    
    summary_df = pd.DataFrame(summary_data)
    
    # Create summary table
    summary_table = doc.add_table(rows=len(summary_data) + 1, cols=5)
    summary_table.style = 'Table Grid'
    headers = ["Sr. No.", "University", "Days Logged", "Tasks Completed", "Nodal Officer"]
    
    header_row = summary_table.rows[0].cells
    for i, header in enumerate(headers):
        header_row[i].text = header
        header_row[i].paragraphs[0].runs[0].bold = True
    
    for i, row in summary_df.iterrows():
        row_cells = summary_table.rows[i + 1].cells
        row_cells[0].text = str(i + 1)
        row_cells[1].text = row["University"]
        row_cells[2].text = str(row["Days Logged"])
        row_cells[3].text = str(row["Tasks Completed"])
        row_cells[4].text = row["Nodal Officer"]
    
    doc.add_paragraph()
    
    # Overall Statistics
    doc.add_heading("3. OVERALL STATISTICS", level=1)
    
    total_entries = summary_df["Days Logged"].sum()
    total_tasks = summary_df["Tasks Completed"].sum()
    total_hours = summary_df["Total Hours"].sum()
    
    stats_table = doc.add_table(rows=5, cols=2)
    stats_table.style = 'Table Grid'
    stats_data = [
        ("Total Universities", str(len(UNIVERSITIES))),
        ("Total Days Logged", str(total_entries)),
        ("Total Tasks Completed", str(total_tasks)),
        ("Total Hours Invested", f"{total_hours:.1f} hours"),
        ("Average per University", f"{(total_entries/len(UNIVERSITIES)):.1f} days")
    ]
    for i, (label, value) in enumerate(stats_data):
        stats_table.rows[i].cells[0].text = label
        stats_table.rows[i].cells[1].text = value
        stats_table.rows[i].cells[0].paragraphs[0].runs[0].bold = True
    
    doc.add_paragraph()
    
    # Task Category Distribution
    doc.add_heading("4. TASK CATEGORY DISTRIBUTION", level=1)
    
    category_data = []
    for uni_code in UNIVERSITIES.keys():
        entries = get_monthly_summary(uni_code, year, month)
        for e in entries:
            category_data.append({"Category": e.get("task_category", "Other")})
    
    if category_data:
        category_df = pd.DataFrame(category_data)
        category_counts = category_df["Category"].value_counts()
        
        cat_table = doc.add_table(rows=len(category_counts) + 1, cols=2)
        cat_table.style = 'Table Grid'
        cat_table.rows[0].cells[0].text = "Task Category"
        cat_table.rows[0].cells[1].text = "Count"
        cat_table.rows[0].cells[0].paragraphs[0].runs[0].bold = True
        cat_table.rows[0].cells[1].paragraphs[0].runs[0].bold = True
        
        for i, (cat, count) in enumerate(category_counts.items()):
            cat_table.rows[i + 1].cells[0].text = cat
            cat_table.rows[i + 1].cells[1].text = str(count)
    
    doc.add_paragraph()
    
    # Key Observations
    doc.add_heading("5. KEY OBSERVATIONS", level=1)
    doc.add_paragraph("• All 7 universities have active data collection underway")
    doc.add_paragraph("• IQAC coordinators are effectively engaged with ICARE team")
    doc.add_paragraph("• Daily stand-up meetings (10:30-11:00 AM) with ICARE Team are being conducted regularly")
    doc.add_paragraph("• Data collection from academic, research, and placement cells progressing as per plan")
    doc.add_paragraph("• Weekly progress reports submitted to PMU, MahaSTRIDE")
    
    doc.add_paragraph()
    
    # Recommendations
    doc.add_heading("6. RECOMMENDATIONS", level=1)
    doc.add_paragraph("• Expedite data availability from financial departments")
    doc.add_paragraph("• Strengthen coordination with library and IT infrastructure teams")
    doc.add_paragraph("• Schedule additional review meetings for gap closure")
    
    doc.add_paragraph()
    
    # Signatures - Consolidated
    doc.add_heading("7. APPROVALS AND SIGNATURES", level=1)
    
    sig_table = doc.add_table(rows=5, cols=2)
    sig_table.style = 'Table Grid'
    
    signatures = [
        ("Prepared by:", f"{ICARE_OFFICIALS['project_head']}\n(Project Head, ICARE Pvt. Ltd.)"),
        ("Reviewed by:", f"{MITRA_OFFICIALS['project_director']}\n(Project Director, MahaSTRIDE)"),
        ("Approved by:", f"{MITRA_OFFICIALS['jt_ceo']}\n(Jt. CEO, MITRA)"),
        ("Copy to:", "Addl. Chief Secretary, Higher and Technical Education Department"),
        ("Copy to:", "Secretary to Hon. Governor Maharashtra")
    ]
    
    for i, (role, name) in enumerate(signatures):
        sig_table.rows[i].cells[0].text = role
        sig_table.rows[i].cells[1].text = name
        sig_table.rows[i].cells[0].paragraphs[0].runs[0].bold = True
    
    doc.add_paragraph()
    
    footer = doc.add_paragraph()
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = footer.add_run("This consolidated report is submitted as per SOP Section 2 - Monthly Progress Report (MPR)")
    run.font.size = Pt(9)
    run.italic = True
    
    doc_bytes = BytesIO()
    doc.save(doc_bytes)
    doc_bytes.seek(0)
    return doc_bytes

def show_sangam_info():
    st.markdown('<div class="sangam-card">', unsafe_allow_html=True)
    st.markdown("### 🎉 SANGAM Orientation & Training Program")
    st.markdown(f"**Dates:** May 5-6, 2026 | **Location:** Mumbai")
    st.markdown("✅ **Status:** Completed successfully")
    st.markdown('</div>', unsafe_allow_html=True)

def create_admin_dashboard():
    st.markdown('<div class="admin-card"><h2>📊 Admin Dashboard</h2><p>Complete Project Analytics & Infographics</p></div>', unsafe_allow_html=True)
    
    st.markdown('<span class="storage-status storage-connected">✅ Persistent Storage Active - Data is saved between sessions</span>', unsafe_allow_html=True)
    
    show_sangam_info()
    
    st.markdown("---")
    
    st.info(f"⏰ **Project Duration:** 2 Years ({PROJECT_START_DATE.strftime('%d-%b-%Y')} to {PROJECT_END_DATE.strftime('%d-%b-%Y')}) | **Working Hours:** {WORKING_HOURS}")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Project Start", PROJECT_START_DATE.strftime("%d-%b-%Y"))
    with col2:
        st.metric("Project End", PROJECT_END_DATE.strftime("%d-%b-%Y"))
    with col3:
        total_unis = len(UNIVERSITIES)
        st.metric("Universities", f"{total_unis}")
    with col4:
        days_elapsed = (datetime.now() - PROJECT_START_DATE).days
        st.metric("Days Elapsed", max(0, days_elapsed))
    
    st.markdown("---")
    
    # Infographics Section
    st.subheader("📊 Progress Infographics")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Daily Progress", "📅 Weekly Progress", "📆 Monthly Progress", "🏛️ University-wise", "📄 MPR Reports"])
    
    with tab1:
        st.markdown("### Daily Progress Overview")
        
        daily_df = get_daily_progress_data()
        if not daily_df.empty:
            daily_summary = daily_df.groupby("Date").agg({
                "Task": "count",
                "Hours": "sum"
            }).reset_index()
            daily_summary.columns = ["Date", "Tasks Logged", "Total Hours"]
            
            col1, col2 = st.columns(2)
            with col1:
                fig1 = px.bar(daily_summary, x="Date", y="Tasks Logged", title="Daily Tasks Logged", color="Tasks Logged", height=400)
                st.plotly_chart(fig1, use_container_width=True)
            with col2:
                fig2 = px.line(daily_summary, x="Date", y="Total Hours", title="Daily Hours Invested", markers=True, height=400)
                st.plotly_chart(fig2, use_container_width=True)
            
            st.dataframe(daily_summary.sort_values("Date", ascending=False), use_container_width=True)
        else:
            st.info("No data available yet")
    
    with tab2:
        st.markdown("### Weekly Progress Overview")
        
        weekly_df = get_weekly_progress_data()
        if not weekly_df.empty:
            weekly_agg = weekly_df.groupby("Week_Start").agg({
                "Total Hours": "sum",
                "Tasks Completed": "sum"
            }).reset_index()
            
            col1, col2 = st.columns(2)
            with col1:
                fig3 = px.bar(weekly_agg, x="Week_Start", y="Tasks Completed", title="Weekly Tasks Completed", color="Tasks Completed", height=400)
                st.plotly_chart(fig3, use_container_width=True)
            with col2:
                fig4 = px.line(weekly_agg, x="Week_Start", y="Total Hours", title="Weekly Hours Invested", markers=True, height=400)
                st.plotly_chart(fig4, use_container_width=True)
            
            st.subheader("University-wise Weekly Breakdown")
            st.dataframe(weekly_df.sort_values(["Week_Start", "University"]), use_container_width=True)
        else:
            st.info("No data available yet")
    
    with tab3:
        st.markdown("### Monthly Progress Overview")
        
        monthly_df = get_monthly_progress_data()
        if not monthly_df.empty:
            monthly_agg = monthly_df.groupby("Month_Name").agg({
                "Total Hours": "sum",
                "Tasks Completed": "sum"
            }).reset_index()
            
            col1, col2 = st.columns(2)
            with col1:
                fig5 = px.bar(monthly_agg, x="Month_Name", y="Tasks Completed", title="Monthly Tasks Completed", color="Tasks Completed", height=400)
                st.plotly_chart(fig5, use_container_width=True)
            with col2:
                fig6 = px.pie(monthly_agg, values="Total Hours", names="Month_Name", title="Monthly Hours Distribution", height=400)
                st.plotly_chart(fig6, use_container_width=True)
            
            st.subheader("University-wise Monthly Breakdown")
            st.dataframe(monthly_df.sort_values(["Year", "Month", "University"]), use_container_width=True)
        else:
            st.info("No data available yet")
    
    with tab4:
        st.markdown("### University-wise Progress")
        
        uni_progress = []
        for uni_code, uni_info in UNIVERSITIES.items():
            entries = get_university_entries(uni_code)
            if not entries.empty:
                total_tasks = len(entries)
                completed = len(entries[entries["Status"] == "COMPLETED"])
                total_hours = entries["Hours Spent"].sum() if "Hours Spent" in entries.columns else 0
                uni_progress.append({
                    "University": uni_info["name"],
                    "Nodal Officer": uni_info["nodal_officer"],
                    "Total Tasks": total_tasks,
                    "Completed": completed,
                    "Completion %": round(completed / total_tasks * 100, 1) if total_tasks > 0 else 0,
                    "Total Hours": total_hours
                })
        
        if uni_progress:
            uni_df = pd.DataFrame(uni_progress)
            
            col1, col2 = st.columns(2)
            with col1:
                fig7 = px.bar(uni_df, x="University", y="Completion %", title="University-wise Completion %", color="Completion %", text="Completion %", height=500)
                fig7.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                st.plotly_chart(fig7, use_container_width=True)
            with col2:
                fig8 = px.bar(uni_df, x="University", y="Total Hours", title="University-wise Total Hours", color="Total Hours", text="Total Hours", height=500)
                fig8.update_traces(texttemplate='%{text:.1f}', textposition='outside')
                st.plotly_chart(fig8, use_container_width=True)
            
            st.dataframe(uni_df, use_container_width=True)
        else:
            st.info("No data available yet")
    
    with tab5:
        st.markdown("### Monthly Progress Report (MPR)")
        st.markdown("Generate MPR for submission to MITRA as per SOP Section 2")
        
        col1, col2 = st.columns(2)
        with col1:
            report_year = st.selectbox("Select Year", [2026, 2027, 2028], key="admin_report_year")
            report_month = st.selectbox("Select Month", list(range(1, 13)), key="admin_report_month",
                                       format_func=lambda x: datetime(2000, x, 1).strftime("%B"))
            report_type = st.radio("Report Type", ["Individual University", "Consolidated (All Universities)"])
        
        with col2:
            if report_type == "Individual University":
                selected_uni = st.selectbox("Select University", list(UNIVERSITIES.keys()), format_func=lambda x: UNIVERSITIES[x]["name"])
        
        if st.button("📄 Generate MPR", use_container_width=True):
            with st.spinner("Generating MPR..."):
                if report_type == "Individual University":
                    doc_bytes = create_mpr_word_document(selected_uni, report_year, report_month, UNIVERSITIES[selected_uni]["coordinators"][0])
                    filename = f"MPR_{UNIVERSITIES[selected_uni]['name'].replace(' ', '_')}_{report_year}_{report_month:02d}.docx"
                else:
                    doc_bytes = create_consolidated_mpr(report_year, report_month)
                    filename = f"Consolidated_MPR_{report_year}_{report_month:02d}.docx"
                
                st.download_button("📥 Download MPR (Word)", doc_bytes, filename, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")

def create_project_lead_dashboard():
    st.markdown('<div class="projectlead-card"><h2>👨‍💼 Project Lead Dashboard - Dr. Harshal Kotwal</h2><p>Assign Tasks & Monitor Progress (2-Year Project)</p></div>', unsafe_allow_html=True)
    
    st.info(f"📅 **Project Duration:** {PROJECT_START_DATE.strftime('%d-%b-%Y')} to {PROJECT_END_DATE.strftime('%d-%b-%Y')} (2 Years)")
    
    show_sangam_info()
    
    st.markdown("---")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📅 Assign Task to Date", "📊 Progress Dashboard", "📝 Manage Assignments", "📈 Analytics"])
    
    with tab1:
        st.subheader("📅 Assign a Custom Task for Any Date")
        st.markdown("You can assign tasks for any date during the 2-year project period. Coordinators will see these as their assigned tasks.")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            with st.form("add_custom_task_form"):
                task_date = st.date_input("Select Date", min_value=PROJECT_START_DATE, max_value=PROJECT_END_DATE)
                task_category = st.selectbox("Task Category", ["Data Collection", "Meetings", "Documentation", "Analysis", "Training", "WFH", "Other"])
                task_name = st.text_input("Task Name")
                description = st.text_area("Task Description", height=100)
                deliverables = st.text_area("Expected Deliverables", height=80)
                
                if st.form_submit_button("Assign Task to Date"):
                    if task_name and description:
                        date_str = task_date.strftime("%Y-%m-%d")
                        add_custom_task_for_date(date_str, task_category, task_name, description, deliverables, "Dr. Harshal Kotwal")
                        st.success(f"Task assigned to {date_str} successfully!")
                        st.rerun()
                    else:
                        st.error("Please fill Task Name and Description")
        
        with col2:
            st.markdown("### Currently Assigned Custom Tasks")
            custom_tasks = load_custom_tasks_data()
            if custom_tasks["date_specific_tasks"]:
                for date_str, task in list(custom_tasks["date_specific_tasks"].items())[:10]:
                    with st.expander(f"📌 {date_str} - {task['task'][:40]}"):
                        st.markdown(f"**Category:** {task['task_category']}")
                        st.markdown(f"**Description:** {task['description'][:100]}...")
                        st.markdown(f"**Added:** {task['added_at'][:10]}")
            else:
                st.info("No custom tasks assigned yet")
    
    with tab2:
        st.subheader("📊 Coordinator Progress Overview")
        
        uni_progress = []
        for uni_code, uni_info in UNIVERSITIES.items():
            entries = get_university_entries(uni_code)
            if not entries.empty:
                total_tasks = len(entries)
                completed = len(entries[entries["Status"] == "COMPLETED"])
                uni_progress.append({
                    "University": uni_info["name"],
                    "Coordinator": ", ".join(uni_info["coordinators"]),
                    "Tasks Logged": total_tasks,
                    "Completed": completed,
                    "Completion %": round(completed / total_tasks * 100, 1) if total_tasks > 0 else 0,
                    "Nodal Officer": uni_info["nodal_officer"]
                })
        
        if uni_progress:
            uni_df = pd.DataFrame(uni_progress)
            fig = px.bar(uni_df, x="University", y="Completion %", title="University-wise Progress", color="Completion %", text="Completion %", height=500)
            fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(uni_df, use_container_width=True)
        else:
            st.info("No progress data available yet")
        
        st.markdown("---")
        st.subheader("Detailed University Logs")
        
        selected_uni = st.selectbox("Select University", list(UNIVERSITIES.keys()), format_func=lambda x: UNIVERSITIES[x]["name"])
        if selected_uni:
            df = get_university_entries(selected_uni)
            if not df.empty:
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No entries logged yet")
    
    with tab3:
        st.subheader("📝 Manage Assignments")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            with st.form("create_assignment"):
                st.markdown("### Create New Assignment")
                title = st.text_input("Assignment Title")
                description = st.text_area("Description")
                due_date = st.date_input("Due Date", min_value=datetime.now().date())
                assigned_unis = st.multiselect("Assign to Universities", list(UNIVERSITIES.keys()), format_func=lambda x: UNIVERSITIES[x]["name"])
                
                if st.form_submit_button("Create Assignment"):
                    if title and assigned_unis:
                        create_assignment(title, description, due_date.strftime("%Y-%m-%d"), assigned_unis, "Dr. Harshal Kotwal")
                        st.success("Assignment created!")
                        st.rerun()
        
        with col2:
            st.markdown("### Active Assignments")
            assignments_data = load_assignments_data()
            active = [a for a in assignments_data["assignments"] if a["status"] == "active"]
            if active:
                for a in active[-5:]:
                    st.markdown(f"**📌 {a['title']}** (Due: {a['due_date']})")
                    st.caption(f"Assigned to: {', '.join([UNIVERSITIES[c]['name'][:20] for c in a['assigned_universities']])}")
                    st.markdown("---")
            else:
                st.info("No active assignments")
    
    with tab4:
        st.subheader("📈 Advanced Analytics")
        
        daily_df = get_daily_progress_data()
        weekly_df = get_weekly_progress_data()
        monthly_df = get_monthly_progress_data()
        
        if not daily_df.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                daily_cumulative = daily_df.groupby("Date").size().cumsum().reset_index()
                daily_cumulative.columns = ["Date", "Cumulative Tasks"]
                fig_cum = px.area(daily_cumulative, x="Date", y="Cumulative Tasks", title="Cumulative Tasks Over Time", height=400)
                st.plotly_chart(fig_cum, use_container_width=True)
            
            with col2:
                hours_trend = daily_df.groupby("Date")["Hours"].sum().reset_index()
                fig_hours = px.line(hours_trend, x="Date", y="Hours", title="Daily Hours Trend", markers=True, height=400)
                st.plotly_chart(fig_hours, use_container_width=True)
            
            if not weekly_df.empty:
                weekly_pivot = weekly_df.pivot_table(index="University", columns="Week_Start", values="Tasks Completed", fill_value=0)
                fig_heatmap = px.imshow(weekly_pivot, title="Weekly Tasks Heatmap", height=500, color_continuous_scale="Viridis")
                st.plotly_chart(fig_heatmap, use_container_width=True)
            
            st.subheader("📥 Export Data")
            col1, col2 = st.columns(2)
            with col1:
                csv_daily = daily_df.to_csv(index=False)
                st.download_button("📊 Export Daily Data (CSV)", csv_daily, "daily_progress.csv", "text/csv")
            with col2:
                if not monthly_df.empty:
                    csv_monthly = monthly_df.to_csv(index=False)
                    st.download_button("📆 Export Monthly Data (CSV)", csv_monthly, "monthly_progress.csv", "text/csv")

def create_coordinator_dashboard(university_code, coordinator_name):
    st.markdown('<div class="info-card"><h2>📋 Coordinator Dashboard</h2><p>Log Your Daily Work</p></div>', unsafe_allow_html=True)
    
    uni_info = UNIVERSITIES[university_code]
    st.markdown(f"**🏛️ University:** {uni_info['name']}")
    st.markdown(f"**👤 Coordinator:** {coordinator_name}")
    st.markdown(f"**📌 Nodal Officer:** {uni_info['nodal_officer']}")
    
    st.info(f"⏰ **Working Hours:** {WORKING_HOURS} | Daily Stand-up: 10:30-11:00 AM with ICARE Team Only")
    
    st.markdown("---")
    
    st.subheader("📋 Daily Work Routine")
    st.markdown(DAILY_ROUTINE)
    
    st.markdown("---")
    
    with st.expander("📋 View Your Previous Entries", expanded=False):
        df = get_university_entries(university_code)
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No entries logged yet")
    
    st.markdown("---")
    
    st.subheader("📝 Log Today's Work")
    
    today_date = datetime.now().date()
    today_str = today_date.strftime("%Y-%m-%d")
    today_day = today_date.strftime("%A")
    
    existing_data = load_progress_data()
    already_logged = today_str in existing_data.get(university_code, {})
    
    plan_for_today = get_plan_for_date(today_str)
    
    if already_logged:
        st.warning(f"⚠️ You have already logged work for {today_str}. You can edit below.")
        
        existing_entry = existing_data[university_code][today_str]
        
        with st.form("edit_entry_form"):
            st.markdown("### Edit Today's Entry")
            
            task_category = st.selectbox("Task Category", ["Data Collection", "Meetings", "Documentation", "Analysis", "Training", "WFH", "Other"],
                                        index=["Data Collection", "Meetings", "Documentation", "Analysis", "Training", "WFH", "Other"].index(existing_entry.get("task_category", "Data Collection")) if existing_entry.get("task_category") in ["Data Collection", "Meetings", "Documentation", "Analysis", "Training", "WFH", "Other"] else 0)
            
            task_name = st.text_input("Task", value=existing_entry.get("task_name", ""))
            description = st.text_area("Detailed Description", value=existing_entry.get("description", ""), height=100)
            deliverables = st.text_area("Deliverables Produced", value=existing_entry.get("deliverables", ""), height=80)
            
            col1, col2 = st.columns(2)
            with col1:
                status = st.selectbox("Status", ["in_progress", "completed"], index=0 if existing_entry.get("status") == "in_progress" else 1)
            with col2:
                hours_spent = st.number_input("Hours Spent", min_value=0.5, max_value=12.0, step=0.5, value=float(existing_entry.get("hours_spent", 8)))
            
            remarks = st.text_area("Additional Remarks", value=existing_entry.get("remarks", ""))
            
            if st.form_submit_button("Update Entry"):
                if log_daily_entry(university_code, today_str, task_category, task_name, description, deliverables, status, hours_spent, remarks, False, False, coordinator_name):
                    st.success("Entry updated successfully!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("Failed to update entry")
    else:
        if plan_for_today:
            st.markdown(f"""
            <div class="default-task-card">
                <strong>📌 Your Assigned Task for Today ({today_day}, {today_str})</strong><br>
                <strong>Task:</strong> {plan_for_today['task']}<br>
                <strong>Category:</strong> {plan_for_today['task_category']}<br>
                <strong>Description:</strong> {plan_for_today['description']}<br>
                <strong>Expected Deliverables:</strong> {plan_for_today['deliverables']}
            </div>
            """, unsafe_allow_html=True)
            
            use_assigned = st.radio("", ["✅ Use Assigned Task", "🔄 Log Different Task"], horizontal=True)
        else:
            use_assigned = "🔄 Log Different Task"
            st.info(f"No assigned task for {today_str}. Please log your work below.")
        
        with st.form("daily_entry_form"):
            st.markdown("### Today's Work Log")
            
            if use_assigned == "✅ Use Assigned Task" and plan_for_today:
                task_category = plan_for_today['task_category']
                task_name = plan_for_today['task']
                description = plan_for_today['description']
                deliverables = plan_for_today['deliverables']
                st.info(f"Using assigned task: {task_name}")
                st.text_input("Task Category", value=task_category, disabled=True)
                st.text_input("Task", value=task_name, disabled=True)
            else:
                task_category = st.selectbox("Task Category", ["Data Collection", "Meetings", "Documentation", "Analysis", "Training", "WFH", "Other"])
                task_name = st.text_input("Task")
                description = st.text_area("Detailed Description", placeholder="Describe what you did today...", height=100)
                deliverables = st.text_area("Deliverables Produced", placeholder="What outputs/deliverables were created?", height=80)
            
            col1, col2 = st.columns(2)
            with col1:
                status = st.selectbox("Status", ["in_progress", "completed"])
            with col2:
                hours_spent = st.number_input("Hours Spent", min_value=0.5, max_value=12.0, step=0.5, value=8.0)
            
            remarks = st.text_area("Additional Remarks", placeholder="Any challenges, blockers, or notes...")
            
            if st.form_submit_button("Submit Daily Log"):
                if use_assigned == "✅ Use Assigned Task" and plan_for_today:
                    if log_daily_entry(university_code, today_str, plan_for_today['task_category'], plan_for_today['task'],
                                      plan_for_today['description'], plan_for_today['deliverables'], status, hours_spent, remarks, False, False, coordinator_name):
                        st.success("Daily work log submitted successfully!")
                        st.balloons()
                        st.rerun()
                else:
                    if task_name:
                        if log_daily_entry(university_code, today_str, task_category, task_name, description, deliverables, status, hours_spent, remarks, True, True, coordinator_name):
                            st.success("Daily work log submitted successfully!")
                            st.balloons()
                            st.rerun()
                    else:
                        st.error("Please fill Task field")
    
    st.markdown("---")
    
    st.subheader("📎 Pending Assignments")
    assignments = get_university_assignments(university_code)
    
    if assignments:
        for assignment in assignments:
            if assignment["submission_status"] != "completed":
                with st.container():
                    st.markdown(f"""
                    <div class="assignment-card">
                        <strong>📌 {assignment['title']}</strong><br>
                        <small>Due: {assignment['due_date']}</small><br>
                        <small>{assignment['description']}</small>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"Mark Complete", key=f"complete_{assignment['id']}"):
                        update_assignment_submission(assignment["id"], university_code, "completed", "", coordinator_name)
                        st.success("Assignment marked as completed!")
                        st.rerun()
    else:
        st.info("No pending assignments")
    
    st.markdown("---")
    st.subheader("📅 MPR Submission Reminder")
    st.warning("📋 **Note:** As per SOP Section 1 & 2, approved attendance and MPR must reach PMU MahaSTRIDE by the 10th of each month.")

def main():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    
    if not st.session_state["authenticated"]:
        with st.container():
            st.markdown('<div class="main-header"><h1>🔐 mahaSTRIDE NIRF Data Collection Tracker</h1><p>2-Year Project Progress Monitoring System</p></div>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.markdown("### Login")
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                
                if st.button("Login", type="primary", use_container_width=True):
                    if email and password:
                        success, role, name, university = authenticate_user(email, password)
                        if success:
                            st.session_state["authenticated"] = True
                            st.session_state["user_email"] = email
                            st.session_state["user_role"] = role
                            st.session_state["user_name"] = name
                            if university:
                                st.session_state["user_university"] = university
                            st.rerun()
                        else:
                            st.error("Invalid email or password")
                    else:
                        st.warning("Please enter both email and password")
                
                st.markdown("---")
                st.markdown("### Demo Credentials")
                st.markdown("""
                **Admin:** admin@mahastride.com / Admin@2026<br>
                **Project Lead:** projectlead@mahastride.com / ProjectLead@2026<br>
                **Coordinators:** (Password: Name@2026)<br>
                - sneha@mu.edu (Mumbai University)<br>
                - jagan@sspu.edu (SPPU Pune)<br>
                - vaibhav@coep.edu (COEP Tech)<br>
                - pratham@au.edu (Amravati University)<br>
                - anjali@nu.edu (Nagpur University)<br>
                - nitish@kbcnmu.edu (KBCNMU Jalgaon)<br>
                - atharv@bamu.edu (BAMU Aurangabad)
                """, unsafe_allow_html=True)
        return
    
    user_role = st.session_state["user_role"]
    user_name = st.session_state["user_name"]
    
    with st.sidebar:
        st.title("📊 mahaSTRIDE")
        st.markdown(f"**Welcome, {user_name}**")
        
        if user_role == "admin":
            st.markdown("*Role: Admin*")
        elif user_role == "project_lead":
            st.markdown("*Role: Project Lead (Dr. Harshal Kotwal)*")
        else:
            st.markdown("*Role: Coordinator*")
            if "user_university" in st.session_state:
                uni = st.session_state["user_university"]
                st.markdown(f"*University: {UNIVERSITIES[uni]['name'][:30]}...*")
        
        st.markdown("---")
        st.markdown(f"**Today:** {datetime.now().strftime('%d-%b-%Y')}")
        st.markdown(f"**Project:** {PROJECT_START_DATE.strftime('%d-%b-%Y')} to {PROJECT_END_DATE.strftime('%d-%b-%Y')}")
        
        st.markdown("---")
        
        if user_role == "admin":
            menu = st.radio("Navigation", ["📊 Admin Dashboard", "📄 MPR Reports", "ℹ️ About"])
        elif user_role == "project_lead":
            menu = st.radio("Navigation", ["👨‍💼 Project Lead Dashboard", "📝 Assignments", "📊 Analytics", "ℹ️ About"])
        else:
            menu = st.radio("Navigation", ["📋 Log Work", "📊 My Progress", "ℹ️ About"])
        
        st.markdown("---")
        st.caption(f"⏰ {WORKING_HOURS}")
        st.caption("🔄 Stand-up: 10:30-11:00 AM")
        st.caption("📅 2-Year Project")
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            for key in ["authenticated", "user_email", "user_role", "user_name", "user_university"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    
    if user_role == "admin":
        if menu == "📊 Admin Dashboard":
            create_admin_dashboard()
        elif menu == "📄 MPR Reports":
            st.title("📄 Monthly Progress Reports")
            col1, col2 = st.columns(2)
            with col1:
                report_year = st.selectbox("Year", [2026, 2027, 2028])
                report_month = st.selectbox("Month", list(range(1, 13)), format_func=lambda x: datetime(2000, x, 1).strftime("%B"))
            with col2:
                report_type = st.radio("Report Type", ["Individual University", "Consolidated (All Universities)"])
                if report_type == "Individual University":
                    selected_uni = st.selectbox("University", list(UNIVERSITIES.keys()), format_func=lambda x: UNIVERSITIES[x]["name"])
            
            if st.button("Generate MPR"):
                with st.spinner("Generating..."):
                    if report_type == "Individual University":
                        doc_bytes = create_mpr_word_document(selected_uni, report_year, report_month, UNIVERSITIES[selected_uni]["coordinators"][0])
                        filename = f"MPR_{UNIVERSITIES[selected_uni]['name'].replace(' ', '_')}_{report_year}_{report_month:02d}.docx"
                    else:
                        doc_bytes = create_consolidated_mpr(report_year, report_month)
                        filename = f"Consolidated_MPR_{report_year}_{report_month:02d}.docx"
                    
                    st.download_button("Download MPR", doc_bytes, filename, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        else:
            st.title("ℹ️ About")
            st.markdown(f"""
            ### mahaSTRIDE Project Tracker
            
            **Project Duration:** 2 Years ({PROJECT_START_DATE.strftime('%d-%b-%Y')} to {PROJECT_END_DATE.strftime('%d-%b-%Y')})
            
            **Participating Universities:**
            {chr(10).join([f"• {uni['name']} (Nodal Officer: {uni['nodal_officer']})" for uni in UNIVERSITIES.values()])}
            
            **Features:**
            - Daily progress logging by coordinators
            - Weekly and monthly progress visualizations
            - Automated MPR generation in Word format
            - Consolidated reports for MITRA submission
            - 2-year project timeline support
            """)
    
    elif user_role == "project_lead":
        if menu == "👨‍💼 Project Lead Dashboard":
            create_project_lead_dashboard()
        elif menu == "📝 Assignments":
            st.title("📝 Manage Assignments")
            
            col1, col2 = st.columns([1, 1])
            with col1:
                with st.form("create_assignment"):
                    title = st.text_input("Title")
                    description = st.text_area("Description")
                    due_date = st.date_input("Due Date")
                    assigned_unis = st.multiselect("Assign to", list(UNIVERSITIES.keys()), format_func=lambda x: UNIVERSITIES[x]["name"])
                    if st.form_submit_button("Create"):
                        if title and assigned_unis:
                            create_assignment(title, description, due_date.strftime("%Y-%m-%d"), assigned_unis, "Dr. Harshal Kotwal")
                            st.success("Assignment created!")
                            st.rerun()
            with col2:
                st.markdown("### Active Assignments")
                assignments_data = load_assignments_data()
                active = [a for a in assignments_data["assignments"] if a["status"] == "active"]
                for a in active:
                    st.markdown(f"**📌 {a['title']}** (Due: {a['due_date']})")
        elif menu == "📊 Analytics":
            st.title("📊 Analytics Dashboard")
            
            daily_df = get_daily_progress_data()
            if not daily_df.empty:
                fig = px.line(daily_df.groupby("Date").size().reset_index(), x="Date", y=0, title="Daily Activity Trend", markers=True)
                st.plotly_chart(fig, use_container_width=True)
                
                uni_progress = []
                for uni_code in UNIVERSITIES.keys():
                    entries = get_university_entries(uni_code)
                    if not entries.empty:
                        uni_progress.append({"University": UNIVERSITIES[uni_code]["name"], "Tasks": len(entries)})
                if uni_progress:
                    fig2 = px.bar(pd.DataFrame(uni_progress), x="University", y="Tasks", title="Tasks by University")
                    st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("No data available yet")
        else:
            st.title("ℹ️ About")
            st.markdown("### Project Lead Dashboard\n\n**Features:**\n- Assign tasks to specific dates\n- Monitor coordinator progress\n- Create and manage assignments\n- Generate progress reports\n- 2-year project timeline support")
    
    else:  # coordinator
        university_code = st.session_state.get("user_university")
        if not university_code:
            st.error("University not assigned. Please contact admin.")
        else:
            if menu == "📋 Log Work":
                create_coordinator_dashboard(university_code, user_name)
            elif menu == "📊 My Progress":
                st.title("📊 My Progress")
                df = get_university_entries(university_code)
                if not df.empty:
                    st.dataframe(df, use_container_width=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        completed = len(df[df["Status"] == "COMPLETED"])
                        st.metric("Completed Tasks", completed)
                    with col2:
                        total_hours = df["Hours Spent"].sum() if "Hours Spent" in df.columns else 0
                        st.metric("Total Hours", f"{total_hours:.1f}")
                    
                    if "Task Category" in df.columns:
                        task_counts = df["Task Category"].value_counts()
                        fig = px.pie(values=task_counts.values, names=task_counts.index, title="Task Distribution", hole=0.3)
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No entries logged yet")
            else:
                st.title("ℹ️ About")
                st.markdown(f"""
                ### Coordinator Dashboard
                
                **University:** {UNIVERSITIES[university_code]['name']}
                **Nodal Officer:** {UNIVERSITIES[university_code]['nodal_officer']}
                
                **Daily Schedule:**
                - 10:00 AM: Report to university
                - 10:30-11:00 AM: Stand-up with ICARE Team
                - 6:00 PM: Departure
                
                **Responsibilities:**
                - Log daily work activities
                - Submit deliverables
                - Complete assignments
                - Prepare MPR inputs
                """)

if __name__ == "__main__":
    for file in [PROGRESS_DATA_FILE, ASSIGNMENTS_DATA_FILE, CUSTOM_TASKS_DATA_FILE, ATTENDANCE_DATA_FILE]:
        if not os.path.exists(file):
            if file == PROGRESS_DATA_FILE:
                save_progress_data(create_initial_progress_data())
            elif file == ASSIGNMENTS_DATA_FILE:
                save_assignments_data(create_initial_assignments_data())
            elif file == CUSTOM_TASKS_DATA_FILE:
                save_custom_tasks_data(create_initial_custom_tasks_data())
            else:
                save_attendance_data(create_initial_attendance_data())
    
    main()
