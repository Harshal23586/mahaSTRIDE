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

# University details
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

# Default daily plan for Phase 1 (May 7 - May 30, 2026)
DEFAULT_PLAN = {
    "2026-05-07": {
        "task_category": "Setup",
        "task": "University Onboarding & Role Introduction",
        "description": "Join university, meet VC & Registrar, introduce role. Meet Nodal Officer & ICARE Team to confirm workspace, access, and data sources.",
        "deliverables": "Introduction email to PMU & ICARE Head. Meeting minutes.",
        "framework": "Setup"
    },
    "2026-05-08": {
        "task_category": "Setup",
        "task": "NIRF Data Source Mapping",
        "description": "With Nodal Officer & ICARE Team, map all NIRF-related data sources: admission, academic, research, placement, finance, outreach. Identify missing data owners.",
        "deliverables": "NIRF Data Source Map (university-specific).",
        "framework": "Setup"
    },
    "2026-05-09": {
        "task_category": "WFH",
        "task": "WFH: Digital Forms & Data Requests",
        "description": "WFH: Review NIRF data templates. Create digital data collection forms. Organize department-wise data request letters.",
        "deliverables": "Digital forms created. Data request letters drafted.",
        "framework": "Setup"
    },
    "2026-05-11": {
        "task_category": "Documentation",
        "task": "NIRF Data Gap Template",
        "description": "Create NIRF Data Gap Template for FY 2022-23, 2023-24, 2024-25. Share with Nodal Officer & ICARE Team for validation.",
        "deliverables": "Gap template v1.0.",
        "framework": "Setup"
    },
    "2026-05-12": {
        "task_category": "Data Collection",
        "task": "Student Data Collection",
        "description": "Meet HoD (Academic) & Exam Cell - collect student enrollment, graduation, and backlog data.",
        "deliverables": "Raw data files saved.",
        "framework": "Data Collection"
    },
    "2026-05-13": {
        "task_category": "Data Collection",
        "task": "Faculty Data Collection",
        "description": "Meet Faculty/HR department - collect faculty count, designation, PhD qualification, experience.",
        "deliverables": "Faculty master data.",
        "framework": "Data Collection"
    },
    "2026-05-14": {
        "task_category": "Data Collection",
        "task": "Research Data Collection",
        "description": "Meet Research Cell - collect publications (Scopus/WoS/PubMed/UGC CARE), citations, patents, sponsored research projects.",
        "deliverables": "Research output spreadsheet.",
        "framework": "Data Collection"
    },
    "2026-05-15": {
        "task_category": "Data Collection",
        "task": "Placement Data Collection",
        "description": "Meet Placement Cell - collect placement data, median salary, higher education admission data.",
        "deliverables": "Placement & higher ed data.",
        "framework": "Data Collection"
    },
    "2026-05-16": {
        "task_category": "WFH",
        "task": "WFH: Data Digitization & Weekly Report",
        "description": "WFH: Digitize collected data. Create data validation scripts. Prepare weekly progress report for ICARE Team.",
        "deliverables": "Digitized dataset. Weekly report submitted.",
        "framework": "Data Collection"
    },
    "2026-05-18": {
        "task_category": "Data Collection",
        "task": "Financial Data Collection",
        "description": "Meet Finance/Accounts - collect financial data: research expenditure, infrastructure spending, university income.",
        "deliverables": "Finance data file.",
        "framework": "Data Collection"
    },
    "2026-05-19": {
        "task_category": "Data Collection",
        "task": "Library & IT Data Collection",
        "description": "Meet Library/IT - collect e-resources, digital repository, library subscriptions, IT infrastructure details.",
        "deliverables": "Library & IT data.",
        "framework": "Data Collection"
    },
    "2026-05-20": {
        "task_category": "Analysis",
        "task": "Data Consolidation & Gap Identification",
        "description": "Consolidate all collected data. Cross-verify with Nodal Officer & ICARE Team. Identify major gaps.",
        "deliverables": "Consolidated university dataset v1.",
        "framework": "Validation"
    },
    "2026-05-21": {
        "task_category": "Reporting",
        "task": "NIRF Gap Report",
        "description": "Prepare NIRF gap report - list missing data, incomplete years, inconsistent formats. Share with Nodal Officer & VC.",
        "deliverables": "Gap report submitted to Nodal Officer.",
        "framework": "Reporting"
    },
    "2026-05-22": {
        "task_category": "Meetings",
        "task": "Responsibility Assignment",
        "description": "Work with Nodal Officer & ICARE Team to assign responsibility for each gap to specific department heads.",
        "deliverables": "Responsibility matrix.",
        "framework": "Action Plan"
    },
    "2026-05-23": {
        "task_category": "WFH",
        "task": "WFH: Action Plan & Follow-ups",
        "description": "WFH: Analyze gap report. Create action plan templates. Prepare follow-up email drafts for departments.",
        "deliverables": "Action plan templates. Follow-up email drafts.",
        "framework": "Action Plan"
    },
    "2026-05-25": {
        "task_category": "Data Collection",
        "task": "Missing Data Follow-up",
        "description": "Follow up with departments for missing data. Assist them in extracting data in NIRF-required format.",
        "deliverables": "Updated data files.",
        "framework": "Data Collection"
    },
    "2026-05-26": {
        "task_category": "Analysis",
        "task": "Data Consistency Validation",
        "description": "Validate data consistency (enrollment totals, faculty counts match department lists).",
        "deliverables": "Validation log.",
        "framework": "Validation"
    },
    "2026-05-27": {
        "task_category": "Documentation",
        "task": "NIRF Draft Template",
        "description": "Prepare first draft of NIRF data template as per NIRF 2026 format. Share with Nodal Officer & ICARE Team for review.",
        "deliverables": "Draft NIRF submission file.",
        "framework": "Reporting"
    },
    "2026-05-28": {
        "task_category": "Meetings",
        "task": "Review Meeting with ICARE Team",
        "description": "Conduct review meeting with Nodal Officer, ICARE Team & IQAC team. Document pending items and action owners.",
        "deliverables": "Meeting minutes.",
        "framework": "Review"
    },
    "2026-05-29": {
        "task_category": "Reporting",
        "task": "May MPR Preparation",
        "description": "Finalize data collection status for May 2026. Prepare inputs for Monthly Progress Report (MPR).",
        "deliverables": "MPR inputs (to ICARE Head).",
        "framework": "Reporting"
    },
    "2026-05-30": {
        "task_category": "WFH",
        "task": "WFH: Finalize May MPR",
        "description": "WFH: Finalize May MPR. Compile all deliverables. Prepare for June action plan. Submit end-of-month report.",
        "deliverables": "May MPR final. End-of-month report.",
        "framework": "Reporting"
    }
}

# Pre-defined task categories for swapping/editing
TASK_CATEGORIES = {
    "Data Collection": [
        "Student enrollment data collection",
        "Faculty roster collection",
        "Research publications data",
        "Placement data collection",
        "Financial records collection",
        "Infrastructure data collection",
        "Library resources data",
        "Patent/IPR documentation",
        "Missing data follow-up",
        "Data validation"
    ],
    "Meetings": [
        "Meeting with Nodal Officer",
        "Meeting with VC/Registrar",
        "Meeting with ICARE Team",
        "Stakeholder consultation",
        "Department head coordination",
        "IQAC team meeting",
        "Review meeting"
    ],
    "Documentation": [
        "NIRF data template preparation",
        "Gap analysis report",
        "MPR preparation",
        "Weekly progress report",
        "Meeting minutes documentation",
        "Data request letters"
    ],
    "Analysis": [
        "Data consolidation",
        "Cross-verification of data",
        "Quality check",
        "Trend analysis",
        "Data validation"
    ],
    "Training": [
        "IQAC team training",
        "Department staff orientation",
        "Data entry training"
    ],
    "WFH": [
        "Data digitization",
        "Report compilation",
        "Email communications",
        "Documentation review",
        "Action plan preparation"
    ],
    "Other": [
        "Admin tasks",
        "Follow-up emails",
        "Document review",
        "Report generation"
    ]
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
PROJECT_END_DATE = datetime(2028, 5, 6)

# Data file paths
PROGRESS_DATA_FILE = "coordinator_progress_data.json"
ASSIGNMENTS_DATA_FILE = "assignments_data.json"
CUSTOM_TASKS_DATA_FILE = "custom_tasks_data.json"

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

def get_default_plan_for_date(date_str):
    """Get default plan for a specific date"""
    return DEFAULT_PLAN.get(date_str, None)

def add_custom_task_for_date(date_str, task_category, task_name, description, deliverables, added_by):
    """Add a custom task that overrides the default plan for a specific date"""
    custom_tasks = load_custom_tasks_data()
    custom_tasks["date_specific_tasks"][date_str] = {
        "task_category": task_category, 
        "task": task_name, 
        "description": description,
        "deliverables": deliverables, 
        "added_by": added_by, 
        "added_at": datetime.now().isoformat(),
        "is_custom": True
    }
    return save_custom_tasks_data(custom_tasks)

def get_plan_for_date(date_str):
    """Get plan for a specific date - custom task if exists, otherwise default"""
    custom_tasks = load_custom_tasks_data()
    if date_str in custom_tasks["date_specific_tasks"]:
        return custom_tasks["date_specific_tasks"][date_str]
    return get_default_plan_for_date(date_str)

def remove_custom_task_for_date(date_str):
    """Remove custom task for a date (revert to default)"""
    custom_tasks = load_custom_tasks_data()
    if date_str in custom_tasks["date_specific_tasks"]:
        del custom_tasks["date_specific_tasks"][date_str]
        return save_custom_tasks_data(custom_tasks)
    return False

def log_daily_entry(university_code, date, task_category, task_name, description, deliverables, status, hours_spent, remarks, swapped_from_default, edited_task, updated_by):
    data = load_progress_data()
    if university_code not in data:
        data[university_code] = {}
    
    data[university_code][date] = {
        "date": date, 
        "task_category": task_category, 
        "task_name": task_name,
        "description": description, 
        "deliverables": deliverables, 
        "status": status,
        "hours_spent": hours_spent, 
        "remarks": remarks, 
        "swapped_from_default": swapped_from_default,
        "edited_task": edited_task, 
        "updated_at": datetime.now().isoformat(), 
        "updated_by": updated_by
    }
    return save_progress_data(data)

def get_university_entries(university_code):
    data = load_progress_data()
    if university_code not in data:
        return pd.DataFrame()
    
    records = []
    for date, entry in data[university_code].items():
        records.append({
            "Date": date, 
            "Task Category": entry.get("task_category", ""), 
            "Task": entry.get("task_name", ""),
            "Description": entry.get("description", ""), 
            "Deliverables": entry.get("deliverables", ""),
            "Status": entry.get("status", "").upper(), 
            "Hours Spent": entry.get("hours_spent", 0),
            "Swapped": "✅" if entry.get("swapped_from_default", False) else "❌",
            "Edited": "✅" if entry.get("edited_task", False) else "❌",
            "Remarks": entry.get("remarks", ""), 
            "Updated At": entry.get("updated_at", "")[:16] if entry.get("updated_at") else "",
            "Updated By": entry.get("updated_by", "")
        })
    
    if not records:
        return pd.DataFrame()
    
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
                "date": date, 
                "task_category": entry.get("task_category", ""), 
                "task_name": entry.get("task_name", ""),
                "description": entry.get("description", ""), 
                "deliverables": entry.get("deliverables", ""),
                "status": entry.get("status", ""), 
                "hours_spent": entry.get("hours_spent", 0)
            })
    return monthly_entries

def get_daily_progress_data():
    data = load_progress_data()
    daily_records = []
    
    for uni_code, entries in data.items():
        uni_name = UNIVERSITIES[uni_code]["name"]
        for date, entry in entries.items():
            daily_records.append({
                "Date": date, 
                "University": uni_name, 
                "University Code": uni_code,
                "Task": entry.get("task_name", ""), 
                "Category": entry.get("task_category", ""),
                "Status": entry.get("status", ""), 
                "Hours": entry.get("hours_spent", 0)
            })
    
    df = pd.DataFrame(daily_records)
    if not df.empty:
        df["Date"] = pd.to_datetime(df["Date"])
    return df

def get_weekly_progress_data():
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
                "status": status, 
                "completed_at": datetime.now().isoformat() if status == "completed" else None,
                "remarks": remarks, 
                "completed_by": completed_by
            }
            return save_assignments_data(assignments_data)
    return False

def get_summary_stats():
    data = load_progress_data()
    stats = []
    
    for uni_code, uni_info in UNIVERSITIES.items():
        entries = data.get(uni_code, {})
        total_days = len(entries)
        completed = sum(1 for e in entries.values() if e.get("status") == "completed")
        in_progress = sum(1 for e in entries.values() if e.get("status") == "in_progress")
        total_hours = sum(e.get("hours_spent", 0) for e in entries.values())
        swapped = sum(1 for e in entries.values() if e.get("swapped_from_default", False))
        edited = sum(1 for e in entries.values() if e.get("edited_task", False))
        
        stats.append({
            "University": uni_info["name"],
            "Code": uni_code,
            "Coordinators": uni_info["coordinators"],
            "Nodal Officer": uni_info["nodal_officer"],
            "Days Logged": total_days,
            "Completed": completed,
            "In Progress": in_progress,
            "Total Hours": round(total_hours, 1),
            "Swapped": swapped,
            "Edited": edited,
            "Completion %": round((completed / total_days * 100), 1) if total_days > 0 else 0
        })
    
    return pd.DataFrame(stats)

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
    
    st.subheader("📊 Progress Infographics")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Daily Progress", "📅 Weekly Progress", "📆 Monthly Progress", "🏛️ University-wise"])
    
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
        
        summary_df = get_summary_stats()
        if not summary_df.empty:
            col1, col2 = st.columns(2)
            with col1:
                fig7 = px.bar(summary_df, x="University", y="Completion %", title="University-wise Completion %", color="Completion %", text="Completion %", height=500)
                fig7.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                st.plotly_chart(fig7, use_container_width=True)
            with col2:
                fig8 = px.bar(summary_df, x="University", y="Total Hours", title="University-wise Total Hours", color="Total Hours", text="Total Hours", height=500)
                fig8.update_traces(texttemplate='%{text:.1f}', textposition='outside')
                st.plotly_chart(fig8, use_container_width=True)
            
            st.dataframe(summary_df, use_container_width=True)
        else:
            st.info("No data available yet")

def create_project_lead_dashboard():
    st.markdown('<div class="projectlead-card"><h2>👨‍💼 Project Lead Dashboard - Dr. Harshal Kotwal</h2><p>Assign Tasks & Monitor Progress (2-Year Project)</p></div>', unsafe_allow_html=True)
    
    st.info(f"📅 **Project Duration:** {PROJECT_START_DATE.strftime('%d-%b-%Y')} to {PROJECT_END_DATE.strftime('%d-%b-%Y')} (2 Years)")
    
    show_sangam_info()
    
    st.markdown("---")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📅 Assign Task to Date", "📊 Progress Dashboard", "📝 Manage Assignments", "📈 Analytics"])
    
    with tab1:
        st.subheader("📅 Assign a Custom Task for Any Date")
        st.markdown("Assign tasks that override the default plan for specific dates. Coordinators will see these as their assigned tasks.")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            with st.form("add_custom_task_form"):
                task_date = st.date_input("Select Date", min_value=PROJECT_START_DATE, max_value=PROJECT_END_DATE)
                task_category = st.selectbox("Task Category", list(TASK_CATEGORIES.keys()))
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
                        if st.button(f"Remove", key=f"remove_{date_str}"):
                            remove_custom_task_for_date(date_str)
                            st.rerun()
            else:
                st.info("No custom tasks assigned. Using default plan for all dates.")
        
        st.markdown("---")
        st.markdown("### Default Plan Preview")
        preview_date = st.selectbox("Select Date to View Default Plan", list(DEFAULT_PLAN.keys())[:10])
        if preview_date:
            plan = DEFAULT_PLAN.get(preview_date, {})
            st.markdown(f"""
            <div class="default-task-card">
                <strong>📌 Default Plan for {preview_date}</strong><br>
                <strong>Task:</strong> {plan.get('task', 'N/A')}<br>
                <strong>Category:</strong> {plan.get('task_category', 'N/A')}<br>
                <strong>Description:</strong> {plan.get('description', 'N/A')}<br>
                <strong>Deliverables:</strong> {plan.get('deliverables', 'N/A')}
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.subheader("📊 Coordinator Progress Overview")
        
        summary_df = get_summary_stats()
        if not summary_df.empty:
            fig = px.bar(summary_df, x="University", y="Completion %", title="University-wise Progress", color="Completion %", text="Completion %", height=500)
            fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(summary_df, use_container_width=True)
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
            
            st.subheader("📥 Export Data")
            csv_daily = daily_df.to_csv(index=False)
            st.download_button("📊 Export Daily Data (CSV)", csv_daily, "daily_progress.csv", "text/csv")
        else:
            st.info("No data available yet")

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
            
            task_category = st.selectbox("Task Category", list(TASK_CATEGORIES.keys()),
                                        index=list(TASK_CATEGORIES.keys()).index(existing_entry.get("task_category", "Data Collection")) if existing_entry.get("task_category") in TASK_CATEGORIES else 0)
            
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
                <strong>📌 Your Planned Task for Today ({today_day}, {today_str})</strong><br>
                <strong>Task:</strong> {plan_for_today['task']}<br>
                <strong>Category:</strong> {plan_for_today['task_category']}<br>
                <strong>Description:</strong> {plan_for_today['description']}<br>
                <strong>Expected Deliverables:</strong> {plan_for_today['deliverables']}
            </div>
            """, unsafe_allow_html=True)
            
            use_planned = st.radio("", ["✅ Yes, I completed the planned task", "🔄 No, I want to log a different task"], horizontal=True)
        else:
            use_planned = "🔄 No, I want to log a different task"
            st.info(f"No planned task for {today_str}. Please log your work below.")
        
        with st.form("daily_entry_form"):
            st.markdown("### Today's Work Log")
            
            if use_planned == "✅ Yes, I completed the planned task" and plan_for_today:
                task_category = plan_for_today['task_category']
                task_name = plan_for_today['task']
                description = plan_for_today['description']
                deliverables = plan_for_today['deliverables']
                st.info(f"Using planned task: {task_name}")
                st.text_input("Task Category", value=task_category, disabled=True)
                st.text_input("Task", value=task_name, disabled=True)
            else:
                task_category = st.selectbox("Task Category", list(TASK_CATEGORIES.keys()))
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
                if use_planned == "✅ Yes, I completed the planned task" and plan_for_today:
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
            menu = st.radio("Navigation", ["📊 Admin Dashboard", "ℹ️ About"])
        elif user_role == "project_lead":
            menu = st.radio("Navigation", ["👨‍💼 Project Lead Dashboard", "📝 Assignments", "ℹ️ About"])
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
            - Default planned tasks for Phase 1 (May 7-30, 2026)
            - Custom task assignment by Project Lead
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
        else:
            st.title("ℹ️ About")
            st.markdown("### Project Lead Dashboard\n\n**Features:**\n- Assign custom tasks to specific dates (overrides default plan)\n- Monitor coordinator progress\n- Create and manage assignments\n- View default plan for Phase 1\n- 2-year project timeline support")
    
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
                
                **How to Log Work:**
                1. You'll see your planned task for the day
                2. If you completed it, just confirm and submit
                3. If you did something different, select "Log Different Task"
                4. Add description, deliverables, and hours spent
                
                **Phase 1 (May 7-30, 2026) has default planned tasks.**
                After Phase 1, Project Lead will assign tasks as needed.
                """)

if __name__ == "__main__":
    # Initialize data files if they don't exist
    if not os.path.exists(PROGRESS_DATA_FILE):
        save_progress_data(create_initial_progress_data())
    if not os.path.exists(ASSIGNMENTS_DATA_FILE):
        save_assignments_data(create_initial_assignments_data())
    if not os.path.exists(CUSTOM_TASKS_DATA_FILE):
        save_custom_tasks_data(create_initial_custom_tasks_data())
    
    main()
