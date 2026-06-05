import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import calendar
import json
import os
from hashlib import sha256
import base64

# Page configuration
st.set_page_config(
    page_title="MahaSTRIDE - 24-Month Task Management System",
    page_icon="📋",
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
    .task-card {
        background: linear-gradient(135deg, #e8f8f5 0%, #d4efdf 100%);
        border-left: 4px solid #27ae60;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .task-card-pending {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        border-left: 4px solid #ffc107;
    }
    .task-card-completed {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border-left: 4px solid #28a745;
    }
    .stat-card {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem;
    }
    .credentials-box {
        background-color: #f8f9fa;
        border: 2px solid #2a5298;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .role-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    .admin-badge { background-color: #dc3545; color: white; }
    .lead-badge { background-color: #17a2b8; color: white; }
    .analyst-badge { background-color: #28a745; color: white; }
    .info-note {
        background-color: #d1ecf1;
        border-left: 4px solid #17a2b8;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .mpr-header {
        text-align: center;
        margin-bottom: 20px;
    }
    .mpr-title {
        font-size: 14pt;
        font-weight: bold;
        text-align: center;
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# USER CREDENTIALS
# ============================================================
USERS = {
    "admin@mahastride.com": {
        "password": sha256("Admin@2026".encode()).hexdigest(),
        "role": "admin",
        "name": "Administrator"
    },
    "projectlead@mahastride.com": {
        "password": sha256("ProjectLead@2026".encode()).hexdigest(),
        "role": "project_lead",
        "name": "Dr. Harshal Kotwal"
    },
    "shubham@mitra.gov.in": {
        "password": sha256("Shubham@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Shubham Singh",
        "team": "MITRA"
    },
    "sneha@mu.edu": {
        "password": sha256("Sneha@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Sneha Kashitkar",
        "team": "Mumbai University"
    },
    "sagar@mu.edu": {
        "password": sha256("Sagar@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Sagar Teli",
        "team": "Mumbai University"
    },
    "jagan@sspu.edu": {
        "password": sha256("Jagan@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Jagan Sridhar",
        "team": "Savitribai Phule Pune University"
    },
    "vaibhav@coep.edu": {
        "password": sha256("Vaibhav@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Vaibhav Ambekar",
        "team": "COEP Technological University"
    },
    "pratham@au.edu": {
        "password": sha256("Pratham@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Prathamesh Babhulkar",
        "team": "Sant Gadge Baba Amravati University"
    },
    "anjali@nu.edu": {
        "password": sha256("Anjali@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Anjali Singh",
        "team": "Rashtrasant Tukadoji Maharaj Nagpur University"
    },
    "nitish@kbcnmu.edu": {
        "password": sha256("Nitish@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Nitish Kumbhar",
        "team": "KBCNMU, Jalgaon"
    },
    "atharv@bamu.edu": {
        "password": sha256("Atharv@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Atharav Paturkar",
        "team": "Dr. Babasaheb Ambedkar Marathwada University"
    }
}

# ============================================================
# UNIVERSITY DETAILS (from MPR)
# ============================================================
UNIVERSITIES_DATA = {
    "Mumbai University": {
        "code": "MU",
        "nodal_officer": "Dr. Varsha Kelkar Mane",
        "registrar": "To be updated",
        "coordinators": ["Sneha Kashitkar", "Sagar Teli"]
    },
    "Savitribai Phule Pune University": {
        "code": "SSPU",
        "nodal_officer": "Prof. Vinayak Joshi",
        "registrar": "To be updated",
        "coordinators": ["Jagan Sridhar"]
    },
    "COEP Technological University": {
        "code": "COEP",
        "nodal_officer": "Dr. Uttam Chaskar",
        "registrar": "To be updated",
        "coordinators": ["Vaibhav Ambekar"]
    },
    "KBCNMU, Jalgaon": {
        "code": "KBCNMU",
        "nodal_officer": "Prof. Sameer Narkhede",
        "registrar": "To be updated",
        "coordinators": ["Nitish Kumbhar"]
    },
    "Dr. Babasaheb Ambedkar Marathwada University": {
        "code": "BAMU",
        "nodal_officer": "Prof. G.D. Khedkar",
        "registrar": "To be updated",
        "coordinators": ["Atharav Paturkar"]
    },
    "Rashtrasant Tukadoji Maharaj Nagpur University": {
        "code": "NU",
        "nodal_officer": "Prof. Nandkishor Karade",
        "registrar": "To be updated",
        "coordinators": ["Anjali Singh"]
    },
    "Sant Gadge Baba Amravati University": {
        "code": "AU",
        "nodal_officer": "Dr. A. B. Naik",
        "registrar": "To be updated",
        "coordinators": ["Prathamesh Babhulkar"]
    },
    "MITRA": {
        "code": "MITRA",
        "nodal_officer": "Dr. Harshal Kotwal",
        "registrar": "To be updated",
        "coordinators": ["Shubham Singh"]
    }
}

# ============================================================
# DATA FILES
# ============================================================
TASKS_FILE = "complete_24month_tasks.json"
TASK_COMPLETION_FILE = "task_completion.json"

# ============================================================
# COMPLETED DATE RANGE (May 4 to June 5, 2026)
# ============================================================
COMPLETED_START_DATE = datetime(2026, 5, 4)
COMPLETED_END_DATE = datetime(2026, 6, 5)
START_FRESH_DATE = datetime(2026, 6, 8)

# ============================================================
# MAY 2026 COMPLETED ACTIVITIES (from MPR)
# ============================================================
MAY_ACTIVITIES = [
    {"activity": "SANGAM Orientation & Training (May 4-6 at Trident Board Room)", "status": "Completed", "date": "May 4-6, 2026"},
    {"activity": "University Onboarding & Data Source Mapping", "status": "Completed", "date": "May 7-8, 2026"},
    {"activity": "NIRF Data Collection (Student, Faculty, Research, Placement, Finance)", "status": "Completed", "date": "May 12-20, 2026"},
    {"activity": "Stakeholder Consultation & Review Meetings", "status": "Ongoing", "date": "May 18-27, 2026"},
    {"activity": "Inception Report & GRDAU Framework Development", "status": "Completed", "date": "May 22-26, 2026"},
    {"activity": "May MPR Preparation & Finalization", "status": "Submitted", "date": "May 29, 2026"}
]

MAY_MEETINGS = [
    {"date": "May 4-6, 2026", "agenda": "SANGAM Orientation, Training & Workshop", "outcome": "Training completed. GRDAU concept introduced."},
    {"date": "May 7, 2026", "agenda": "Project Kick-off and data source mapping", "outcome": "Data collection initiated"},
    {"date": "May 18, 2026", "agenda": "Data gap review and action plan", "outcome": "Departments to submit pending data"},
    {"date": "May 27, 2026", "agenda": "Review of May progress", "outcome": "MPR preparation initiated"}
]

# ============================================================
# WORKING HOURS
# ============================================================
WORKING_HOURS = {
    "start": "10:00",
    "end": "18:00",
    "total_hours": 8,
    "working_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
}

# ============================================================
# 24-MONTH DAILY TASK GENERATION
# ============================================================

def get_working_dates(start_date, end_date):
    """Get all working dates (Monday to Friday) between start and end dates"""
    working_dates = []
    current = start_date
    while current <= end_date:
        if current.weekday() < 5:
            working_dates.append(current)
        current += timedelta(days=1)
    return working_dates

def generate_may_2026_tasks(date):
    """Generate May 2026 tasks based on actual MPR"""
    tasks_by_date = {
        "2026-05-04": {"task": "SANGAM Orientation Day 1 - Project Overview", "category": "Training", "priority": "High"},
        "2026-05-05": {"task": "SANGAM Training Day 2 - NIRF Framework", "category": "Training", "priority": "High"},
        "2026-05-06": {"task": "SANGAM Workshop Day 3 - GRDAU Concept", "category": "Training", "priority": "High"},
        "2026-05-07": {"task": "University Reporting & Onboarding", "category": "Setup", "priority": "High"},
        "2026-05-08": {"task": "NIRF Data Source Mapping", "category": "Setup", "priority": "High"},
        "2026-05-11": {"task": "Create Data Gap Template", "category": "Documentation", "priority": "Medium"},
        "2026-05-12": {"task": "Collect Student & Faculty Data", "category": "Data Collection", "priority": "High"},
        "2026-05-13": {"task": "Collect Research & Placement Data", "category": "Data Collection", "priority": "High"},
        "2026-05-14": {"task": "Collect Financial & Infrastructure Data", "category": "Data Collection", "priority": "Medium"},
        "2026-05-15": {"task": "Data Consolidation & Validation", "category": "Analysis", "priority": "High"},
        "2026-05-18": {"task": "Stakeholder Consultation Meeting", "category": "Meetings", "priority": "High"},
        "2026-05-19": {"task": "Missing Data Follow-up", "category": "Data Collection", "priority": "Medium"},
        "2026-05-20": {"task": "NIRF Template Preparation", "category": "Analysis", "priority": "High"},
        "2026-05-21": {"task": "SWOT Analysis & Gap Report", "category": "Documentation", "priority": "High"},
        "2026-05-22": {"task": "Inception Report Drafting", "category": "Reporting", "priority": "High"},
        "2026-05-25": {"task": "GRDAU Team Identification", "category": "Documentation", "priority": "Medium"},
        "2026-05-26": {"task": "GRDAU Operational Framework", "category": "Documentation", "priority": "High"},
        "2026-05-27": {"task": "Review Meeting with ICARE", "category": "Meetings", "priority": "High"},
        "2026-05-29": {"task": "May MPR Finalization", "category": "Reporting", "priority": "High"}
    }
    
    date_str = date.strftime("%Y-%m-%d")
    if date_str in tasks_by_date:
        return tasks_by_date[date_str]
    return {"task": "Data validation and reporting", "category": "Analysis", "priority": "Medium"}

def generate_june_2026_tasks(date):
    """Generate June 2026 tasks"""
    day = date.day
    if day <= 5:
        tasks_by_day = {
            2: {"task": "Complete Diagnostic Assessment Framework", "category": "Assessment", "priority": "High"},
            3: {"task": "Begin University-wise Assessments", "category": "Assessment", "priority": "High"},
            4: {"task": "Review existing data quality", "category": "Analysis", "priority": "High"},
            5: {"task": "Identify data gaps per university", "category": "Assessment", "priority": "High"}
        }
        return tasks_by_day.get(day, {"task": "Continue assessments", "category": "Assessment", "priority": "Medium"})
    else:
        tasks_by_day = {
            8: {"task": "Conduct faculty interviews", "category": "Assessment", "priority": "High"},
            9: {"task": "Analyze research output metrics", "category": "Analysis", "priority": "High"},
            10: {"task": "Evaluate infrastructure readiness", "category": "Assessment", "priority": "Medium"},
            11: {"task": "Assess international collaboration", "category": "Assessment", "priority": "Medium"},
            12: {"task": "Compile assessment findings", "category": "Analysis", "priority": "High"},
            15: {"task": "GRDAU Training Session for Coordinators", "category": "Training", "priority": "High"},
            16: {"task": "Data validation workshop", "category": "Training", "priority": "High"},
            17: {"task": "NIRF submission preparation", "category": "Reporting", "priority": "High"},
            18: {"task": "Review progress with VC", "category": "Meetings", "priority": "High"},
            19: {"task": "Update data repository", "category": "Data Collection", "priority": "Medium"},
            22: {"task": "Finalize Diagnostic Reports", "category": "Reporting", "priority": "High"},
            23: {"task": "Submit Diagnostic Assessment Reports", "category": "Reporting", "priority": "High"},
            24: {"task": "Prepare June MPR", "category": "Reporting", "priority": "High"},
            25: {"task": "Plan July activities", "category": "Planning", "priority": "Medium"},
            26: {"task": "Client review meeting", "category": "Meetings", "priority": "High"},
            29: {"task": "Continue data analysis", "category": "Analysis", "priority": "Medium"},
            30: {"task": "Finalize monthly report", "category": "Reporting", "priority": "High"}
        }
        return tasks_by_day.get(day, {"task": "Continue assessments and reporting", "category": "Assessment", "priority": "Medium"})

def generate_future_tasks(date):
    """Generate template for future tasks beyond June 2026"""
    return {"task": "Continue project activities as per plan", "category": "Implementation", "priority": "Medium"}

def generate_all_tasks():
    """Generate complete 24-month daily tasks"""
    all_tasks = {}
    
    start_date = datetime(2026, 5, 4)
    end_date = datetime(2028, 4, 28)
    working_dates = get_working_dates(start_date, end_date)
    
    for date in working_dates:
        date_str = date.strftime("%Y-%m-%d")
        
        if date.year == 2026 and date.month == 5:
            task_info = generate_may_2026_tasks(date)
        elif date.year == 2026 and date.month == 6:
            task_info = generate_june_2026_tasks(date)
        else:
            task_info = generate_future_tasks(date)
        
        all_tasks[date_str] = {
            "task": task_info["task"],
            "category": task_info["category"],
            "priority": task_info["priority"],
            "target": "coordinator",
            "day_of_week": date.strftime("%A")
        }
    
    return all_tasks

# ============================================================
# DATA MANAGEMENT FUNCTIONS
# ============================================================

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as f:
            return json.load(f)
    tasks = generate_all_tasks()
    save_tasks(tasks)
    return tasks

def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)

def load_completions():
    if os.path.exists(TASK_COMPLETION_FILE):
        with open(TASK_COMPLETION_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_completions(completions):
    with open(TASK_COMPLETION_FILE, 'w') as f:
        json.dump(completions, f, indent=2)

def initialize_completed_tasks():
    """Mark all tasks from May 4 to June 5, 2026 as completed for all data analysts"""
    completions = load_completions()
    
    completed_dates = []
    current = COMPLETED_START_DATE
    while current <= COMPLETED_END_DATE:
        if current.weekday() < 5:
            completed_dates.append(current.strftime("%Y-%m-%d"))
        current += timedelta(days=1)
    
    for email, user in USERS.items():
        if user.get("role") == "data_analyst":
            if email not in completions:
                completions[email] = {}
            
            for date_str in completed_dates:
                if date_str not in completions[email]:
                    completions[email][date_str] = {
                        "completed_at": datetime(2026, 6, 5, 17, 0, 0).isoformat(),
                        "remarks": "Completed as per project plan"
                    }
    
    save_completions(completions)
    return len(completed_dates)

def get_user_tasks(email):
    user = USERS.get(email, {})
    user_role = user.get("role", "")
    
    all_tasks = load_tasks()
    completions = load_completions()
    user_completions = completions.get(email, {})
    
    user_tasks = []
    
    for date_str, task_info in all_tasks.items():
        is_assigned = (user_role == "data_analyst")
        
        if is_assigned:
            is_completed = date_str in user_completions
            completion_info = user_completions.get(date_str, {})
            
            user_tasks.append({
                "date": date_str,
                "day": datetime.strptime(date_str, "%Y-%m-%d").strftime("%A"),
                "task": task_info["task"],
                "category": task_info["category"],
                "priority": task_info["priority"],
                "status": "Completed" if is_completed else "Pending",
                "completed_at": completion_info.get("completed_at", ""),
                "remarks": completion_info.get("remarks", "")
            })
    
    return sorted(user_tasks, key=lambda x: x["date"])

def mark_task_complete(email, date_str, remarks=""):
    completions = load_completions()
    if email not in completions:
        completions[email] = {}
    
    completions[email][date_str] = {
        "completed_at": datetime.now().isoformat(),
        "remarks": remarks
    }
    save_completions(completions)
    return True

def get_team_summary():
    completions = load_completions()
    all_tasks = load_tasks()
    total_tasks = len(all_tasks)
    
    summary = []
    for email, user in USERS.items():
        if user.get("role") == "data_analyst":
            user_completions = len(completions.get(email, {}))
            summary.append({
                "Name": user["name"],
                "Team": user.get("team", "N/A"),
                "Completed": user_completions,
                "Total": total_tasks,
                "Progress %": round((user_completions / total_tasks * 100), 1) if total_tasks > 0 else 0
            })
    
    return pd.DataFrame(summary)

# ============================================================
# MPR GENERATION FUNCTIONS
# ============================================================

def generate_mpr_html(university_name):
    """Generate MPR in the format of the attached Consolidated_MPR.pdf"""
    
    uni_data = UNIVERSITIES_DATA.get(university_name, {})
    completions = load_completions()
    
    # Get coordinator tasks for this university
    coordinators = uni_data.get("coordinators", [])
    
    # Get May 2026 completion data
    may_completions = {}
    for email, user in USERS.items():
        if user.get("name") in coordinators:
            user_completions = completions.get(email, {})
            for date_str in user_completions:
                if date_str.startswith("2026-05"):
                    may_completions[date_str] = user_completions[date_str]
    
    completed_count = len(may_completions)
    
    # Build team table
    team_rows = ""
    sr_no = 1
    
    # MITRA Level
    team_rows += f'<tr style="background-color:#d0d0d0;"><td colspan="7"><strong>MITRA LEVEL</strong></td></tr>'
    team_rows += f"""
    <tr>
        <td>{sr_no}</td><td>Dr. Harshal Kotwal</td><td>Project Lead</td><td>MITRA, Mumbai</td><td>19</td><td>0</td><td>12</td>
    </tr>
    """
    sr_no += 1
    team_rows += f"""
    <tr>
        <td>{sr_no}</td><td>Shubham Singh</td><td>Data Analytics and Dashboard Specialist</td><td>MITRA, Mumbai</td><td>19</td><td>0</td><td>12</td>
    </tr>
    """
    sr_no += 1
    
    # University Level
    team_rows += f'<tr style="background-color:#d0d0d0;"><td colspan="7"><strong>{university_name}</strong></td></tr>'
    for coordinator in coordinators:
        team_rows += f"""
        <tr>
            <td>{sr_no}</td><td>{coordinator}</td><td>Institutional Coordinator cum Research & Innovation Officer</td><td>{university_name}</td><td>19</td><td>0</td><td>12</td>
        </tr>
        """
        sr_no += 1
    
    # Major Activities table
    activities_rows = ""
    for i, activity in enumerate(MAY_ACTIVITIES, 1):
        activities_rows += f"""
        <tr>
            <td>{i}.</td>
            <td>{activity['activity']}</td>
            <td>{', '.join(coordinators) if coordinators else 'ICARE Team'}</td>
            <td>{activity['status']}</td>
            <td>{activity['date']}</td>
        </tr>
        """
    
    # Meetings table
    meetings_rows = ""
    for i, meeting in enumerate(MAY_MEETINGS, 1):
        meetings_rows += f"""
        <tr>
            <td>{i}.</td>
            <td>{meeting['date']}</td>
            <td>ICARE Team + Coordinators</td>
            <td>{meeting['agenda']}</td>
            <td>{meeting['outcome']}</td>
            <td>Institutional Coordinators</td>
        </tr>
        """
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Monthly Progress Report - {university_name}</title>
    <style>
        body {{ font-family: 'Times New Roman', serif; margin: 0.7in; font-size: 11pt; }}
        .header {{ text-align: center; margin-bottom: 20px; }}
        .mitra-title {{ font-size: 12pt; font-weight: bold; }}
        .confidential {{ text-align: right; font-weight: bold; margin-bottom: 20px; }}
        .report-title {{ font-size: 14pt; font-weight: bold; text-align: center; margin: 15px 0; }}
        .section-title {{ font-size: 12pt; font-weight: bold; margin-top: 15px; margin-bottom: 8px; background-color: #f0f0f0; padding: 5px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
        th, td {{ border: 1px solid #000; padding: 6px; vertical-align: top; }}
        th {{ background-color: #e8e8e8; font-weight: bold; text-align: center; }}
        .footer {{ text-align: center; font-size: 9pt; font-style: italic; margin-top: 30px; }}
    </style>
</head>
<body>
<div class="confidential">Confidential</div>
<div class="header">
    <div class="mitra-title">Maharashtra Institution for Transformation (MITRA)</div>
    <div>5th Floor, Nirmal, Nariman Point, Mumbai-400021</div>
    <div>Email: pmu.mahastride@mahamitra.org</div>
</div>
<div class="report-title">MONTHLY PROGRESS REPORT</div>
<div style="text-align: center;">(From 05 May 2026 to 31 May 2026)</div>

<table>
    <tr><th style="width:30%">Work Order Reference</th>
        <td colspan="3">MITRA/Research/MahaSTRIDE/EduRFP/49/2025 dated 25 March 2026</td>
    </tr>
    <tr><th>University / Division</th><td colspan="3">{university_name}</td></tr>
    <tr><th>Project Start Date</th><td>06 May 2026</td><th>Project End Date</th><td>06 May 2028</td></tr>
</table>

<div class="section-title">Project Team Deployment</div>
<table>
    <tr>
        <th>Sr. No.</th><th>Name of the Key Professional</th><th>Profile as per contract</th><th>Location</th><th>Total Present Days</th><th>Total Absent Days</th><th>Total Holidays/Weekly offs</th>
    </tr>
    {team_rows}
</table>

<div class="section-title">A. Major Activities</div>
<table>
    <tr><th>Sr. No.</th><th>Major Activities</th><th>Team Member Name</th><th>Activity Status</th><th>Date of Submission</th></tr>
    {activities_rows}
</table>

<div class="section-title">B. Minutes of Meetings Conducted</div>
<table>
    <tr><th>Sr. No.</th><th>Date</th><th>Chairperson & Key Participants</th><th>Agenda</th><th>Decision / Way Forward</th><th>Responsibility</th></tr>
    {meetings_rows}
</table>

<div class="section-title">C. Major Deliverables (As committed under Contract)</div>
<table>
    <tr><th>Sr. No.</th><th>Major Deliverables</th><th>Team Member Name</th><th>Activity Status</th><th>Due Date</th></tr>
    <tr><td>1.</td><td>Inception Report and Deployment Plan</td><td>{', '.join(coordinators) if coordinators else 'ICARE Team'}</td><td>✅ Completed</td><td>June 6, 2026</td></tr>
    <tr><td>2.</td><td>GRDAUs Establishment & Operationalization</td><td>{', '.join(coordinators) if coordinators else 'ICARE Team'}</td><td>✅ Completed</td><td>July 6, 2026</td></tr>
    <tr><td>3.</td><td>Monthly Progress Report (May 2026)</td><td>{', '.join(coordinators) if coordinators else 'ICARE Team'}</td><td>✅ Completed</td><td>June 10, 2026</td></tr>
</table>

<div class="section-title">D. Administration & Risk Management</div>
<table>
    <tr><th>Sr. No.</th><th>Description of Identified Risk</th><th>Possible Impact</th><th>Severity Level</th><th>Mitigation Strategy</th><th>Responsibility</th></tr>
    <tr><td>1.</td><td>Delay in data availability from departments</td><td>Incomplete NIRF submission</td><td>Medium</td><td>Regular follow-ups with Nodal Officer</td><td>Coordinator</td></tr>
    <tr><td>2.</td><td>Inconsistent data formats across departments</td><td>Data validation challenges</td><td>Low</td><td>Standardized templates provided</td><td>Coordinator</td></tr>
    <tr><td>3.</td><td>Staff turnover in key departments</td><td>Loss of data continuity</td><td>Medium</td><td>Documentation of processes</td><td>ICARE Team</td></tr>
</table>

<div class="section-title">E. Status of Initiatives under the Project</div>
<table>
    <tr><th>Sr. No.</th><th>Sub-Sector</th><th>Objective</th><th>Specific Intervention</th><th>Current Status</th><th>Way Forward</th></tr>
    <tr><td>1.</td><td>NIRF Data Collection</td><td>Complete baseline data</td><td>Student, Faculty, Research, Placement data</td><td>✅ Completed</td><td>Validation by June 15</td></tr>
    <tr><td>2.</td><td>Capacity Building</td><td>Train coordinators</td><td>SANGAM Training Program</td><td>✅ Completed</td><td>Reinforcement in June</td></tr>
    <tr><td>3.</td><td>GRDAU Setup</td><td>Establish Data Analytics Unit</td><td>Team identification, role definition</td><td>✅ Completed</td><td>Operational by June 30</td></tr>
</table>

<div class="section-title">Approvals and Signatures</div>
<table style="border:none">
    <tr><td style="border:none; width:30%"><strong>Prepared by:</strong></td><td style="border:none">{', '.join(coordinators) if coordinators else 'Institutional Coordinators'}<br>(Institutional Coordinators)</td></tr>
    <tr><td style="border:none"><strong>Verified by:</strong></td><td style="border:none">{uni_data.get('nodal_officer', 'Nodal Officer')}<br>(Nodal Officer, IQAC Coordinator)</td></tr>
    <tr><td style="border:none"><strong>Approved by:</strong></td><td style="border:none">{uni_data.get('registrar', 'Registrar')}<br>(Registrar)</td></tr>
    <tr><td style="border:none"><strong>Approved by:</strong></td><td style="border:none">Jt. CEO, MITRA<br>(Jt. CEO, MITRA)</td></tr>
</table>

<div class="footer">This report is submitted as per SOP Section 2 - Monthly Progress Report (MPR)<br>Generated on {datetime.now().strftime('%d-%b-%Y %H:%M:%S')}</div>
</body>
</html>"""
    
    return html

def generate_consolidated_mpr_html():
    """Generate consolidated MPR for all universities"""
    
    # Build team table for all members
    team_rows = ""
    sr_no = 1
    
    team_rows += '<tr style="background-color:#d0d0d0;"><td colspan="7"><strong>MITRA LEVEL</strong></td></tr>'
    team_rows += f"""
    <tr><td>{sr_no}</td><td>Dr. Harshal Kotwal</td><td>Project Lead</td><td>MITRA, Mumbai</td><td>19</td><td>0</td><td>12</td></tr>
    """
    sr_no += 1
    team_rows += f"""
    <tr><td>{sr_no}</td><td>Shubham Singh</td><td>Data Analytics and Dashboard Specialist</td><td>MITRA, Mumbai</td><td>19</td><td>0</td><td>12</td></tr>
    """
    sr_no += 1
    
    for uni_name, uni_data in UNIVERSITIES_DATA.items():
        if uni_name != "MITRA":
            team_rows += f'<tr style="background-color:#d0d0d0;"><td colspan="7"><strong>{uni_name}</strong></td></tr>'
            for coordinator in uni_data.get("coordinators", []):
                team_rows += f"""
                <tr>
                    <td>{sr_no}</td>
                    <td>{coordinator}</td>
                    <td>Institutional Coordinator cum Research & Innovation Officer</td>
                    <td>{uni_name}</td>
                    <td>19</div>
                    <td>0</div>
                    <td>12</div>
                </tr>
                """
                sr_no += 1
    
    # Activities table
    activities_rows = ""
    for i, activity in enumerate(MAY_ACTIVITIES, 1):
        activities_rows += f"""
        <tr>
            <td>{i}.</td>
            <td>{activity['activity']}</td>
            <td>All Coordinators</div>
            <td>{activity['status']}</div>
            <td>{activity['date']}</div>
        </tr>
        """
    
    # Meetings table
    meetings_rows = ""
    for i, meeting in enumerate(MAY_MEETINGS, 1):
        meetings_rows += f"""
        <tr>
            <td>{i}.</div>
            <td>{meeting['date']}</div>
            <td>ICARE Team + All Coordinators</div>
            <td>{meeting['agenda']}</div>
            <td>{meeting['outcome']}</div>
            <td>All Institutional Coordinators</div>
        </tr>
        """
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Consolidated Monthly Progress Report - All Universities</title>
    <style>
        body {{ font-family: 'Times New Roman', serif; margin: 0.7in; font-size: 11pt; }}
        .header {{ text-align: center; margin-bottom: 20px; }}
        .mitra-title {{ font-size: 12pt; font-weight: bold; }}
        .confidential {{ text-align: right; font-weight: bold; margin-bottom: 20px; }}
        .report-title {{ font-size: 14pt; font-weight: bold; text-align: center; margin: 15px 0; }}
        .section-title {{ font-size: 12pt; font-weight: bold; margin-top: 15px; margin-bottom: 8px; background-color: #f0f0f0; padding: 5px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
        th, td {{ border: 1px solid #000; padding: 6px; vertical-align: top; }}
        th {{ background-color: #e8e8e8; font-weight: bold; text-align: center; }}
        .footer {{ text-align: center; font-size: 9pt; font-style: italic; margin-top: 30px; }}
    </style>
</head>
<body>
<div class="confidential">Confidential</div>
<div class="header">
    <div class="mitra-title">Maharashtra Institution for Transformation (MITRA)</div>
    <div>5th Floor, Nirmal, Nariman Point, Mumbai-400021</div>
</div>
<div class="report-title">CONSOLIDATED MONTHLY PROGRESS REPORT</div>
<div style="text-align: center;">All Maharashtra State Universities</div>
<div style="text-align: center;">Reporting Period: 05 May 2026 to 31 May 2026</div>

<div class="section-title">Project Team Deployment</div>
<table>
    <tr><th>Sr. No.</th><th>Name of the Key Professional</th><th>Profile as per contract</th><th>Location</th><th>Total Present Days</th><th>Total Absent Days</th><th>Total Holidays/Weekly offs</th></tr>
    {team_rows}
</table>

<div class="section-title">A. Major Activities</div>
<table>
    <tr><th>Sr. No.</th><th>Major Activities</th><th>Team Member Name</th><th>Activity Status</th><th>Date of Submission</th></tr>
    {activities_rows}
</table>

<div class="section-title">B. Minutes of Meetings Conducted</div>
<table>
    <tr><th>Sr. No.</th><th>Date</th><th>Chairperson & Key Participants</th><th>Agenda</th><th>Decision / Way Forward</th><th>Responsibility</th></tr>
    {meetings_rows}
</table>

<div class="section-title">C. Major Deliverables (As committed under Contract)</div>
<table>
    <tr><th>Sr. No.</th><th>Major Deliverables</th><th>Team Member Name</th><th>Activity Status</th><th>Due Date</th></tr>
    <tr><td>1.</div><td>Inception Report and Deployment Plan</div><td>All Coordinators</div><td>✅ Completed</div><td>June 6, 2026</div></tr>
    <tr><td>2.</div><td>GRDAUs Establishment & Operationalization</div><td>All Coordinators</div><td>✅ Completed</div><td>July 6, 2026</div></tr>
    <tr><td>3.</div><td>Monthly Progress Report (May 2026)</div><td>All Coordinators</div><td>✅ Completed</div><td>June 10, 2026</div></tr>
<table>

<div class="section-title">D. Administration & Risk Management</div>
<table>
    <tr><th>Sr. No.</th><th>Description of Identified Risk</th><th>Possible Impact</th><th>Severity Level</th><th>Mitigation Strategy</th><th>Responsibility</th></tr>
    <tr><td>1.</div><td>Delay in data availability from departments</div><td>Incomplete NIRF submission</div><td>Medium</div><td>Regular follow-ups with Nodal Officer</div><td>Coordinator</div></tr>
    <tr><td>2.</div><td>Inconsistent data formats across departments</div><td>Data validation challenges</div><td>Low</div><td>Standardized templates provided</div><td>Coordinator</div></tr>
    <tr><td>3.</div><td>Staff turnover in key departments</div><td>Loss of data continuity</div><td>Medium</div><td>Documentation of processes</div><td>ICARE Team</div></tr>
</table>

<div class="section-title">E. Status of Initiatives under the Project</div>
<table>
    <tr><th>Sr. No.</th><th>Sub-Sector</th><th>Objective</th><th>Specific Intervention</th><th>Current Status</th><th>Way Forward</th></tr>
    <tr><td>1.</div><td>NIRF Data Collection</div><td>Complete baseline data</div><td>Student, Faculty, Research, Placement data</div><td>✅ Completed</div><td>Validation by June 15</div></tr>
    <tr><td>2.</div><td>Capacity Building</div><td>Train coordinators</div><td>SANGAM Training Program</div><td>✅ Completed</div><td>Reinforcement in June</div></tr>
    <tr><td>3.</div><td>GRDAU Setup</div><td>Establish Data Analytics Unit</div><td>Team identification, role definition</div><td>✅ Completed</div><td>Operational by June 30</div></tr>
</table>

<div class="section-title">Approvals and Signatures</div>
<table style="border:none">
    <tr><td style="border:none; width:30%"><strong>Prepared by:</strong></div><td style="border:none">All Institutional Coordinators</div></tr>
    <tr><td style="border:none"><strong>Verified by:</strong></div><td style="border:none">Nodal Officers of respective Universities</div></tr>
    <tr><td style="border:none"><strong>Approved by:</strong></div><td style="border:none">Jt. CEO, MITRA</div></tr>
</table>

<div class="footer">This consolidated report is submitted as per SOP Section 2 - Monthly Progress Report (MPR)<br>Generated on {datetime.now().strftime('%d-%b-%Y %H:%M:%S')}</div>
</body>
</html>"""
    
    return html

def get_download_link(html, filename):
    b64 = base64.b64encode(html.encode()).decode()
    return f'<a href="data:text/html;base64,{b64}" download="{filename}" style="background:#4CAF50;color:white;padding:10px 20px;text-decoration:none;border-radius:5px;">📥 Download {filename}</a>'

def show_credentials():
    st.markdown("""
    <div class="credentials-box">
        <h4>🔐 Default Login Credentials</h4>
        <p><strong>Password format:</strong> <code>FirstName@2026</code> (e.g., Admin@2026, Sneha@2026)</p>
        <table style="width:100%">
            <tr><th>Role</th><th>Email</th><th>Password</th></tr>
            <tr><td style="background:#dc3545;color:white;padding:2px 8px;border-radius:5px;">Admin</td>
                <td>admin@mahastride.com</td><td>Admin@2026</td></tr>
            <tr><td style="background:#17a2b8;color:white;padding:2px 8px;border-radius:5px;">Project Lead</td>
                <td>projectlead@mahastride.com</td><td>ProjectLead@2026</td></tr>
            <tr><td rowspan="2" style="background:#28a745;color:white;padding:2px 8px;border-radius:5px;">Data Analyst</td>
                <td>sneha@mu.edu</td><td>Sneha@2026</td></tr>
            <tr><td>shubham@mitra.gov.in</td><td>Shubham@2026</td></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# DASHBOARD FUNCTIONS
# ============================================================

def admin_dashboard():
    st.markdown("## 📊 Administrator Dashboard")
    
    all_tasks = load_tasks()
    completions = load_completions()
    
    total_tasks = len(all_tasks)
    total_completions = sum(len(c) for c in completions.values())
    total_analysts = sum(1 for u in USERS.values() if u.get("role") == "data_analyst")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📅 Total Working Days", total_tasks)
    col2.metric("✅ Total Completions", total_completions)
    col3.metric("👥 Data Analysts", total_analysts)
    col4.metric("📊 Avg Progress", f"{total_completions/(total_tasks*total_analysts)*100:.1f}%" if total_tasks > 0 else "0%")
    
    st.markdown("---")
    
    # Info note
    st.markdown("""
    <div class="info-note">
        <strong>ℹ️ Note:</strong> All tasks from <strong>May 4 to June 5, 2026</strong> have been automatically marked as 
        <strong>COMPLETED</strong> for all Data Analysts. The counts below reflect actual completed tasks.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Team Performance
    st.subheader("👥 Team Performance")
    df_summary = get_team_summary()
    st.dataframe(df_summary, use_container_width=True, hide_index=True)
    
    fig = px.bar(df_summary, x="Name", y="Progress %", color="Team", title="Team Progress (%)")
    st.plotly_chart(fig, use_container_width=True)

def project_lead_dashboard():
    st.markdown("## 👨‍💼 Project Lead Dashboard")
    st.markdown("**Dr. Harshal Kotwal** - ICARE Project Director")
    
    tab1, tab2, tab3 = st.tabs(["📊 Progress Overview", "📄 MPR Reports", "👥 Team Tasks"])
    
    all_tasks = load_tasks()
    completions = load_completions()
    total_tasks = len(all_tasks)
    
    with tab1:
        st.markdown("### Overall Progress")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📊 Total Working Days (24 months)", total_tasks)
        with col2:
            df_summary = get_team_summary()
            avg_progress = df_summary["Progress %"].mean() if not df_summary.empty else 0
            st.metric("📈 Average Team Progress", f"{avg_progress:.1f}%")
        
        st.markdown("---")
        
        # Team Performance Chart
        st.subheader("Team Performance")
        df_summary = get_team_summary()
        fig = px.bar(df_summary, x="Name", y="Completed", color="Team", 
                     title="Tasks Completed by Team Member",
                     labels={"Completed": "Number of Tasks Completed", "Name": "Team Member"})
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### 📄 Generate Monthly Progress Reports")
        st.markdown("Generate MPR in the format as per the attached Consolidated_MPR.pdf")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("University-wise MPR")
            university = st.selectbox("Select University", list(UNIVERSITIES_DATA.keys()))
            if st.button("Generate MPR", key="uni_mpr", use_container_width=True):
                html = generate_mpr_html(university)
                st.markdown(get_download_link(html, f"MPR_{university.replace(' ', '_')}_May2026.html"), unsafe_allow_html=True)
        
        with col2:
            st.subheader("Consolidated MPR")
            if st.button("Generate Consolidated MPR", key="consolidated_mpr", use_container_width=True):
                html = generate_consolidated_mpr_html()
                st.markdown(get_download_link(html, "Consolidated_MPR_May2026.html"), unsafe_allow_html=True)
        
        # Preview of May 2026 activities
        st.markdown("---")
        st.subheader("📋 May 2026 Completed Activities (from MPR)")
        
        for activity in MAY_ACTIVITIES:
            status_icon = "✅" if activity["status"] == "Completed" else "🔄" if activity["status"] == "Ongoing" else "📄"
            st.markdown(f"- {status_icon} **{activity['activity']}** - {activity['status']} ({activity['date']})")
    
    with tab3:
        st.subheader("Team Member Task Status")
        
        for email, user in USERS.items():
            if user.get("role") == "data_analyst":
                with st.expander(f"👤 {user['name']} - {user.get('team', 'N/A')}"):
                    user_tasks = get_user_tasks(email)
                    completed = sum(1 for t in user_tasks if t["status"] == "Completed")
                    total = len(user_tasks)
                    
                    st.progress(completed/total if total > 0 else 0)
                    st.caption(f"Progress: {completed}/{total} tasks completed ({completed/total*100:.1f}%)")

def data_analyst_dashboard(email, user):
    st.markdown(f"## 📋 Task Dashboard")
    st.markdown(f"**Welcome, {user['name']}**")
    st.markdown(f"**Team:** {user.get('team', 'N/A')}")
    st.markdown(f"**Working Hours:** 10:00 AM - 6:00 PM (Monday to Friday)")
    
    user_tasks = get_user_tasks(email)
    completed = sum(1 for t in user_tasks if t["status"] == "Completed")
    total = len(user_tasks)
    
    # Info note - show actual completion status
    st.markdown(f"""
    <div class="info-note">
        <strong>📊 Your Progress Summary:</strong><br>
        ✅ <strong>{completed}</strong> out of <strong>{total}</strong> tasks completed ({completed/total*100:.1f}%)<br>
        📅 Tasks from <strong>May 4 to June 5, 2026</strong> are marked as completed automatically.
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📝 Today's Tasks", "📊 My Progress", "📅 All Tasks"])
    
    today = datetime.now().strftime("%Y-%m-%d")
    today_task = next((t for t in user_tasks if t["date"] == today), None)
    
    with tab1:
        if today_task:
            if today_task["status"] == "Completed":
                st.markdown(f"""
                <div class="task-card task-card-completed">
                    ✅ <strong>COMPLETED</strong><br>
                    📅 {today_task['date']} ({today_task['day']})<br>
                    🎯 {today_task['task']}<br>
                    📂 Category: {today_task['category']}<br>
                    🏷️ Priority: {today_task['priority']}
                </div>
                """, unsafe_allow_html=True)
            else:
                with st.form(key=f"task_{today_task['date']}"):
                    st.markdown(f"""
                    <div class="task-card task-card-pending">
                        ⏳ <strong>TASK TO COMPLETE</strong><br>
                        🎯 {today_task['task']}<br>
                        📂 Category: {today_task['category']}<br>
                        🏷️ Priority: {today_task['priority']}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("**Work Log (10:00 AM - 6:00 PM)**")
                    col1, col2 = st.columns(2)
                    with col1:
                        start_time = st.time_input("Start Time", value=datetime.strptime("10:00", "%H:%M").time())
                    with col2:
                        end_time = st.time_input("End Time", value=datetime.strptime("18:00", "%H:%M").time())
                    
                    remarks = st.text_area("Work Accomplished / Remarks", height=100)
                    
                    if st.form_submit_button("✅ Mark as Complete", use_container_width=True):
                        work_log = f"Worked from {start_time} to {end_time}. {remarks}"
                        if mark_task_complete(email, today_task["date"], work_log):
                            st.success("Task completed! Great work!")
                            st.rerun()
        else:
            st.info("No task assigned for today. This may be a weekend or holiday.")
            st.markdown("**Working Days:** Monday to Friday only")
    
    with tab2:
        col1, col2, col3 = st.columns(3)
        col1.metric("📊 Total Tasks", total)
        col2.metric("✅ Completed", completed)
        col3.metric("⏳ Remaining", total - completed)
        
        st.progress(completed/total if total > 0 else 0)
        
        # Show completion chart
        if completed > 0:
            fig = go.Figure(data=[go.Pie(
                labels=['Completed', 'Pending'],
                values=[completed, total - completed],
                marker_colors=['#28a745', '#ffc107'],
                hole=0.4
            )])
            fig.update_layout(title="Your Overall Progress", height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        # Filter options
        filter_status = st.selectbox("Filter by Status", ["All", "Pending", "Completed"])
        
        filtered_tasks = user_tasks
        if filter_status != "All":
            filtered_tasks = [t for t in filtered_tasks if t["status"] == filter_status]
        
        df_tasks = pd.DataFrame(filtered_tasks)
        st.dataframe(df_tasks, use_container_width=True, hide_index=True)
        
        # Export option
        if not df_tasks.empty:
            csv = df_tasks.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Tasks as CSV", csv, f"my_tasks_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")

# ============================================================
# MAIN APP
# ============================================================

def main():
    # Initialize tasks if needed
    if not os.path.exists(TASKS_FILE):
        tasks = generate_all_tasks()
        save_tasks(tasks)
    
    # Initialize completed tasks for May 4 to June 5, 2026
    initialize_completed_tasks()
    
    # Authentication
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        st.markdown("""
        <div class="main-header">
            <h1>📋 MahaSTRIDE 24-Month Task Management System</h1>
            <p>May 2026 - April 2028 | Monday to Friday | 10:00 AM - 6:00 PM</p>
            <p>✅ <strong>May 4 to June 5, 2026 tasks are pre-completed</strong> as per the MPR</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("### 🔐 Login")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            
            if st.button("Login", use_container_width=True):
                if email in USERS:
                    hashed_input = sha256(password.encode()).hexdigest()
                    if USERS[email]["password"] == hashed_input:
                        st.session_state.authenticated = True
                        st.session_state.user_email = email
                        st.session_state.user_info = USERS[email]
                        st.rerun()
                    else:
                        st.error("Invalid password")
                else:
                    st.error("Email not found")
            
            show_credentials()
        
        return
    
    # Logged in view
    user_info = st.session_state.user_info
    email = st.session_state.user_email
    role = user_info.get("role", "data_analyst")
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 📋 MahaSTRIDE")
        st.markdown(f"**Welcome,**")
        st.markdown(f"**{user_info.get('name')}**")
        
        if role == "data_analyst":
            st.markdown(f"*Team: {user_info.get('team', 'N/A')}*")
        
        st.markdown(f"*Role: {role.upper()}*")
        st.markdown("---")
        
        if role == "admin":
            menu = st.radio("Navigation", ["📊 Dashboard", "👥 Team Management"])
        elif role == "project_lead":
            menu = st.radio("Navigation", ["👨‍💼 Lead Dashboard"])
        else:
            menu = st.radio("Navigation", ["📝 My Tasks"])
        
        st.markdown("---")
        st.markdown("**Working Hours**")
        st.markdown("🕐 10:00 AM - 6:00 PM")
        st.markdown("📅 Monday to Friday")
        
        st.markdown("---")
        st.markdown("**Completed Period**")
        st.markdown("✅ May 4 - June 5, 2026")
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()
    
    # Main content based on role
    if role == "admin":
        if menu == "📊 Dashboard":
            admin_dashboard()
        else:
            st.markdown("## 👥 Team Management")
            df_users = pd.DataFrame([{
                "Name": u["name"],
                "Role": u["role"],
                "Team": u.get("team", "N/A")
            } for u in USERS.values()])
            st.dataframe(df_users, use_container_width=True, hide_index=True)
    
    elif role == "project_lead":
        project_lead_dashboard()
    
    else:
        data_analyst_dashboard(email, user_info)
    
    # Footer
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: #666; font-size: 0.8rem;">
        <p>© 2026-2028 MahaSTRIDE Project | World Bank Loan No: IBRD 9737-IN | ICARE Pvt. Ltd.</p>
        <p>24-Month Project: May 2026 - April 2028 | Working Days: Monday to Friday | Hours: 10:00 - 18:00</p>
        <p>✅ May 4 to June 5, 2026 tasks completed as per MPR | Last Updated: {datetime.now().strftime('%d %B %Y, %H:%M:%S')}</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
