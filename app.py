import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os
import json
from hashlib import sha256
import base64

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
    .storage-disconnected {
        background-color: #f8d7da;
        color: #721c24;
    }
    .default-task-card {
        background: linear-gradient(135deg, #e8f8f5 0%, #d4efdf 100%);
        border-left: 4px solid #27ae60;
        padding: 1.2rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .completed-badge {
        background-color: #28a745;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# USER CREDENTIALS - Updated with all coordinators
# ============================================================
USERS = {
    # Admin
    "admin@mahastride.com": {
        "password": sha256("Admin@2026".encode()).hexdigest(),
        "role": "admin",
        "name": "Admin"
    },
    # Project Lead (MITRA Level)
    "projectlead@mahastride.com": {
        "password": sha256("ProjectLead@2026".encode()).hexdigest(),
        "role": "project_lead",
        "name": "Dr. Harshal Kotwal"
    },
    # MITRA Level Coordinator
    "shubham@mitra.gov.in": {
        "password": sha256("Shubham@2026".encode()).hexdigest(),
        "role": "coordinator",
        "name": "Shubham",
        "university": "MITRA"
    },
    # Mumbai University (2 coordinators)
    "sneha@mu.edu": {
        "password": sha256("Sneha@2026".encode()).hexdigest(),
        "role": "coordinator",
        "name": "Ms Sneha",
        "university": "MU"
    },
    "sagar@mu.edu": {
        "password": sha256("Sagar@2026".encode()).hexdigest(),
        "role": "coordinator",
        "name": "Mr Sagar",
        "university": "MU"
    },
    # SPPU Pune
    "jagan@sspu.edu": {
        "password": sha256("Jagan@2026".encode()).hexdigest(),
        "role": "coordinator",
        "name": "Mr Jagan",
        "university": "SSPU"
    },
    # COEP Pune
    "vaibhav@coep.edu": {
        "password": sha256("Vaibhav@2026".encode()).hexdigest(),
        "role": "coordinator",
        "name": "Mr Vaibhav",
        "university": "COEP"
    },
    # Amravati University
    "pratham@au.edu": {
        "password": sha256("Pratham@2026".encode()).hexdigest(),
        "role": "coordinator",
        "name": "Mr Pratham",
        "university": "AU"
    },
    # Nagpur University
    "anjali@nu.edu": {
        "password": sha256("Anjali@2026".encode()).hexdigest(),
        "role": "coordinator",
        "name": "Ms Anjali",
        "university": "NU"
    },
    # KBCNMU Jalgaon
    "nitish@kbcnmu.edu": {
        "password": sha256("Nitish@2026".encode()).hexdigest(),
        "role": "coordinator",
        "name": "Mr Nitish",
        "university": "KBCNMU"
    },
    # BAMU Aurangabad
    "atharv@bamu.edu": {
        "password": sha256("Atharv@2026".encode()).hexdigest(),
        "role": "coordinator",
        "name": "Mr Atharv",
        "university": "BAMU"
    }
}

# ============================================================
# UNIVERSITY DETAILS - Updated with correct coordinators
# ============================================================
UNIVERSITIES = {
    "MU": {
        "name": "Mumbai University",
        "coordinators": ["Ms Sneha", "Mr Sagar"],
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
        "name": "COEP Technological University, Pune",
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
        "name": "KBCNMU, Jalgaon",
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
    },
    "MITRA": {
        "name": "MITRA (PMU)",
        "coordinators": ["Shubham"],
        "nodal_officer": "Dr. Harshal Kotwal",
        "registrar": "_________",
        "vc": "_________"
    }
}

# MITRA Officials
MITRA_OFFICIALS = {
    "project_director": "Dr. Harshal Kotwal, Project Director, MahaSTRIDE",
    "coordinator": "Shubham, Coordinator, MITRA",
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
| 11:00 AM-1:00 PM | Data collection / meetings with departments / Training sessions |
| 1:00-2:00 PM | Lunch |
| 2:00-5:30 PM | Data validation, gap analysis, documentation |
| 5:30-6:00 PM | Update daily tracker; email summary to ICARE Project Head |
| 6:00 PM | Departure |
"""

WORKING_HOURS = "10:00 AM - 6:00 PM"

# ============================================================
# DEFAULT PLAN FOR MAY 2026 - 20 WORKING DAYS
# Working days: May 7,8,9,11,12,13,14,15,16,18,19,20,21,22,23,25,26,27,29,30
# Total: 20 working days (May 7-30 excluding weekends and May 1, May 28 holidays)
# ============================================================

DEFAULT_PLAN = {
    # Week 1 (May 7-9) - Setup & Onboarding
    "2026-05-07": {
        "task_category": "Setup", 
        "task": "University Reporting & Onboarding", 
        "description": "Report to university. Meet VC & Registrar, introduce role. Meet Nodal Officer & ICARE Team to confirm workspace, access, and data sources.", 
        "deliverables": "Onboarding completion report. Meeting minutes.",
        "framework": "Setup"
    },
    "2026-05-08": {
        "task_category": "Setup", 
        "task": "NIRF Data Source Mapping", 
        "description": "With Nodal Officer & ICARE Team, map all NIRF-related data sources across the university. Identify data owners for each parameter.", 
        "deliverables": "NIRF Data Source Map (university-specific). Data owner contact list.",
        "framework": "Setup"
    },
    "2026-05-09": {
        "task_category": "Setup", 
        "task": "WFH: Digital Forms & Data Templates", 
        "description": "Review NIRF data templates. Create digital data collection forms. Prepare department-wise data request letters.", 
        "deliverables": "Digital forms created. Data request letters drafted.",
        "framework": "Setup"
    },
    
    # Week 2 (May 11-16) - Training Programs (6 days intensive training)
    "2026-05-11": {
        "task_category": "Training", 
        "task": "Training: NIRF Framework & Formula Interpretation", 
        "description": "Training session on NIRF framework structure, architecture, and category-specific indicators. Introduction to GRDAU concept.", 
        "deliverables": "Training completion report. Attendance sheet.",
        "framework": "Training"
    },
    "2026-05-12": {
        "task_category": "Training", 
        "task": "Training: Teaching, Learning & Resources (TLR) Parameter", 
        "description": "Detailed training on TLR indicators: Student Strength (SS), Faculty-Student Ratio (FSR), Faculty Qualifications (FQE), Financial Resources (FRU).", 
        "deliverables": "Training materials. Exercise solutions.",
        "framework": "Training"
    },
    "2026-05-13": {
        "task_category": "Training", 
        "task": "Training: Research & Professional Practice (RP) Parameter", 
        "description": "Training on bibliometric indicators, research productivity, citation analysis, IPR, patents.", 
        "deliverables": "Research metrics training completion.",
        "framework": "Training"
    },
    "2026-05-14": {
        "task_category": "Training", 
        "task": "Training: Graduation Outcomes (GO) & Outreach (OI) Parameters", 
        "description": "Training on graduation rates, placement statistics, median salary, gender representation, outreach activities.", 
        "deliverables": "Training completion report.",
        "framework": "Training"
    },
    "2026-05-15": {
        "task_category": "Training", 
        "task": "Training: Perception (PR) & NIRF Submission Process", 
        "description": "Training on Perception parameter, peer perception, public perception. NIRF submission process overview.", 
        "deliverables": "Training completion report.",
        "framework": "Training"
    },
    "2026-05-16": {
        "task_category": "WFH", 
        "task": "WFH: Training Review & Data Preparation", 
        "description": "Review training materials. Prepare training feedback summary. Organize data collection templates.", 
        "deliverables": "Training feedback report. Organized data templates.",
        "framework": "Training Review"
    },
    
    # Week 3 (May 18-23) - Data Collection
    "2026-05-18": {
        "task_category": "Data Collection", 
        "task": "Student Enrollment & Faculty Data Collection", 
        "description": "Collect student enrollment (UG/PG/PhD), graduation data (batch-wise) and faculty details including PhD qualifications, experience.", 
        "deliverables": "Student and faculty data files.",
        "framework": "Data Collection"
    },
    "2026-05-19": {
        "task_category": "Data Collection", 
        "task": "Research & Placement Data Collection", 
        "description": "Collect research publications (Scopus/WoS indexed), citations data, patents filed/granted, and placement statistics with salary details.", 
        "deliverables": "Research and placement data files.",
        "framework": "Data Collection"
    },
    "2026-05-20": {
        "task_category": "Data Collection", 
        "task": "Financial & Infrastructure Data Collection", 
        "description": "Collect financial records (annual budget, utilization), library resources (books, journals, e-resources), and IT infrastructure details.", 
        "deliverables": "Financial and infrastructure data files.",
        "framework": "Data Collection"
    },
    "2026-05-21": {
        "task_category": "Analysis", 
        "task": "Data Consolidation & Validation - Phase 1", 
        "description": "Consolidate all collected data. Cross-verify with source documents. Identify gaps in student, faculty, research data.", 
        "deliverables": "Consolidated dataset v1. Gap analysis report (Phase 1).",
        "framework": "Analysis"
    },
    "2026-05-22": {
        "task_category": "Meetings", 
        "task": "Stakeholder Consultation Meeting", 
        "description": "Conduct meeting with department heads to discuss data gaps, validate collected data, and plan for missing data collection.", 
        "deliverables": "Meeting minutes with decisions and action items.",
        "framework": "Coordination"
    },
    "2026-05-23": {
        "task_category": "WFH", 
        "task": "WFH: Inception Report Drafting", 
        "description": "Begin drafting Inception Report: team deployment structure, project roll-out methodology, execution roadmap, communication plan.", 
        "deliverables": "Inception Report draft v1 (Deliverable 1 - Due June 6)",
        "framework": "Reporting"
    },
    
    # Week 4 (May 25-30) - Reporting & GRDAU Planning
    "2026-05-25": {
        "task_category": "Data Collection", 
        "task": "Missing Data Follow-up", 
        "description": "Follow up with departments for missing data. Assist in data extraction and validation.", 
        "deliverables": "Updated data files for missing parameters.",
        "framework": "Data Collection"
    },
    "2026-05-26": {
        "task_category": "Analysis", 
        "task": "NIRF Data Template Preparation", 
        "description": "Prepare first draft of NIRF data template as per NIRF 2026 format using collected data.", 
        "deliverables": "Draft NIRF submission file.",
        "framework": "Reporting"
    },
    "2026-05-27": {
        "task_category": "Documentation", 
        "task": "SWOT Analysis & Gap Report", 
        "description": "Finalize university-specific SWOT analysis and gap identification report.", 
        "deliverables": "SWOT analysis report. Final gap report.",
        "framework": "Reporting"
    },
    "2026-05-29": {
        "task_category": "Meetings", 
        "task": "Review Meeting with ICARE Team", 
        "description": "Conduct review meeting with Nodal Officer, ICARE Team & IQAC team to review May progress.", 
        "deliverables": "Meeting minutes with action items.",
        "framework": "Coordination"
    },
    "2026-05-30": {
        "task_category": "Reporting", 
        "task": "May MPR Finalization", 
        "description": "Finalize data collection status for May 2026. Prepare Monthly Progress Report (MPR) for submission.", 
        "deliverables": "May MPR ready for submission.",
        "framework": "Reporting"
    },
}

# Pre-defined task categories
TASK_CATEGORIES = {
    "Setup": ["University onboarding", "NIRF data source mapping", "Creating data collection forms"],
    "Training": ["NIRF Framework training", "TLR parameter training", "RP parameter training", "GO & OI training", "PR parameter training"],
    "Data Collection": ["Student data", "Faculty data", "Research data", "Placement data", "Financial data", "Infrastructure data"],
    "Analysis": ["Data consolidation", "Data validation", "Gap analysis", "SWOT analysis"],
    "Reporting": ["NIRF template", "Diagnostic report", "MPR preparation", "Inception Report"],
    "Meetings": ["Stakeholder consultation", "Department coordination", "Review meeting"],
    "WFH": ["Data digitization", "Report compilation", "Training review"],
    "Coordination": ["Department follow-up", "Email communications", "Action item tracking"]
}

# ============================================================
# TEAM MEMBERS - Updated with correct structure
# MITRA Level: Dr. Harshal Kotwal (Project Director), Shubham (Coordinator), ICARE Team
# University Level: Coordinators as specified
# ============================================================
TEAM_MEMBERS = {
    "MITRA": [
        {"name": "Dr. Harshal Kotwal", "profile": "Project Director, MahaSTRIDE", "location": "MITRA, Mumbai"},
        {"name": "Shubham", "profile": "Coordinator, MITRA", "location": "MITRA, Mumbai"},
        {"name": "Shri Karthick Sridhar", "profile": "Project Head, ICARE", "location": "MITRA, Mumbai"},
        {"name": "Data Analytics Specialist", "profile": "Data Analytics and Dashboard Specialist", "location": "MITRA, Mumbai"}
    ],
    "MU": [
        {"name": "Ms Sneha", "profile": "Institutional Coordinator cum Research & Innovation Officer", "location": "Mumbai University"},
        {"name": "Mr Sagar", "profile": "Institutional Coordinator cum Research & Innovation Officer", "location": "Mumbai University"},
        {"name": "Statistician", "profile": "Statistician & Program Designer", "location": "Mumbai University"}
    ],
    "SSPU": [{"name": "Mr Jagan", "profile": "Institutional Coordinator cum Research & Innovation Officer", "location": "Savitribai Phule Pune University"}],
    "COEP": [{"name": "Mr Vaibhav", "profile": "Institutional Coordinator cum Research & Innovation Officer", "location": "COEP Technological University"}],
    "AU": [{"name": "Mr Pratham", "profile": "Institutional Coordinator cum Research & Innovation Officer", "location": "Sant Gadge Baba Amravati University"}],
    "NU": [{"name": "Ms Anjali", "profile": "Institutional Coordinator cum Research & Innovation Officer", "location": "Rashtrasant Tukadoji Maharaj Nagpur University"}],
    "KBCNMU": [{"name": "Mr Nitish", "profile": "Institutional Coordinator cum Research & Innovation Officer", "location": "KBCNMU Jalgaon University"}],
    "BAMU": [{"name": "Mr Atharv", "profile": "Institutional Coordinator cum Research & Innovation Officer", "location": "BAMU Aurangabad"}]
}

def hash_password(password):
    return sha256(password.encode()).hexdigest()

def authenticate_user(email, password):
    if email in USERS:
        if USERS[email]["password"] == hash_password(password):
            return True, USERS[email]["role"], USERS[email]["name"], USERS[email].get("university", None)
    return False, None, None, None

# ============================================================
# DATA MANAGEMENT FUNCTIONS
# ============================================================

# File paths for local storage
PROGRESS_DATA_FILE = "coordinator_progress_data.json"
ASSIGNMENTS_DATA_FILE = "assignments_data.json"
CUSTOM_TASKS_DATA_FILE = "custom_tasks_data.json"
ATTENDANCE_DATA_FILE = "attendance_data.json"
MPR_DATA_FILE = "mpr_data.json"

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

def create_initial_mpr_data():
    return {
        "work_order_ref": "MITRA/Research/MahaSTRIDE/EduRFP/49/2025",
        "work_order_date": "11-05-2026",
        "period_start": "2026-05-07",
        "period_end": "2026-05-30",
        "major_activities": [],
        "meetings": [],
        "deliverables": [],
        "risks": [],
        "initiatives": []
    }

def load_progress_data():
    try:
        if os.path.exists(PROGRESS_DATA_FILE):
            with open(PROGRESS_DATA_FILE, 'r') as f:
                data = json.load(f)
                for uni_code in UNIVERSITIES.keys():
                    if uni_code not in data:
                        data[uni_code] = {}
                return data
    except:
        pass
    return create_initial_progress_data()

def save_progress_data(data):
    try:
        with open(PROGRESS_DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except:
        return False

def load_assignments_data():
    try:
        if os.path.exists(ASSIGNMENTS_DATA_FILE):
            with open(ASSIGNMENTS_DATA_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return create_initial_assignments_data()

def save_assignments_data(data):
    try:
        with open(ASSIGNMENTS_DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except:
        return False

def load_custom_tasks_data():
    try:
        if os.path.exists(CUSTOM_TASKS_DATA_FILE):
            with open(CUSTOM_TASKS_DATA_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return create_initial_custom_tasks_data()

def save_custom_tasks_data(data):
    try:
        with open(CUSTOM_TASKS_DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except:
        return False

def load_attendance_data():
    try:
        if os.path.exists(ATTENDANCE_DATA_FILE):
            with open(ATTENDANCE_DATA_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return create_initial_attendance_data()

def save_attendance_data(data):
    try:
        with open(ATTENDANCE_DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except:
        return False

def load_mpr_data():
    try:
        if os.path.exists(MPR_DATA_FILE):
            with open(MPR_DATA_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return create_initial_mpr_data()

def save_mpr_data(data):
    try:
        with open(MPR_DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except:
        return False

def load_team_attendance():
    return load_attendance_data()

def save_team_attendance(data):
    return save_attendance_data(data)

def update_team_attendance(team_type, member_name, present_days, absent_days, holidays):
    attendance = load_team_attendance()
    if team_type not in attendance:
        attendance[team_type] = {}
    attendance[team_type][member_name] = {
        "present_days": present_days,
        "absent_days": absent_days,
        "holidays": holidays,
        "total_working_days": present_days + absent_days + holidays,
        "updated_at": datetime.now().isoformat()
    }
    return save_team_attendance(attendance)

def get_plan_for_date(date_str):
    custom_tasks = load_custom_tasks_data()
    if date_str in custom_tasks.get("date_specific_tasks", {}):
        return custom_tasks["date_specific_tasks"][date_str]
    return DEFAULT_PLAN.get(date_str, None)

def get_all_planned_dates():
    return list(DEFAULT_PLAN.keys())

def get_pending_tasks_for_coordinator(university_code):
    data = load_progress_data()
    completed_dates = set(data.get(university_code, {}).keys())
    all_planned_dates = get_all_planned_dates()
    
    pending_dates = []
    for date in all_planned_dates:
        if date not in completed_dates:
            plan = get_plan_for_date(date)
            if plan:
                pending_dates.append({
                    "date": date,
                    "task": plan.get("task", ""),
                    "category": plan.get("task_category", ""),
                    "description": plan.get("description", ""),
                    "deliverables": plan.get("deliverables", ""),
                    "framework": plan.get("framework", "")
                })
    return pending_dates

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

def mark_all_tasks_completed(university_code):
    """Mark all tasks as completed for a university"""
    data = load_progress_data()
    if university_code not in data:
        data[university_code] = {}
    
    all_dates = get_all_planned_dates()
    for date in all_dates:
        plan = get_plan_for_date(date)
        if plan:
            data[university_code][date] = {
                "date": date, 
                "task_category": plan.get("task_category", ""), 
                "task_name": plan.get("task", ""),
                "description": plan.get("description", ""), 
                "deliverables": plan.get("deliverables", ""),
                "status": "completed", 
                "hours_spent": 8.0, 
                "remarks": "Task completed as per plan",
                "swapped_from_default": False, 
                "edited_task": False, 
                "updated_at": datetime.now().isoformat(), 
                "updated_by": "system"
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
            "Remarks": entry.get("remarks", ""), "Updated At": entry.get("updated_at", "")[:16] if entry.get("updated_at") else "",
            "Updated By": entry.get("updated_by", "")
        })
    
    if not records:
        return pd.DataFrame()
    return pd.DataFrame(records).sort_values("Date", ascending=False)

def get_summary_stats():
    data = load_progress_data()
    stats = []
    
    for uni_code, uni_info in UNIVERSITIES.items():
        entries = data.get(uni_code, {})
        total_planned = len(get_all_planned_dates())
        completed = sum(1 for e in entries.values() if e.get("status") == "completed")
        total_hours = sum(e.get("hours_spent", 0) for e in entries.values())
        pending = total_planned - completed
        
        if completed == total_planned:
            status_label = "✅ Completed"
        elif completed >= total_planned * 0.5:
            status_label = "🟡 Substantially Complete"
        elif completed > 0:
            status_label = "🔵 Initiated"
        else:
            status_label = "⚪ Not Started"
        
        stats.append({
            "University": uni_info["name"],
            "Code": uni_code,
            "Coordinators": ", ".join(uni_info["coordinators"]),
            "Nodal Officer": uni_info["nodal_officer"],
            "Planned Tasks": total_planned,
            "Completed Tasks": completed,
            "Pending Tasks": pending,
            "Total Hours Invested": round(total_hours, 1),
            "Status": status_label
        })
    return pd.DataFrame(stats)

def reset_all_data():
    save_progress_data(create_initial_progress_data())
    save_assignments_data(create_initial_assignments_data())
    save_custom_tasks_data(create_initial_custom_tasks_data())
    save_attendance_data(create_initial_attendance_data())
    save_mpr_data(create_initial_mpr_data())
    return True

def initialize_all_data():
    """Initialize all data with completed tasks for all universities"""
    for uni_code in UNIVERSITIES.keys():
        mark_all_tasks_completed(uni_code)
    
    # Set default attendance data
    attendance = load_team_attendance()
    for team_type, members in TEAM_MEMBERS.items():
        if team_type not in attendance:
            attendance[team_type] = {}
        for member in members:
            attendance[team_type][member["name"]] = {
                "present_days": 20,
                "absent_days": 0,
                "holidays": 11,
                "total_working_days": 31,
                "updated_at": datetime.now().isoformat()
            }
    save_team_attendance(attendance)
    
    return True

def generate_complete_mpr_html(university_code):
    """Generate complete MPR as per Annexure C format"""
    uni_info = UNIVERSITIES[university_code]
    entries_df = get_university_entries(university_code)
    attendance_data = load_team_attendance()
    mpr_data = load_mpr_data()
    
    completed_count = len(entries_df) if not entries_df.empty else 0
    total_planned = len(get_all_planned_dates())
    
    period_start = datetime.strptime(mpr_data.get("period_start", "2026-05-07"), "%Y-%m-%d")
    period_end = datetime.strptime(mpr_data.get("period_end", "2026-05-30"), "%Y-%m-%d")
    
    if completed_count == total_planned:
        activity_status = "✅ Completed"
        inception_status = "✅ Completed"
    elif completed_count >= total_planned * 0.5:
        activity_status = "🟡 Substantially Complete"
        inception_status = "🟡 Substantially Complete"
    elif completed_count > 0:
        activity_status = "🔵 Initiated"
        inception_status = "🟡 In Progress"
    else:
        activity_status = "⚪ Not Started"
        inception_status = "⚪ Not Started"
    
    coordinators_str = ", ".join(uni_info['coordinators'])
    nodal_officer_str = uni_info['nodal_officer']
    registrar_str = uni_info['registrar']
    
    # Build team attendance rows for MITRA level
    mitra_rows = ""
    mitra_members = TEAM_MEMBERS.get("MITRA", [])
    sr_no = 1
    for member in mitra_members:
        att = attendance_data.get("MITRA", {}).get(member["name"], {})
        present = att.get('present_days', 20)
        absent = att.get('absent_days', 0)
        holidays = att.get('holidays', 11)
        mitra_rows += f"""
        <tr>
            <td>{sr_no}</td>
            <td>{member['name']}</td>
            <td>{member['profile']}</td>
            <td>{member['location']}</td>
            <td>{present}</td>
            <td>{absent}</td>
            <td>{holidays}</td>
        </tr>"""
        sr_no += 1
    
    # Build team attendance rows for this university
    uni_rows = ""
    uni_members = TEAM_MEMBERS.get(university_code, [])
    for member in uni_members:
        att = attendance_data.get(university_code, {}).get(member["name"], {})
        present = att.get('present_days', 20)
        absent = att.get('absent_days', 0)
        holidays = att.get('holidays', 11)
        uni_rows += f"""
        <tr>
            <td>{sr_no}</td>
            <td>{member['name']}</td>
            <td>{member['profile']}</td>
            <td>{member['location']}</td>
            <td>{present}</td>
            <td>{absent}</td>
            <td>{holidays}</td>
        </tr>"""
        sr_no += 1
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Monthly Progress Report - {uni_info['name']}</title>
        <style>
            body {{ font-family: 'Times New Roman', serif; margin: 0.7in; font-size: 11pt; line-height: 1.2; }}
            .header {{ text-align: center; margin-bottom: 20px; }}
            .mitra-title {{ font-size: 12pt; font-weight: bold; }}
            .confidential {{ text-align: right; font-weight: bold; margin-bottom: 20px; font-size: 10pt; }}
            .report-title {{ font-size: 14pt; font-weight: bold; text-align: center; margin: 15px 0; }}
            .section-title {{ font-size: 12pt; font-weight: bold; margin-top: 15px; margin-bottom: 8px; background-color: #e8e8e8; padding: 5px; }}
            table {{ width: 100%; border-collapse: collapse; margin: 10px 0; font-size: 10pt; }}
            th, td {{ border: 1px solid #000; padding: 5px; vertical-align: top; }}
            th {{ background-color: #e8e8e8; font-weight: bold; text-align: center; }}
            .sub-header {{ background-color: #d0d0d0; font-weight: bold; }}
            .footer {{ text-align: center; font-size: 9pt; font-style: italic; margin-top: 30px; }}
            .signature-table {{ border: none; }}
            .signature-table td {{ border: none; padding: 5px; }}
            .completed {{ color: #28a745; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="confidential">Confidential</div>
        <div class="header">
            <div class="mitra-title">Maharashtra Institution for Transformation (MITRA)</div>
            <div>5th Floor, Nirmal, Nariman Point, Mumbai-400021</div>
            <div>Office Tel. No. 022 69979440 | Email: pmu.mahastride@mahamitra.org</div>
        </div>
        
        <div class="report-title">MONTHLY PROGRESS REPORT</div>
        <div style="text-align: center;">(From {period_start.strftime('%d-%m-%Y')} to {period_end.strftime('%d-%m-%Y')})</div>
        
        <table>
            <tr><td style="width:30%"><strong>Work Order Reference</strong></td>
            <td>{mpr_data.get('work_order_ref', 'MITRA/Research/MahaSTRIDE/EduRFP/49/2025')}<br>dated {mpr_data.get('work_order_date', '11-05-2026')}</td>
            <td style="width:30%"><strong>University / Division</strong></td>
            <td>{uni_info['name']}</td>
        </tr>
        <tr>
            <td><strong>Work Order Start Date</strong></td>
            <td>{period_start.strftime('%d-%b-%Y')}</td>
            <td><strong>Work Order End Date</strong></td>
            <td>{period_end.strftime('%d-%b-%Y')}</td>
        </tr>
        <tr>
            <td><strong>Project Start Date</strong></td>
            <td>07-May-2026</td>
            <td><strong>Project End Date</strong></td>
            <td>06-May-2028</td>
        </tr>
        </table>
        
        <div class="section-title">Project Team Deployment</div>
        <table>
            <tr class="sub-header"><th>Sr. No.</th><th>Name of the Key Professional</th><th>Profile as per contract</th><th>Location</th><th>Present Days</th><th>Absent Days</th><th>Holidays</th></tr>
            <tr class="sub-header"><td colspan="7"><strong>MITRA LEVEL</strong></td></tr>
            {mitra_rows}
            <tr class="sub-header"><td colspan="7"><strong>{uni_info['name']}</strong></td></tr>
            {uni_rows}
        </table>
        
        <div class="section-title">A. Major Activities</div>
        <table>
            <tr><th>Sr. No.</th><th>Major Activities</th><th>Team Member Name</th><th>Activity Status</th><th>Date of Submission</th></tr>
            <tr><td>1</td><td>Finalisation of Annual Action Plan for the FY etc</td><td>All Coordinators</td><td>In Progress</td><td>-</td></tr>
            <tr><td>2</td><td>Coordination with Universities / MITRA for data collection & reporting</td><td>All Coordinators</td><td>Ongoing</td><td>Daily</td></tr>
            <tr><td>3</td><td>Conducted Stakeholder Consultation with institutions</td><td>ICARE Team</td><td>Completed</td><td>May 2026</td></tr>
            <tr><td>4</td><td>NIRF Framework & GRDAU Training Programs</td><td>All Coordinators</td><td>Completed</td><td>May 11-16, 2026</td></tr>
            <tr><td>5</td><td>NIRF Data Collection Initiation</td><td>All Coordinators</td><td>{activity_status}</td><td>-</td></tr>
        </table>
        
        <div class="section-title">B. Minutes of Meetings Conducted</div>
        <table>
            <tr><th>Sr. No.</th><th>Date</th><th>Chairperson + Key Participants</th><th>Agenda</th><th>Decision / Way Forward</th><th>Responsibility</th></tr>
            <tr><td>1</td><td>May 7, 2026</td><td>ICARE Team + Nodal Officer</td><td>Project Kick-off and data source mapping</td><td>Data collection initiated</td><td>Coordinators</td></tr>
            <tr><td>2</td><td>May 11-16, 2026</td><td>ICARE Team</td><td>NIRF Framework & GRDAU Training</td><td>Training completed for all coordinators</td><td>All Coordinators</td></tr>
            <tr><td>3</td><td>May 22, 2026</td><td>ICARE Team + Nodal Officer</td><td>Data gap review and action plan</td><td>Departments to submit pending data</td><td>Coordinators</td></tr>
            <tr><td>4</td><td>May 29, 2026</td><td>ICARE Team + IQAC Team</td><td>Review of May progress</td><td>MPR preparation initiated</td><td>Coordinators</td></tr>
        </table>
        
        <div class="section-title">C. Major Deliverables (As committed under Contract)</div>
        <tr>
            <tr><th>Sr. No.</th><th>Major Deliverables</th><th>Team Member Name</th><th>Activity Status</th><th>Due Date</th></tr>
            <tr><td>1</td><td>Inception Report and Deployment Plan</td><td>{coordinators_str}</td><td>{inception_status}</td><td>June 6, 2026</td></tr>
            <tr><td>2</td><td>Diagnostic Assessment Reports</td><td>{coordinators_str}</td><td>In Progress</td><td>July 6, 2026</td></tr>
            <tr><td>3</td><td>Institutional Development Plans (IDPs)</td><td>{coordinators_str}</td><td>Not Started</td><td>August 15, 2026</td></tr>
            <tr><td>4</td><td>GRDAUs Establishment & Operationalization</td><td>{coordinators_str}</td><td>Planning Phase</td><td>July 6, 2026</td></tr>
            <tr><td>5</td><td>Monthly Progress Report (May 2026)</td><td>{coordinators_str}</td><td>In Progress</td><td>June 10, 2026</td></tr>
        </table>
        
        <div class="section-title">D. Administration & Risk Management</div>
        <table>
            <tr><th>Sr. No.</th><th>Description of Identified Risk</th><th>Possible Impact</th><th>Severity Level</th><th>Mitigation Strategy</th><th>Responsibility</th></tr>
            <tr><td>1</td><td>Delay in data availability from departments</td><td>Incomplete NIRF submission</td><td>Medium</td><td>Regular follow-ups with Nodal Officer</td><td>Coordinator</td></tr>
            <tr><td>2</td><td>Inconsistent data formats across departments</td><td>Data validation challenges</td><td>Low</td><td>Standardized templates provided</td><td>Coordinator</td></tr>
            <tr><td>3</td><td>Staff turnover in key departments</td><td>Loss of data continuity</td><td>Medium</td><td>Documentation of processes</td><td>ICARE Team</td></tr>
        </table>
        
        <div class="section-title">E. Status of Initiatives under the Project and Other Works</div>
        <table>
            <tr><th>Sr. No.</th><th>Sub-Sector</th><th>Objective</th><th>Specific Intervention</th><th>Current Status</th><th>Way Forward / Actionable</th></tr>
            <tr><td>1</td><td>NIRF Data Collection</td><td>Complete baseline data</td><td>Student, Faculty, Research, Placement data</td><td>In Progress</td><td>Complete by June 15</td></tr>
            <tr><td>2</td><td>Capacity Building</td><td>Train coordinators</td><td>NIRF Framework & GRDAU Training</td><td>Completed</td><td>Reinforcement sessions in June</td></tr>
            <tr><td>3</td><td>GRDAU Setup</td><td>Establish Data Analytics Unit</td><td>Team identification, role definition</td><td>Planning Phase</td><td>Finalize by June 30</td></tr>
            <tr><td>4</td><td>Diagnostic Assessment</td><td>Identify gaps and SWOT</td><td>Data gap analysis</td><td>In Progress</td><td>Draft by June 15</td></tr>
        </table>
        
        <div class="section-title">Approvals and Signatures</div>
        <table class="signature-table">
            <tr><td style="width: 30%;"><strong>Prepared by:</strong></td><td>{coordinators_str}<br>(Institutional Coordinators)</td></tr>
            <tr><td><strong>Verified by:</strong></td><td>{nodal_officer_str}<br>(Nodal Officer, IQAC Coordinator)</td></tr>
            <tr><td><strong>Approved by:</strong></td><td>{registrar_str}<br>(Registrar)</td></tr>
            <tr><td><strong>Reviewed by:</strong></td><td>{ICARE_OFFICIALS['project_head']}<br>(Project Head, ICARE Pvt. Ltd.)</td></tr>
            <tr><td><strong>Approved by:</strong></td><td>{MITRA_OFFICIALS['project_director']}<br>(Project Director, MahaSTRIDE)</td></tr>
        </table>
        
        <div class="footer">
            This report is submitted as per SOP Section 2 - Monthly Progress Report (MPR)<br>
            Report generated on {datetime.now().strftime('%d-%b-%Y %H:%M:%S')}
        </div>
    </body>
    </html>
    """
    return html

def generate_consolidated_mpr_html():
    """Generate consolidated MPR for all universities"""
    summary_df = get_summary_stats()
    attendance_data = load_team_attendance()
    mpr_data = load_mpr_data()
    
    total_planned = len(get_all_planned_dates()) * len(UNIVERSITIES)
    total_completed = summary_df["Completed Tasks"].sum() if not summary_df.empty else 0
    total_hours = summary_df["Total Hours Invested"].sum() if not summary_df.empty else 0
    
    period_start = datetime.strptime(mpr_data.get("period_start", "2026-05-07"), "%Y-%m-%d")
    period_end = datetime.strptime(mpr_data.get("period_end", "2026-05-30"), "%Y-%m-%d")
    
    if total_completed == total_planned:
        overall_status = "✅ Fully Completed"
    elif total_completed >= total_planned * 0.5:
        overall_status = "🟡 Substantially Complete"
    elif total_completed > 0:
        overall_status = "🔵 Initiated"
    else:
        overall_status = "⚪ Not Started"
    
    # Build Project Team Deployment table
    team_rows = ""
    sr_no = 1
    
    team_rows += '<tr class="sub-header"><td colspan="7"><strong>MITRA LEVEL</strong></td></table>'
    for member in TEAM_MEMBERS.get("MITRA", []):
        att = attendance_data.get("MITRA", {}).get(member["name"], {})
        present = att.get('present_days', 20)
        absent = att.get('absent_days', 0)
        holidays = att.get('holidays', 11)
        team_rows += f"""
        <tr>
            <td>{sr_no}</td>
            <td>{member['name']}</td>
            <td>{member['profile']}</td>
            <td>{member['location']}</td>
            <td>{present}</td>
            <td>{absent}</td>
            <td>{holidays}</td>
        </tr>"""
        sr_no += 1
    
    for uni_code, uni_info in UNIVERSITIES.items():
        team_rows += f'<tr class="sub-header"><td colspan="7"><strong>{uni_info["name"]}</strong></td></tr>'
        for member in TEAM_MEMBERS.get(uni_code, []):
            att = attendance_data.get(uni_code, {}).get(member["name"], {})
            present = att.get('present_days', 20)
            absent = att.get('absent_days', 0)
            holidays = att.get('holidays', 11)
            team_rows += f"""
            <tr>
                <td>{sr_no}</td>
                <td>{member['name']}</td>
                <td>{member['profile']}</td>
                <td>{member['location']}</td>
                <td>{present}</td>
                <td>{absent}</td>
                <td>{holidays}</td>
            </tr>"""
            sr_no += 1
    
    summary_rows = ""
    for i, (_, row) in enumerate(summary_df.iterrows()):
        summary_rows += f"""
        <tr>
            <td>{i+1}</td>
            <td>{row['University']}</td>
            <td>{row['Nodal Officer']}</td>
            <td>{row['Completed Tasks']}</td>
            <td>{row['Pending Tasks']}</td>
            <td>{row['Status']}</td>
            <td>{row['Total Hours Invested']}</td>
        </tr>"""
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Consolidated Monthly Progress Report - All Universities</title>
        <style>
            body {{ font-family: 'Times New Roman', serif; margin: 0.7in; font-size: 11pt; line-height: 1.2; }}
            .header {{ text-align: center; margin-bottom: 20px; }}
            .mitra-title {{ font-size: 12pt; font-weight: bold; }}
            .confidential {{ text-align: right; font-weight: bold; margin-bottom: 20px; }}
            .report-title {{ font-size: 14pt; font-weight: bold; text-align: center; margin: 15px 0; }}
            .section-title {{ font-size: 12pt; font-weight: bold; margin-top: 15px; margin-bottom: 8px; background-color: #f0f0f0; padding: 5px; }}
            table {{ width: 100%; border-collapse: collapse; margin: 10px 0; font-size: 10pt; }}
            th, td {{ border: 1px solid #000; padding: 5px; vertical-align: top; }}
            th {{ background-color: #e8e8e8; font-weight: bold; text-align: center; }}
            .sub-header {{ background-color: #d0d0d0; font-weight: bold; }}
            .footer {{ text-align: center; font-size: 9pt; font-style: italic; margin-top: 30px; }}
        </style>
    </head>
    <body>
        <div class="confidential">Confidential</div>
        <div class="header">
            <div class="mitra-title">Maharashtra Institution for Transformation (MITRA)</div>
            <div>5th Floor, Nirmal, Nariman Point, Mumbai-400021</div>
            <div>Office Tel. No. 022 69979440 | Email: pmu.mahastride@mahamitra.org</div>
        </div>
        
        <div class="report-title">CONSOLIDATED MONTHLY PROGRESS REPORT</div>
        <div style="text-align: center;">All Maharashtra State Universities</div>
        <div style="text-align: center;">Reporting Period: {period_start.strftime('%d-%m-%Y')} to {period_end.strftime('%d-%m-%Y')}</div>
        
        <div class="section-title">Project Team Deployment</div>
        <table>
            <tr class="sub-header">
                <th>Sr. No.</th><th>Name of the Key Professional</th><th>Profile as per contract</th><th>Location</th><th>Present Days</th><th>Absent Days</th><th>Holidays</th>
            </tr>
            {team_rows}
        </table>
        
        <div class="section-title">Overall Project Progress</div>
        <div style="margin: 10px 0;">
            <strong>Overall Status: {overall_status}</strong><br>
            <strong>Tasks Completed:</strong> {total_completed} / {total_planned}<br>
            <strong>Total Hours Invested:</strong> {total_hours:.1f} hours<br>
            <strong>Working Days in May 2026:</strong> 20 days (May 7-30 excluding weekends and holidays)
        </div>
        
        <div class="section-title">University-wise Progress Summary</div>
        <table>
            <tr><th>Sr. No.</th><th>University</th><th>Nodal Officer</th><th>Tasks Completed</th><th>Tasks Pending</th><th>Status</th><th>Hours</th></tr>
            {summary_rows}
        </table>
        
        <div class="section-title">Major Deliverables Status</div>
        <table>
            <tr><th>Sr. No.</th><th>Major Deliverables</th><th>Status</th><th>Due Date</th></tr>
            <tr><td>1</td><td>Inception Report and Deployment Plan</td><td>{'✅ Completed' if total_completed >= total_planned * 0.6 else '🟡 In Progress'}</td><td>June 6, 2026</td></tr>
            <tr><td>2</td><td>Diagnostic Assessment Reports</td><td>🟡 In Progress</td><td>July 6, 2026</td></tr>
            <tr><td>3</td><td>Institutional Development Plans (IDPs)</td><td>⚪ Not Started</td><td>August 15, 2026</td></tr>
            <tr><td>4</td><td>GRDAUs Establishment & Operationalization</td><td>🟡 Planning Phase</td><td>July 6, 2026</td></tr>
            <tr><td>5</td><td>Monthly Progress Report (May 2026)</td><td>🟡 In Progress</td><td>June 10, 2026</td></tr>
        </table>
        
        <div class="section-title">Training Programs Conducted (May 11-16, 2026)</div>
        <table>
            <tr><th>Date</th><th>Topic</th><th>Participants</th><th>Status</th></tr>
            <tr><td>May 11, 2026</td><td>NIRF Framework & Formula Interpretation</td><td>All Coordinators</td><td>✅ Completed</td></tr>
            <tr><td>May 12, 2026</td><td>Teaching, Learning & Resources (TLR) Parameter</td><td>All Coordinators</td><td>✅ Completed</td></tr>
            <tr><td>May 13, 2026</td><td>Research & Professional Practice (RP) Parameter</td><td>All Coordinators</td><td>✅ Completed</td></tr>
            <tr><td>May 14, 2026</td><td>Graduation Outcomes (GO) & Outreach (OI) Parameters</td><td>All Coordinators</td><td>✅ Completed</td></tr>
            <tr><td>May 15, 2026</td><td>Perception (PR) & NIRF Submission Process</td><td>All Coordinators</td><td>✅ Completed</td></tr>
        </table>
        
        <div class="section-title">Plan for June 2026</div>
        </table>
            <tr><th>Activity</th><th>Target Completion</th><th>Responsible</th></tr>
            <tr><td>Complete NIRF data collection across all universities</td><td>June 15, 2026</td><td>All Coordinators</td></tr>
            <tr><td>Submit Diagnostic Assessment Reports</td><td>June 30, 2026</td><td>ICARE Team</td></tr>
            <tr><td>Finalize GRDAU team compositions for each university</td><td>June 30, 2026</td><td>ICARE Team + Universities</td></tr>
            <tr><td>Submit Monthly Progress Report (June 2026)</td><td>July 10, 2026</td><td>All Coordinators</td></tr>
        </table>
        
        <div class="footer">
            This report is submitted as per SOP Section 2 - Monthly Progress Report (MPR)<br>
            As per Contract Ref.: Progress Report clause - Consultant shall submit monthly Progress Reports<br>
            Report generated on {datetime.now().strftime('%d-%b-%Y %H:%M:%S')}
        </div>
    </body>
    </html>
    """
    return html

def get_html_download_link(html_content, filename):
    b64 = base64.b64encode(html_content.encode()).decode()
    return f'<a href="data:text/html;base64,{b64}" download="{filename}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">📥 Download {filename}</a>'

def show_sangam_info():
    st.markdown('<div class="sangam-card">', unsafe_allow_html=True)
    st.markdown("### 🎉 SANGAM Orientation & Training Program")
    st.markdown(f"**Dates:** May 5-6, 2026 | **Location:** Mumbai")
    st.markdown("✅ **Status:** Completed successfully")
    st.markdown('</div>', unsafe_allow_html=True)

def create_admin_dashboard():
    st.markdown('<div class="admin-card"><h2>📊 Admin Dashboard</h2><p>Complete Project Analytics & Reports</p></div>', unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 🗑️ Data Management")
        if st.button("🔄 Reset All Data (Start Fresh)", use_container_width=True):
            if reset_all_data():
                st.success("✅ All data has been reset! Starting fresh.")
                st.rerun()
        if st.button("📋 Mark All Tasks as Completed", use_container_width=True):
            if initialize_all_data():
                st.success("✅ All tasks have been marked as completed for all universities!")
                st.rerun()
    
    show_sangam_info()
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    total_unis = len(UNIVERSITIES)
    total_planned = len(get_all_planned_dates()) * total_unis
    summary_df = get_summary_stats()
    total_completed = summary_df["Completed Tasks"].sum() if not summary_df.empty else 0
    pending = total_planned - total_completed
    
    with col1: 
        st.metric("Project Phase", "May 7-30, 2026 (20 Working Days)")
    with col2: 
        st.metric("Universities", f"{total_unis}")
    with col3: 
        st.metric("Total Tasks", total_planned)
    with col4: 
        st.metric("Completed Tasks", total_completed, delta=f"{pending} remaining")
    
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["📊 Progress Overview", "🏛️ University Details", "📄 Generate Reports"])
    
    with tab1:
        if not summary_df.empty:
            fig3 = px.bar(summary_df, x="University", y="Completed Tasks", title="University-wise Completed Tasks", color="Completed Tasks", text="Completed Tasks", height=500)
            fig3.update_traces(texttemplate='%{text}', textposition='outside')
            st.plotly_chart(fig3, use_container_width=True)
            st.dataframe(summary_df, use_container_width=True)
    
    with tab2:
        selected_uni = st.selectbox("Select University", list(UNIVERSITIES.keys()), format_func=lambda x: UNIVERSITIES[x]["name"])
        if selected_uni:
            df = get_university_entries(selected_uni)
            if not df.empty:
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No entries logged yet")
    
    with tab3:
        st.subheader("📄 Generate Monthly Progress Reports")
        st.markdown("Generate complete MPR in Annexure C format (HTML - can be printed as PDF or copied to Word)")
        
        st.markdown("### Individual University Report")
        selected_uni = st.selectbox("Select University", list(UNIVERSITIES.keys()), format_func=lambda x: UNIVERSITIES[x]["name"], key="report_uni")
        if st.button("Generate University MPR", use_container_width=True):
            with st.spinner("Generating MPR..."):
                html_content = generate_complete_mpr_html(selected_uni)
                filename = f"MPR_{UNIVERSITIES[selected_uni]['name'].replace(' ', '_')}_May2026.html"
                st.markdown(get_html_download_link(html_content, filename), unsafe_allow_html=True)
                st.success("MPR generated! Click the download link above.")
        
        st.markdown("---")
        st.markdown("### Consolidated Report (All Universities)")
        if st.button("Generate Consolidated MPR", use_container_width=True):
            with st.spinner("Generating consolidated MPR..."):
                html_content = generate_consolidated_mpr_html()
                filename = "Consolidated_MPR_All_Universities_May2026.html"
                st.markdown(get_html_download_link(html_content, filename), unsafe_allow_html=True)
                st.success("Consolidated MPR generated! Click the download link above.")
        
        st.info("💡 **How to use:** Download the HTML file, open in browser, and print as PDF or copy to Microsoft Word.")

def create_project_lead_dashboard():
    st.markdown('<div class="projectlead-card"><h2>👨‍💼 Project Lead Dashboard - Dr. Harshal Kotwal</h2><p>Manage MPR Data & Generate Reports</p></div>', unsafe_allow_html=True)
    
    show_sangam_info()
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["📝 MPR Data Entry", "📊 Progress Overview", "📄 Reports"])
    
    with tab1:
        st.subheader("MPR Header Information")
        st.markdown("Enter the work order and project details for the MPR.")
        
        mpr_data = load_mpr_data()
        
        col1, col2 = st.columns(2)
        with col1:
            work_order_ref = st.text_input("Work Order Reference", value=mpr_data.get("work_order_ref", "MITRA/Research/MahaSTRIDE/EduRFP/49/2025"))
            period_start = st.date_input("Reporting Period Start", value=datetime.strptime(mpr_data.get("period_start", "2026-05-07"), "%Y-%m-%d").date())
        with col2:
            work_order_date = st.text_input("Work Order Date", value=mpr_data.get("work_order_date", "11-05-2026"))
            period_end = st.date_input("Reporting Period End", value=datetime.strptime(mpr_data.get("period_end", "2026-05-30"), "%Y-%m-%d").date())
        
        if st.button("Save MPR Header Information", use_container_width=True):
            mpr_data["work_order_ref"] = work_order_ref
            mpr_data["work_order_date"] = work_order_date
            mpr_data["period_start"] = period_start.strftime("%Y-%m-%d")
            mpr_data["period_end"] = period_end.strftime("%Y-%m-%d")
            save_mpr_data(mpr_data)
            st.success("✅ MPR header information saved!")
    
    with tab2:
        summary_df = get_summary_stats()
        if not summary_df.empty:
            fig = px.bar(summary_df, x="University", y="Completed Tasks", title="University-wise Completed Tasks", color="Completed Tasks", text="Completed Tasks", height=500)
            fig.update_traces(texttemplate='%{text}', textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(summary_df, use_container_width=True)
    
    with tab3:
        st.subheader("📄 Generate Monthly Progress Reports")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Individual University Report")
            selected_uni = st.selectbox("Select University", list(UNIVERSITIES.keys()), format_func=lambda x: UNIVERSITIES[x]["name"])
            if st.button("Generate University MPR", use_container_width=True):
                with st.spinner("Generating MPR..."):
                    html_content = generate_complete_mpr_html(selected_uni)
                    filename = f"MPR_{UNIVERSITIES[selected_uni]['name'].replace(' ', '_')}_May2026.html"
                    st.markdown(get_html_download_link(html_content, filename), unsafe_allow_html=True)
                    st.success("MPR generated!")
        
        with col2:
            st.markdown("### Consolidated Report")
            if st.button("Generate Consolidated MPR", use_container_width=True):
                with st.spinner("Generating consolidated MPR..."):
                    html_content = generate_consolidated_mpr_html()
                    filename = "Consolidated_MPR_All_Universities_May2026.html"
                    st.markdown(get_html_download_link(html_content, filename), unsafe_allow_html=True)
                    st.success("Consolidated MPR generated!")

def create_coordinator_dashboard(university_code, coordinator_name):
    st.markdown('<div class="info-card"><h2>📋 Coordinator Dashboard</h2><p>Log Your Daily Work</p></div>', unsafe_allow_html=True)
    
    uni_info = UNIVERSITIES[university_code]
    st.markdown(f"**🏛️ University:** {uni_info['name']}")
    st.markdown(f"**👤 Coordinator:** {coordinator_name}")
    st.markdown(f"**📌 Nodal Officer:** {uni_info['nodal_officer']}")
    st.info(f"⏰ **Working Hours:** {WORKING_HOURS} | Daily Stand-up: 10:30-11:00 AM with ICARE Team Only")
    st.info(f"📅 **May 2026 Working Days:** 20 days (May 7-30). Holidays: May 1, May 28. Weekends: All Saturdays & Sundays")
    
    st.markdown("---")
    st.subheader("📋 Daily Work Routine")
    st.markdown(DAILY_ROUTINE)
    st.markdown("---")
    
    pending_tasks = get_pending_tasks_for_coordinator(university_code)
    completed_entries = get_university_entries(university_code)
    total_planned = len(get_all_planned_dates())
    completed_count = len(completed_entries)
    pending_count = total_planned - completed_count
    
    col1, col2, col3 = st.columns(3)
    with col1: 
        st.metric("📋 Total Tasks", total_planned)
    with col2: 
        st.metric("✅ Completed", completed_count)
    with col3: 
        st.metric("⏳ Pending", pending_count)
    
    if total_planned > 0:
        progress_ratio = completed_count / total_planned
        st.progress(progress_ratio)
        if progress_ratio == 1.0:
            st.success("🎉 Congratulations! You have completed all tasks for May 2026!")
        elif progress_ratio >= 0.5:
            st.info(f"📈 Good progress! {pending_count} task(s) remaining.")
        else:
            st.warning(f"⚠️ {pending_count} task(s) pending. Keep going!")
    
    st.markdown("---")
    
    st.subheader("📋 YOUR PENDING TASKS")
    
    if pending_tasks:
        selected_date_str = st.selectbox("Select Date to Log Work", [task["date"] for task in pending_tasks])
        
        if selected_date_str:
            selected_task = next((t for t in pending_tasks if t["date"] == selected_date_str), None)
            if selected_task:
                st.markdown(f"""
                <div class="default-task-card">
                    <strong>📋 TASK FOR {selected_task['date']}</strong><br><br>
                    <strong>🎯 Task:</strong> {selected_task['task']}<br>
                    <strong>📂 Category:</strong> {selected_task['category']}<br>
                    <strong>📝 Description:</strong> {selected_task['description']}<br>
                    <strong>📦 Deliverables:</strong> {selected_task['deliverables']}
                </div>
                """, unsafe_allow_html=True)
                
                with st.form("log_task_form"):
                    use_planned = st.radio("Did you complete the planned task?", ["✅ Yes", "🔄 No"], horizontal=True)
                    
                    if use_planned == "✅ Yes":
                        task_category = selected_task['category']
                        task_name = selected_task['task']
                        description = selected_task['description']
                        deliverables = selected_task['deliverables']
                    else:
                        task_category = st.selectbox("Task Category", list(TASK_CATEGORIES.keys()))
                        task_name = st.text_input("Task")
                        description = st.text_area("Description", height=100)
                        deliverables = st.text_area("Deliverables", height=80)
                    
                    col1, col2 = st.columns(2)
                    with col1: 
                        status = st.selectbox("Status", ["completed"], index=0)
                    with col2: 
                        hours_spent = st.number_input("Hours Spent", min_value=0.5, max_value=12.0, step=0.5, value=8.0)
                    remarks = st.text_area("Remarks")
                    
                    if st.form_submit_button("✅ Submit Work Log"):
                        if log_daily_entry(university_code, selected_task['date'], task_category, task_name, description, deliverables, status, hours_spent, remarks, use_planned != "✅ Yes", use_planned != "✅ Yes", coordinator_name):
                            st.success("✅ Work logged successfully!")
                            st.balloons()
                            st.rerun()
    else:
        st.success("🎉 Congratulations! You have completed all tasks for May 2026!")
    
    st.markdown("---")
    with st.expander("📋 View Your Completed Entries", expanded=False):
        df = get_university_entries(university_code)
        if not df.empty:
            st.dataframe(df, use_container_width=True)
    
    st.markdown("---")
    st.subheader("📅 MPR Submission Reminder")
    st.warning("📋 As per SOP Section 1 & 2, approved MPR must reach PMU MahaSTRIDE by the 10th of June 2026.")

def main():
    # Initialize all data on first run
    if not os.path.exists(PROGRESS_DATA_FILE):
        initialize_all_data()
    
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    
    if not st.session_state["authenticated"]:
        with st.container():
            st.markdown('<div class="main-header"><h1>🔐 mahaSTRIDE NIRF Data Collection Tracker</h1><p>Phase 1: May 7-30, 2026 (20 Working Days)</p></div>', unsafe_allow_html=True)
            
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
                **Project Lead:** projectlead@mahastride.com / ProjectLead@2026<br><br>
                **Coordinators:** (Password: Name@2026)<br>
                - sneha@mu.edu (Mumbai University)<br>
                - sagar@mu.edu (Mumbai University)<br>
                - shubham@mitra.gov.in (MITRA)<br>
                - jagan@sspu.edu (SPPU Pune)<br>
                - vaibhav@coep.edu (COEP Pune)<br>
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
        st.markdown(f"**Today:** {datetime.now().strftime('%d-%b-%Y')}")
        st.markdown("**Phase 1:** May 7-30, 2026 (20 Working Days)")
        st.markdown("---")
        
        if user_role == "admin":
            menu = st.radio("Navigation", ["📊 Admin Dashboard", "ℹ️ About"])
        elif user_role == "project_lead":
            menu = st.radio("Navigation", ["👨‍💼 Project Lead Dashboard", "ℹ️ About"])
        else:
            menu = st.radio("Navigation", ["📋 My Tasks", "📊 My Progress", "ℹ️ About"])
        
        st.markdown("---")
        st.caption(f"⏰ {WORKING_HOURS}")
        st.caption("🔄 Stand-up: 10:30-11:00 AM")
        
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
            st.markdown("""
            ### mahaSTRIDE Project Tracker
            
            **Complete MPR Generation in Annexure C Format**
            - Project Team Deployment table included
            - Major Activities, Meetings, Deliverables sections
            - Risk Management and Initiatives tracking
            - Signatures section for approvals
            
            **Key Deliverables:**
            1. Inception Report and Deployment Plan (Due: June 6, 2026)
            2. GRDAUs Establishment & Operationalization (Due: July 6, 2026)
            
            **Working Days in May 2026:** 20 days
            - May 7-30 (excluding weekends and May 1, May 28 holidays)
            """)
    
    elif user_role == "project_lead":
        if menu == "👨‍💼 Project Lead Dashboard":
            create_project_lead_dashboard()
        else:
            st.title("ℹ️ About")
            st.markdown("""
            ### Project Lead Dashboard
            
            **Your Responsibilities:**
            1. Enter MPR header information (Work Order, dates)
            2. Generate MPR reports for all universities
            
            **The MPR includes:**
            - Project Team Deployment table
            - Major Activities section
            - Minutes of Meetings
            - Major Deliverables status (Inception Report, GRDAUs)
            - Risk Management
            - Status of Initiatives
            - Approvals and Signatures
            """)
    
    else:
        university_code = st.session_state.get("user_university")
        if not university_code:
            st.error("University not assigned. Please contact admin.")
        else:
            if menu == "📋 My Tasks":
                create_coordinator_dashboard(university_code, user_name)
            elif menu == "📊 My Progress":
                st.title("📊 My Progress")
                df = get_university_entries(university_code)
                if not df.empty:
                    st.dataframe(df, use_container_width=True)
                    completed = len(df[df["Status"] == "COMPLETED"])
                    total_planned = len(get_all_planned_dates())
                    st.metric("Completed Tasks", f"{completed}/{total_planned}")
                    st.metric("Working Days", "20 (May 7-30)")
                else:
                    st.info("No entries logged yet")
            else:
                st.title("ℹ️ About")
                st.markdown("""
                ### Coordinator Dashboard
                
                **How to Log Work:**
                1. Select a date from pending tasks
                2. Confirm if you completed the planned task
                3. Add hours spent and submit
                
                **Training Completed (May 11-16, 2026):**
                - NIRF Framework & Formula Interpretation
                - Teaching, Learning & Resources (TLR)
                - Research & Professional Practice (RP)
                - Graduation Outcomes (GO) & Outreach (OI)
                - Perception (PR) & NIRF Submission Process
                
                **Key Deliverables You Support:**
                - Inception Report (Due June 6)
                - GRDAU Establishment (Due July 6)
                """)

if __name__ == "__main__":
    main()
