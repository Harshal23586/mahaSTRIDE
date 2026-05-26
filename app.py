import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
import json
from hashlib import sha256

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
    .wfh-badge {
        background-color: #cfe2ff;
        color: #084298;
        padding: 0.2rem 0.5rem;
        border-radius: 5px;
        font-size: 0.8rem;
        display: inline-block;
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
    .weekend-badge {
        background-color: #f8d7da;
        color: #721c24;
        padding: 0.2rem 0.5rem;
        border-radius: 5px;
        font-size: 0.8rem;
        display: inline-block;
    }
    .working-day-badge {
        background-color: #d4edda;
        color: #155724;
        padding: 0.2rem 0.5rem;
        border-radius: 5px;
        font-size: 0.8rem;
        display: inline-block;
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
    .edit-task-card {
        background-color: #fff3e0;
        border-left: 4px solid #ff9800;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# User credentials
USERS = {
    "admin@mahastride.com": {
        "password": sha256("Admin@2026".encode()).hexdigest(),
        "role": "admin",
        "name": "Admin",
        "permissions": "full"
    },
    "projectlead@mahastride.com": {
        "password": sha256("ProjectLead@2026".encode()).hexdigest(),
        "role": "project_lead",
        "name": "Dr. Harshal Kotwal",
        "permissions": "edit_all"
    },
    # Coordinators (Project Leads for respective universities - can edit their own)
    "sneha@mu.edu": {
        "password": sha256("Coord@2026".encode()).hexdigest(),
        "role": "coordinator",
        "name": "Ms Sneha",
        "university": "MU",
        "permissions": "self"
    },
    "shubham@mu.edu": {
        "password": sha256("Coord@2026".encode()).hexdigest(),
        "role": "coordinator",
        "name": "Shubham",
        "university": "MU",
        "permissions": "self"
    },
    "jagan@sspu.edu": {
        "password": sha256("Coord@2026".encode()).hexdigest(),
        "role": "coordinator",
        "name": "Mr Jagan",
        "university": "SSPU",
        "permissions": "self"
    },
    "vaibhav@coep.edu": {
        "password": sha256("Coord@2026".encode()).hexdigest(),
        "role": "coordinator",
        "name": "Mr Vaibhav",
        "university": "COEP",
        "permissions": "self"
    },
    "pratham@au.edu": {
        "password": sha256("Coord@2026".encode()).hexdigest(),
        "role": "coordinator",
        "name": "Mr Pratham",
        "university": "AU",
        "permissions": "self"
    },
    "anjali@nu.edu": {
        "password": sha256("Coord@2026".encode()).hexdigest(),
        "role": "coordinator",
        "name": "Ms Anjali",
        "university": "NU",
        "permissions": "self"
    },
    "nitish@kbcnmu.edu": {
        "password": sha256("Coord@2026".encode()).hexdigest(),
        "role": "coordinator",
        "name": "Mr Nitish",
        "university": "KBCNMU",
        "permissions": "self"
    },
    "atharv@bamu.edu": {
        "password": sha256("Coord@2026".encode()).hexdigest(),
        "role": "coordinator",
        "name": "Mr Atharv",
        "university": "BAMU",
        "permissions": "self"
    }
}

# University to Project Lead mapping
UNIVERSITY_LEAD_MAPPING = {
    "MU": "sneha@mu.edu",
    "SSPU": "jagan@sspu.edu",
    "COEP": "vaibhav@coep.edu",
    "AU": "pratham@au.edu",
    "NU": "anjali@nu.edu",
    "KBCNMU": "nitish@kbcnmu.edu",
    "BAMU": "atharv@bamu.edu",
}

# NIRF Data Collection Tasks (7 May - 30 May 2026)
# Working days: Monday to Saturday (Sunday off) | Saturdays have meaningful WFH tasks
NIRF_TASK_SCHEDULE = {
    1: {"date": "2026-05-07", "day_name": "Thursday", "day_type": "Onsite", "task": "Join university, meet VC & Registrar, introduce role. Meet Nodal Officer & ICARE Team to confirm workspace, access, and data sources.", "deliverable": "Introduction email to PMU & ICARE Head. Meeting minutes.", "framework": "Setup"},
    2: {"date": "2026-05-08", "day_name": "Friday", "day_type": "Onsite", "task": "With Nodal Officer & ICARE Team, map all NIRF-related data sources: admission, academic, research, placement, finance, outreach. Identify missing data owners.", "deliverable": "NIRF Data Source Map (university-specific).", "framework": "Setup"},
    3: {"date": "2026-05-09", "day_name": "Saturday", "day_type": "WFH", "task": "WFH: Review NIRF data templates. Create digital data collection forms. Organize department-wise data request letters.", "deliverable": "Digital forms created. Data request letters drafted.", "framework": "Setup"},
    4: {"date": "2026-05-10", "day_name": "Sunday", "day_type": "Off", "task": "Weekly off", "deliverable": "No work", "framework": "Holiday"},
    5: {"date": "2026-05-11", "day_name": "Monday", "day_type": "Onsite", "task": "Create NIRF Data Gap Template for FY 2022-23, 2023-24, 2024-25. Share with Nodal Officer & ICARE Team for validation.", "deliverable": "Gap template v1.0.", "framework": "Setup"},
    6: {"date": "2026-05-12", "day_name": "Tuesday", "day_type": "Onsite", "task": "Meet HoD (Academic) & Exam Cell - collect student enrollment, graduation, and backlog data.", "deliverable": "Raw data files saved.", "framework": "Data Collection"},
    7: {"date": "2026-05-13", "day_name": "Wednesday", "day_type": "Onsite", "task": "Meet Faculty/HR department - collect faculty count, designation, PhD qualification, experience.", "deliverable": "Faculty master data.", "framework": "Data Collection"},
    8: {"date": "2026-05-14", "day_name": "Thursday", "day_type": "Onsite", "task": "Meet Research Cell - collect publications (Scopus/WoS/PubMed/UGC CARE), citations, patents, sponsored research projects.", "deliverable": "Research output spreadsheet.", "framework": "Data Collection"},
    9: {"date": "2026-05-15", "day_name": "Friday", "day_type": "Onsite", "task": "Meet Placement Cell - collect placement data, median salary, higher education admission data.", "deliverable": "Placement & higher ed data.", "framework": "Data Collection"},
    10: {"date": "2026-05-16", "day_name": "Saturday", "day_type": "WFH", "task": "WFH: Digitize collected data. Create data validation scripts. Prepare weekly progress report for ICARE Team.", "deliverable": "Digitized dataset. Weekly report submitted.", "framework": "Data Collection"},
    11: {"date": "2026-05-17", "day_name": "Sunday", "day_type": "Off", "task": "Weekly off", "deliverable": "No work", "framework": "Holiday"},
    12: {"date": "2026-05-18", "day_name": "Monday", "day_type": "Onsite", "task": "Meet Finance/Accounts - collect financial data: research expenditure, infrastructure spending, university income.", "deliverable": "Finance data file.", "framework": "Data Collection"},
    13: {"date": "2026-05-19", "day_name": "Tuesday", "day_type": "Onsite", "task": "Meet Library/IT - collect e-resources, digital repository, library subscriptions, IT infrastructure details.", "deliverable": "Library & IT data.", "framework": "Data Collection"},
    14: {"date": "2026-05-20", "day_name": "Wednesday", "day_type": "Onsite", "task": "Consolidate all collected data. Cross-verify with Nodal Officer & ICARE Team. Identify major gaps.", "deliverable": "Consolidated university dataset v1.", "framework": "Validation"},
    15: {"date": "2026-05-21", "day_name": "Thursday", "day_type": "Onsite", "task": "Prepare NIRF gap report - list missing data, incomplete years, inconsistent formats. Share with Nodal Officer & VC.", "deliverable": "Gap report submitted to Nodal Officer.", "framework": "Reporting"},
    16: {"date": "2026-05-22", "day_name": "Friday", "day_type": "Onsite", "task": "Work with Nodal Officer & ICARE Team to assign responsibility for each gap to specific department heads.", "deliverable": "Responsibility matrix.", "framework": "Action Plan"},
    17: {"date": "2026-05-23", "day_name": "Saturday", "day_type": "WFH", "task": "WFH: Analyze gap report. Create action plan templates. Prepare follow-up email drafts for departments.", "deliverable": "Action plan templates. Follow-up email drafts.", "framework": "Action Plan"},
    18: {"date": "2026-05-24", "day_name": "Sunday", "day_type": "Off", "task": "Weekly off", "deliverable": "No work", "framework": "Holiday"},
    19: {"date": "2026-05-25", "day_name": "Monday", "day_type": "Onsite", "task": "Follow up with departments for missing data. Assist them in extracting data in NIRF-required format.", "deliverable": "Updated data files.", "framework": "Data Collection"},
    20: {"date": "2026-05-26", "day_name": "Tuesday", "day_type": "Onsite", "task": "Validate data consistency (enrollment totals, faculty counts match department lists).", "deliverable": "Validation log.", "framework": "Validation"},
    21: {"date": "2026-05-27", "day_name": "Wednesday", "day_type": "Onsite", "task": "Prepare first draft of NIRF data template as per NIRF 2026 format. Share with Nodal Officer & ICARE Team for review.", "deliverable": "Draft NIRF submission file.", "framework": "Reporting"},
    22: {"date": "2026-05-28", "day_name": "Thursday", "day_type": "Onsite", "task": "Conduct review meeting with Nodal Officer, ICARE Team & IQAC team. Document pending items and action owners.", "deliverable": "Meeting minutes.", "framework": "Review"},
    23: {"date": "2026-05-29", "day_name": "Friday", "day_type": "Onsite", "task": "Finalize data collection status for May 2026. Prepare inputs for Monthly Progress Report (MPR).", "deliverable": "MPR inputs (to ICARE Head).", "framework": "Reporting"},
    24: {"date": "2026-05-30", "day_name": "Saturday", "day_type": "WFH", "task": "WFH: Finalize May MPR. Compile all deliverables. Prepare for June action plan. Submit end-of-month report.", "deliverable": "May MPR final. End-of-month report.", "framework": "Reporting"},
}

# Daily Work Routine - Updated with correct stand-up timing
DAILY_ROUTINE = """
| Time | Activity |
|------|----------|
| 10:00 AM | Report to university / IQAC cell |
| 10:00-10:30 AM | Prepare for daily stand-up; review pending tasks |
| 10:30-11:00 AM | **Daily stand-up with Nodal Officer & ICARE Team** |
| 11:00 AM-1:00 PM | Data collection / meetings with departments |
| 1:00-2:00 PM | Lunch |
| 2:00-5:30 PM | Data validation, gap analysis, documentation |
| 5:30-6:00 PM | Update daily tracker; email summary to ICARE Project Head |
| 6:00 PM | Departure |
"""

# Saturday WFH Routine
SATURDAY_WFH_ROUTINE = """
| Time | Activity |
|------|----------|
| 10:00 AM | Log in remotely; check emails and messages |
| 10:00-10:30 AM | Virtual stand-up with ICARE Team |
| 10:30 AM-1:00 PM | WFH Tasks: Data digitization, analysis, documentation |
| 1:00-2:00 PM | Lunch break |
| 2:00-5:30 PM | Complete assigned WFH deliverables; data validation |
| 5:30-6:00 PM | Update tracker; submit WFH completion report |
| 6:00 PM | Sign off |
"""

# Universities data
UNIVERSITIES = {
    "MU": {"name": "Mumbai University", "coordinators": "Ms Sneha, Shubham"},
    "SSPU": {"name": "SSPU Pune", "coordinators": "Mr Jagan"},
    "COEP": {"name": "COEP Tech University", "coordinators": "Mr Vaibhav"},
    "AU": {"name": "Amravati University", "coordinators": "Mr Pratham"},
    "NU": {"name": "Nagpur University", "coordinators": "Ms Anjali"},
    "KBCNMU": {"name": "KBCNMU Jalgaon University", "coordinators": "Mr Nitish"},
    "BAMU": {"name": "BAMU University Aurangabad", "coordinators": "Mr Atharv"},
}

# Working hours
WORKING_HOURS = "10:00 AM - 6:00 PM"
WORKING_HOURS_NOTE = "Monday-Friday: Onsite at University | Saturday: Work from Home"

# Project dates
SANGAM_DATE_START = datetime(2026, 5, 5)
SANGAM_DATE_END = datetime(2026, 5, 6)
PROJECT_START_DATE = datetime(2026, 5, 7)  # First working day after Sangam

def get_working_date(working_day_number):
    """Convert working day number to actual calendar date"""
    current_date = PROJECT_START_DATE
    working_days_counted = 0
    
    while working_days_counted < working_day_number:
        if current_date.weekday() != 6:  # Sunday is weekend
            working_days_counted += 1
            if working_days_counted == working_day_number:
                return current_date
        current_date += timedelta(days=1)
    
    return current_date

def is_saturday(date):
    return date.weekday() == 5

def is_sunday(date):
    return date.weekday() == 6

def get_day_type(date):
    if date.weekday() == 5:
        return "Working Day (WFH)"
    elif date.weekday() == 6:
        return "Weekend (Off)"
    else:
        return "Working Day (Onsite)"

def get_current_working_day():
    """Get current working day number (Monday-Saturday only)"""
    today = datetime.now()
    
    if today < PROJECT_START_DATE:
        return 0
    
    current_date = PROJECT_START_DATE
    working_days_counted = 0
    
    while current_date <= today:
        if current_date.weekday() != 6:  # Monday to Saturday
            working_days_counted += 1
        current_date += timedelta(days=1)
    
    return min(working_days_counted, len(NIRF_TASK_SCHEDULE))

# Data file paths
PROGRESS_DATA_FILE = "nirf_progress_data.json"
ASSIGNMENTS_DATA_FILE = "nirf_assignments_data.json"

def hash_password(password):
    return sha256(password.encode()).hexdigest()

def authenticate_user(email, password):
    if email in USERS:
        if USERS[email]["password"] == hash_password(password):
            return True, USERS[email]["role"], USERS[email]["name"], USERS[email].get("permissions", "self")
    return False, None, None, None

def create_initial_progress_data():
    data = {}
    for uni_code in UNIVERSITIES.keys():
        data[uni_code] = {}
        for day in NIRF_TASK_SCHEDULE.keys():
            data[uni_code][str(day)] = {
                "status": "pending",
                "remarks": "",
                "deliverable_submitted": False,
                "task_description": NIRF_TASK_SCHEDULE[day]["task"],
                "deliverable_description": NIRF_TASK_SCHEDULE[day]["deliverable"],
                "updated_at": None,
                "updated_by": None
            }
    return data

def create_initial_assignments_data():
    return {
        "assignments": [],
        "submissions": {}
    }

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

def update_task_status(university_code, day, status, remarks="", deliverable_submitted=False, updated_by=""):
    data = load_progress_data()
    if university_code in data and str(day) in data[university_code]:
        data[university_code][str(day)]["status"] = status
        if remarks:
            data[university_code][str(day)]["remarks"] = remarks
        data[university_code][str(day)]["deliverable_submitted"] = deliverable_submitted
        data[university_code][str(day)]["updated_at"] = datetime.now().isoformat()
        data[university_code][str(day)]["updated_by"] = updated_by
        return save_progress_data(data)
    return False

def update_task_details(university_code, day, task_description, deliverable_description, updated_by=""):
    """Project Lead function to modify task details"""
    data = load_progress_data()
    if university_code in data and str(day) in data[university_code]:
        data[university_code][str(day)]["task_description"] = task_description
        data[university_code][str(day)]["deliverable_description"] = deliverable_description
        data[university_code][str(day)]["updated_at"] = datetime.now().isoformat()
        data[university_code][str(day)]["updated_by"] = updated_by
        return save_progress_data(data)
    return False

def get_university_progress(university_code):
    data = load_progress_data()
    if university_code not in data:
        return pd.DataFrame()
    
    records = []
    for day, task_info in NIRF_TASK_SCHEDULE.items():
        task_data = data[university_code].get(str(day), {})
        status = task_data.get("status", "pending")
        
        records.append({
            "Day": day,
            "Date": task_info["date"],
            "Day Name": task_info["day_name"],
            "Day Type": task_info["day_type"],
            "Framework": task_info["framework"],
            "Task": task_data.get("task_description", task_info["task"]),
            "Deliverable": task_data.get("deliverable_description", task_info["deliverable"]),
            "Status": status.upper(),
            "Status_Code": status,
            "Deliverable Submitted": "✅" if task_data.get("deliverable_submitted", False) else "❌",
            "Working Hours": WORKING_HOURS,
            "Remarks": task_data.get("remarks", ""),
            "Last Updated": task_data.get("updated_at", "")[:10] if task_data.get("updated_at") else "",
            "Updated By": task_data.get("updated_by", "")
        })
    return pd.DataFrame(records)

def get_summary_stats():
    data = load_progress_data()
    stats = []
    
    for uni_code, uni_info in UNIVERSITIES.items():
        uni_data = data.get(uni_code, {})
        total = len(NIRF_TASK_SCHEDULE)
        # Count only working days (not holidays) for completion tracking
        working_days = [d for d, info in NIRF_TASK_SCHEDULE.items() if info["framework"] != "Holiday"]
        total_working = len(working_days)
        
        completed = sum(1 for d in working_days if uni_data.get(str(d), {}).get("status") == "completed")
        in_progress = sum(1 for d in working_days if uni_data.get(str(d), {}).get("status") == "in_progress")
        pending = total_working - completed - in_progress
        
        current_working_day = get_current_working_day()
        expected_completion = (current_working_day / total_working * 100) if current_working_day > 0 else 0
        actual_completion = (completed / total_working * 100) if total_working > 0 else 0
        is_on_track = actual_completion >= expected_completion - 10
        
        stats.append({
            "University": uni_info["name"],
            "Code": uni_code,
            "Coordinators": uni_info["coordinators"],
            "Completed": completed,
            "In Progress": in_progress,
            "Pending": pending,
            "Completion %": round((completed / total_working * 100), 1),
            "On Track": "✅ Yes" if is_on_track else "⚠️ Behind"
        })
    
    return pd.DataFrame(stats)

def create_assignment(title, description, due_date, assigned_universities, created_by):
    assignments_data = load_assignments_data()
    
    assignment_id = f"ASSIGN_{len(assignments_data['assignments']) + 1}_{int(datetime.now().timestamp())}"
    
    new_assignment = {
        "id": assignment_id,
        "title": title,
        "description": description,
        "due_date": due_date,
        "assigned_universities": assigned_universities,
        "created_by": created_by,
        "created_at": datetime.now().isoformat(),
        "status": "active"
    }
    
    assignments_data["assignments"].append(new_assignment)
    
    if assignment_id not in assignments_data["submissions"]:
        assignments_data["submissions"][assignment_id] = {}
        for uni_code in assigned_universities:
            assignments_data["submissions"][assignment_id][uni_code] = {
                "status": "pending",
                "completed_at": None,
                "remarks": "",
                "completed_by": None
            }
    
    save_assignments_data(assignments_data)
    return assignment_id

def update_assignment_submission(assignment_id, university_code, status, remarks="", completed_by=""):
    assignments_data = load_assignments_data()
    
    if assignment_id in assignments_data["submissions"]:
        if university_code in assignments_data["submissions"][assignment_id]:
            assignments_data["submissions"][assignment_id][university_code] = {
                "status": status,
                "completed_at": datetime.now().isoformat() if status == "completed" else None,
                "remarks": remarks,
                "completed_by": completed_by
            }
            return save_assignments_data(assignments_data)
    return False

def get_university_assignments(university_code):
    assignments_data = load_assignments_data()
    university_assignments = []
    
    for assignment in assignments_data["assignments"]:
        if assignment["status"] == "active" and university_code in assignment["assigned_universities"]:
            submission = assignments_data["submissions"].get(assignment["id"], {}).get(university_code, {})
            assignment_copy = assignment.copy()
            assignment_copy["submission_status"] = submission.get("status", "pending")
            assignment_copy["submission_remarks"] = submission.get("remarks", "")
            assignment_copy["completed_at"] = submission.get("completed_at", "")
            university_assignments.append(assignment_copy)
    
    return university_assignments

def get_all_assignments_with_status():
    assignments_data = load_assignments_data()
    result = []
    
    for assignment in assignments_data["assignments"]:
        if assignment["status"] == "active":
            for uni_code in assignment["assigned_universities"]:
                submission = assignments_data["submissions"].get(assignment["id"], {}).get(uni_code, {})
                result.append({
                    "assignment_id": assignment["id"],
                    "title": assignment["title"],
                    "description": assignment["description"],
                    "due_date": assignment["due_date"],
                    "university": UNIVERSITIES[uni_code]["name"],
                    "university_code": uni_code,
                    "submission_status": submission.get("status", "pending"),
                    "submission_remarks": submission.get("remarks", ""),
                    "completed_at": submission.get("completed_at", ""),
                    "created_at": assignment["created_at"],
                    "created_by": assignment["created_by"]
                })
    
    return pd.DataFrame(result)

def delete_assignment(assignment_id):
    assignments_data = load_assignments_data()
    
    for assignment in assignments_data["assignments"]:
        if assignment["id"] == assignment_id:
            assignment["status"] = "inactive"
            return save_assignments_data(assignments_data)
    return False

def show_sangam_info():
    st.markdown('<div class="sangam-card">', unsafe_allow_html=True)
    st.markdown("### 🎉 SANGAM Orientation & Training Program")
    st.markdown(f"**Dates:** May 5-6, 2026 | **Location:** Mumbai")
    st.markdown("**Agenda Included:**")
    st.markdown("""
    - Project overview and MahaSTRIDE framework introduction
    - NIRF data collection methodology and standards
    - Role clarification for Institutional Coordinators
    - IQAC collaboration and ICARE Team engagement
    - Hands-on training on data templates and validation
    - Q&A and university-specific planning
    """)
    st.markdown("✅ **Status:** Completed successfully")
    st.markdown('</div>', unsafe_allow_html=True)

def create_admin_dashboard():
    st.markdown('<div class="admin-card"><h2>📊 Admin Dashboard - NIRF Data Collection Tracker</h2><p>Complete Project Analytics & Insights</p></div>', unsafe_allow_html=True)
    
    st.markdown('<span class="storage-status storage-connected">✅ Persistent Storage Active - Data is saved between sessions</span>', unsafe_allow_html=True)
    
    show_sangam_info()
    
    st.markdown("---")
    
    st.info(f"⏰ **Working Hours:** {WORKING_HOURS} | {WORKING_HOURS_NOTE}")
    
    st.markdown("---")
    
    current_working_day = get_current_working_day()
    total_working_days = len([d for d, info in NIRF_TASK_SCHEDULE.items() if info["framework"] != "Holiday"])
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Working Day", f"{current_working_day}/{total_working_days}")
    with col2:
        st.metric("Project Start", PROJECT_START_DATE.strftime("%d-%b-%Y"))
    with col3:
        last_date = get_working_date(total_working_days)
        st.metric("Phase End", last_date.strftime("%d-%b-%Y"))
    with col4:
        days_left = total_working_days - current_working_day if current_working_day > 0 else total_working_days
        st.metric("Working Days Left", days_left)
    with col5:
        st.metric("Universities", len(UNIVERSITIES))
    
    st.info(f"📅 **Working Schedule:** Monday to Saturday (Sunday off) | Saturdays are Work from Home | Hours: {WORKING_HOURS}")
    
    st.markdown("---")
    
    st.subheader("🎯 Key Performance Indicators")
    summary_df = get_summary_stats()
    
    if not summary_df.empty:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            total_completed = summary_df["Completed"].sum()
            total_possible = len([d for d in NIRF_TASK_SCHEDULE if NIRF_TASK_SCHEDULE[d]["framework"] != "Holiday"]) * len(UNIVERSITIES)
            st.metric("✅ Total Tasks Completed", f"{total_completed}/{total_possible}", delta=f"{(total_completed/total_possible*100):.1f}%")
        with col2:
            avg_completion = summary_df["Completion %"].mean()
            st.metric("📊 Avg Completion", f"{avg_completion:.1f}%")
        with col3:
            on_track_count = len(summary_df[summary_df["On Track"] == "✅ Yes"])
            st.metric("🏆 On Track", f"{on_track_count}/{len(UNIVERSITIES)}")
        with col4:
            best_uni = summary_df.loc[summary_df["Completion %"].idxmax(), "University"]
            st.metric("🥇 Top Performer", best_uni[:20])
    
    st.markdown("---")
    
    st.subheader("📋 Daily Work Routine")
    st.markdown(DAILY_ROUTINE)
    
    st.subheader("🏠 Saturday WFH Routine")
    st.markdown(SATURDAY_WFH_ROUTINE)
    
    st.markdown("---")
    
    st.subheader("📅 NIRF Task Progress Heatmap")
    
    data = load_progress_data()
    heatmap_data = []
    for uni_code, uni_info in UNIVERSITIES.items():
        uni_data = data.get(uni_code, {})
        for day, task_info in NIRF_TASK_SCHEDULE.items():
            if task_info["framework"] != "Holiday":
                task_data = uni_data.get(str(day), {})
                status = task_data.get("status", "pending")
                status_value = 2 if status == "completed" else 1 if status == "in_progress" else 0
                heatmap_data.append({
                    "University": uni_info["name"],
                    "Day": day,
                    "Date": task_info["date"],
                    "Status": status_value
                })
    
    heatmap_df = pd.DataFrame(heatmap_data)
    pivot_data = heatmap_df.pivot(index="University", columns="Day", values="Status")
    
    fig = px.imshow(
        pivot_data,
        color_continuous_scale=["red", "yellow", "green"],
        aspect="auto",
        title="Task Progress Heatmap (Red=Pending, Yellow=In Progress, Green=Completed)",
        labels=dict(x="Working Day", y="University", color="Status")
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("📈 Performance Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = px.bar(
            summary_df, 
            x="University", 
            y="Completion %", 
            color="Completion %",
            color_continuous_scale="Viridis",
            title="Completion % by University",
            text="Completion %",
            height=400
        )
        fig1.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        framework_df = pd.DataFrame()
        for uni_code, uni_info in UNIVERSITIES.items():
            uni_data = data.get(uni_code, {})
            for framework in ["Setup", "Data Collection", "Validation", "Reporting", "Action Plan", "Review"]:
                days = [d for d, info in NIRF_TASK_SCHEDULE.items() if info["framework"] == framework]
                if days:
                    completed = sum(1 for d in days if uni_data.get(str(d), {}).get("status") == "completed")
                    percentage = (completed / len(days) * 100)
                    framework_df = pd.concat([framework_df, pd.DataFrame([{
                        "University": uni_info["name"],
                        "Framework": framework,
                        "Percentage": percentage
                    }])])
        
        if not framework_df.empty:
            framework_avg = framework_df.groupby("Framework")["Percentage"].mean().reset_index()
            fig2 = px.bar(
                framework_avg, 
                x="Framework", 
                y="Percentage", 
                color="Percentage",
                color_continuous_scale="Plasma",
                title="Average Framework Completion",
                text="Percentage",
                height=400
            )
            fig2.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            st.plotly_chart(fig2, use_container_width=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        status_counts = {
            "Completed": summary_df["Completed"].sum(),
            "In Progress": summary_df["In Progress"].sum(),
            "Pending": summary_df["Pending"].sum()
        }
        fig3 = px.pie(
            values=list(status_counts.values()), 
            names=list(status_counts.keys()),
            title="Overall Task Status Distribution",
            color_discrete_sequence=["#90EE90", "#FFD700", "#FFB6C1"],
            hole=0.3,
            height=400
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with col4:
        daily_progress = []
        for day in NIRF_TASK_SCHEDULE.keys():
            if NIRF_TASK_SCHEDULE[day]["framework"] != "Holiday":
                completed = sum(1 for uni_data in data.values() if uni_data.get(str(day), {}).get("status") == "completed")
                daily_progress.append({"Working Day": day, "Completed": completed})
        daily_df = pd.DataFrame(daily_progress)
        
        fig4 = px.line(
            daily_df, 
            x="Working Day", 
            y="Completed", 
            markers=True,
            title="Daily Tasks Completed Across All Universities",
            height=400
        )
        fig4.update_traces(line=dict(color='green', width=3), marker=dict(size=8))
        st.plotly_chart(fig4, use_container_width=True)
    
    st.subheader("🏆 University Rankings")
    ranking_df = summary_df[["University", "Completion %", "Completed", "In Progress", "Pending", "On Track"]].sort_values("Completion %", ascending=False)
    ranking_df.index = range(1, len(ranking_df) + 1)
    st.dataframe(ranking_df, use_container_width=True)
    
    st.subheader("🔄 Recent Activity Log")
    recent_updates = []
    for uni_code, uni_data in data.items():
        for day_str, task_data in uni_data.items():
            if task_data.get("updated_at"):
                day = int(day_str)
                if day in NIRF_TASK_SCHEDULE:
                    recent_updates.append({
                        "University": UNIVERSITIES[uni_code]["name"],
                        "Working Day": day,
                        "Date": NIRF_TASK_SCHEDULE[day]["date"],
                        "Task": task_data.get("task_description", NIRF_TASK_SCHEDULE[day]["task"])[:50] + "...",
                        "Status": task_data.get("status", "").upper(),
                        "Updated By": task_data.get("updated_by", ""),
                        "Updated At": task_data["updated_at"]
                    })
    
    if recent_updates:
        recent_df = pd.DataFrame(recent_updates).sort_values("Updated At", ascending=False).head(20)
        st.dataframe(recent_df, use_container_width=True)
    else:
        st.info("No updates recorded yet")
    
    st.subheader("💾 Export Data")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📥 Export Complete Report (CSV)", use_container_width=True):
            all_data = []
            for uni_code in UNIVERSITIES.keys():
                df = get_university_progress(uni_code)
                df["University"] = UNIVERSITIES[uni_code]["name"]
                all_data.append(df)
            if all_data:
                combined = pd.concat(all_data, ignore_index=True)
                csv = combined.to_csv(index=False)
                st.download_button("Download CSV", csv, "nirf_progress_data.csv", "text/csv")
    with col2:
        if st.button("📊 Export Summary Report (CSV)", use_container_width=True):
            csv = summary_df.to_csv(index=False)
            st.download_button("Download CSV", csv, "nirf_summary_report.csv", "text/csv")

def create_project_lead_dashboard(user_email):
    """Project Lead (Dr Harshal Kotwal) Dashboard - can edit all coordinators' tasks"""
    st.markdown('<div class="projectlead-card"><h2>👨‍💼 Project Lead Dashboard - Dr. Harshal Kotwal</h2><p>Manage all coordinators, modify tasks, track progress</p></div>', unsafe_allow_html=True)
    
    st.info(f"⏰ **Working Hours:** {WORKING_HOURS} | {WORKING_HOURS_NOTE}")
    
    show_sangam_info()
    
    st.markdown("---")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("📊 Quick Stats")
        summary_df = get_summary_stats()
        if not summary_df.empty:
            total_completed = summary_df["Completed"].sum()
            total_possible = len([d for d in NIRF_TASK_SCHEDULE if NIRF_TASK_SCHEDULE[d]["framework"] != "Holiday"]) * len(UNIVERSITIES)
            st.metric("Overall Progress", f"{(total_completed/total_possible*100):.1f}%")
    
    with col2:
        st.subheader("📋 Daily Work Routine")
        st.markdown(DAILY_ROUTINE)
        st.markdown(SATURDAY_WFH_ROUTINE)
    
    st.markdown("---")
    
    # Select university to manage
    selected_uni_code = st.selectbox(
        "Select University to Manage",
        list(UNIVERSITIES.keys()),
        format_func=lambda x: f"{UNIVERSITIES[x]['name']} - Lead: {UNIVERSITIES[x]['coordinators']}"
    )
    
    if selected_uni_code:
        st.markdown(f"### 📋 Tasks for {UNIVERSITIES[selected_uni_code]['name']}")
        
        df = get_university_progress(selected_uni_code)
        
        if not df.empty:
            working_days_df = df[df["Day Type"] != "Weekend (Off)"]
            
            col1, col2, col3, col4 = st.columns(4)
            total_working = len(working_days_df)
            completed = len(working_days_df[working_days_df["Status"] == "COMPLETED"])
            in_progress = len(working_days_df[working_days_df["Status"] == "IN PROGRESS"])
            
            with col1:
                st.metric("✅ Completed", completed)
            with col2:
                st.metric("🔄 In Progress", in_progress)
            with col3:
                st.metric("⏳ Pending", total_working - completed - in_progress)
            with col4:
                st.metric("📊 Progress", f"{(completed/total_working*100):.1f}%")
            
            st.progress(completed/total_working)
            
            st.markdown("---")
            
            # Two tabs: Update Status and Edit Tasks
            tab1, tab2 = st.tabs(["📝 Update Task Status", "✏️ Modify Task Details"])
            
            with tab1:
                st.subheader("Update Task Status for Coordinator")
                
                pending_tasks = working_days_df[working_days_df["Status_Code"].isin(["pending", "in_progress"])]
                
                if not pending_tasks.empty:
                    selected_day = st.selectbox(
                        "Select Task to Update",
                        pending_tasks["Day"].tolist(),
                        key="update_status_select",
                        format_func=lambda x: f"Day {x}: {pending_tasks[pending_tasks['Day']==x]['Date'].iloc[0]} - {pending_tasks[pending_tasks['Day']==x]['Task'].iloc[0][:60]}..."
                    )
                    
                    task_data = pending_tasks[pending_tasks["Day"] == selected_day].iloc[0]
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.info(f"**Current Status:** {task_data['Status']}")
                    with col2:
                        st.warning(f"**Date:** {task_data['Date']} ({task_data['Day Name']}) - {task_data['Day Type']}")
                    
                    st.markdown(f"**Task:** {task_data['Task']}")
                    st.markdown(f"**Deliverable:** {task_data['Deliverable']}")
                    
                    new_status = st.radio(
                        "Update Status To:",
                        ["in_progress", "completed"],
                        key="status_update_radio",
                        format_func=lambda x: "🔄 In Progress" if x == "in_progress" else "✅ Completed"
                    )
                    
                    deliverable_submitted = st.checkbox("Deliverable submitted?", key="deliverable_check")
                    remarks = st.text_area("Remarks (for coordinator)", placeholder="Add instructions or feedback for the coordinator...")
                    
                    if st.button("🚀 Update Status", type="primary", use_container_width=True):
                        if update_task_status(selected_uni_code, selected_day, new_status, remarks, deliverable_submitted, user_email):
                            st.success(f"✅ Task status updated to {new_status.upper()} successfully!")
                            st.balloons()
                            st.rerun()
                        else:
                            st.error("❌ Failed to update status")
                else:
                    st.success("🎉 All tasks completed for this university!")
            
            with tab2:
                st.subheader("✏️ Modify Task Details (Customize for Coordinator)")
                st.markdown("As Project Lead, you can modify task descriptions and deliverables for any coordinator.")
                
                all_tasks = working_days_df[working_days_df["Day Type"] != "Off"]
                
                selected_day_edit = st.selectbox(
                    "Select Task to Modify",
                    all_tasks["Day"].tolist(),
                    key="edit_task_select",
                    format_func=lambda x: f"Day {x}: {all_tasks[all_tasks['Day']==x]['Date'].iloc[0]} - {all_tasks[all_tasks['Day']==x]['Task'].iloc[0][:50]}..."
                )
                
                if selected_day_edit:
                    task_data_edit = all_tasks[all_tasks["Day"] == selected_day_edit].iloc[0]
                    
                    with st.container():
                        st.markdown('<div class="edit-task-card">', unsafe_allow_html=True)
                        
                        new_task_desc = st.text_area(
                            "Task Description",
                            value=task_data_edit["Task"],
                            height=100,
                            key="task_desc_edit"
                        )
                        
                        new_deliverable = st.text_area(
                            "Deliverable",
                            value=task_data_edit["Deliverable"],
                            height=80,
                            key="deliverable_edit"
                        )
                        
                        edit_remarks = st.text_area(
                            "Modification Note (reason for change)",
                            placeholder="Explain why this task is being modified...",
                            key="edit_remarks"
                        )
                        
                        if st.button("💾 Save Task Modifications", type="primary", use_container_width=True):
                            if update_task_details(selected_uni_code, selected_day_edit, new_task_desc, new_deliverable, user_email):
                                st.success(f"✅ Task details modified successfully for Day {selected_day_edit}!")
                                if edit_remarks:
                                    st.info(f"Note: {edit_remarks}")
                                st.rerun()
                            else:
                                st.error("❌ Failed to save modifications")
                        
                        st.markdown('</div>', unsafe_allow_html=True)
            
            with st.expander("📋 View All Tasks"):
                display_df = df[["Day", "Date", "Day Name", "Day Type", "Framework", "Task", "Deliverable", "Status", "Deliverable Submitted", "Remarks", "Updated By"]]
                st.dataframe(display_df, use_container_width=True)
        
        st.markdown("---")
        st.subheader("📎 Manage Assignments for this University")
        
        assignments = get_university_assignments(selected_uni_code)
        
        col1, col2 = st.columns([1, 2])
        with col1:
            with st.form("create_assignment_form_lead"):
                title = st.text_input("Assignment Title")
                description = st.text_area("Description")
                due_date = st.date_input("Due Date")
                
                if st.form_submit_button("Create Assignment"):
                    if title:
                        create_assignment(title, description, due_date.strftime("%Y-%m-%d"), [selected_uni_code], user_email)
                        st.success("Assignment created successfully!")
                        st.rerun()
                    else:
                        st.error("Please enter title")
        
        with col2:
            if assignments:
                for assignment in assignments:
                    with st.container():
                        st.markdown(f"""
                        <div class="assignment-card">
                            <strong>📌 {assignment['title']}</strong><br>
                            <small>Due: {assignment['due_date']}</small><br>
                            <small>{assignment['description']}</small><br>
                            <small>Status: {assignment['submission_status'].upper()}</small>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if assignment["submission_status"] != "completed":
                            if st.button(f"Mark as Completed", key=f"lead_complete_{assignment['id']}"):
                                update_assignment_submission(assignment["id"], selected_uni_code, "completed", "Marked complete by Project Lead", user_email)
                                st.success("Assignment marked as completed!")
                                st.rerun()
            else:
                st.info("No pending assignments for this university.")
        
        st.markdown("---")
        st.subheader("📅 MPR Submission Reminder")
        st.warning("📋 **Note:** As per SOP Section 1 & 2, approved attendance and MPR must reach PMU MahaSTRIDE by the 10th of each month. Ensure coordinators prepare MPR inputs.")

def create_coordinator_dashboard(user_email, university_code):
    """Coordinator Dashboard - can only edit own tasks"""
    st.markdown('<div class="info-card"><h2>📋 Coordinator Dashboard</h2><p>Your NIRF Data Collection Tasks</p></div>', unsafe_allow_html=True)
    
    st.info(f"🏛️ **University:** {UNIVERSITIES[university_code]['name']}")
    st.info(f"⏰ **Working Hours:** {WORKING_HOURS} | {WORKING_HOURS_NOTE}")
    
    show_sangam_info()
    
    st.markdown("---")
    
    st.subheader("📋 Daily Work Routine")
    st.markdown(DAILY_ROUTINE)
    
    st.subheader("🏠 Saturday WFH Routine")
    st.markdown(SATURDAY_WFH_ROUTINE)
    
    st.markdown("---")
    
    df = get_university_progress(university_code)
    
    if not df.empty:
        working_days_df = df[df["Day Type"] != "Weekend (Off)"]
        
        col1, col2, col3, col4 = st.columns(4)
        total_working = len(working_days_df)
        completed = len(working_days_df[working_days_df["Status"] == "COMPLETED"])
        in_progress = len(working_days_df[working_days_df["Status"] == "IN PROGRESS"])
        
        with col1:
            st.metric("✅ Completed", completed, delta=f"{(completed/total_working*100):.1f}%")
        with col2:
            st.metric("🔄 In Progress", in_progress)
        with col3:
            st.metric("⏳ Pending", total_working - completed - in_progress)
        with col4:
            st.metric("📊 Progress", f"{(completed/total_working*100):.1f}%")
        
        st.progress(completed/total_working)
        
        st.markdown("---")
        st.subheader("✏️ Update Your Task Status")
        
        pending_tasks = working_days_df[working_days_df["Status_Code"].isin(["pending", "in_progress"])]
        
        if not pending_tasks.empty:
            selected_day = st.selectbox(
                "Select Task to Update",
                pending_tasks["Day"].tolist(),
                format_func=lambda x: f"Day {x}: {pending_tasks[pending_tasks['Day']==x]['Date'].iloc[0]} ({pending_tasks[pending_tasks['Day']==x]['Day Name'].iloc[0]}) - {pending_tasks[pending_tasks['Day']==x]['Task'].iloc[0][:60]}..."
            )
            
            task_data = pending_tasks[pending_tasks["Day"] == selected_day].iloc[0]
            
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"**Framework:** {task_data['Framework']}\n\n**Current Status:** {task_data['Status']}")
            with col2:
                st.warning(f"**Date:** {task_data['Date']} ({task_data['Day Name']}) - {task_data['Day Type']}")
            
            st.markdown(f"**📝 Task:** {task_data['Task']}")
            st.markdown(f"**📎 Deliverable:** {task_data['Deliverable']}")
            
            new_status = st.radio(
                "Update Status To:",
                ["in_progress", "completed"],
                format_func=lambda x: "🔄 In Progress" if x == "in_progress" else "✅ Completed"
            )
            
            deliverable_submitted = st.checkbox("Deliverable submitted?")
            remarks = st.text_area("Remarks (optional)", placeholder="Add any notes about this task or deliverable...")
            
            if st.button("🚀 Update Status", type="primary", use_container_width=True):
                if update_task_status(university_code, selected_day, new_status, remarks, deliverable_submitted, user_email):
                    st.success(f"✅ Task status updated to {new_status.upper()} successfully!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ Failed to update status")
        else:
            st.success("🎉 Congratulations! All tasks are completed!")
        
        with st.expander("📋 View All Your Tasks"):
            display_df = df[["Day", "Date", "Day Name", "Day Type", "Framework", "Task", "Deliverable", "Status", "Deliverable Submitted", "Remarks"]]
            st.dataframe(display_df, use_container_width=True)
        
        st.markdown("---")
        st.subheader("📎 Admin/Project Lead Assignments")
        
        assignments = get_university_assignments(university_code)
        
        if assignments:
            for assignment in assignments:
                with st.container():
                    st.markdown(f"""
                    <div class="assignment-card">
                        <strong>📌 {assignment['title']}</strong><br>
                        <small>Due: {assignment['due_date']}</small><br>
                        <small>{assignment['description']}</small><br>
                        <small>Status: {assignment['submission_status'].upper()}</small>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if assignment["submission_status"] != "completed":
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            assign_remarks = st.text_input(f"Remarks for {assignment['title']}", key=f"assign_remarks_{assignment['id']}")
                        with col2:
                            if st.button(f"Mark Complete", key=f"complete_{assignment['id']}"):
                                update_assignment_submission(assignment["id"], university_code, "completed", assign_remarks, user_email)
                                st.success("Assignment marked as completed!")
                                st.rerun()
        else:
            st.info("No pending assignments.")
        
        st.markdown("---")
        st.subheader("📅 MPR Submission Reminder")
        st.warning("📋 **Note:** As per SOP Section 1 & 2, approved attendance and MPR must reach PMU MahaSTRIDE by the 10th of each month. Please prepare your MPR inputs by end of month.")
        
        st.markdown("---")
        st.subheader("✅ End of Day Checklist")
        st.markdown("""
        Before departure at **6:00 PM**, please ensure:
        - [ ] Daily tracker updated
        - [ ] Email summary sent to ICARE Project Head
        - [ ] All meetings attended and minutes recorded
        - [ ] Tomorrow's schedule confirmed with Nodal Officer & ICARE Team
        """)

def create_data_analyst_dashboard(user_email):
    """Data Analyst Dashboard - monitoring only"""
    st.markdown('<div class="info-card"><h2>📊 Data Analyst Dashboard</h2><p>Monitor university progress</p></div>', unsafe_allow_html=True)
    
    assigned_universities = [code for code, email in UNIVERSITY_LEAD_MAPPING.items() if email == user_email]
    
    if not assigned_universities:
        st.warning("No universities assigned to you. Please contact admin.")
        return
    
    selected_uni_code = st.selectbox(
        "Select University", 
        assigned_universities,
        format_func=lambda x: UNIVERSITIES[x]["name"]
    )
    
    if selected_uni_code:
        df = get_university_progress(selected_uni_code)
        
        if not df.empty:
            working_days_df = df[df["Day Type"] != "Weekend (Off)"]
            
            col1, col2, col3 = st.columns(3)
            completed = len(working_days_df[working_days_df["Status"] == "COMPLETED"])
            in_progress = len(working_days_df[working_days_df["Status"] == "IN PROGRESS"])
            total = len(working_days_df)
            
            with col1:
                st.metric("✅ Completed", completed)
            with col2:
                st.metric("🔄 In Progress", in_progress)
            with col3:
                st.metric("📊 Progress", f"{(completed/total*100):.1f}%")
            
            st.progress(completed/total)
            
            st.subheader("📋 Task Progress")
            display_df = df[["Day", "Date", "Day Name", "Day Type", "Framework", "Task", "Status", "Deliverable Submitted", "Remarks"]]
            st.dataframe(display_df, use_container_width=True)
            
            st.subheader("📊 Framework Summary")
            framework_summary = df[df["Day Type"] != "Weekend (Off)"].groupby("Framework")["Status"].value_counts().unstack().fillna(0)
            st.dataframe(framework_summary, use_container_width=True)

def main():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    
    if not st.session_state["authenticated"]:
        with st.container():
            st.markdown('<div class="main-header"><h1>🔐 mahaSTRIDE NIRF Data Collection Tracker</h1><p>Institutional Coordinator Progress Monitoring System</p></div>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.markdown("### Login")
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                
                if st.button("Login", type="primary", use_container_width=True):
                    if email and password:
                        success, role, name, permissions = authenticate_user(email, password)
                        if success:
                            st.session_state["authenticated"] = True
                            st.session_state["user_email"] = email
                            st.session_state["user_role"] = role
                            st.session_state["user_name"] = name
                            st.session_state["user_permissions"] = permissions
                            if role == "coordinator":
                                st.session_state["user_university"] = USERS[email].get("university")
                            st.rerun()
                        else:
                            st.error("Invalid email or password")
                    else:
                        st.warning("Please enter both email and password")
                
                st.markdown("---")
                st.markdown("### Demo Credentials")
                st.markdown("""
                **Admin:** admin@mahastride.com / Admin@2026<br>
                **Project Lead (Dr. Harshal Kotwal):** projectlead@mahastride.com / ProjectLead@2026<br>
                **Coordinator (MU):** sneha@mu.edu / Coord@2026<br>
                """, unsafe_allow_html=True)
        return
    
    user_role = st.session_state["user_role"]
    user_name = st.session_state["user_name"]
    user_email = st.session_state["user_email"]
    
    with st.sidebar:
        st.title("📊 mahaSTRIDE")
        st.markdown(f"**Welcome, {user_name}**")
        
        if user_role == "project_lead":
            st.markdown("*Role: Project Lead (Dr. Harshal Kotwal)*")
            st.markdown("*Permissions: Can edit all coordinator tasks*")
        else:
            st.markdown(f"*Role: {user_role.title()}*")
        
        st.markdown("---")
        
        current_working_day = get_current_working_day()
        total_working = len([d for d, info in NIRF_TASK_SCHEDULE.items() if info["framework"] != "Holiday"])
        st.markdown(f"**Working Day:** {current_working_day}/{total_working}")
        
        st.markdown("---")
        
        if user_role == "admin":
            menu = st.radio("Navigation", ["Admin Dashboard", "Manage Assignments", "University Details", "About"])
        elif user_role == "project_lead":
            menu = st.radio("Navigation", ["Project Lead Dashboard", "Manage All Universities", "About"])
        elif user_role == "coordinator":
            menu = st.radio("Navigation", ["My Dashboard", "My Tasks", "About"])
        else:
            menu = st.radio("Navigation", ["Analyst Dashboard", "University Progress", "About"])
        
        st.markdown("---")
        
        summary_df = get_summary_stats()
        if not summary_df.empty:
            total_completed = summary_df["Completed"].sum()
            total_possible = total_working * len(UNIVERSITIES)
            overall_pct = (total_completed / total_possible * 100) if total_possible > 0 else 0
            st.metric("Overall Progress", f"{overall_pct:.1f}%")
            st.progress(overall_pct / 100)
        
        st.markdown("---")
        st.caption(f"⏰ Working Hours: {WORKING_HOURS}")
        st.caption("🔄 Stand-up: 10:30-11:00 AM with Nodal Officer & ICARE Team")
        st.caption("🚪 Departure: 6:00 PM")
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            for key in ["authenticated", "user_email", "user_role", "user_name", "user_university", "user_permissions"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    
    if user_role == "admin":
        if menu == "Admin Dashboard":
            create_admin_dashboard()
        elif menu == "Manage Assignments":
            st.title("📝 Manage Assignments")
            
            tab1, tab2, tab3 = st.tabs(["Create Assignment", "View Assignments", "Track Submissions"])
            
            with tab1:
                with st.form("create_assignment_form"):
                    title = st.text_input("Assignment Title")
                    description = st.text_area("Description")
                    due_date = st.date_input("Due Date")
                    assigned_universities = st.multiselect(
                        "Assign to Universities",
                        list(UNIVERSITIES.keys()),
                        format_func=lambda x: UNIVERSITIES[x]["name"]
                    )
                    
                    if st.form_submit_button("Create Assignment"):
                        if title and assigned_universities:
                            create_assignment(title, description, due_date.strftime("%Y-%m-%d"), assigned_universities, user_email)
                            st.success("Assignment created successfully!")
                        else:
                            st.error("Please fill all required fields")
            
            with tab2:
                assignments_data = load_assignments_data()
                if assignments_data["assignments"]:
                    for assignment in assignments_data["assignments"]:
                        if assignment["status"] == "active":
                            with st.expander(f"📌 {assignment['title']}"):
                                st.write(f"**Description:** {assignment['description']}")
                                st.write(f"**Due Date:** {assignment['due_date']}")
                                st.write(f"**Assigned To:** {', '.join([UNIVERSITIES[code]['name'] for code in assignment['assigned_universities']])}")
                                st.write(f"**Created:** {assignment['created_at'][:10]}")
                                if st.button(f"Delete Assignment", key=f"del_{assignment['id']}"):
                                    delete_assignment(assignment['id'])
                                    st.rerun()
                else:
                    st.info("No active assignments")
            
            with tab3:
                submissions_df = get_all_assignments_with_status()
                if not submissions_df.empty:
                    st.dataframe(submissions_df, use_container_width=True)
                else:
                    st.info("No submissions yet")
        elif menu == "University Details":
            st.title("🏛️ University Details")
            summary_df = get_summary_stats()
            if not summary_df.empty:
                st.dataframe(summary_df, use_container_width=True)
        else:
            st.title("ℹ️ About")
            st.markdown(f"""
            ### mahaSTRIDE NIRF Data Collection Tracker
            
            **Project Lead:** Dr. Harshal Kotwal  
            **Sangam Orientation:** May 5-6, 2026  
            **Project Start:** May 7, 2026  
            
            **Working Schedule:** 
            - Monday to Friday: Onsite at University (10:00 AM - 6:00 PM)
            - Saturday: Work from Home (10:00 AM - 6:00 PM)
            - Sunday: Weekly off
            
            **Daily Stand-up:** 10:30 AM - 11:00 AM with Nodal Officer & ICARE Team
            **Daily Departure:** 6:00 PM
            
            **Roles:**
            - **Admin:** Full system access
            - **Project Lead (Dr. Harshal Kotwal):** Can modify tasks for any coordinator
            - **Coordinators:** Update own tasks only
            
            ### Demo Credentials:
            - **Admin:** admin@mahastride.com / Admin@2026
            - **Project Lead:** projectlead@mahastride.com / ProjectLead@2026
            - **Coordinator:** sneha@mu.edu / Coord@2026
            """)
    
    elif user_role == "project_lead":
        if menu == "Project Lead Dashboard":
            create_project_lead_dashboard(user_email)
        elif menu == "Manage All Universities":
            st.title("🏛️ All Universities Progress")
            summary_df = get_summary_stats()
            if not summary_df.empty:
                st.dataframe(summary_df, use_container_width=True)
                
                fig = px.bar(
                    summary_df,
                    x="University",
                    y="Completion %",
                    color="Completion %",
                    text="Completion %",
                    title="University-wise Progress"
                )
                fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.title("ℹ️ About")
            st.markdown("""
            ### Project Lead Dashboard - Dr. Harshal Kotwal
            
            **Your Permissions:**
            - View progress of all universities
            - Modify task descriptions and deliverables for any coordinator
            - Update task status for any coordinator
            - Create and manage assignments for all universities
            - Override task completions if needed
            
            **Features:**
            - Edit Task Details tab allows you to customize tasks per university
            - Create assignments for specific universities
            - Track overall project progress
            """)
    
    elif user_role == "coordinator":
        university_code = st.session_state.get("user_university")
        if not university_code:
            st.error("University not assigned. Please contact admin.")
        else:
            if menu == "My Dashboard":
                create_coordinator_dashboard(user_email, university_code)
            elif menu == "My Tasks":
                st.title("📋 My Tasks")
                df = get_university_progress(university_code)
                if not df.empty:
                    display_df = df[["Day", "Date", "Day Name", "Day Type", "Framework", "Task", "Deliverable", "Status", "Deliverable Submitted"]]
                    st.dataframe(display_df, use_container_width=True)
            else:
                st.title("ℹ️ About")
                st.markdown("""
                ### Your Role as Institutional Coordinator
                
                **Responsibilities:**
                - Work alongside Nodal Officer & ICARE Team
                - Collect NIRF-related data from various departments
                - Validate and consolidate university data
                - Submit daily task updates
                - Prepare Monthly Progress Report (MPR)
                
                **Daily Schedule:**
                - 10:00 AM: Report to university
                - 10:30-11:00 AM: Stand-up with Nodal Officer & ICARE Team
                - 6:00 PM: Departure
                """)
    
    else:  # data_analyst
        if menu == "Analyst Dashboard":
            create_data_analyst_dashboard(user_email)
        elif menu == "University Progress":
            st.title("📊 University Progress Summary")
            summary_df = get_summary_stats()
            if not summary_df.empty:
                st.dataframe(summary_df, use_container_width=True)
                
                fig = px.bar(
                    summary_df,
                    x="University",
                    y="Completion %",
                    color="Completion %",
                    text="Completion %",
                    title="University-wise Progress"
                )
                fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.title("ℹ️ About")
            st.markdown("### Data Analyst Dashboard")
            st.markdown("""
            **Your Role:** Monitor and track progress of assigned universities
            
            **Features:**
            - View university-wise task completion
            - Track deliverable submissions
            - Monitor framework-wise progress
            - Export progress reports
            """)

if __name__ == "__main__":
    if not os.path.exists(PROGRESS_DATA_FILE):
        save_progress_data(create_initial_progress_data())
    if not os.path.exists(ASSIGNMENTS_DATA_FILE):
        save_assignments_data(create_initial_assignments_data())
    
    main()
