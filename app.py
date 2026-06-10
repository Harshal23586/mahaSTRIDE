import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import os
import json
from hashlib import sha256
import base64
import time

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
    .analyst-card {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .filter-bar {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# GITHUB STORAGE CLASS
# ============================================================

class GitHubStorage:
    """Handle data storage using GitHub API"""
    
    DATA_FILES = {
        "progress": "progress_data.json",
        "attendance": "attendance_data.json",
        "mpr_config": "mpr_data.json",
        "daily_logs": "daily_work_logs.json"
    }
    
    def __init__(self):
        self.repo = None
        self._auth_success = False
        self.file_shas = {}
        
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
# AUTHENTICATION FUNCTION
# ============================================================

def authenticate_user(email, password):
    """Authenticate user with email and password"""
    if email in USERS and USERS[email]["password"] == sha256(password.encode()).hexdigest():
        return True, USERS[email]["role"], USERS[email]["name"], USERS[email].get("university")
    return False, None, None, None

# ============================================================
# USER CREDENTIALS
# ============================================================
USERS = {
    "admin@mahastride.com": {
        "password": sha256("Admin@2026".encode()).hexdigest(),
        "role": "admin",
        "name": "Administrator",
        "avatar": "👨‍💼"
    },
    "projectlead@mahastride.com": {
        "password": sha256("ProjectLead@2026".encode()).hexdigest(),
        "role": "project_lead",
        "name": "Dr. Harshal Kotwal",
        "avatar": "👨‍🔬"
    },
    "shubham@mitra.gov.in": {
        "password": sha256("Shubham@2026".encode()).hexdigest(),
        "role": "coordinator",
        "name": "Shubham Singh",
        "university": "MITRA",
        "avatar": "👨‍💻"
    },
    "sneha@mu.edu": {
        "password": sha256("Sneha@2026".encode()).hexdigest(),
        "role": "coordinator",
        "name": "Sneha Kashitkar",
        "university": "MU",
        "avatar": "👩‍🎓"
    },
    "sagar@mu.edu": {
        "password": sha256("Sagar@2026".encode()).hexdigest(),
        "role": "coordinator",
        "name": "Sagar Teli",
        "university": "MU",
        "avatar": "👨‍🎓"
    },
    "jagan@sspu.edu": {
        "password": sha256("Jagan@2026".encode()).hexdigest(),
        "role": "coordinator",
        "name": "Jagan Sridhar",
        "university": "SSPU",
        "avatar": "👨‍🏫"
    },
    "vaibhav@coep.edu": {
        "password": sha256("Vaibhav@2026".encode()).hexdigest(),
        "role": "coordinator",
        "name": "Vaibhav Ambekar",
        "university": "COEP",
        "avatar": "👨‍🔧"
    },
    "pratham@au.edu": {
        "password": sha256("Pratham@2026".encode()).hexdigest(),
        "role": "coordinator",
        "name": "Prathamesh Babhulkar",
        "university": "AU",
        "avatar": "👨‍🎓"
    },
    "anjali@nu.edu": {
        "password": sha256("Anjali@2026".encode()).hexdigest(),
        "role": "coordinator",
        "name": "Anjali Singh",
        "university": "NU",
        "avatar": "👩‍🎓"
    },
    "nitish@kbcnmu.edu": {
        "password": sha256("Nitish@2026".encode()).hexdigest(),
        "role": "coordinator",
        "name": "Nitish Kumbhar",
        "university": "KBCNMU",
        "avatar": "👨‍🎓"
    },
    "atharv@bamu.edu": {
        "password": sha256("Atharv@2026".encode()).hexdigest(),
        "role": "coordinator",
        "name": "Atharav Paturkar",
        "university": "BAMU",
        "avatar": "👨‍🎓"
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
# COMPLETE 24-MONTH PLAN
# ============================================================

def get_all_working_dates():
    """Generate all working dates from May 4, 2026 to April 28, 2028"""
    dates = []
    start_date = datetime(2026, 5, 4)
    end_date = datetime(2028, 4, 28)
    
    current = start_date
    while current <= end_date:
        if current.weekday() < 5:
            dates.append(current.strftime("%Y-%m-%d"))
        current += timedelta(days=1)
    return dates


def get_task_for_date(date_str):
    """Get specific task for a date based on the 24-month plan"""
    date = datetime.strptime(date_str, "%Y-%m-%d")
    month = date.month
    year = date.year
    day = date.day
    
    # Phase 1: Foundation (May - July 2026)
    if year == 2026 and month == 5:
        may_tasks = {
            "2026-05-04": "SANGAM Orientation Day 1 - Project Overview & MahaSTRIDE Introduction",
            "2026-05-05": "SANGAM Training Day 2 - NIRF Framework Deep Dive",
            "2026-05-06": "SANGAM Workshop Day 3 - GRDAU Concept & Data Templates",
            "2026-05-07": "University Reporting & Onboarding - Meet VC & Registrar",
            "2026-05-08": "NIRF Data Source Mapping - Map data sources across departments",
            "2026-05-11": "Create Data Gap Template and Request Letters",
            "2026-05-12": "Collect Student Enrollment & Faculty Data from all departments",
            "2026-05-13": "Collect Research Publications & Placement Data",
            "2026-05-14": "Collect Financial & Infrastructure Data",
            "2026-05-15": "Data Consolidation & Validation - First Pass",
            "2026-05-18": "Stakeholder Consultation Meeting with Department Heads",
            "2026-05-19": "Missing Data Follow-up and Verification",
            "2026-05-20": "NIRF Template Preparation and Draft Submission",
            "2026-05-21": "SWOT Analysis & Gap Report Preparation",
            "2026-05-22": "Inception Report Drafting",
            "2026-05-25": "GRDAU Team Identification and Nomination",
            "2026-05-26": "GRDAU Operational Framework Finalization",
            "2026-05-27": "Review Meeting with ICARE Leadership",
            "2026-05-29": "May MPR Finalization and Submission"
        }
        return may_tasks.get(date_str, "Continue May 2026 project activities")
    
    elif year == 2026 and month == 6:
        june_tasks = {
            "2026-06-01": "Complete Diagnostic Assessment Framework and Methodology",
            "2026-06-02": "Begin University-wise Assessments - Start with Mumbai University",
            "2026-06-03": "Review Existing Data Quality Across All Departments",
            "2026-06-04": "Identify Data Gaps per University and Prioritize",
            "2026-06-05": "Prepare Assessment Templates and Get PMU Approval",
            "2026-06-08": "Conduct Faculty Interviews at Mumbai University",
            "2026-06-09": "Analyze Research Output Metrics for All Universities",
            "2026-06-10": "Evaluate Library Resources and Digital Infrastructure",
            "2026-06-11": "Assess Laboratory Facilities and Research Equipment",
            "2026-06-12": "Compile All Assessment Findings and Create Dashboards",
            "2026-06-15": "GRDAU Training Session for Coordinators - Module 1",
            "2026-06-16": "Data Validation Workshop - Standardization and Quality Checks",
            "2026-06-17": "NIRF Submission Preparation - Complete Data Templates",
            "2026-06-18": "Review Progress with Vice Chancellor",
            "2026-06-19": "Update Central Data Repository with All Collected Data",
            "2026-06-22": "Finalize Diagnostic Reports for All 7 Universities",
            "2026-06-23": "Submit Diagnostic Assessment Reports to PMU",
            "2026-06-24": "Prepare June Monthly Progress Report",
            "2026-06-25": "Plan July Activities and Resource Allocation",
            "2026-06-26": "Client Review Meeting - Present June Progress",
            "2026-06-29": "Continue Data Analysis and Identify Improvement Areas",
            "2026-06-30": "Finalize and Submit June MPR"
        }
        return june_tasks.get(date_str, "Continue June 2026 diagnostic assessments")
    
    elif year == 2026 and month == 7:
        july_tasks = {
            "2026-07-01": "Complete Gap Analysis Against NIRF/NAAC/Global Rankings",
            "2026-07-02": "Prepare SWOT Analysis Report for Mumbai University",
            "2026-07-03": "Prepare SWOT Analysis Report for Pune University",
            "2026-07-06": "Prepare SWOT Analysis Report for Nagpur University",
            "2026-07-07": "Prepare SWOT Analysis Report for Amravati University",
            "2026-07-08": "Prepare SWOT Analysis Report for COEP University",
            "2026-07-09": "Prepare SWOT Analysis Report for KBCNMU Jalgaon",
            "2026-07-10": "Prepare SWOT Analysis Report for BAMU Aurangabad",
            "2026-07-13": "Finalize GRDAU Establishment Plan and Submit for Approval",
            "2026-07-14": "Setup GRDAU Office with Required Hardware and Software",
            "2026-07-15": "Conduct Data Entry Training for Newly Appointed GRDAU Staff",
            "2026-07-16": "Create Data Validation Protocols and Quality Checklists",
            "2026-07-17": "Develop Dashboard Requirements Document",
            "2026-07-20": "Design Baseline Report Template for Phase 1 Completion",
            "2026-07-21": "Compile All Phase 1 Deliverables",
            "2026-07-22": "Present Phase 1 Findings to MITRA Steering Committee",
            "2026-07-23": "Document Lessons Learned and Best Practices",
            "2026-07-24": "Plan Phase 2 Activities",
            "2026-07-27": "Prepare July Monthly Progress Report",
            "2026-07-28": "Submit July MPR and Phase 1 Completion Report",
            "2026-07-29": "Review and Incorporate Client Feedback",
            "2026-07-30": "Finalize Phase 2 Work Plan and Resource Allocation",
            "2026-07-31": "Conduct Phase 2 Kickoff Meeting"
        }
        return july_tasks.get(date_str, "Continue July 2026 Phase 1 completion")
    
    # For remaining months, provide phase-based tasks
    elif year == 2026 and month >= 8:
        phases = {
            8: "Phase 2: IDP Development - Drafting institutional plans",
            9: "Phase 2: Dashboard Design - Creating wireframes and prototypes",
            10: "Phase 2: Milestone 2 - IDP execution monitoring",
            11: "Phase 3: Portal Deployment - Launching data portal",
            12: "Phase 3: Training - Capacity building programs"
        }
        return f"{phases.get(month, 'Phase 3: Implementation')} - Day {day}"
    
    elif year == 2027:
        if month <= 4:
            return f"Phase 3: Implementation - Data quality and research enhancement - Day {day}"
        elif month <= 8:
            return f"Phase 4: Enhancement - Rankings and international collaboration - Day {day}"
        else:
            return f"Phase 4: Enhancement - Academic reputation building - Day {day}"
    
    else:
        return f"Phase 5: Finalization - Project closure and handover - Day {day}"


# Generate DEFAULT_PLAN
DEFAULT_PLAN = {}
for date_str in get_all_working_dates():
    DEFAULT_PLAN[date_str] = {
        "task": get_task_for_date(date_str),
        "category": "Project Activity",
        "description": "As per project plan",
        "venue": "Respective Location"
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

def load_daily_logs():
    data = storage.load_data("daily_logs")
    if data is None:
        return {}
    return data

def save_daily_logs(data):
    return storage.save_data(data, "daily_logs")

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
    save_progress(data)
    
    # Also save to daily logs for detailed tracking
    daily_logs = load_daily_logs()
    if university not in daily_logs:
        daily_logs[university] = {}
    daily_logs[university][date] = {
        "task": task,
        "hours": hours,
        "remarks": remarks,
        "logged_by": user,
        "logged_at": datetime.now().isoformat()
    }
    save_daily_logs(daily_logs)
    return True

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

def get_analyst_performance():
    """Get performance data for all analysts for admin/project lead view"""
    data = load_progress()
    daily_logs = load_daily_logs()
    
    analyst_performance = []
    for email, user in USERS.items():
        if user.get("role") == "coordinator":
            uni_code = user.get("university")
            uni_name = UNIVERSITIES.get(uni_code, {}).get("name", "Unknown")
            user_progress = data.get(uni_code, {})
            completed = len(user_progress)
            total = len(DEFAULT_PLAN)
            
            # Get recent activity
            user_logs = daily_logs.get(uni_code, {})
            recent_logs = sorted(user_logs.items(), key=lambda x: x[0], reverse=True)[:5]
            
            analyst_performance.append({
                "name": user["name"],
                "university": uni_name,
                "avatar": user.get("avatar", "👤"),
                "completed": completed,
                "total": total,
                "progress": round((completed / total * 100), 1) if total > 0 else 0,
                "last_activity": max([log["logged_at"] for log in user_logs.values()]) if user_logs else "No activity",
                "recent_tasks": [(date, log["task"][:50]) for date, log in recent_logs]
            })
    
    return pd.DataFrame(analyst_performance)

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
    for file_key in ["progress", "attendance", "mpr_config", "daily_logs"]:
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
    
    team_rows = ""
    sr_no = 1
    
    team_rows += '<tr class="sub-header"><td colspan="7"><strong>MITRA LEVEL</strong></tr>'
    for m in TEAM_MEMBERS.get("MITRA", []):
        att = attendance.get("MITRA", {}).get(m["name"], {})
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
</div>
<div class="report-title">MONTHLY PROGRESS REPORT</div>
<div style="text-align: center;">{period_start.strftime('%d-%m-%Y')} to {period_end.strftime('%d-%m-%Y')}</div>

<div class="section-title">Project Team Deployment</div>
<table>
    <tr><th>Sr. No.</th><th>Name</th><th>Profile</th><th>Location</th><th>Present</th><th>Absent</th><th>Holidays</th></tr>
    {team_rows}
</table>

<div class="section-title">Tasks Completed</div>
<table>
    <tr><th>Date</th><th>Task Completed</th></tr>
    {''.join([f'<tr><td>{date}</td><td>{DEFAULT_PLAN.get(date, {}).get("task", "Task completed")}</td></tr>' for date in sorted(completed_tasks)[-10:]])}
</table>

<div class="section-title">Approvals</div>
<table style="border:none">
    <tr><td style="border:none"><strong>Prepared by:</strong></td><td style="border:none">{coordinators}</td></tr>
    <tr><td style="border:none"><strong>Approved by:</strong></td><td style="border:none">{MITRA_OFFICIALS['project_director']}</td></tr>
</table>
<div class="footer">Generated on {datetime.now().strftime('%d-%b-%Y %H:%M:%S')}</div>
</body>
</html>"""
    return html

def generate_consolidated_html():
    summary = get_summary()
    analyst_performance = get_analyst_performance()
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Consolidated Progress Report</title>
    <style>
        body {{ font-family: 'Times New Roman', serif; margin: 0.7in; font-size: 11pt; }}
        .header {{ text-align: center; }}
        .section-title {{ font-size: 12pt; font-weight: bold; background-color: #f0f0f0; padding: 5px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
        th, td {{ border: 1px solid #000; padding: 6px; }}
        th {{ background-color: #e8e8e8; }}
    </style>
</head>
<body>
<div class="header">
    <h2>Maharashtra Institution for Transformation (MITRA)</h2>
    <h3>Consolidated Progress Report</h3>
</div>

<div class="section-title">University-wise Progress</div>
<table>
    <tr><th>University</th><th>Tasks Completed</th><th>Total Tasks</th><th>Progress</th></tr>
    {''.join([f'<tr><td>{row["University"]}</td><td>{row["Completed"]}</td><td>{row["Total"]}</td><td>{row["Completed"]/row["Total"]*100:.1f}%</td>' for _, row in summary.iterrows()])}
</table>

<div class="section-title">Analyst Performance</div>
<table>
    <tr><th>Analyst</th><th>University</th><th>Completed</th><th>Progress</th></tr>
    {''.join([f'<tr><td>{row["name"]}</td><td>{row["university"]}</td><td>{row["completed"]}</div><td>{row["progress"]}%</div></tr>' for _, row in analyst_performance.iterrows()])}
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
        <div class="cred-row"><strong>Data Analysts:</strong> sneha@mu.edu, shubham@mitra.gov.in, sagar@mu.edu, jagan@sspu.edu, vaibhav@coep.edu, pratham@au.edu, anjali@nu.edu, nitish@kbcnmu.edu, atharv@bamu.edu</div>
    </div>
    """, unsafe_allow_html=True)

def show_sangam():
    st.markdown('<div class="sangam-card"><h3>🎉 SANGAM Orientation & Training</h3><p><strong>Dates:</strong> May 4-6, 2026 | <strong>Venue:</strong> Trident Board Room, Mumbai | ✅ Completed</p></div>', unsafe_allow_html=True)

# ============================================================
# ADMIN DASHBOARD - WITH ANALYST MONITORING
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
    
    # Key metrics
    total_planned = len(DEFAULT_PLAN) * len(UNIVERSITIES)
    summary = get_summary()
    total_completed = summary["Completed"].sum() if not summary.empty else 0
    analyst_df = get_analyst_performance()
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("📅 Working Days", len(DEFAULT_PLAN))
    with col2:
        st.metric("🏫 Universities", len(UNIVERSITIES))
    with col3:
        st.metric("📋 Total Tasks", total_planned)
    with col4:
        st.metric("✅ Completed", total_completed)
    with col5:
        st.metric("👥 Data Analysts", len(analyst_df))
    
    st.markdown("---")
    
    # Tabs for different views
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 University Progress", "👥 Analyst Performance", "📋 Daily Activity Log", "📄 Reports", "⚙️ Settings"])
    
    with tab1:
        st.subheader("University-wise Progress")
        fig = px.bar(summary, x="University", y="Completed", title="Tasks Completed by University", text="Completed")
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(summary, use_container_width=True, hide_index=True)
    
    with tab2:
        st.subheader("Data Analyst Performance")
        
        # Filters
        col1, col2 = st.columns(2)
        with col1:
            selected_analyst = st.selectbox("Filter by Analyst", ["All"] + analyst_df["name"].tolist())
        with col2:
            min_progress = st.slider("Minimum Progress (%)", 0, 100, 0)
        
        filtered_df = analyst_df
        if selected_analyst != "All":
            filtered_df = filtered_df[filtered_df["name"] == selected_analyst]
        filtered_df = filtered_df[filtered_df["progress"] >= min_progress]
        
        # Display analysts
        for _, row in filtered_df.iterrows():
            with st.expander(f"{row['avatar']} {row['name']} - {row['university']} ({row['progress']}% complete)"):
                st.progress(row['progress']/100)
                st.metric("Tasks Completed", f"{row['completed']}/{row['total']}")
                st.caption(f"Last Activity: {row['last_activity'][:16] if row['last_activity'] != 'No activity' else 'No activity'}")
                
                if row['recent_tasks']:
                    st.markdown("**Recent Tasks:**")
                    for date, task in row['recent_tasks']:
                        st.markdown(f"- {date}: {task}")
        
        # Performance chart
        fig = px.bar(analyst_df, x="name", y="progress", color="university", text="progress", title="Analyst Progress (%)")
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Daily Activity Log - All Analysts")
        
        # Date range filter
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", datetime(2026, 6, 8))
        with col2:
            end_date = st.date_input("End Date", datetime.now())
        
        daily_logs = load_daily_logs()
        all_activities = []
        
        for uni_code, logs in daily_logs.items():
            uni_name = UNIVERSITIES.get(uni_code, {}).get("name", uni_code)
            for date, log in logs.items():
                if start_date <= datetime.strptime(date, "%Y-%m-%d").date() <= end_date:
                    all_activities.append({
                        "Date": date,
                        "University": uni_name,
                        "Analyst": log.get("logged_by", "Unknown"),
                        "Task": log.get("task", "")[:80],
                        "Hours": log.get("hours", 0),
                        "Remarks": log.get("remarks", "")[:100],
                        "Logged At": log.get("logged_at", "")[:16]
                    })
        
        if all_activities:
            df_activities = pd.DataFrame(all_activities).sort_values("Date", ascending=False)
            st.dataframe(df_activities, use_container_width=True, hide_index=True)
        else:
            st.info("No activity logs found for the selected date range")
    
    with tab4:
        st.subheader("Generate Reports")
        col1, col2 = st.columns(2)
        with col1:
            sel = st.selectbox("Select University", list(UNIVERSITIES.keys()), format_func=lambda x: UNIVERSITIES[x]["name"])
            if st.button("Generate University MPR"):
                html = generate_mpr_html(sel)
                st.markdown(get_download_link(html, f"MPR_{UNIVERSITIES[sel]['name'].replace(' ', '_')}.html"), unsafe_allow_html=True)
        with col2:
            if st.button("Generate Consolidated Report"):
                html = generate_consolidated_html()
                st.markdown(get_download_link(html, "Consolidated_Report.html"), unsafe_allow_html=True)
        
        # Export data
        st.subheader("Export Data")
        if st.button("📊 Export Analyst Performance CSV"):
            csv = analyst_df.to_csv(index=False).encode('utf-8')
            st.download_button("Download CSV", csv, "analyst_performance.csv", "text/csv")
    
    with tab5:
        st.subheader("System Settings")
        if storage.is_authenticated():
            st.success("✅ GitHub storage is connected. Data is being saved to the cloud.")
        else:
            st.warning("⚠️ GitHub storage not configured. Data is saved locally only.")
        
        if st.button("📦 Create Backup", use_container_width=True):
            st.info("Backup feature coming soon")


# ============================================================
# PROJECT LEAD DASHBOARD - WITH ANALYST MONITORING
# ============================================================

def project_lead_dashboard():
    st.markdown('<div class="projectlead-card"><h2>👨‍💼 Project Lead Dashboard</h2></div>', unsafe_allow_html=True)
    st.markdown("**Dr. Harshal Kotwal** - ICARE Project Director")
    
    show_sangam()
    
    # MPR Settings
    with st.expander("📝 MPR Settings", expanded=False):
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
    
    # Key metrics
    summary = get_summary()
    analyst_df = get_analyst_performance()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🏫 Universities", len(UNIVERSITIES))
    with col2:
        st.metric("👥 Data Analysts", len(analyst_df))
    with col3:
        total_completed = summary["Completed"].sum() if not summary.empty else 0
        st.metric("✅ Total Tasks Completed", total_completed)
    with col4:
        avg_progress = analyst_df["progress"].mean() if not analyst_df.empty else 0
        st.metric("📈 Avg Analyst Progress", f"{avg_progress:.1f}%")
    
    st.markdown("---")
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Progress Overview", "👥 Team Performance", "📋 Activity Monitor", "📄 Reports"])
    
    with tab1:
        # University progress chart
        fig = px.bar(summary, x="University", y="Completed", title="University-wise Progress", text="Completed", color="University")
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True)
        
        # Overall progress gauge
        total_planned = len(DEFAULT_PLAN) * len(UNIVERSITIES)
        overall_progress = (total_completed / total_planned * 100) if total_planned > 0 else 0
        st.subheader(f"Overall Project Progress: {overall_progress:.1f}%")
        st.progress(overall_progress / 100)
    
    with tab2:
        st.subheader("Data Analyst Performance")
        
        # Search filter
        search = st.text_input("Search Analyst", "")
        filtered_df = analyst_df[analyst_df["name"].str.contains(search, case=False)] if search else analyst_df
        
        for _, row in filtered_df.iterrows():
            with st.expander(f"{row['avatar']} {row['name']} - {row['university']} ({row['progress']}% complete)"):
                st.progress(row['progress']/100)
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Tasks Completed", f"{row['completed']}/{row['total']}")
                with col2:
                    st.metric("Last Activity", row['last_activity'][:16] if row['last_activity'] != 'No activity' else "No activity")
                
                if row['recent_tasks']:
                    st.markdown("**Recent Tasks:**")
                    for date, task in row['recent_tasks']:
                        st.markdown(f"- {date}: {task}")
        
        # Leaderboard
        st.subheader("🏆 Analyst Leaderboard")
        leaderboard = analyst_df.nlargest(5, "progress")[["avatar", "name", "university", "progress", "completed"]]
        st.dataframe(leaderboard, use_container_width=True, hide_index=True)
    
    with tab3:
        st.subheader("Real-time Activity Monitor")
        
        # Auto-refresh option
        auto_refresh = st.checkbox("Auto-refresh (every 30 seconds)")
        if auto_refresh:
            time.sleep(30)
            st.rerun()
        
        daily_logs = load_daily_logs()
        recent_activities = []
        
        for uni_code, logs in daily_logs.items():
            uni_name = UNIVERSITIES.get(uni_code, {}).get("name", uni_code)
            for date, log in logs.items():
                recent_activities.append({
                    "Time": log.get("logged_at", "")[:16],
                    "Analyst": log.get("logged_by", "Unknown"),
                    "University": uni_name,
                    "Date": date,
                    "Task": log.get("task", "")[:60],
                    "Hours": log.get("hours", 0)
                })
        
        if recent_activities:
            df_activities = pd.DataFrame(recent_activities).sort_values("Time", ascending=False).head(20)
            st.dataframe(df_activities, use_container_width=True, hide_index=True)
        else:
            st.info("No recent activities")
    
    with tab4:
        st.subheader("Generate Reports")
        col1, col2 = st.columns(2)
        with col1:
            sel = st.selectbox("Select University", list(UNIVERSITIES.keys()), format_func=lambda x: UNIVERSITIES[x]["name"])
            if st.button("Generate University MPR"):
                html = generate_mpr_html(sel)
                st.markdown(get_download_link(html, f"MPR_{UNIVERSITIES[sel]['name'].replace(' ', '_')}.html"), unsafe_allow_html=True)
        with col2:
            if st.button("Generate Consolidated Report"):
                html = generate_consolidated_html()
                st.markdown(get_download_link(html, "Consolidated_Report.html"), unsafe_allow_html=True)


# ============================================================
# COORDINATOR DASHBOARD
# ============================================================

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
            
            remarks = st.text_area("Work Accomplished / Remarks", height=100, placeholder="Describe what you accomplished today...")
            
            if st.form_submit_button("✅ Submit Work Log", use_container_width=True, type="primary"):
                if remarks:
                    work_hours = f"{start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"
                    if log_work(code, selected_date, task["category"], task["task"], task["description"], hours, f"{work_hours} - {remarks}", name):
                        st.success("🎉 Work logged successfully!")
                        st.balloons()
                        time.sleep(1)
                        st.rerun()
                else:
                    st.error("Please describe your work accomplishments")
    else:
        st.success("🎉 All tasks completed! Great job!")
    
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
        st.markdown(f"**Total Working Days:** {len(DEFAULT_PLAN)}")
        
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
            project_lead_dashboard()
        else:
            st.title("ℹ️ About")
            st.markdown("**Project Lead Dashboard**\n- Monitor team performance\n- Generate reports\n- Track project progress")
    else:
        if uni and menu == "📋 My Tasks":
            coordinator_dashboard(uni, name)
        else:
            st.title("ℹ️ About")
            st.markdown("**Coordinator Dashboard**\n- Log daily work\n- Track your progress\n- 24-month project timeline")

if __name__ == "__main__":
    main()
