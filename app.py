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
    }
    .default-task-card {
        background: linear-gradient(135deg, #e8f8f5 0%, #d4efdf 100%);
        border-left: 4px solid #27ae60;
        padding: 1.2rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .credentials-box {
        background-color: #f8f9fa;
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 1rem;
        margin-top: 1rem;
    }
    .credentials-box h4 {
        margin-top: 0;
        color: #1e3c72;
    }
    .cred-row {
        font-family: monospace;
        font-size: 12px;
        padding: 4px 0;
        border-bottom: 1px solid #eee;
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
        "name": "Admin"
    },
    "projectlead@mahastride.com": {
        "password": sha256("ProjectLead@2026".encode()).hexdigest(),
        "role": "project_lead",
        "name": "Dr. Harshal Kotwal"
    },
    "shubham@mitra.gov.in": {
        "password": sha256("Shubham@2026".encode()).hexdigest(),
        "role": "coordinator",
        "name": "Shubham",
        "university": "MITRA"
    },
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

# ============================================================
# UNIVERSITY DETAILS
# ============================================================
UNIVERSITIES = {
    "MU": {"name": "Mumbai University", "coordinators": ["Ms Sneha", "Mr Sagar"], "nodal_officer": "Dr. Varsha Kelkar Mane", "registrar": "_________"},
    "SSPU": {"name": "Savitribai Phule Pune University", "coordinators": ["Mr Jagan"], "nodal_officer": "Prof. Vinayak Joshi", "registrar": "_________"},
    "COEP": {"name": "COEP Technological University, Pune", "coordinators": ["Mr Vaibhav"], "nodal_officer": "Dr. Uttam Chaskar", "registrar": "_________"},
    "AU": {"name": "Sant Gadge Baba Amravati University", "coordinators": ["Mr Pratham"], "nodal_officer": "Dr. A. B. Naik", "registrar": "_________"},
    "NU": {"name": "Rashtrasant Tukadoji Maharaj Nagpur University", "coordinators": ["Ms Anjali"], "nodal_officer": "Prof. Nandkishor Karade", "registrar": "_________"},
    "KBCNMU": {"name": "KBCNMU, Jalgaon", "coordinators": ["Mr Nitish"], "nodal_officer": "Prof. Sameer Narkhede", "registrar": "_________"},
    "BAMU": {"name": "Dr. Babasaheb Ambedkar Marathwada University", "coordinators": ["Mr Atharv"], "nodal_officer": "Prof. G.D. Khedkar", "registrar": "_________"},
    "MITRA": {"name": "MITRA (PMU)", "coordinators": ["Shubham"], "nodal_officer": "Dr. Harshal Kotwal", "registrar": "_________"}
}

# Officials - Updated: Dr. Harshal Kotwal is Project Director of ICARE
ICARE_OFFICIALS = {
    "project_director": "Dr. Harshal Kotwal, Project Director, ICARE Pvt. Ltd."
}

MITRA_OFFICIALS = {
    "jt_ceo": "Jt. CEO, MITRA"
}

WORKING_HOURS = "10:00 AM - 6:00 PM"

# ============================================================
# DATA FILE PATHS
# ============================================================
PROGRESS_DATA_FILE = "progress_data.json"
TEAM_ATTENDANCE_FILE = "attendance_data.json"
MPR_DATA_FILE = "mpr_data.json"

# ============================================================
# DEFAULT PLAN - 19 WORKING DAYS
# ============================================================
DEFAULT_PLAN = {
    "2026-05-04": {"task": "SANGAM Orientation Day 1", "category": "Training", "description": "Project overview, MahaSTRIDE introduction", "venue": "Trident Board Room, Mumbai"},
    "2026-05-05": {"task": "SANGAM Training Day 2", "category": "Training", "description": "NIRF framework deep dive", "venue": "Trident Board Room, Mumbai"},
    "2026-05-06": {"task": "SANGAM Workshop Day 3", "category": "Training", "description": "GRDAU concept, data templates", "venue": "Trident Board Room, Mumbai"},
    "2026-05-07": {"task": "University Reporting & Onboarding", "category": "Setup", "description": "Report to university, meet VC & Registrar", "venue": "Respective University"},
    "2026-05-08": {"task": "NIRF Data Source Mapping", "category": "Setup", "description": "Map data sources across departments", "venue": "Respective University"},
    "2026-05-11": {"task": "Data Gap Template", "category": "Documentation", "description": "Create gap template and request letters", "venue": "Respective University"},
    "2026-05-12": {"task": "Student & Faculty Data", "category": "Data Collection", "description": "Collect enrollment and faculty data", "venue": "Respective University"},
    "2026-05-13": {"task": "Research & Placement Data", "category": "Data Collection", "description": "Collect publications and placement data", "venue": "Respective University"},
    "2026-05-14": {"task": "Financial & Infrastructure Data", "category": "Data Collection", "description": "Collect finance and infrastructure data", "venue": "Respective University"},
    "2026-05-15": {"task": "Data Consolidation", "category": "Analysis", "description": "Consolidate and validate data", "venue": "Respective University"},
    "2026-05-18": {"task": "Stakeholder Consultation", "category": "Meetings", "description": "Meeting with department heads", "venue": "Respective University"},
    "2026-05-19": {"task": "Missing Data Follow-up", "category": "Data Collection", "description": "Follow up for missing data", "venue": "Respective University"},
    "2026-05-20": {"task": "NIRF Template Preparation", "category": "Analysis", "description": "Prepare draft NIRF submission", "venue": "Respective University"},
    "2026-05-21": {"task": "SWOT Analysis & Gap Report", "category": "Documentation", "description": "Prepare SWOT and gap report", "venue": "Respective University"},
    "2026-05-22": {"task": "Inception Report Drafting", "category": "Reporting", "description": "Draft Inception Report", "venue": "Respective University"},
    "2026-05-25": {"task": "GRDAU Team Identification", "category": "Documentation", "description": "Identify GRDAU team members", "venue": "Respective University"},
    "2026-05-26": {"task": "GRDAU Operational Framework", "category": "Documentation", "description": "Finalize GRDAU framework", "venue": "Respective University"},
    "2026-05-27": {"task": "Review Meeting with ICARE", "category": "Meetings", "description": "Review May progress", "venue": "Respective University"},
    "2026-05-29": {"task": "May MPR Finalization", "category": "Reporting", "description": "Finalize May MPR", "venue": "Respective University"}
}

TASK_CATEGORIES = {
    "Setup": ["Onboarding", "Data mapping"],
    "Training": ["SANGAM", "NIRF training"],
    "Data Collection": ["Student", "Faculty", "Research", "Placement"],
    "Analysis": ["Consolidation", "Validation", "Gap analysis"],
    "Reporting": ["NIRF template", "Inception Report", "MPR"],
    "Meetings": ["Consultation", "Review"],
    "Documentation": ["Gap template", "SWOT", "GRDAU"],
    "Coordination": ["Follow-up"]
}

# ============================================================
# TEAM MEMBERS - Dr. Harshal Kotwal as ICARE Project Director
# ============================================================
TEAM_MEMBERS = {
    "MITRA": [
        {"name": "Shubham", "profile": "Coordinator, MITRA", "location": "MITRA, Mumbai"}
    ],
    "ICARE": [
        {"name": "Dr. Harshal Kotwal", "profile": "Project Director, ICARE Pvt. Ltd.", "location": "ICARE, Mumbai"}
    ],
    "MU": [
        {"name": "Ms Sneha", "profile": "Institutional Coordinator", "location": "Mumbai University"},
        {"name": "Mr Sagar", "profile": "Institutional Coordinator", "location": "Mumbai University"}
    ],
    "SSPU": [{"name": "Mr Jagan", "profile": "Institutional Coordinator", "location": "SPPU, Pune"}],
    "COEP": [{"name": "Mr Vaibhav", "profile": "Institutional Coordinator", "location": "COEP, Pune"}],
    "AU": [{"name": "Mr Pratham", "profile": "Institutional Coordinator", "location": "Amravati University"}],
    "NU": [{"name": "Ms Anjali", "profile": "Institutional Coordinator", "location": "Nagpur University"}],
    "KBCNMU": [{"name": "Mr Nitish", "profile": "Institutional Coordinator", "location": "KBCNMU, Jalgaon"}],
    "BAMU": [{"name": "Mr Atharv", "profile": "Institutional Coordinator", "location": "BAMU, Aurangabad"}]
}

def hash_password(password):
    return sha256(password.encode()).hexdigest()

def authenticate_user(email, password):
    if email in USERS and USERS[email]["password"] == hash_password(password):
        return True, USERS[email]["role"], USERS[email]["name"], USERS[email].get("university")
    return False, None, None, None

# ============================================================
# DATA MANAGEMENT
# ============================================================

def load_progress():
    try:
        if os.path.exists(PROGRESS_DATA_FILE):
            with open(PROGRESS_DATA_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return {}

def save_progress(data):
    try:
        with open(PROGRESS_DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except:
        return False

def load_attendance():
    try:
        if os.path.exists(TEAM_ATTENDANCE_FILE):
            with open(TEAM_ATTENDANCE_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return {}

def save_attendance(data):
    try:
        with open(TEAM_ATTENDANCE_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except:
        return False

def load_mpr_config():
    try:
        if os.path.exists(MPR_DATA_FILE):
            with open(MPR_DATA_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return {"work_order_ref": "MITRA/Research/MahaSTRIDE/EduRFP/49/2025", "work_order_date": "11-05-2026", "period_start": "2026-05-04", "period_end": "2026-05-29"}

def save_mpr_config(data):
    try:
        with open(MPR_DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except:
        return False

def get_all_dates():
    return list(DEFAULT_PLAN.keys())

def get_pending(university):
    data = load_progress()
    completed = set(data.get(university, {}).keys())
    pending = []
    for date in get_all_dates():
        if date not in completed:
            plan = DEFAULT_PLAN.get(date)
            if plan:
                pending.append({"date": date, "task": plan["task"], "category": plan["category"], "description": plan["description"], "venue": plan["venue"]})
    return pending

def log_work(university, date, category, task, description, hours, remarks, user):
    data = load_progress()
    if university not in data:
        data[university] = {}
    data[university][date] = {"category": category, "task": task, "description": description, "status": "completed", "hours": hours, "remarks": remarks, "updated_by": user, "updated_at": datetime.now().isoformat()}
    return save_progress(data)

def mark_all_completed(university):
    data = load_progress()
    if university not in data:
        data[university] = {}
    for date, plan in DEFAULT_PLAN.items():
        data[university][date] = {"category": plan["category"], "task": plan["task"], "description": plan["description"], "status": "completed", "hours": 8.0, "remarks": "Completed", "updated_by": "system", "updated_at": datetime.now().isoformat()}
    return save_progress(data)

def get_entries(university):
    data = load_progress()
    if university not in data:
        return pd.DataFrame()
    records = []
    for date, entry in data[university].items():
        records.append({"Date": date, "Task": entry.get("task", ""), "Status": entry.get("status", "").upper(), "Hours": entry.get("hours", 0)})
    return pd.DataFrame(records).sort_values("Date")

def get_summary():
    data = load_progress()
    stats = []
    for code, info in UNIVERSITIES.items():
        entries = data.get(code, {})
        total = len(DEFAULT_PLAN)
        completed = sum(1 for e in entries.values() if e.get("status") == "completed")
        stats.append({"University": info["name"], "Completed": completed, "Total": total})
    return pd.DataFrame(stats)

def init_all():
    for code in UNIVERSITIES:
        mark_all_completed(code)
    attendance = {}
    for team_type, members in TEAM_MEMBERS.items():
        attendance[team_type] = {}
        for member in members:
            attendance[team_type][member["name"]] = {"present": 19, "absent": 0, "holidays": 12}
    save_attendance(attendance)
    return True

def reset_all():
    for f in [PROGRESS_DATA_FILE, TEAM_ATTENDANCE_FILE, MPR_DATA_FILE]:
        if os.path.exists(f):
            os.remove(f)
    init_all()
    return True

# ============================================================
# MPR GENERATION - EXACT SOP ANNEXURE C FORMAT
# Removed Reviewed by section
# GRDAU Status changed to Completed
# Dr. Harshal Kotwal as ICARE Project Director
# ============================================================

def generate_mpr_html(university_code):
    uni = UNIVERSITIES[university_code]
    attendance = load_attendance()
    mpr = load_mpr_config()
    
    period_start = datetime.strptime(mpr.get("period_start", "2026-05-04"), "%Y-%m-%d")
    period_end = datetime.strptime(mpr.get("period_end", "2026-05-29"), "%Y-%m-%d")
    
    # Build team table
    team_rows = ""
    sr_no = 1
    
    team_rows += '<tr class="sub-header"><td colspan="7"><strong>ICARE LEVEL</strong></td>'
    for m in TEAM_MEMBERS.get("ICARE", []):
        att = attendance.get("ICARE", {}).get(m["name"], {})
        team_rows += f"""
        <tr>
            <td>{sr_no}</td>
            <td>{m['name']}</td>
            <td>{m['profile']}</td>
            <td>{m['location']}</td>
            <td>{att.get('present', 19)}</td>
            <td>{att.get('absent', 0)}</td>
            <td>{att.get('holidays', 12)}</td>
        </tr>"""
        sr_no += 1
    
    team_rows += '<tr class="sub-header"><td colspan="7"><strong>MITRA LEVEL</strong></td>'
    for m in TEAM_MEMBERS.get("MITRA", []):
        att = attendance.get("MITRA", {}).get(m["name"], {})
        team_rows += f"""
        <tr>
            <td>{sr_no}</td>
            <td>{m['name']}</td>
            <td>{m['profile']}</td>
            <td>{m['location']}</td>
            <td>{att.get('present', 19)}</td>
            <td>{att.get('absent', 0)}</td>
            <td>{att.get('holidays', 12)}</td>
        </tr>"""
        sr_no += 1
    
    team_rows += f'<tr class="sub-header"><td colspan="7"><strong>{uni["name"]}</strong></td>'
    for m in TEAM_MEMBERS.get(university_code, []):
        att = attendance.get(university_code, {}).get(m["name"], {})
        team_rows += f"""
        <tr>
            <td>{sr_no}</td>
            <td>{m['name']}</td>
            <td>{m['profile']}</td>
            <td>{m['location']}</td>
            <td>{att.get('present', 19)}</td>
            <td>{att.get('absent', 0)}</td>
            <td>{att.get('holidays', 12)}</td>
        </tr>"""
        sr_no += 1
    
    coordinators = ", ".join(uni["coordinators"])
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Monthly Progress Report - {uni['name']}</title>
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
        .sub-header {{ background-color: #d0d0d0; font-weight: bold; }}
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
<div style="text-align: center;">(From {period_start.strftime('%d-%m-%Y')} to {period_end.strftime('%d-%m-%Y')})</div>

<tr>
    <tr><td style="width:30%"><strong>Work Order Reference</strong></td><td>{mpr.get('work_order_ref')}<br>dated {mpr.get('work_order_date')}</td>
        <td style="width:30%"><strong>University / Division</strong></td><td>{uni['name']}</td></tr>
    <tr><td><strong>Work Order Start Date</strong></td><td>{period_start.strftime('%d-%b-%Y')}</div>
    <td><strong>Work Order End Date</strong></div>
    <td>{period_end.strftime('%d-%b-%Y')}</div>
    </tr>
    <tr><td><strong>Project Start Date</strong></div>
    <td>04-May-2026</div>
    <td><strong>Project End Date</strong></div>
    <td>06-May-2028</div>
    </table>
</table>

<div class="section-title">Project Team Deployment</div>
<table>
    <tr><th>Sr. No.</th><th>Name</th><th>Profile</th><th>Location</th><th>Present</th><th>Absent</th><th>Holidays</th></tr>
    {team_rows}
</table>

<div class="section-title">A. Major Activities</div>
<table>
    <tr><th>Sr. No.</th><th>Major Activities</th><th>Team Member</th><th>Status</th><th>Date</th></tr>
    <tr><td>1.</div><td>SANGAM Orientation & Training (May 4-6 at Trident Board Room)</div><td>All Coordinators</div><td>Completed</div><td>May 4-6, 2026</div></tr>
    <tr><td>2.</div><td>University Onboarding & Data Source Mapping</div><td>{coordinators}</div><td>Completed</div><td>May 7-8, 2026</div></tr>
    <tr><td>3.</div><td>NIRF Data Collection (Student, Faculty, Research, Placement, Finance)</div><td>{coordinators}</div><td>Completed</div><td>May 12-20, 2026</div></tr>
    <tr><td>4.</div><td>Stakeholder Consultation & Review Meetings</div><td>{coordinators}</div><td>Completed</div><td>May 18-27, 2026</div></tr>
    <tr><td>5.</div><td>Inception Report & GRDAU Framework Development</div><td>{coordinators}</div><td>Completed</div><td>May 22-26, 2026</div></tr>
    <tr><td>6.</div><td>May MPR Preparation & Finalization</div><td>{coordinators}</div><td>Completed</div><td>May 29, 2026</div></tr>
</table>

<div class="section-title">B. Minutes of Meetings Conducted</div>
<table>
    <tr><th>Sr. No.</th><th>Date</th><th>Chairperson + Key Participants</th><th>Agenda</th><th>Decision / Way Forward</th><th>Responsibility</th></tr>
    <tr><td>1.</div><td>May 4-6, 2026</div><td>ICARE Team + All Coordinators</div><td>SANGAM Orientation, Training & Workshop</div><td>Training completed. GRDAU concept introduced.</div><td>All Coordinators</div></tr>
    <tr><td>2.</div><td>May 7, 2026</div><td>ICARE Team + Nodal Officer</div><td>Project Kick-off and data source mapping</div><td>Data collection initiated</div><td>Coordinators</div></tr>
    <tr><td>3.</div><td>May 18, 2026</div><td>ICARE Team + Nodal Officer + Dept Heads</div><td>Data gap review and action plan</div><td>Departments to submit pending data</div><td>Coordinators</div></tr>
    <tr><td>4.</div><td>May 27, 2026</div><td>ICARE Team + IQAC</div><td>Review of May progress</div><td>MPR preparation initiated</div><td>Coordinators</div></tr>
</table>

<div class="section-title">C. Major Deliverables (As committed under Contract)</div>
<table>
    <tr><th>Sr. No.</th><th>Major Deliverables</th><th>Team Member Name</th><th>Activity Status</th><th>Due Date</th></tr>
    <tr><td>1.</div><td>Inception Report and Deployment Plan</div><td>{coordinators}</div><td>In Progress</div><td>June 6, 2026</div></tr>
    <tr><td>2.</div><td>GRDAUs Establishment & Operationalization</div><td>{coordinators}</div><td>In Progress</div><td>July 6, 2026</div></tr>
    <tr><td>3.</div><td>Monthly Progress Report (May 2026)</div><td>{coordinators}</div><td>Completed</div><td>June 10, 2026</div></tr>
</table>

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
    <tr><td>1.</div><td>NIRF Data Collection</div><td>Complete baseline data</div><td>Student, Faculty, Research, Placement data</div><td>Completed</div><td>Validation by June 15</div></tr>
    <tr><td>2.</div><td>Capacity Building</div><td>Train coordinators</div><td>SANGAM Training Program</div><td>Completed</div><td>Reinforcement in June</div></tr>
    <tr><td>3.</div><td>GRDAU Setup</div><td>Establish Data Analytics Unit</div><td>Team identification, role definition</div><td>Completed</div><td>Operational by June 30</div></tr>
</table>

<div class="section-title">Approvals and Signatures</div>
<table style="border:none">
    <tr><td style="border:none; width:30%"><strong>Prepared by:</strong></div><td style="border:none">{coordinators}<br>(Institutional Coordinators)</div></tr>
    <tr><td style="border:none"><strong>Verified by:</strong></div><td style="border:none">{uni['nodal_officer']}<br>(Nodal Officer, IQAC Coordinator)</div></tr>
    <tr><td style="border:none"><strong>Approved by:</strong></div><td style="border:none">{uni['registrar']}<br>(Registrar)</div></tr>
    <tr><td style="border:none"><strong>Approved by:</strong></div><td style="border:none">{MITRA_OFFICIALS['jt_ceo']}<br>(Jt. CEO, MITRA)</div></tr>
</table>

<div class="footer">This report is submitted as per SOP Section 2 - Monthly Progress Report (MPR)<br>Generated on {datetime.now().strftime('%d-%b-%Y %H:%M:%S')}</div>
</body>
</html>"""
    return html

def generate_consolidated_html():
    summary = get_summary()
    attendance = load_attendance()
    mpr = load_mpr_config()
    
    period_start = datetime.strptime(mpr.get("period_start", "2026-05-04"), "%Y-%m-%d")
    period_end = datetime.strptime(mpr.get("period_end", "2026-05-29"), "%Y-%m-%d")
    
    total_planned = len(DEFAULT_PLAN) * len(UNIVERSITIES)
    total_completed = summary["Completed"].sum() if not summary.empty else 0
    
    # Build consolidated team table
    team_rows = ""
    sr_no = 1
    
    team_rows += '<tr class="sub-header"><td colspan="7"><strong>ICARE LEVEL</strong></tr>'
    for m in TEAM_MEMBERS.get("ICARE", []):
        att = attendance.get("ICARE", {}).get(m["name"], {})
        team_rows += f"""
        <tr><td>{sr_no}</div><td>{m['name']}</div><td>{m['profile']}</div><td>{m['location']}</div>
        <td>{att.get('present', 19)}</div><td>{att.get('absent', 0)}</div><td>{att.get('holidays', 12)}</div></tr>"""
        sr_no += 1
    
    team_rows += '<tr class="sub-header"><td colspan="7"><strong>MITRA LEVEL</strong></tr>'
    for m in TEAM_MEMBERS.get("MITRA", []):
        att = attendance.get("MITRA", {}).get(m["name"], {})
        team_rows += f"""
        <tr><td>{sr_no}</div><td>{m['name']}</div><td>{m['profile']}</div><td>{m['location']}</div>
        <td>{att.get('present', 19)}</div><td>{att.get('absent', 0)}</div><td>{att.get('holidays', 12)}</div></tr>"""
        sr_no += 1
    
    for code, uni in UNIVERSITIES.items():
        if code not in ["MITRA"]:
            team_rows += f'<tr class="sub-header"><td colspan="7"><strong>{uni["name"]}</strong></tr>'
            for m in TEAM_MEMBERS.get(code, []):
                att = attendance.get(code, {}).get(m["name"], {})
                team_rows += f"""
                <tr><td>{sr_no}</div><td>{m['name']}</div><td>{m['profile']}</div><td>{m['location']}</div>
                <td>{att.get('present', 19)}</div><td>{att.get('absent', 0)}</div><td>{att.get('holidays', 12)}</div></tr>"""
                sr_no += 1
    
    summary_rows = ""
    for i, (_, row) in enumerate(summary.iterrows()):
        status = "Completed" if row["Completed"] == row["Total"] else "In Progress"
        summary_rows += f"<tr><td>{i+1}</div><td>{row['University']}</div><td>{row['Completed']}</div><td>{row['Total']}</div><td>{status}</div></tr>"
    
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
        .sub-header {{ background-color: #d0d0d0; font-weight: bold; }}
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
<div style="text-align: center;">Reporting Period: {period_start.strftime('%d-%m-%Y')} to {period_end.strftime('%d-%m-%Y')}</div>

<div class="section-title">Overall Project Progress</div>
<div style="margin: 10px 0;">
    <strong>Overall Status:</strong> {'Fully Completed' if total_completed == total_planned else 'Substantially Complete'}<br>
    <strong>Tasks Completed:</strong> {total_completed} / {total_planned}<br>
    <strong>Working Days:</strong> 19 days (May 4-29, 2026)
</div>

<div class="section-title">Project Team Deployment</div>
<table>
    <tr><th>Sr. No.</th><th>Name</th><th>Profile</th><th>Location</th><th>Present</th><th>Absent</th><th>Holidays</th></tr>
    {team_rows}
</table>

<div class="section-title">University-wise Progress Summary</div>
<table>
    <tr><th>Sr. No.</th><th>University</th><th>Tasks Completed</th><th>Total Tasks</th><th>Status</th></tr>
    {summary_rows}
</table>

<div class="section-title">Training Programs Conducted (May 4-6, 2026 at Trident Board Room, Mumbai)</div>
<table>
    <tr><th>Date</th><th>Program</th><th>Status</th></tr>
    <tr><td>May 4, 2026</div><td>SANGAM Orientation - Project Overview</div><td>Completed</div></tr>
    <tr><td>May 5, 2026</div><td>SANGAM Training - NIRF Framework</div><td>Completed</div></tr>
    <tr><td>May 6, 2026</div><td>SANGAM Workshop - GRDAU & Data Templates</div><td>Completed</div></tr>
</table>

<div class="section-title">Major Deliverables Status</div>
<table>
    <tr><th>Deliverable</th><th>Status</th><th>Due Date</th></tr>
    <tr><td>Inception Report and Deployment Plan</div><td>In Progress</div><td>June 6, 2026</div></tr>
    <tr><td>GRDAUs Establishment</div><td>In Progress</div><td>July 6, 2026</div></tr>
    <tr><td>Monthly Progress Report (May 2026)</div><td>Completed</div><td>June 10, 2026</div></tr>
</table>

<div class="section-title">Approvals and Signatures</div>
<table style="border:none">
    <tr><td style="border:none; width:30%"><strong>Prepared by:</strong></div><td style="border:none">All Institutional Coordinators</div></tr>
    <tr><td style="border:none"><strong>Verified by:</strong></div><td style="border:none">Nodal Officers of respective Universities</div></tr>
    <tr><td style="border:none"><strong>Approved by:</strong></div><td style="border:none">{MITRA_OFFICIALS['jt_ceo']}<br>(Jt. CEO, MITRA)</div></tr>
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
        <h4>🔐 Demo Credentials (Password: <strong>Name@2026</strong> for all)</h4>
        <div class="cred-row"><strong>Admin:</strong> admin@mahastride.com</div>
        <div class="cred-row"><strong>Project Lead (ICARE):</strong> projectlead@mahastride.com</div>
        <div class="cred-row"><strong>MITRA Coordinator:</strong> shubham@mitra.gov.in</div>
        <div class="cred-row"><strong>Mumbai University:</strong> sneha@mu.edu | sagar@mu.edu</div>
        <div class="cred-row"><strong>SPPU Pune:</strong> jagan@sspu.edu</div>
        <div class="cred-row"><strong>COEP Pune:</strong> vaibhav@coep.edu</div>
        <div class="cred-row"><strong>Amravati University:</strong> pratham@au.edu</div>
        <div class="cred-row"><strong>Nagpur University:</strong> anjali@nu.edu</div>
        <div class="cred-row"><strong>KBCNMU Jalgaon:</strong> nitish@kbcnmu.edu</div>
        <div class="cred-row"><strong>BAMU Aurangabad:</strong> atharv@bamu.edu</div>
    </div>
    """, unsafe_allow_html=True)

def show_sangam():
    st.markdown('<div class="sangam-card"><h3>🎉 SANGAM Orientation & Training</h3><p><strong>Dates:</strong> May 4-6, 2026 | <strong>Venue:</strong> Trident Board Room, Mumbai | ✅ Completed</p></div>', unsafe_allow_html=True)

# ============================================================
# DASHBOARDS
# ============================================================

def admin_dashboard():
    st.markdown('<div class="admin-card"><h2>📊 Admin Dashboard</h2></div>', unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("---")
        if st.button("🔄 Reset All Data", use_container_width=True):
            reset_all()
            st.success("Data reset!")
            st.rerun()
        if st.button("✅ Mark All Tasks Completed", use_container_width=True):
            for code in UNIVERSITIES:
                mark_all_completed(code)
            st.success("All tasks marked completed!")
            st.rerun()
    
    show_sangam()
    
    col1, col2, col3, col4 = st.columns(4)
    total_planned = len(DEFAULT_PLAN) * len(UNIVERSITIES)
    summary = get_summary()
    total_completed = summary["Completed"].sum() if not summary.empty else 0
    col1.metric("Working Days", "19")
    col2.metric("Universities", len(UNIVERSITIES))
    col3.metric("Total Tasks", total_planned)
    col4.metric("Completed", total_completed)
    
    st.dataframe(summary, use_container_width=True)
    
    st.subheader("📄 Generate Reports")
    col1, col2 = st.columns(2)
    with col1:
        sel = st.selectbox("Select University", list(UNIVERSITIES.keys()), format_func=lambda x: UNIVERSITIES[x]["name"])
        if st.button("Generate University MPR"):
            html = generate_mpr_html(sel)
            st.markdown(get_download_link(html, f"MPR_{UNIVERSITIES[sel]['name'].replace(' ', '_')}_May2026.html"), unsafe_allow_html=True)
    with col2:
        if st.button("Generate Consolidated MPR"):
            html = generate_consolidated_html()
            st.markdown(get_download_link(html, "Consolidated_MPR_May2026.html"), unsafe_allow_html=True)

def lead_dashboard():
    st.markdown('<div class="projectlead-card"><h2>👨‍💼 ICARE Project Lead Dashboard - Dr. Harshal Kotwal</h2></div>', unsafe_allow_html=True)
    show_sangam()
    
    st.subheader("📝 MPR Settings")
    mpr = load_mpr_config()
    col1, col2 = st.columns(2)
    with col1:
        wo_ref = st.text_input("Work Order Reference", value=mpr.get("work_order_ref"))
        ps = st.date_input("Period Start", value=datetime.strptime(mpr.get("period_start", "2026-05-04"), "%Y-%m-%d").date())
    with col2:
        wo_date = st.text_input("Work Order Date", value=mpr.get("work_order_date"))
        pe = st.date_input("Period End", value=datetime.strptime(mpr.get("period_end", "2026-05-29"), "%Y-%m-%d").date())
    if st.button("Save Settings"):
        mpr["work_order_ref"] = wo_ref
        mpr["work_order_date"] = wo_date
        mpr["period_start"] = ps.strftime("%Y-%m-%d")
        mpr["period_end"] = pe.strftime("%Y-%m-%d")
        save_mpr_config(mpr)
        st.success("Saved!")
    
    st.subheader("📄 Generate Reports")
    col1, col2 = st.columns(2)
    with col1:
        sel = st.selectbox("Select University", list(UNIVERSITIES.keys()), format_func=lambda x: UNIVERSITIES[x]["name"])
        if st.button("Generate University MPR"):
            html = generate_mpr_html(sel)
            st.markdown(get_download_link(html, f"MPR_{UNIVERSITIES[sel]['name'].replace(' ', '_')}_May2026.html"), unsafe_allow_html=True)
    with col2:
        if st.button("Generate Consolidated MPR"):
            html = generate_consolidated_html()
            st.markdown(get_download_link(html, "Consolidated_MPR_May2026.html"), unsafe_allow_html=True)

def coordinator_dashboard(code, name):
    uni = UNIVERSITIES[code]
    st.markdown(f'<div class="info-card"><h2>📋 Coordinator Dashboard</h2><p>{uni["name"]} | {name}</p></div>', unsafe_allow_html=True)
    
    pending = get_pending(code)
    entries = get_entries(code)
    total = len(DEFAULT_PLAN)
    completed = len(entries)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Tasks", total)
    col2.metric("Completed", completed)
    col3.metric("Pending", total - completed)
    st.progress(completed/total if total else 0)
    
    if pending:
        sel = st.selectbox("Select Date", [p["date"] for p in pending])
        task = next(p for p in pending if p["date"] == sel)
        st.markdown(f"""
        <div class="default-task-card">
            <strong>📋 {task['date']}</strong><br>
            <strong>📍 Venue:</strong> {task['venue']}<br>
            <strong>🎯 Task:</strong> {task['task']}<br>
            <strong>📝 Description:</strong> {task['description']}
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("log"):
            hours = st.number_input("Hours Spent", 0.5, 12.0, 8.0)
            remarks = st.text_area("Remarks")
            if st.form_submit_button("✅ Submit"):
                if log_work(code, sel, task["category"], task["task"], task["description"], hours, remarks, name):
                    st.success("Logged!")
                    st.rerun()
    else:
        st.success("🎉 All tasks completed!")

# ============================================================
# MAIN
# ============================================================

def main():
    if not os.path.exists(PROGRESS_DATA_FILE):
        init_all()
    
    if "auth" not in st.session_state:
        st.session_state["auth"] = False
    
    if not st.session_state["auth"]:
        st.markdown('<div class="main-header"><h1>🔐 mahaSTRIDE Project Tracker</h1><p>May 4-29, 2026 (19 Working Days)</p></div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.markdown("### Login")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            if st.button("Login", use_container_width=True):
                ok, role, name, uni = authenticate_user(email, password)
                if ok:
                    st.session_state.update({"auth": True, "role": role, "name": name, "uni": uni})
                    st.rerun()
                else:
                    st.error("Invalid credentials")
            show_credentials()
        return
    
    role, name, uni = st.session_state["role"], st.session_state["name"], st.session_state.get("uni")
    
    with st.sidebar:
        st.title("📊 mahaSTRIDE")
        st.markdown(f"**Welcome, {name}**")
        st.markdown("---")
        if role == "admin":
            menu = st.radio("Navigate", ["📊 Admin Dashboard", "ℹ️ About"])
        elif role == "project_lead":
            menu = st.radio("Navigate", ["👨‍💼 ICARE Lead Dashboard", "ℹ️ About"])
        else:
            menu = st.radio("Navigate", ["📋 My Tasks", "ℹ️ About"])
        if st.button("🚪 Logout"):
            for k in ["auth", "role", "name", "uni"]:
                st.session_state.pop(k, None)
            st.rerun()
    
    if role == "admin":
        if menu == "📊 Admin Dashboard":
            admin_dashboard()
        else:
            st.title("ℹ️ About")
            st.markdown("**mahaSTRIDE** - Maharashtra University Rankings Improvement Project\n\n- 19 Working Days (May 4-29, 2026)\n- SANGAM Training: May 4-6 at Trident Board Room\n- 7 Universities + MITRA PMU + ICARE")
    elif role == "project_lead":
        if menu == "👨‍💼 ICARE Lead Dashboard":
            lead_dashboard()
        else:
            st.title("ℹ️ About")
            st.markdown("**ICARE Project Lead Dashboard**\n- Configure MPR settings\n- Generate university-wise and consolidated reports")
    else:
        if uni and menu == "📋 My Tasks":
            coordinator_dashboard(uni, name)
        else:
            st.title("ℹ️ About")
            st.markdown("**Coordinator Dashboard**\n- Log daily work\n- Track your progress\n- May 2026: 19 working days")

if __name__ == "__main__":
    main()
