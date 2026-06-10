import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os
import json
from hashlib import sha256
import base64
import time

# ============================================================
# GITHUB STORAGE CLASS
# ============================================================

class GitHubStorage:
    """Handle data storage using GitHub API"""
    
    DATA_FILES = {
        "progress": "progress_data.json",
        "attendance": "attendance_data.json",
        "mpr_config": "mpr_data.json"
    }
    
    def __init__(self):
        self.repo = None
        self._auth_success = False
        self.file_shas = {}
        
        # Try to get secrets from Streamlit Cloud secrets
        try:
            self.token = st.secrets.get("GITHUB_TOKEN")
            self.repo_name = st.secrets.get("GITHUB_REPO")
            self.branch = st.secrets.get("GITHUB_BRANCH", "main")
            self.data_prefix = st.secrets.get("DATA_FILE_PREFIX", "")
        except:
            self.token = None
            self.repo_name = None
            self.branch = "main"
            self.data_prefix = ""
        
        if not self.token or not self.repo_name:
            return
        
        try:
            from github import Github, GithubException
            self.g = Github(self.token)
            user = self.g.get_user()
            self._auth_success = True
            self.repo = self.g.get_repo(self.repo_name)
        except:
            self.repo = None
    
    def is_authenticated(self):
        return self._auth_success and self.repo is not None
    
    def _get_full_path(self, file_key):
        file_name = self.DATA_FILES.get(file_key, f"{file_key}.json")
        if self.data_prefix:
            return f"{self.data_prefix}{file_name}"
        return file_name
    
    def save_data(self, data, file_key="progress"):
        if not self.repo:
            return self._save_local(data, file_key)
        
        try:
            from github import GithubException
            file_path = self._get_full_path(file_key)
            content = json.dumps(data, indent=2, default=str)
            
            try:
                contents = self.repo.get_contents(file_path, ref=self.branch)
                self.repo.update_file(
                    file_path,
                    f"Update {file_key} data",
                    content,
                    contents.sha,
                    branch=self.branch
                )
                return True
            except GithubException as e:
                if e.status == 404:
                    self.repo.create_file(
                        file_path,
                        f"Create {file_key} data file",
                        content,
                        branch=self.branch
                    )
                    return True
                raise
        except Exception:
            return self._save_local(data, file_key)
    
    def load_data(self, file_key="progress"):
        if not self.repo:
            return self._load_local(file_key)
        
        try:
            from github import GithubException
            file_path = self._get_full_path(file_key)
            contents = self.repo.get_contents(file_path, ref=self.branch)
            content = base64.b64decode(contents.content).decode('utf-8')
            return json.loads(content)
        except:
            return self._load_local(file_key)
    
    def _save_local(self, data, file_key):
        try:
            file_name = self.DATA_FILES.get(file_key, f"{file_key}.json")
            with open(file_name, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            return True
        except:
            return False
    
    def _load_local(self, file_key):
        try:
            file_name = self.DATA_FILES.get(file_key, f"{file_key}.json")
            if os.path.exists(file_name):
                with open(file_name, 'r') as f:
                    return json.load(f)
            return None
        except:
            return None


# Initialize storage
@st.cache_resource
def get_storage():
    return GitHubStorage()

storage = get_storage()


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
        "name": "Shubham Singh",
        "university": "MITRA"
    },
    "sneha@mu.edu": {
        "password": sha256("Sneha@2026".encode()).hexdigest(),
        "role": "coordinator",
        "name": "Sneha Kashitkar",
        "university": "MU"
    },
    "sagar@mu.edu": {
        "password": sha256("Sagar@2026".encode()).hexdigest(),
        "role": "coordinator",
        "name": "Sagar Teli",
        "university": "MU"
    },
    "jagan@sspu.edu": {
        "password": sha256("Jagan@2026".encode()).hexdigest(),
        "role": "coordinator",
        "name": "Jagan Sridhar",
        "university": "SSPU"
    },
    "vaibhav@coep.edu": {
        "password": sha256("Vaibhav@2026".encode()).hexdigest(),
        "role": "coordinator",
        "name": "Vaibhav Ambekar",
        "university": "COEP"
    },
    "pratham@au.edu": {
        "password": sha256("Pratham@2026".encode()).hexdigest(),
        "role": "coordinator",
        "name": "Prathamesh Babhulkar",
        "university": "AU"
    },
    "anjali@nu.edu": {
        "password": sha256("Anjali@2026".encode()).hexdigest(),
        "role": "coordinator",
        "name": "Anjali Singh",
        "university": "NU"
    },
    "nitish@kbcnmu.edu": {
        "password": sha256("Nitish@2026".encode()).hexdigest(),
        "role": "coordinator",
        "name": "Nitish Kumbhar",
        "university": "KBCNMU"
    },
    "atharv@bamu.edu": {
        "password": sha256("Atharv@2026".encode()).hexdigest(),
        "role": "coordinator",
        "name": "Atharav Paturkar",
        "university": "BAMU"
    }
}

# ============================================================
# UNIVERSITY DETAILS
# ============================================================
UNIVERSITIES = {
    "MU": {"name": "Mumbai University", "coordinators": ["Sneha Kashitkar", "Sagar Teli"], "nodal_officer": "Dr. Varsha Kelkar Mane", "registrar": "To be updated"},
    "SSPU": {"name": "Savitribai Phule Pune University", "coordinators": ["Jagan Sridhar"], "nodal_officer": "Prof. Vinayak Joshi", "registrar": "To be updated"},
    "COEP": {"name": "COEP Technological University, Pune", "coordinators": ["Vaibhav Ambekar"], "nodal_officer": "Dr. Uttam Chaskar", "registrar": "To be updated"},
    "AU": {"name": "Sant Gadge Baba Amravati University", "coordinators": ["Prathamesh Babhulkar"], "nodal_officer": "Dr. A. B. Naik", "registrar": "To be updated"},
    "NU": {"name": "Rashtrasant Tukadoji Maharaj Nagpur University", "coordinators": ["Anjali Singh"], "nodal_officer": "Prof. Nandkishor Karade", "registrar": "To be updated"},
    "KBCNMU": {"name": "KBCNMU, Jalgaon", "coordinators": ["Nitish Kumbhar"], "nodal_officer": "Prof. Sameer Narkhede", "registrar": "To be updated"},
    "BAMU": {"name": "Dr. Babasaheb Ambedkar Marathwada University", "coordinators": ["Atharav Paturkar"], "nodal_officer": "Prof. G.D. Khedkar", "registrar": "To be updated"},
    "MITRA": {"name": "MITRA (PMU)", "coordinators": ["Shubham Singh"], "nodal_officer": "Dr. Harshal Kotwal", "registrar": "To be updated"}
}

MITRA_OFFICIALS = {"project_director": "Dr. Harshal Kotwal, Project Director, MahaSTRIDE", "jt_ceo": "Jt. CEO, MITRA"}
ICARE_OFFICIALS = {"project_head": "Shri Karthick Sridhar, Project Head, ICARE Pvt. Ltd."}
WORKING_HOURS = "10:00 AM - 6:00 PM"

# ============================================================
# DEFAULT PLAN - 24 MONTHS (Full working days)
# ============================================================

def get_all_working_dates():
    """Generate all working dates from May 4, 2026 to April 28, 2028"""
    dates = []
    start_date = datetime(2026, 5, 4)
    end_date = datetime(2028, 4, 28)
    
    current = start_date
    while current <= end_date:
        if current.weekday() < 5:  # Monday to Friday
            dates.append(current.strftime("%Y-%m-%d"))
        current += timedelta(days=1)
    return dates

def get_task_for_date(date_str):
    """Get task for a specific date"""
    date = datetime.strptime(date_str, "%Y-%m-%d")
    month = date.month
    year = date.year
    
    # Phase 1 tasks (May-July 2026)
    if year == 2026 and month == 5:
        tasks = {
            "2026-05-04": "SANGAM Orientation Day 1 - Project Overview",
            "2026-05-05": "SANGAM Training Day 2 - NIRF Framework",
            "2026-05-06": "SANGAM Workshop Day 3 - GRDAU Concept",
            "2026-05-07": "University Reporting & Onboarding",
            "2026-05-08": "NIRF Data Source Mapping",
            "2026-05-11": "Create Data Gap Template",
            "2026-05-12": "Collect Student & Faculty Data",
            "2026-05-13": "Collect Research & Placement Data",
            "2026-05-14": "Collect Financial & Infrastructure Data",
            "2026-05-15": "Data Consolidation & Validation",
            "2026-05-18": "Stakeholder Consultation Meeting",
            "2026-05-19": "Missing Data Follow-up",
            "2026-05-20": "NIRF Template Preparation",
            "2026-05-21": "SWOT Analysis & Gap Report",
            "2026-05-22": "Inception Report Drafting",
            "2026-05-25": "GRDAU Team Identification",
            "2026-05-26": "GRDAU Operational Framework",
            "2026-05-27": "Review Meeting with ICARE",
            "2026-05-29": "May MPR Finalization"
        }
        return tasks.get(date_str, "Continue project activities")
    
    elif year == 2026 and month == 6:
        tasks = {
            "2026-06-01": "Complete Diagnostic Assessment Framework",
            "2026-06-02": "Begin University-wise Assessments",
            "2026-06-03": "Review existing data quality",
            "2026-06-04": "Identify data gaps per university",
            "2026-06-05": "Prepare assessment templates",
            "2026-06-08": "Conduct faculty interviews",
            "2026-06-09": "Analyze research output metrics",
            "2026-06-10": "Evaluate infrastructure readiness",
            "2026-06-11": "Assess international collaboration",
            "2026-06-12": "Compile assessment findings",
            "2026-06-15": "GRDAU Training Session for Coordinators",
            "2026-06-16": "Data validation workshop",
            "2026-06-17": "NIRF submission preparation",
            "2026-06-18": "Review progress with VC",
            "2026-06-19": "Update data repository",
            "2026-06-22": "Finalize Diagnostic Reports",
            "2026-06-23": "Submit Diagnostic Assessment Reports",
            "2026-06-24": "Prepare June MPR",
            "2026-06-25": "Plan July activities",
            "2026-06-26": "Client review meeting",
            "2026-06-29": "Continue data analysis",
            "2026-06-30": "Finalize monthly report"
        }
        return tasks.get(date_str, "Continue diagnostic assessments")
    
    elif year == 2026 and month == 7:
        tasks = {
            "2026-07-01": "Complete gap analysis against NIRF",
            "2026-07-02": "Prepare SWOT analysis for universities",
            "2026-07-03": "Submit GRDAU establishment plan",
            "2026-07-06": "Finalize GRDAU in all universities",
            "2026-07-07": "Train GRDAU staff",
            "2026-07-08": "Develop SOP for GRDAU",
            "2026-07-09": "Setup data management systems",
            "2026-07-10": "Review GRDAU readiness",
            "2026-07-13": "Data quality framework implementation",
            "2026-07-14": "Dashboard requirements gathering",
            "2026-07-15": "Prepare baseline report",
            "2026-07-16": "Stakeholder feedback session",
            "2026-07-17": "Update project plan",
            "2026-07-20": "Finalize July MPR",
            "2026-07-21": "Phase 1 completion review",
            "2026-07-22": "Plan Phase 2 activities",
            "2026-07-23": "Client presentation",
            "2026-07-24": "Document lessons learned"
        }
        return tasks.get(date_str, "Continue Phase 1 wrap-up")
    
    # For remaining months, provide phase-appropriate tasks
    elif year == 2026 and month >= 8:
        phase = "Phase 2: Planning (IDP Development)"
        task_templates = [
            "Develop IDP framework", "Collect strategic plans", "Analyze existing plans",
            "Draft IDP document", "Review with VC", "Incorporate feedback",
            "Finalize IDP", "Design portal architecture", "Create dashboard wireframes"
        ]
        day = date.day
        return f"{phase} - {task_templates[day % len(task_templates)]}"
    
    elif year == 2027 and month <= 4:
        phase = "Phase 3: Implementation"
        task_templates = [
            "Deploy data portal", "Conduct training", "Upload baseline data",
            "Verify data accuracy", "Implement dashboards", "Generate reports"
        ]
        day = date.day
        return f"{phase} - {task_templates[day % len(task_templates)]}"
    
    elif year == 2027 and month <= 10:
        phase = "Phase 4: Enhancement"
        task_templates = [
            "Enhance analytics", "Prepare ranking data", "Conduct workshops",
            "Improve dashboards", "Train users", "Submit ranking submissions"
        ]
        day = date.day
        return f"{phase} - {task_templates[day % len(task_templates)]}"
    
    else:
        phase = "Phase 5: Finalization"
        task_templates = [
            "Prepare final report", "Submit deliverables", "Handover documentation",
            "Complete closure", "Celebrate success"
        ]
        day = date.day
        return f"{phase} - {task_templates[day % len(task_templates)]}"


DEFAULT_PLAN = {}
for date_str in get_all_working_dates():
    DEFAULT_PLAN[date_str] = {
        "task": get_task_for_date(date_str),
        "category": "Project Activity",
        "description": "As per project plan",
        "venue": "Respective Location"
    }

TASK_CATEGORIES = {
    "Training": ["SANGAM", "NIRF training", "GRDAU training"],
    "Setup": ["Onboarding", "Data mapping", "GRDAU setup"],
    "Data Collection": ["Student", "Faculty", "Research", "Placement", "NIRF data"],
    "Analysis": ["Consolidation", "Validation", "Gap analysis", "SWOT"],
    "Reporting": ["NIRF template", "Inception Report", "MPR", "Diagnostic Reports"],
    "Meetings": ["Consultation", "Review", "VC meeting", "Client meeting"],
    "Documentation": ["Gap template", "SWOT", "GRDAU", "SOP", "IDP"],
    "Technical": ["Portal", "Dashboard", "Development", "Testing"],
    "Planning": ["IDP", "Work plan", "Phase planning"],
    "Implementation": ["Deployment", "Training", "Data upload"],
    "Enhancement": ["Analytics", "Rankings", "Workshops"],
    "Finalization": ["Reports", "Handover", "Closure"]
}

# ============================================================
# TEAM MEMBERS
# ============================================================
TEAM_MEMBERS = {
    "MITRA": [
        {"name": "Dr. Harshal Kotwal", "profile": "Project Director, MahaSTRIDE", "location": "MITRA, Mumbai"},
        {"name": "Shubham Singh", "profile": "Data Analytics Specialist", "location": "MITRA, Mumbai"}
    ],
    "MU": [
        {"name": "Sneha Kashitkar", "profile": "Institutional Coordinator", "location": "Mumbai University"},
        {"name": "Sagar Teli", "profile": "Institutional Coordinator", "location": "Mumbai University"}
    ],
    "SSPU": [{"name": "Jagan Sridhar", "profile": "Institutional Coordinator", "location": "SPPU, Pune"}],
    "COEP": [{"name": "Vaibhav Ambekar", "profile": "Institutional Coordinator", "location": "COEP, Pune"}],
    "AU": [{"name": "Prathamesh Babhulkar", "profile": "Institutional Coordinator", "location": "Amravati University"}],
    "NU": [{"name": "Anjali Singh", "profile": "Institutional Coordinator", "location": "Nagpur University"}],
    "KBCNMU": [{"name": "Nitish Kumbhar", "profile": "Institutional Coordinator", "location": "KBCNMU, Jalgaon"}],
    "BAMU": [{"name": "Atharav Paturkar", "profile": "Institutional Coordinator", "location": "BAMU, Aurangabad"}]
}

# ============================================================
# DATA MANAGEMENT FUNCTIONS
# ============================================================

def load_progress():
    data = storage.load_data("progress")
    if data is None:
        return {}
    return data

def save_progress(data):
    return storage.save_data(data, "progress")

def load_attendance():
    data = storage.load_data("attendance")
    if data is None:
        return {}
    return data

def save_attendance(data):
    return storage.save_data(data, "attendance")

def load_mpr_config():
    data = storage.load_data("mpr_config")
    if data is None:
        return {"work_order_ref": "MITRA/Research/MahaSTRIDE/EduRFP/49/2025", "work_order_date": "25-03-2026", "period_start": "2026-05-04", "period_end": "2026-05-29"}
    return data

def save_mpr_config(data):
    return storage.save_data(data, "mpr_config")

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
    data[university][date] = {
        "category": category, 
        "task": task, 
        "description": description, 
        "status": "completed", 
        "hours": hours, 
        "remarks": remarks, 
        "updated_by": user, 
        "updated_at": datetime.now().isoformat()
    }
    return save_progress(data)

def mark_all_completed(university):
    data = load_progress()
    if university not in data:
        data[university] = {}
    for date, plan in DEFAULT_PLAN.items():
        if date not in data[university]:
            data[university][date] = {
                "category": plan["category"], 
                "task": plan["task"], 
                "description": plan["description"], 
                "status": "completed", 
                "hours": 8.0, 
                "remarks": "Auto-completed", 
                "updated_by": "system", 
                "updated_at": datetime.now().isoformat()
            }
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
    for file_key in ["progress", "attendance", "mpr_config"]:
        storage.save_data({}, file_key)
    init_all()
    return True

# ============================================================
# MPR GENERATION FUNCTIONS
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
    
    team_rows += '<tr class="sub-header"><td colspan="7"><strong>MITRA LEVEL</strong></td>'
    for m in TEAM_MEMBERS.get("MITRA", []):
        att = attendance.get("MITRA", {}).get(m["name"], {})
        team_rows += f"""
        <tr>
            <td>{sr_no}</td>
            <td>{m['name']}</td>
            <td>{m['profile']}</td>
            <td>{m['location']}</td>
            <td>{att.get('present', 19)}</div>
            <td>{att.get('absent', 0)}</div>
            <td>{att.get('holidays', 12)}</div>
        </tr>"""
        sr_no += 1
    
    team_rows += f'<tr class="sub-header"><td colspan="7"><strong>{uni["name"]}</strong></div></tr>'
    for m in TEAM_MEMBERS.get(university_code, []):
        att = attendance.get(university_code, {}).get(m["name"], {})
        team_rows += f"""
        <tr>
            <td>{sr_no}</div>
            <td>{m['name']}</div>
            <td>{m['profile']}</div>
            <td>{m['location']}</div>
            <td>{att.get('present', 19)}</div>
            <td>{att.get('absent', 0)}</div>
            <td>{att.get('holidays', 12)}</div>
        </tr>"""
        sr_no += 1
    
    coordinators = ", ".join(uni["coordinators"])
    
    # Get recent completed tasks
    progress_data = load_progress()
    uni_progress = progress_data.get(university_code, {})
    completed_tasks = [date for date, info in uni_progress.items() if info.get("status") == "completed"]
    
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

<table>
    <tr><td style="width:30%"><strong>Work Order Reference</strong></div><td colspan="3">{mpr.get('work_order_ref')}<br>dated {mpr.get('work_order_date')}</div></tr>
    <tr><th>University / Division</th><td colspan="3">{uni['name']}</div></tr>
    <tr><th>Project Start Date</th><td>06 May 2026</div><th>Project End Date</th><td>06 May 2028</div></tr>
</table>

<div class="section-title">Project Team Deployment</div>
<table>
    <tr><th>Sr. No.</th><th>Name of the Key Professional</th><th>Profile as per contract</th><th>Location</th><th>Total Present Days</th><th>Total Absent Days</th><th>Total Holidays/Weekly offs</th></tr>
    {team_rows}
</table>

<div class="section-title">A. Major Activities</div>
<table>
    <tr><th>Sr. No.</th><th>Major Activities</th><th>Team Member Name</th><th>Activity Status</th><th>Date of Submission</th></tr>
    <tr><td>1.</div><td>SANGAM Orientation & Training</div><td>All Coordinators</div><td>✅ Completed</div><td>May 4-6, 2026</div></tr>
    <tr><td>2.</div><td>University Onboarding & Data Source Mapping</div><td>{coordinators}</div><td>✅ Completed</div><td>May 7-8, 2026</div></tr>
    <tr><td>3.</div><td>NIRF Data Collection</div><td>{coordinators}</div><td>✅ Completed</div><td>May 12-20, 2026</div></tr>
    <tr><td>4.</div><td>Stakeholder Consultation & Review Meetings</div><td>{coordinators}</div><td>✅ Completed</div><td>May 18-27, 2026</div></tr>
    <tr><td>5.</div><td>Inception Report & GRDAU Framework</div><td>{coordinators}</div><td>✅ Completed</div><td>May 22-26, 2026</div></tr>
    <tr><td>6.</div><td>Monthly Progress Report</div><td>{coordinators}</div><td>✅ Completed</div><td>May 29, 2026</div></tr>
</table>

<div class="section-title">B. Tasks Completed ({len(completed_tasks)} tasks)</div>
<table>
    <tr><th>Date</th><th>Task Completed</th></tr>
    {''.join([f'<tr><td>{date}</div><td>{DEFAULT_PLAN.get(date, {}).get("task", "Task completed")}</div></tr>' for date in sorted(completed_tasks)[-10:]])}
</table>

<div class="section-title">Approvals and Signatures</div>
<table style="border:none">
    <tr><td style="border:none; width:30%"><strong>Prepared by:</strong></div><td style="border:none">{coordinators}<br>(Institutional Coordinators)</div></tr>
    <tr><td style="border:none"><strong>Verified by:</strong></div><td style="border:none">{uni['nodal_officer']}<br>(Nodal Officer)</div></tr>
    <tr><td style="border:none"><strong>Approved by:</strong></div><td style="border:none">{MITRA_OFFICIALS['project_director']}<br>(Project Director, MahaSTRIDE)</div></tr>
</table>

<div class="footer">Generated on {datetime.now().strftime('%d-%b-%Y %H:%M:%S')}</div>
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
    
    team_rows += '<tr class="sub-header"><td colspan="7"><strong>MITRA LEVEL</strong></td>'
    for m in TEAM_MEMBERS.get("MITRA", []):
        att = attendance.get("MITRA", {}).get(m["name"], {})
        team_rows += f"""
        <tr><td>{sr_no}</div><td>{m['name']}</div><td>{m['profile']}</div><td>{m['location']}</div>
        <td>{att.get('present', 19)}</div><td>{att.get('absent', 0)}</div><td>{att.get('holidays', 12)}</div></tr>"""
        sr_no += 1
    
    for code, uni in UNIVERSITIES.items():
        if code != "MITRA":
            team_rows += f'<tr class="sub-header"><td colspan="7"><strong>{uni["name"]}</strong></div></tr>'
            for m in TEAM_MEMBERS.get(code, []):
                att = attendance.get(code, {}).get(m["name"], {})
                team_rows += f"""
                <tr><td>{sr_no}</div><td>{m['name']}</div><td>{m['profile']}</div><td>{m['location']}</div>
                <td>{att.get('present', 19)}</div><td>{att.get('absent', 0)}</div><td>{att.get('holidays', 12)}</div></tr>"""
                sr_no += 1
    
    summary_rows = ""
    for i, (_, row) in enumerate(summary.iterrows()):
        status = "✅ Completed" if row["Completed"] == row["Total"] else "🔄 In Progress"
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
    <strong>Overall Status:</strong> {'✅ Fully Completed' if total_completed == total_planned else '🔄 In Progress'}<br>
    <strong>Tasks Completed:</strong> {total_completed} / {total_planned}<br>
    <strong>Working Days:</strong> {len(DEFAULT_PLAN)} days
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

<div class="section-title">Approvals and Signatures</div>
<table style="border:none">
    <tr><td style="border:none; width:30%"><strong>Prepared by:</strong></div><td style="border:none">All Institutional Coordinators</div></tr>
    <tr><td style="border:none"><strong>Verified by:</strong></div><td style="border:none">Nodal Officers of respective Universities</div></tr>
    <tr><td style="border:none"><strong>Approved by:</strong></div><td style="border:none">{MITRA_OFFICIALS['project_director']}</div></tr>
</table>

<div class="footer">Generated on {datetime.now().strftime('%d-%b-%Y %H:%M:%S')}</div>
</body>
</html>"""
    return html

def get_download_link(html, filename):
    b64 = base64.b64encode(html.encode()).decode()
    return f'<a href="data:text/html;base64,{b64}" download="{filename}" style="background:#4CAF50;color:white;padding:10px 20px;text-decoration:none;border-radius:5px;">📥 Download {filename}</a>'

def show_credentials():
    st.markdown("""
    <div class="credentials-box">
        <h4>🔐 Login Credentials (Password: <strong>Name@2026</strong> for all)</h4>
        <div class="cred-row"><strong>Admin:</strong> admin@mahastride.com</div>
        <div class="cred-row"><strong>Project Lead:</strong> projectlead@mahastride.com</div>
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
            st.success("Data reset successfully!")
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
    col1.metric("Total Working Days", len(DEFAULT_PLAN))
    col2.metric("Universities", len(UNIVERSITIES))
    col3.metric("Total Tasks", total_planned)
    col4.metric("Completed Tasks", total_completed)
    
    st.dataframe(summary, use_container_width=True)
    
    st.subheader("📄 Generate Reports")
    col1, col2 = st.columns(2)
    with col1:
        sel = st.selectbox("Select University", list(UNIVERSITIES.keys()), format_func=lambda x: UNIVERSITIES[x]["name"])
        if st.button("Generate University MPR"):
            html = generate_mpr_html(sel)
            st.markdown(get_download_link(html, f"MPR_{UNIVERSITIES[sel]['name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.html"), unsafe_allow_html=True)
    with col2:
        if st.button("Generate Consolidated MPR"):
            html = generate_consolidated_html()
            st.markdown(get_download_link(html, f"Consolidated_MPR_{datetime.now().strftime('%Y%m%d')}.html"), unsafe_allow_html=True)
    
    # GitHub storage status
    st.markdown("---")
    if storage.is_authenticated():
        st.success("✅ Data is being saved to GitHub cloud storage")
    else:
        st.warning("⚠️ GitHub storage not configured. Data is saved locally only.")

def lead_dashboard():
    st.markdown('<div class="projectlead-card"><h2>👨‍💼 Project Lead Dashboard</h2></div>', unsafe_allow_html=True)
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
        st.success("Settings saved!")
    
    st.subheader("📄 Generate Reports")
    col1, col2 = st.columns(2)
    with col1:
        sel = st.selectbox("Select University", list(UNIVERSITIES.keys()), format_func=lambda x: UNIVERSITIES[x]["name"])
        if st.button("Generate University MPR"):
            html = generate_mpr_html(sel)
            st.markdown(get_download_link(html, f"MPR_{UNIVERSITIES[sel]['name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.html"), unsafe_allow_html=True)
    with col2:
        if st.button("Generate Consolidated MPR"):
            html = generate_consolidated_html()
            st.markdown(get_download_link(html, f"Consolidated_MPR_{datetime.now().strftime('%Y%m%d')}.html"), unsafe_allow_html=True)
    
    # Show progress summary
    st.markdown("---")
    st.subheader("📊 Overall Progress")
    summary = get_summary()
    fig = px.bar(summary, x="University", y="Completed", title="Tasks Completed by University", text="Completed")
    st.plotly_chart(fig, use_container_width=True)

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
    
    st.markdown("---")
    st.subheader("📝 Log Your Work")
    
    if pending:
        # Date selector
        selected_date = st.selectbox("Select Date", [p["date"] for p in pending], format_func=lambda x: f"{x} - {DEFAULT_PLAN.get(x, {}).get('task', 'No task')[:50]}...")
        task = next(p for p in pending if p["date"] == selected_date)
        
        st.markdown(f"""
        <div class="default-task-card">
            <strong>📋 Task for {task['date']}</strong><br>
            <strong>📍 Venue:</strong> {task['venue']}<br>
            <strong>🎯 Task:</strong> {task['task']}<br>
            <strong>📝 Description:</strong> {task['description']}
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("log_work_form"):
            col1, col2 = st.columns(2)
            with col1:
                hours = st.number_input("Hours Spent", 0.5, 12.0, 8.0, step=0.5)
                start_time = st.time_input("Start Time", value=datetime.strptime("10:00", "%H:%M").time())
            with col2:
                end_time = st.time_input("End Time", value=datetime.strptime("18:00", "%H:%M").time())
                work_hours = f"{start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"
            
            remarks = st.text_area("Work Accomplished / Remarks", height=100, placeholder="Describe what you accomplished today...")
            
            if st.form_submit_button("✅ Submit Work Log", use_container_width=True, type="primary"):
                if remarks:
                    if log_work(code, selected_date, task["category"], task["task"], task["description"], hours, f"{work_hours} - {remarks}", name):
                        st.success("🎉 Work logged successfully!")
                        st.balloons()
                        time.sleep(1)
                        st.rerun()
                else:
                    st.error("Please describe your work accomplishments")
    else:
        st.success("🎉 All tasks completed! Great job!")
    
    # Show recent completions
    if completed > 0:
        st.markdown("---")
        st.subheader("✅ Recently Completed Tasks")
        entries_df = get_entries(code).head(10)
        st.dataframe(entries_df, use_container_width=True, hide_index=True)

# ============================================================
# MAIN
# ============================================================

def main():
    if not os.path.exists("progress_data.json") and not storage.load_data("progress"):
        init_all()
    
    if "auth" not in st.session_state:
        st.session_state["auth"] = False
    
    if not st.session_state["auth"]:
        st.markdown('<div class="main-header"><h1>🔐 mahaSTRIDE Project Tracker</h1><p>24-Month Project | May 2026 - April 2028</p><p>Monday to Friday | 10:00 AM - 6:00 PM</p></div>', unsafe_allow_html=True)
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
            menu = st.radio("Navigate", ["👨‍💼 Lead Dashboard", "ℹ️ About"])
        else:
            menu = st.radio("Navigate", ["📋 My Tasks", "ℹ️ About"])
        
        st.markdown("---")
        st.markdown("**Working Hours**")
        st.markdown("🕐 10:00 AM - 6:00 PM")
        st.markdown("📅 Monday to Friday")
        
        if st.button("🚪 Logout"):
            for k in ["auth", "role", "name", "uni"]:
                st.session_state.pop(k, None)
            st.rerun()
    
    if role == "admin":
        if menu == "📊 Admin Dashboard":
            admin_dashboard()
        else:
            st.title("ℹ️ About")
            st.markdown("**mahaSTRIDE** - Maharashtra University Rankings Improvement Project\n\n- 24 Months Project (May 2026 - April 2028)\n- SANGAM Training: May 4-6 at Trident Board Room\n- 7 Universities + MITRA PMU\n- Working Hours: 10 AM - 6 PM (Mon-Fri)")
    elif role == "project_lead":
        if menu == "👨‍💼 Lead Dashboard":
            lead_dashboard()
        else:
            st.title("ℹ️ About")
            st.markdown("**Project Lead Dashboard**\n- Configure MPR settings\n- Generate university-wise and consolidated reports\n- Track overall project progress")
    else:
        if uni and menu == "📋 My Tasks":
            coordinator_dashboard(uni, name)
        else:
            st.title("ℹ️ About")
            st.markdown("**Coordinator Dashboard**\n- Log daily work\n- Track your progress\n- 24-month project timeline")

if __name__ == "__main__":
    # Add timedelta import
    from datetime import timedelta
    main()
