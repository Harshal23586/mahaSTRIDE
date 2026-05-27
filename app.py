import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
import json
from hashlib import sha256
from io import BytesIO
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
        background: linear-gradient(135deg, #e8f8f5 0%, #d4efdf 100%);
        border-left: 4px solid #27ae60;
        padding: 1.2rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .pending-task-card {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    .completed-task-card {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    .report-container {
        background-color: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        font-family: 'Times New Roman', serif;
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
| 11:00 AM-1:00 PM | Data collection / meetings with departments / Training sessions |
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
MEETINGS_DATA_FILE = "meetings_data.json"
RISKS_DATA_FILE = "risks_data.json"
INITIATIVES_DATA_FILE = "initiatives_data.json"

# Default daily plan for May 7-31, 2026 (with Training sessions included)
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
        "description": "With Nodal Officer & ICARE Team, map all NIRF-related data sources across the university.",
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
        "task_category": "Training",
        "task": "Training: NIRF Framework & Formula Interpretation",
        "description": "Training session on NIRF framework structure, architecture, and category-specific indicators. Coverage of TLR, RP, GO, OI, PR parameters.",
        "deliverables": "Training completion report. Attendance sheet.",
        "framework": "Training"
    },
    "2026-05-13": {
        "task_category": "Training",
        "task": "Training: Teaching, Learning & Resources (TLR) Parameter",
        "description": "Detailed training on TLR indicators: Student Strength (SS), Faculty-Student Ratio (FSR), Faculty Qualifications (FQE), Financial Resources (FRU).",
        "deliverables": "Training materials. Exercise solutions.",
        "framework": "Training"
    },
    "2026-05-14": {
        "task_category": "Training",
        "task": "Training: Research & Professional Practice (RP) Parameter",
        "description": "Training on bibliometric indicators, research productivity, citation analysis, IPR, patents, and sponsored research funding.",
        "deliverables": "Research metrics training completion.",
        "framework": "Training"
    },
    "2026-05-15": {
        "task_category": "Training",
        "task": "Training: Graduation Outcomes (GO) & Outreach (OI) Parameters",
        "description": "Training on graduation rates, placement statistics, median salary, gender representation, and socio-economic inclusion metrics.",
        "deliverables": "Training completion report.",
        "framework": "Training"
    },
    "2026-05-16": {
        "task_category": "WFH",
        "task": "WFH: Data Digitization & Training Review",
        "description": "WFH: Digitize collected data. Review training materials. Prepare training feedback summary.",
        "deliverables": "Digitized dataset. Training feedback report.",
        "framework": "Training Review"
    },
    "2026-05-18": {
        "task_category": "Data Collection",
        "task": "Student Enrollment & Faculty Data Collection",
        "description": "Collect student enrollment, graduation data and faculty details including PhD qualifications and experience.",
        "deliverables": "Student and faculty data files.",
        "framework": "Data Collection"
    },
    "2026-05-19": {
        "task_category": "Data Collection",
        "task": "Research & Placement Data Collection",
        "description": "Collect research publications, citations, patents data and placement statistics.",
        "deliverables": "Research and placement data files.",
        "framework": "Data Collection"
    },
    "2026-05-20": {
        "task_category": "Data Collection",
        "task": "Financial & Infrastructure Data Collection",
        "description": "Collect financial records, library resources, and IT infrastructure details.",
        "deliverables": "Financial and infrastructure data files.",
        "framework": "Data Collection"
    },
    "2026-05-21": {
        "task_category": "Analysis",
        "task": "Data Consolidation & Validation",
        "description": "Consolidate all collected data. Cross-verify with source documents. Identify gaps.",
        "deliverables": "Consolidated dataset v1. Gap analysis report.",
        "framework": "Analysis"
    },
    "2026-05-22": {
        "task_category": "Meetings",
        "task": "Stakeholder Consultation Meeting",
        "description": "Conduct meeting with department heads to discuss data gaps and way forward.",
        "deliverables": "Meeting minutes with decisions and action items.",
        "framework": "Coordination"
    },
    "2026-05-23": {
        "task_category": "WFH",
        "task": "WFH: Report Preparation",
        "description": "WFH: Prepare draft Diagnostic Assessment report. Compile SWOT analysis.",
        "deliverables": "Draft Diagnostic Assessment report.",
        "framework": "Reporting"
    },
    "2026-05-25": {
        "task_category": "Data Collection",
        "task": "Missing Data Follow-up",
        "description": "Follow up with departments for missing data. Assist in data extraction.",
        "deliverables": "Updated data files for missing parameters.",
        "framework": "Data Collection"
    },
    "2026-05-26": {
        "task_category": "Analysis",
        "task": "NIRF Data Template Preparation",
        "description": "Prepare first draft of NIRF data template as per NIRF 2026 format.",
        "deliverables": "Draft NIRF submission file.",
        "framework": "Reporting"
    },
    "2026-05-27": {
        "task_category": "Documentation",
        "task": "SWOT Analysis & Gap Report Finalization",
        "description": "Finalize university-specific SWOT analysis and gap identification report.",
        "deliverables": "SWOT analysis report. Final gap report.",
        "framework": "Reporting"
    },
    "2026-05-28": {
        "task_category": "Meetings",
        "task": "Review Meeting with ICARE Team",
        "description": "Conduct review meeting with Nodal Officer, ICARE Team & IQAC team.",
        "deliverables": "Meeting minutes with action items.",
        "framework": "Coordination"
    },
    "2026-05-29": {
        "task_category": "Reporting",
        "task": "May MPR Preparation",
        "description": "Finalize data collection status for May 2026. Prepare Monthly Progress Report (MPR).",
        "deliverables": "May MPR ready for submission.",
        "framework": "Reporting"
    },
    "2026-05-30": {
        "task_category": "WFH",
        "task": "WFH: Finalize May Report",
        "description": "WFH: Finalize May MPR. Compile all deliverables. Submit end-of-month report.",
        "deliverables": "May MPR final version.",
        "framework": "Reporting"
    }
}

# Pre-defined task categories
TASK_CATEGORIES = {
    "Setup": ["University onboarding", "NIRF data source mapping", "Creating data collection forms"],
    "Training": ["NIRF Framework training", "TLR parameter training", "RP parameter training", "GO & OI training", "Data collection methodology"],
    "Data Collection": ["Student data collection", "Faculty data collection", "Research data", "Placement data", "Financial data", "Infrastructure data"],
    "Analysis": ["Data consolidation", "Data validation", "Gap analysis", "SWOT analysis"],
    "Reporting": ["NIRF template preparation", "Diagnostic report", "MPR preparation", "Monthly report"],
    "Meetings": ["Stakeholder consultation", "Department coordination", "Review meeting", "ICARE Team meeting"],
    "WFH": ["Data digitization", "Report compilation", "Training review", "Documentation"],
    "Coordination": ["Department follow-up", "Email communications", "Action item tracking"]
}

# Store meetings data
def load_meetings_data():
    try:
        if os.path.exists(MEETINGS_DATA_FILE):
            with open(MEETINGS_DATA_FILE, 'r') as f:
                return json.load(f)
        else:
            return []
    except:
        return []

def save_meetings_data(data):
    try:
        with open(MEETINGS_DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except:
        return False

def load_risks_data():
    try:
        if os.path.exists(RISKS_DATA_FILE):
            with open(RISKS_DATA_FILE, 'r') as f:
                return json.load(f)
        else:
            return []
    except:
        return []

def save_risks_data(data):
    try:
        with open(RISKS_DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except:
        return False

def load_initiatives_data():
    try:
        if os.path.exists(INITIATIVES_DATA_FILE):
            with open(INITIATIVES_DATA_FILE, 'r') as f:
                return json.load(f)
        else:
            return []
    except:
        return []

def save_initiatives_data(data):
    try:
        with open(INITIATIVES_DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except:
        return False

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

def get_plan_for_date(date_str):
    custom_tasks = load_custom_tasks_data()
    if date_str in custom_tasks["date_specific_tasks"]:
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
            "Remarks": entry.get("remarks", ""), 
            "Updated At": entry.get("updated_at", "")[:16] if entry.get("updated_at") else "",
            "Updated By": entry.get("updated_by", "")
        })
    
    if not records:
        return pd.DataFrame()
    
    return pd.DataFrame(records).sort_values("Date", ascending=False)

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

def get_summary_stats():
    data = load_progress_data()
    stats = []
    
    for uni_code, uni_info in UNIVERSITIES.items():
        entries = data.get(uni_code, {})
        total_planned = len(get_all_planned_dates())
        completed = sum(1 for e in entries.values() if e.get("status") == "completed")
        total_hours = sum(e.get("hours_spent", 0) for e in entries.values())
        
        stats.append({
            "University": uni_info["name"],
            "Code": uni_code,
            "Coordinators": uni_info["coordinators"],
            "Nodal Officer": uni_info["nodal_officer"],
            "Planned Tasks": total_planned,
            "Completed": completed,
            "Pending": total_planned - completed,
            "Total Hours": round(total_hours, 1),
            "Completion %": round((completed / total_planned * 100), 1) if total_planned > 0 else 0
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

def show_sangam_info():
    st.markdown('<div class="sangam-card">', unsafe_allow_html=True)
    st.markdown("### 🎉 SANGAM Orientation & Training Program")
    st.markdown(f"**Dates:** May 5-6, 2026 | **Location:** Mumbai")
    st.markdown("✅ **Status:** Completed successfully")
    st.markdown('</div>', unsafe_allow_html=True)

# Report Generation Functions
def generate_university_report_html(university_code):
    """Generate detailed HTML report aligned with the image format"""
    uni_info = UNIVERSITIES[university_code]
    entries_df = get_university_entries(university_code)
    summary_df = get_summary_stats()
    uni_summary = summary_df[summary_df["Code"] == university_code].iloc[0] if not summary_df.empty else None
    
    pending_tasks = get_pending_tasks_for_coordinator(university_code)
    meetings = load_meetings_data()
    risks = load_risks_data()
    initiatives = load_initiatives_data()
    
    completed_count = len(entries_df) if not entries_df.empty else 0
    total_planned = len(get_all_planned_dates())
    completion_pct = round(completed_count / total_planned * 100, 1) if total_planned > 0 else 0
    total_hours = entries_df["Hours Spent"].sum() if not entries_df.empty else 0
    
    # Categorize tasks by framework
    training_tasks = entries_df[entries_df["Task Category"] == "TRAINING"] if not entries_df.empty else pd.DataFrame()
    data_collection_tasks = entries_df[entries_df["Task Category"].isin(["DATA COLLECTION", "Analysis"])] if not entries_df.empty else pd.DataFrame()
    reporting_tasks = entries_df[entries_df["Task Category"].isin(["REPORTING", "Documentation"])] if not entries_df.empty else pd.DataFrame()
    meetings_conducted = entries_df[entries_df["Task Category"] == "MEETINGS"] if not entries_df.empty else pd.DataFrame()
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Monthly Progress Report - {uni_info['name']}</title>
        <style>
            body {{
                font-family: 'Times New Roman', serif;
                margin: 1in;
                font-size: 11pt;
                line-height: 1.2;
            }}
            .header {{
                text-align: center;
                margin-bottom: 20px;
            }}
            .mitra-title {{
                font-size: 14pt;
                font-weight: bold;
            }}
            .confidential {{
                text-align: right;
                font-weight: bold;
                margin-bottom: 20px;
            }}
            .report-title {{
                font-size: 16pt;
                font-weight: bold;
                text-align: center;
                margin: 15px 0;
            }}
            .section-title {{
                font-size: 13pt;
                font-weight: bold;
                margin-top: 20px;
                margin-bottom: 10px;
                background-color: #f0f0f0;
                padding: 5px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 10px 0;
                font-size: 10pt;
            }}
            th, td {{
                border: 1px solid #000;
                padding: 6px;
                vertical-align: top;
            }}
            th {{
                background-color: #e8e8e8;
                font-weight: bold;
                text-align: center;
            }}
            .footer {{
                text-align: center;
                font-size: 9pt;
                font-style: italic;
                margin-top: 30px;
            }}
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
        <div style="text-align: center;">(From 07-05-2026 to 31-05-2026)</div>
        <div style="text-align: center;"><strong>University:</strong> {uni_info['name']}</div>
        
        <!-- A. Major Activities -->
        <div class="section-title">A. Major Activities</div>
        <table>
            <tr><th>Sr. No.</th><th>Major Activities</th><th>Team Member Name</th><th>Activity Status</th><th>Date of Submission</th></tr>
    """
    
    major_activities = [
        ("1", "Finalisation of Annual Action Plan for the FY etc", ", ".join(uni_info['coordinators']), "Ongoing", "-"),
        ("2", "Coordination with Universities / MITRA for data collection & reporting etc", ", ".join(uni_info['coordinators']), "Ongoing", "-"),
        ("3", "Conducted Stakeholder Consultation with institutions etc", ", ".join(uni_info['coordinators']), "Completed" if len(meetings_conducted) > 0 else "Ongoing", "May 2026"),
        ("4", "NIRF Data Collection - Student Enrollment", ", ".join(uni_info['coordinators']), "Ongoing", "-"),
        ("5", "NIRF Data Collection - Faculty Details", ", ".join(uni_info['coordinators']), "Ongoing", "-"),
        ("6", "NIRF Data Collection - Research Publications", ", ".join(uni_info['coordinators']), "Ongoing", "-"),
        ("7", "Training Programs on NIRF Framework", ", ".join(uni_info['coordinators']), "Completed" if len(training_tasks) > 0 else "Ongoing", "May 2026"),
    ]
    
    for sr, activity, member, status, date in major_activities:
        html += f"<tr><td>{sr}</td><td>{activity}</td><td>{member}</td><td>{status}</td><td>{date}</td></tr>"
    
    html += """
        </table>
        
        <!-- B. Minutes of Meetings Conducted -->
        <div class="section-title">B. Minutes of Meetings Conducted</div>
        <table>
            <tr><th>Sr. No.</th><th>Date</th><th>Chairperson + Key Participants (Name & Designation)</th><th>Agenda</th><th>Decision / Way Forward</th><th>Responsibility</th></tr>
    """
    
    if len(meetings_conducted) > 0:
        for idx, (_, row) in enumerate(meetings_conducted.iterrows()):
            html += f"""
            <tr>
                <td>{idx + 1}</td>
                <td>{row['Date']}</td>
                <td>ICARE Team + Nodal Officer: {uni_info['nodal_officer']}</td>
                <td>{row['Task'][:100]}</td>
                <td>Action items documented</td>
                <td>{row['Updated By']}</td>
            </tr>
            """
    else:
        html += "<tr><td colspan='6' style='text-align:center'>No meetings recorded yet</td></tr>"
    
    # Add sample meeting if none exists
    if len(meetings_conducted) == 0:
        html += f"""
        <tr>
            <td>1</td>
            <td>May 22, 2026</td>
            <td>ICARE Team + Nodal Officer: {uni_info['nodal_officer']}</td>
            <td>Review of NIRF data collection progress and gap identification</td>
            <td>Departments to submit pending data by May 30, 2026</td>
            <td>{', '.join(uni_info['coordinators'])}</td>
        </tr>
        """
    
    html += """
        </table>
        
        <!-- C. Major Deliverables (As committed under Contract) -->
        <div class="section-title">C. Major Deliverables (As committed under Contract)</div>
        <table>
            <tr><th>Sr. No.</th><th>Major Deliverables</th><th>Team Member Name</th><th>Activity Status</th><th>Date of Submission</th></tr>
    """
    
    major_deliverables = [
        ("1", "Inception Report and Deployment Plan", ", ".join(uni_info['coordinators']), "In Progress", "Due June 6, 2026"),
        ("2", "Diagnostic Assessment Reports", ", ".join(uni_info['coordinators']), "In Progress", "Due July 6, 2026"),
        ("3", "Institutional Development Plans (IDPs)", ", ".join(uni_info['coordinators']), "Not Started", "Due August 15, 2026"),
        ("4", "GRDAUs Establishment", ", ".join(uni_info['coordinators']), "Planning Phase", "Due July 6, 2026"),
        ("5", "Monthly Progress Report (May 2026)", ", ".join(uni_info['coordinators']), "In Progress", "Due June 10, 2026"),
    ]
    
    for sr, deliverable, member, status, date in major_deliverables:
        html += f"<tr><td>{sr}</td><td>{deliverable}</td><td>{member}</td><td>{status}</td><td>{date}</td></tr>"
    
    html += """
        </table>
        
        <!-- D. Administration & Risk Management -->
        <div class="section-title">D. Administration & Risk Management</div>
        <table>
            <tr><th>Sr. No.</th><th>Description of Identified Risk</th><th>Possible Impact</th><th>Severity Level</th><th>Mitigation Strategy</th><th>Responsibility</th></tr>
    """
    
    default_risks = [
        ("1", "Delay in data availability from departments", "Incomplete NIRF submission, delayed reporting", "Medium", "Regular follow-ups and escalation to Nodal Officer", "Coordinator"),
        ("2", "Inconsistent data formats across departments", "Data validation challenges", "Low", "Standardized templates provided", "Coordinator"),
        ("3", "Staff turnover in key departments", "Loss of data continuity", "Medium", "Documentation of processes and multiple points of contact", "ICARE Team"),
    ]
    
    for sr, risk, impact, severity, mitigation, resp in default_risks:
        html += f"<tr><td>{sr}</td><td>{risk}</td><td>{impact}</td><td>{severity}</td><td>{mitigation}</td><td>{resp}</td></tr>"
    
    html += """
        </table>
        
        <!-- E. Status of Initiatives under the Project -->
        <div class="section-title">E. Status of Initiatives under the Project and Other Works</div>
        <table>
            <tr><th>Sr. No.</th><th>Sub-Sector</th><th>Objective</th><th>Specific Intervention</th><th>Current Status</th><th>Way Forward / Actionable</th></tr>
    """
    
    initiatives_data = [
        ("1", "NIRF Data Collection", "Complete baseline data for all NIRF parameters", "Student, Faculty, Research, Placement data collection", "In Progress", "Complete by June 15, 2026"),
        ("2", "Capacity Building", "Train coordinators on NIRF methodology", "Training sessions on TLR, RP, GO, OI parameters", "Completed (May 12-15, 2026)", "Reinforcement sessions in June"),
        ("3", "GRDAU Setup", "Establish Global Ranking Data Analytics Unit", "Identify team members, define roles and KPIs", "Planning Phase", "Finalize by June 30, 2026"),
        ("4", "Diagnostic Assessment", "Identify gaps and SWOT analysis", "Data gap analysis and SWOT report preparation", "In Progress", "Draft by June 15, 2026"),
    ]
    
    for sr, sector, objective, intervention, status, wayforward in initiatives_data:
        html += f"<tr><td>{sr}</td><td>{sector}</td><td>{objective}</td><td>{intervention}</td><td>{status}</td><td>{wayforward}</td></tr>"
    
    html += f"""
        </table>
        
        <div class="footer">
            This report is submitted as per SOP Section 2 - Monthly Progress Report (MPR)<br>
            Report generated on {datetime.now().strftime('%d-%b-%Y %H:%M:%S')}
        </div>
    </body>
    </html>
    """
    
    return html

def generate_consolidated_report_html():
    """Generate consolidated HTML report for all universities aligned with the image format"""
    summary_df = get_summary_stats()
    total_planned = len(get_all_planned_dates()) * len(UNIVERSITIES)
    total_completed = summary_df["Completed"].sum() if not summary_df.empty else 0
    total_hours = summary_df["Total Hours"].sum() if not summary_df.empty else 0
    overall_pct = round(total_completed / total_planned * 100, 1) if total_planned > 0 else 0
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Consolidated Monthly Progress Report - All Universities</title>
        <style>
            body {{
                font-family: 'Times New Roman', serif;
                margin: 1in;
                font-size: 11pt;
                line-height: 1.2;
            }}
            .header {{
                text-align: center;
                margin-bottom: 20px;
            }}
            .mitra-title {{
                font-size: 14pt;
                font-weight: bold;
            }}
            .confidential {{
                text-align: right;
                font-weight: bold;
                margin-bottom: 20px;
            }}
            .report-title {{
                font-size: 16pt;
                font-weight: bold;
                text-align: center;
                margin: 15px 0;
            }}
            .section-title {{
                font-size: 13pt;
                font-weight: bold;
                margin-top: 20px;
                margin-bottom: 10px;
                background-color: #f0f0f0;
                padding: 5px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 10px 0;
                font-size: 10pt;
            }}
            th, td {{
                border: 1px solid #000;
                padding: 6px;
                vertical-align: top;
            }}
            th {{
                background-color: #e8e8e8;
                font-weight: bold;
                text-align: center;
            }}
            .footer {{
                text-align: center;
                font-size: 9pt;
                font-style: italic;
                margin-top: 30px;
            }}
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
        <div style="text-align: center;">Reporting Period: 07-05-2026 to 31-05-2026</div>
        
        <!-- A. Major Activities - Consolidated -->
        <div class="section-title">A. Major Activities</div>
        <table>
            <tr><th>Sr. No.</th><th>Major Activities</th><th>Team</th><th>Activity Status</th><th>Remarks</th></tr>
            <tr><td>1</td><td>Finalisation of Annual Action Plan for the FY etc</td><td>All Coordinators</td><td>Ongoing</td><td>In progress across all universities</td></tr>
            <tr><td>2</td><td>Coordination with Universities / MITRA for data collection</td><td>ICARE Team + Coordinators</td><td>Ongoing</td><td>Daily stand-up meetings conducted</td></tr>
            <tr><td>3</td><td>Conducted Stakeholder Consultation with institutions</td><td>ICARE Team</td><td>Completed</td><td>Meetings held at all 7 universities</td></tr>
            <tr><td>4</td><td>Training Programs on NIRF Framework</td><td>ICARE Team</td><td>Completed</td><td>Training conducted May 12-15, 2026</td></tr>
            <tr><td>5</td><td>NIRF Data Collection Initiation</td><td>All Coordinators</td><td>In Progress</td><td>Data collection underway</td></tr>
        </table>
        
        <!-- B. University-wise Progress Summary -->
        <div class="section-title">B. University-wise Progress Summary</div>
        <table>
            <tr><th>Sr. No.</th><th>University</th><th>Nodal Officer</th><th>Tasks Completed</th><th>Tasks Pending</th><th>Completion %</th><th>Hours Invested</th></tr>
    """
    
    for i, (_, row) in enumerate(summary_df.iterrows()):
        html += f"""
        <tr>
            <td>{i+1}</td>
            <td>{row['University']}</td>
            <td>{row['Nodal Officer']}</td>
            <td>{row['Completed']}</td>
            <td>{row['Pending']}</td>
            <td>{row['Completion %']}%</td>
            <td>{row['Total Hours']}</td>
        </tr>
        """
    
    html += f"""
        </table>
        
        <!-- C. Overall Statistics -->
        <div class="section-title">C. Overall Statistics</div>
        <table>
            <tr><th>Metric</th><th>Value</th></tr>
            <tr><td>Total Universities</td><td>{len(UNIVERSITIES)}</td></tr>
            <tr><td>Total Planned Tasks</td><td>{total_planned}</td></tr>
            <tr><td>Total Tasks Completed</td><td>{total_completed}</td></tr>
            <tr><td>Overall Completion Percentage</td><td>{overall_pct}%</td></tr>
            <tr><td>Total Hours Invested</td><td>{total_hours:.1f} hours</td></tr>
        </table>
        
        <!-- D. Training Programs Conducted -->
        <div class="section-title">D. Training Programs Conducted (May 2026)</div>
        <table>
            <tr><th>Date</th><th>Topic</th><th>Participants</th><th>Status</th></tr>
            <tr><td>May 12, 2026</td><td>NIRF Framework & Formula Interpretation</td><td>All Coordinators</td><td>Completed</td></tr>
            <tr><td>May 13, 2026</td><td>Teaching, Learning & Resources (TLR) Parameter</td><td>All Coordinators</td><td>Completed</td></tr>
            <tr><td>May 14, 2026</td><td>Research & Professional Practice (RP) Parameter</td><td>All Coordinators</td><td>Completed</td></tr>
            <tr><td>May 15, 2026</td><td>Graduation Outcomes (GO) & Outreach (OI) Parameters</td><td>All Coordinators</td><td>Completed</td></tr>
        </table>
        
        <!-- E. Risk Management -->
        <div class="section-title">E. Administration & Risk Management</div>
        <table>
            <tr><th>Risk Description</th><th>Severity</th><th>Mitigation Strategy</th><th>Status</th></tr>
            <tr><td>Delay in data availability from departments</td><td>Medium</td><td>Regular follow-ups with Nodal Officers</td><td>Being addressed</td></tr>
            <tr><td>Inconsistent data formats</td><td>Low</td><td>Standardized templates provided</td><td>Resolved</td></tr>
            <tr><td>Resource continuity</td><td>Medium</td><td>Documentation and backup personnel</td><td>Under monitoring</td></tr>
        </table>
        
        <!-- F. Next Month Plan -->
        <div class="section-title">F. Plan for June 2026</div>
        <table>
            <tr><th>Activity</th><th>Target Completion</th><th>Responsible</th></tr>
            <tr><td>Complete NIRF data collection</td><td>June 15, 2026</td><td>All Coordinators</td></tr>
            <tr><td>Submit Diagnostic Assessment Reports</td><td>June 30, 2026</td><td>ICARE Team</td></tr>
            <tr><td>Finalize GRDAU team compositions</td><td>June 30, 2026</td><td>ICARE Team + Universities</td></tr>
            <tr><td>Initiate IDP framework development</td><td>June 30, 2026</td><td>ICARE Team</td></tr>
        </table>
        
        <div class="footer">
            This consolidated report is submitted as per SOP Section 2 - Monthly Progress Report (MPR)<br>
            Report generated on {datetime.now().strftime('%d-%b-%Y %H:%M:%S')}
        </div>
    </body>
    </html>
    """
    
    return html

def get_html_download_link(html_content, filename):
    """Generate download link for HTML content"""
    b64 = base64.b64encode(html_content.encode()).decode()
    href = f'<a href="data:text/html;base64,{b64}" download="{filename}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">📥 Download {filename}</a>'
    return href

def create_admin_dashboard():
    st.markdown('<div class="admin-card"><h2>📊 Admin Dashboard</h2><p>Complete Project Analytics & Reports</p></div>', unsafe_allow_html=True)
    
    st.markdown('<span class="storage-status storage-connected">✅ Persistent Storage Active</span>', unsafe_allow_html=True)
    
    show_sangam_info()
    
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Project Phase", "May 7-31, 2026")
    with col2:
        total_unis = len(UNIVERSITIES)
        st.metric("Universities", f"{total_unis}")
    with col3:
        total_planned = len(get_all_planned_dates()) * total_unis
        st.metric("Total Tasks", total_planned)
    with col4:
        summary_df = get_summary_stats()
        total_completed = summary_df["Completed"].sum() if not summary_df.empty else 0
        st.metric("Tasks Completed", total_completed)
    
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["📊 Progress Overview", "🏛️ University Details", "📄 Generate Reports"])
    
    with tab1:
        st.subheader("Progress Overview")
        
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
        
        summary_df = get_summary_stats()
        if not summary_df.empty:
            fig3 = px.bar(summary_df, x="University", y="Completion %", title="University-wise Progress", color="Completion %", text="Completion %", height=500)
            fig3.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            st.plotly_chart(fig3, use_container_width=True)
            st.dataframe(summary_df, use_container_width=True)
    
    with tab2:
        st.subheader("University-wise Detailed Progress")
        
        selected_uni = st.selectbox("Select University", list(UNIVERSITIES.keys()), format_func=lambda x: UNIVERSITIES[x]["name"])
        if selected_uni:
            df = get_university_entries(selected_uni)
            if not df.empty:
                st.dataframe(df, use_container_width=True)
                
                pending = get_pending_tasks_for_coordinator(selected_uni)
                if pending:
                    st.subheader("Pending Tasks")
                    pending_df = pd.DataFrame(pending)
                    st.dataframe(pending_df[["date", "task", "category"]], use_container_width=True)
                else:
                    st.success("All tasks completed!")
            else:
                st.info("No entries logged yet")
    
    with tab3:
        st.subheader("📄 Generate Monthly Progress Reports")
        st.markdown("Generate detailed reports in HTML format (can be printed as PDF or copied to Word)")
        
        st.markdown("### Individual University Reports")
        selected_uni_report = st.selectbox("Select University", list(UNIVERSITIES.keys()), format_func=lambda x: UNIVERSITIES[x]["name"], key="report_uni")
        if st.button("Generate University Report", use_container_width=True):
            with st.spinner("Generating report..."):
                html_content = generate_university_report_html(selected_uni_report)
                filename = f"MPR_{UNIVERSITIES[selected_uni_report]['name'].replace(' ', '_')}_May2026.html"
                st.markdown(get_html_download_link(html_content, filename), unsafe_allow_html=True)
                st.success("Report generated! Click the download link above.")
        
        st.markdown("---")
        st.markdown("### Consolidated Report (All Universities)")
        if st.button("Generate Consolidated Report", use_container_width=True):
            with st.spinner("Generating consolidated report..."):
                html_content = generate_consolidated_report_html()
                filename = "Consolidated_MPR_All_Universities_May2026.html"
                st.markdown(get_html_download_link(html_content, filename), unsafe_allow_html=True)
                st.success("Consolidated report generated! Click the download link above.")
        
        st.info("💡 **How to use:** Click the download link to save the HTML file. You can then open it in any browser and print as PDF or copy to Microsoft Word.")

def create_project_lead_dashboard():
    st.markdown('<div class="projectlead-card"><h2>👨‍💼 Project Lead Dashboard - Dr. Harshal Kotwal</h2><p>Monitor Progress & Manage Reports</p></div>', unsafe_allow_html=True)
    
    show_sangam_info()
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    total_planned = len(get_all_planned_dates()) * len(UNIVERSITIES)
    summary_df = get_summary_stats()
    total_completed = summary_df["Completed"].sum() if not summary_df.empty else 0
    overall_pct = round(total_completed / total_planned * 100, 1) if total_planned > 0 else 0
    
    with col1:
        st.metric("Total Planned Tasks", total_planned)
    with col2:
        st.metric("Tasks Completed", total_completed)
    with col3:
        st.metric("Overall Progress", f"{overall_pct}%")
    
    st.progress(overall_pct / 100)
    
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["📊 Progress Overview", "📋 Training Programs", "📄 Reports"])
    
    with tab1:
        if not summary_df.empty:
            fig = px.bar(summary_df, x="University", y="Completion %", title="University-wise Progress", color="Completion %", text="Completion %", height=500)
            fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(summary_df, use_container_width=True)
    
    with tab2:
        st.subheader("Training Programs Conducted (May 12-15, 2026)")
        
        training_data = [
            {"Date": "May 12, 2026", "Topic": "NIRF Framework & Formula Interpretation", "Duration": "4 hours", "Participants": "All Coordinators", "Status": "Completed"},
            {"Date": "May 13, 2026", "Topic": "Teaching, Learning & Resources (TLR) Parameter", "Duration": "4 hours", "Participants": "All Coordinators", "Status": "Completed"},
            {"Date": "May 14, 2026", "Topic": "Research & Professional Practice (RP) Parameter", "Duration": "4 hours", "Participants": "All Coordinators", "Status": "Completed"},
            {"Date": "May 15, 2026", "Topic": "Graduation Outcomes (GO) & Outreach (OI) Parameters", "Duration": "4 hours", "Participants": "All Coordinators", "Status": "Completed"},
        ]
        
        training_df = pd.DataFrame(training_data)
        st.dataframe(training_df, use_container_width=True)
        
        st.markdown("---")
        st.subheader("Training Content Covered")
        st.markdown("""
        **1. NIRF Framework Overview:**
        - Structure and architecture of NIRF framework
        - Category-specific indicators and weightages
        - Overall, Universities, and State Public Universities categories
        
        **2. Teaching, Learning & Resources (TLR):**
        - Student Strength (SS) and enrollment calculations
        - Faculty-Student Ratio (FSR) methodology
        - Faculty Qualifications and Experience (FQE)
        - Financial Resources and Utilization (FRU)
        
        **3. Research and Professional Practice (RP):**
        - Bibliometric indicators and research productivity
        - Citation analysis and publication quality
        - IPR, patents, and sponsored research funding
        
        **4. Graduation Outcomes (GO):**
        - University examination results
        - Placement statistics and median salary
        - Higher education progression
        
        **5. Outreach and Inclusivity (OI):**
        - Regional diversity and gender representation
        - Socio-economic inclusion metrics
        - Support for disadvantaged groups
        """)
    
    with tab3:
        st.subheader("📄 Generate Reports")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Individual University Report")
            selected_uni = st.selectbox("Select University", list(UNIVERSITIES.keys()), format_func=lambda x: UNIVERSITIES[x]["name"])
            if st.button("Generate Report", use_container_width=True):
                with st.spinner("Generating..."):
                    html_content = generate_university_report_html(selected_uni)
                    filename = f"MPR_{UNIVERSITIES[selected_uni]['name'].replace(' ', '_')}_May2026.html"
                    st.markdown(get_html_download_link(html_content, filename), unsafe_allow_html=True)
        
        with col2:
            st.markdown("### Consolidated Report")
            if st.button("Generate Consolidated Report", use_container_width=True):
                with st.spinner("Generating..."):
                    html_content = generate_consolidated_report_html()
                    filename = "Consolidated_MPR_All_Universities_May2026.html"
                    st.markdown(get_html_download_link(html_content, filename), unsafe_allow_html=True)

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
    
    pending_tasks = get_pending_tasks_for_coordinator(university_code)
    completed_entries = get_university_entries(university_code)
    total_planned = len(get_all_planned_dates())
    completed_count = len(completed_entries)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📋 Total Phase 1 Tasks", total_planned)
    with col2:
        st.metric("✅ Completed", completed_count)
    with col3:
        st.metric("⏳ Pending", total_planned - completed_count)
    
    st.progress(completed_count / total_planned if total_planned > 0 else 0)
    
    st.markdown("---")
    
    st.subheader("📋 YOUR PENDING TASKS")
    
    if pending_tasks:
        st.warning(f"⚠️ You have **{len(pending_tasks)} pending tasks**. Please log them below.")
        
        selected_date_str = st.selectbox(
            "Select Date to Log Work",
            [task["date"] for task in pending_tasks],
            format_func=lambda x: f"📅 {x} - {next((t['task'][:50] for t in pending_tasks if t['date'] == x), '')}"
        )
        
        if selected_date_str:
            selected_task = next((t for t in pending_tasks if t["date"] == selected_date_str), None)
            if selected_task:
                selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d")
                
                st.markdown(f"""
                <div class="default-task-card">
                    <strong>📋 TASK FOR {selected_date_str} ({selected_date.strftime('%A')})</strong><br><br>
                    <strong>🎯 Task:</strong> {selected_task['task']}<br>
                    <strong>📂 Category:</strong> {selected_task['category']}<br>
                    <strong>📝 Description:</strong> {selected_task['description']}<br>
                    <strong>📎 Expected Deliverables:</strong> {selected_task['deliverables']}
                </div>
                """, unsafe_allow_html=True)
                
                with st.form("log_pending_task_form"):
                    use_planned = st.radio(
                        "Did you complete the planned task?",
                        ["✅ Yes, I completed the planned task", "🔄 No, I want to log a different task"],
                        horizontal=True
                    )
                    
                    if use_planned == "✅ Yes, I completed the planned task":
                        task_category = selected_task['category']
                        task_name = selected_task['task']
                        description = selected_task['description']
                        deliverables = selected_task['deliverables']
                        swapped = False
                        st.success(f"✅ Using planned task: **{task_name}**")
                    else:
                        task_category = st.selectbox("Task Category", list(TASK_CATEGORIES.keys()))
                        suggested_tasks = TASK_CATEGORIES.get(task_category, [])
                        task_name = st.selectbox("Task", ["-- Select --"] + suggested_tasks)
                        if task_name == "-- Select --":
                            task_name = st.text_input("Or enter custom task")
                        description = st.text_area("Detailed Description", height=100)
                        deliverables = st.text_area("Deliverables Produced", height=80)
                        swapped = True
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        status = st.selectbox("Status", ["completed"], index=0)
                    with col2:
                        hours_spent = st.number_input("Hours Spent", min_value=0.5, max_value=12.0, step=0.5, value=8.0)
                    
                    remarks = st.text_area("Additional Remarks")
                    
                    if st.form_submit_button("✅ Submit Work Log", use_container_width=True):
                        if use_planned == "✅ Yes, I completed the planned task":
                            if log_daily_entry(university_code, selected_date_str, selected_task['category'], selected_task['task'],
                                              selected_task['description'], selected_task['deliverables'], 
                                              status, hours_spent, remarks, False, False, coordinator_name):
                                st.success(f"✅ Work for {selected_date_str} logged successfully!")
                                st.balloons()
                                st.rerun()
                        else:
                            if task_name and task_name != "-- Select --":
                                if log_daily_entry(university_code, selected_date_str, task_category, task_name, description, 
                                                  deliverables, status, hours_spent, remarks, swapped, True, coordinator_name):
                                    st.success(f"✅ Work for {selected_date_str} logged successfully!")
                                    st.balloons()
                                    st.rerun()
                            else:
                                st.error("Please enter a task")
    else:
        st.success("🎉 Congratulations! You have completed all Phase 1 tasks!")
    
    st.markdown("---")
    
    with st.expander("📋 View Your Completed Entries", expanded=False):
        df = get_university_entries(university_code)
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No entries logged yet")
    
    st.markdown("---")
    st.subheader("📅 Training Programs Attended")
    st.info("""
    **Training Programs Completed (May 12-15, 2026):**
    - May 12: NIRF Framework & Formula Interpretation
    - May 13: Teaching, Learning & Resources (TLR) Parameter
    - May 14: Research & Professional Practice (RP) Parameter
    - May 15: Graduation Outcomes (GO) & Outreach (OI) Parameters
    """)
    
    st.markdown("---")
    st.subheader("📅 MPR Submission Reminder")
    st.warning("📋 **Note:** As per SOP Section 1 & 2, approved attendance and MPR must reach PMU MahaSTRIDE by the 10th of June 2026.")

def main():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    
    if not st.session_state["authenticated"]:
        with st.container():
            st.markdown('<div class="main-header"><h1>🔐 mahaSTRIDE NIRF Data Collection Tracker</h1><p>Phase 1: May 7-31, 2026</p></div>', unsafe_allow_html=True)
            
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
            st.markdown("*Role: Project Lead*")
        else:
            st.markdown("*Role: Coordinator*")
            if "user_university" in st.session_state:
                uni = st.session_state["user_university"]
                st.markdown(f"*University: {UNIVERSITIES[uni]['name'][:30]}...*")
        
        st.markdown("---")
        st.markdown(f"**Today:** {datetime.now().strftime('%d-%b-%Y')}")
        st.markdown("**Phase 1:** May 7-31, 2026")
        
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
            st.markdown("""
            ### mahaSTRIDE Project Tracker
            
            **Phase 1:** May 7-31, 2026
            
            **Participating Universities:**
            - University of Mumbai
            - Savitribai Phule Pune University
            - COEP Technological University
            - Sant Gadge Baba Amravati University
            - Rashtrasant Tukadoji Maharaj Nagpur University
            - KBCNMU Jalgaon
            - BAMU Aurangabad
            
            **Reports Available:**
            - University-wise MPR (aligned with the official format)
            - Consolidated MPR for all universities
            - Includes Major Activities, Meetings, Deliverables, Risks, Initiatives
            
            **How to Use Reports:**
            1. Go to Generate Reports tab
            2. Click Generate button
            3. Download the HTML file
            4. Open in browser and print as PDF or copy to Word
            """)
    
    elif user_role == "project_lead":
        if menu == "👨‍💼 Project Lead Dashboard":
            create_project_lead_dashboard()
        else:
            st.title("ℹ️ About")
            st.markdown("""
            ### Project Lead Dashboard
            
            **Features:**
            - Monitor progress across all universities
            - View training program details
            - Generate university-wise and consolidated reports
            - Track completion percentages
            
            **Training Programs Conducted:**
            - May 12-15, 2026: NIRF Framework training
            - TLR, RP, GO, OI parameters covered
            - All coordinators trained
            """)
    
    else:  # coordinator
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
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        completed = len(df[df["Status"] == "COMPLETED"])
                        total_planned = len(get_all_planned_dates())
                        st.metric("Completed Tasks", f"{completed}/{total_planned}")
                    with col2:
                        total_hours = df["Hours Spent"].sum() if "Hours Spent" in df.columns else 0
                        st.metric("Total Hours", f"{total_hours:.1f}")
                    
                    # Training tasks summary
                    training_tasks = df[df["Task Category"] == "TRAINING"]
                    if not training_tasks.empty:
                        st.subheader("Training Programs Completed")
                        st.dataframe(training_tasks[["Date", "Task", "Status"]], use_container_width=True)
                else:
                    st.info("No entries logged yet")
            else:
                st.title("ℹ️ About")
                st.markdown(f"""
                ### Coordinator Dashboard
                
                **University:** {UNIVERSITIES[university_code]['name']}
                **Nodal Officer:** {UNIVERSITIES[university_code]['nodal_officer']}
                
                **Phase 1 (May 7-31, 2026):**
                - Setup and onboarding
                - Training programs (May 12-15)
                - NIRF data collection
                - Gap analysis and reporting
                
                **Training Attended:**
                - NIRF Framework & Formula Interpretation
                - Teaching, Learning & Resources (TLR)
                - Research & Professional Practice (RP)
                - Graduation Outcomes (GO) & Outreach (OI)
                
                **How to Log Work:**
                1. Select a date from pending tasks
                2. Confirm if you completed the planned task
                3. Add hours spent and submit
                """)

if __name__ == "__main__":
    for file in [PROGRESS_DATA_FILE, ASSIGNMENTS_DATA_FILE, CUSTOM_TASKS_DATA_FILE, MEETINGS_DATA_FILE, RISKS_DATA_FILE, INITIATIVES_DATA_FILE]:
        if not os.path.exists(file):
            if file == PROGRESS_DATA_FILE:
                save_progress_data(create_initial_progress_data())
            elif file == ASSIGNMENTS_DATA_FILE:
                save_assignments_data(create_initial_assignments_data())
            elif file == CUSTOM_TASKS_DATA_FILE:
                save_custom_tasks_data(create_initial_custom_tasks_data())
            elif file == MEETINGS_DATA_FILE:
                save_meetings_data([])
            elif file == RISKS_DATA_FILE:
                save_risks_data([])
            elif file == INITIATIVES_DATA_FILE:
                save_initiatives_data([])
    
    main()
