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
    "MU": {"name": "Mumbai University", "coordinators": ["Ms Sneha", "Mr Sagar"], "nodal_officer": "Dr. Varsha Kelkar Mane", "registrar": "_________", "vc": "_________"},
    "SSPU": {"name": "Savitribai Phule Pune University", "coordinators": ["Mr Jagan"], "nodal_officer": "Prof. Vinayak Joshi", "registrar": "_________", "vc": "_________"},
    "COEP": {"name": "COEP Technological University, Pune", "coordinators": ["Mr Vaibhav"], "nodal_officer": "Dr. Uttam Chaskar", "registrar": "_________", "vc": "_________"},
    "AU": {"name": "Sant Gadge Baba Amravati University", "coordinators": ["Mr Pratham"], "nodal_officer": "Dr. A. B. Naik", "registrar": "_________", "vc": "_________"},
    "NU": {"name": "Rashtrasant Tukadoji Maharaj Nagpur University", "coordinators": ["Ms Anjali"], "nodal_officer": "Prof. Nandkishor Karade", "registrar": "_________", "vc": "_________"},
    "KBCNMU": {"name": "KBCNMU, Jalgaon", "coordinators": ["Mr Nitish"], "nodal_officer": "Prof. Sameer Narkhede", "registrar": "_________", "vc": "_________"},
    "BAMU": {"name": "Dr. Babasaheb Ambedkar Marathwada University, Aurangabad", "coordinators": ["Mr Atharv"], "nodal_officer": "Prof. G.D. Khedkar", "registrar": "_________", "vc": "_________"},
    "MITRA": {"name": "MITRA (PMU)", "coordinators": ["Shubham"], "nodal_officer": "Dr. Harshal Kotwal", "registrar": "_________", "vc": "_________"}
}

# MITRA Officials
MITRA_OFFICIALS = {
    "project_director": "Dr. Harshal Kotwal, Project Director, MahaSTRIDE",
    "jt_ceo": "Jt. CEO, MITRA"
}

# ICARE Officials
ICARE_OFFICIALS = {
    "project_head": "Shri Karthick Sridhar, Project Head, ICARE Pvt. Ltd."
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

# ============================================================
# DATA FILE PATHS
# ============================================================
PROGRESS_DATA_FILE = "coordinator_progress_data.json"
TEAM_ATTENDANCE_FILE = "team_attendance.json"
MPR_DATA_FILE = "mpr_data.json"

# ============================================================
# DEFAULT PLAN - 19 WORKING DAYS (May 4-29, 2026)
# ============================================================
DEFAULT_PLAN = {
    "2026-05-04": {"task_category": "Training", "task": "SANGAM Orientation Day 1", "description": "Joint session at Trident Board Room, Mumbai. Project overview, MahaSTRIDE introduction, roles & responsibilities.", "deliverables": "Orientation completion certificate", "framework": "Training", "venue": "Trident Board Room, Mumbai"},
    "2026-05-05": {"task_category": "Training", "task": "SANGAM Training Day 2", "description": "Joint session at Trident Board Room, Mumbai. NIRF framework deep dive: TLR, RP, GO, OI parameters.", "deliverables": "Training materials", "framework": "Training", "venue": "Trident Board Room, Mumbai"},
    "2026-05-06": {"task_category": "Training", "task": "SANGAM Workshop Day 3", "description": "Joint session at Trident Board Room, Mumbai. GRDAU concept, hands-on data collection templates.", "deliverables": "GRDAU framework draft", "framework": "Training", "venue": "Trident Board Room, Mumbai"},
    "2026-05-07": {"task_category": "Setup", "task": "University Reporting & Onboarding", "description": "Report to university. Meet VC, Registrar, Nodal Officer. Confirm workspace and data access.", "deliverables": "Onboarding report", "framework": "Setup", "venue": "Respective University"},
    "2026-05-08": {"task_category": "Setup", "task": "NIRF Data Source Mapping", "description": "Map all NIRF-related data sources across university departments.", "deliverables": "Data source map", "framework": "Setup", "venue": "Respective University"},
    "2026-05-11": {"task_category": "Documentation", "task": "Data Gap Template & Request Letters", "description": "Create NIRF Data Gap Template. Prepare department-wise data request letters.", "deliverables": "Gap template", "framework": "Setup", "venue": "Respective University"},
    "2026-05-12": {"task_category": "Data Collection", "task": "Student & Faculty Data Collection", "description": "Collect student enrollment, graduation data and faculty details.", "deliverables": "Student and faculty data files", "framework": "Data Collection", "venue": "Respective University"},
    "2026-05-13": {"task_category": "Data Collection", "task": "Research & Placement Data Collection", "description": "Collect research publications, citations, patents and placement statistics.", "deliverables": "Research and placement data", "framework": "Data Collection", "venue": "Respective University"},
    "2026-05-14": {"task_category": "Data Collection", "task": "Financial & Infrastructure Data", "description": "Collect financial records, library resources, IT infrastructure.", "deliverables": "Financial and infrastructure data", "framework": "Data Collection", "venue": "Respective University"},
    "2026-05-15": {"task_category": "Analysis", "task": "Data Consolidation & Validation", "description": "Consolidate collected data. Cross-verify with source documents.", "deliverables": "Consolidated dataset v1", "framework": "Analysis", "venue": "Respective University"},
    "2026-05-18": {"task_category": "Meetings", "task": "Stakeholder Consultation Meeting", "description": "Conduct meeting with department heads to discuss data gaps.", "deliverables": "Meeting minutes", "framework": "Coordination", "venue": "Respective University"},
    "2026-05-19": {"task_category": "Data Collection", "task": "Missing Data Follow-up", "description": "Follow up with departments for missing data.", "deliverables": "Updated data files", "framework": "Data Collection", "venue": "Respective University"},
    "2026-05-20": {"task_category": "Analysis", "task": "NIRF Data Template Preparation", "description": "Prepare first draft of NIRF data template as per NIRF 2026 format.", "deliverables": "Draft NIRF submission", "framework": "Reporting", "venue": "Respective University"},
    "2026-05-21": {"task_category": "Documentation", "task": "SWOT Analysis & Gap Report", "description": "Prepare university-specific SWOT analysis and gap report.", "deliverables": "SWOT analysis report", "framework": "Reporting", "venue": "Respective University"},
    "2026-05-22": {"task_category": "Documentation", "task": "Inception Report Drafting", "description": "Draft Inception Report: deployment structure, methodology, timelines.", "deliverables": "Inception Report draft", "framework": "Reporting", "venue": "Respective University"},
    "2026-05-25": {"task_category": "Documentation", "task": "GRDAU Planning - Team Identification", "description": "Identify GRDAU team members. Define roles and responsibilities.", "deliverables": "GRDAU team structure", "framework": "Reporting", "venue": "Respective University"},
    "2026-05-26": {"task_category": "Documentation", "task": "GRDAU Operational Framework", "description": "Finalize GRDAU operational framework and KPIs.", "deliverables": "GRDAU framework", "framework": "Reporting", "venue": "Respective University"},
    "2026-05-27": {"task_category": "Meetings", "task": "Review Meeting with ICARE Team", "description": "Review May progress, data collection status, GRDAU readiness.", "deliverables": "Meeting minutes", "framework": "Coordination", "venue": "Respective University"},
    "2026-05-29": {"task_category": "Reporting", "task": "May MPR Finalization", "description": "Finalize May MPR as per SOP Annexure C. Compile deliverables.", "deliverables": "May MPR", "framework": "Reporting", "venue": "Respective University"}
}

TASK_CATEGORIES = {
    "Setup": ["University onboarding", "NIRF data source mapping"],
    "Training": ["SANGAM Orientation", "NIRF Framework training"],
    "Data Collection": ["Student data", "Faculty data", "Research data", "Placement data", "Financial data"],
    "Analysis": ["Data consolidation", "Data validation", "Gap analysis", "SWOT analysis"],
    "Reporting": ["NIRF template", "Inception Report", "GRDAU framework", "MPR preparation"],
    "Meetings": ["Stakeholder consultation", "Review meeting"],
    "Coordination": ["Department follow-up"]
}

# ============================================================
# TEAM MEMBERS - MITRA Level: Only Dr. Harshal Kotwal and Shubham
# ============================================================
TEAM_MEMBERS = {
    "MITRA": [
        {"name": "Dr. Harshal Kotwal", "profile": "Project Director, MahaSTRIDE", "location": "MITRA, Mumbai"},
        {"name": "Shubham", "profile": "Coordinator, MITRA", "location": "MITRA, Mumbai"}
    ],
    "MU": [
        {"name": "Ms Sneha", "profile": "Institutional Coordinator cum Research & Innovation Officer", "location": "Mumbai University"},
        {"name": "Mr Sagar", "profile": "Institutional Coordinator cum Research & Innovation Officer", "location": "Mumbai University"}
    ],
    "SSPU": [{"name": "Mr Jagan", "profile": "Institutional Coordinator cum Research & Innovation Officer", "location": "SPPU, Pune"}],
    "COEP": [{"name": "Mr Vaibhav", "profile": "Institutional Coordinator cum Research & Innovation Officer", "location": "COEP, Pune"}],
    "AU": [{"name": "Mr Pratham", "profile": "Institutional Coordinator cum Research & Innovation Officer", "location": "Amravati University"}],
    "NU": [{"name": "Ms Anjali", "profile": "Institutional Coordinator cum Research & Innovation Officer", "location": "Nagpur University"}],
    "KBCNMU": [{"name": "Mr Nitish", "profile": "Institutional Coordinator cum Research & Innovation Officer", "location": "KBCNMU, Jalgaon"}],
    "BAMU": [{"name": "Mr Atharv", "profile": "Institutional Coordinator cum Research & Innovation Officer", "location": "BAMU, Aurangabad"}]
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

def create_initial_progress_data():
    data = {}
    for uni_code in UNIVERSITIES.keys():
        data[uni_code] = {}
    return data

def create_initial_team_attendance():
    data = {}
    for uni_code in UNIVERSITIES.keys():
        data[uni_code] = {}
    data["MITRA"] = {}
    return data

def create_initial_mpr_data():
    return {"work_order_ref": "MITRA/Research/MahaSTRIDE/EduRFP/49/2025", "work_order_date": "11-05-2026", "period_start": "2026-05-04", "period_end": "2026-05-29"}

def load_progress_data():
    try:
        if os.path.exists(PROGRESS_DATA_FILE):
            with open(PROGRESS_DATA_FILE, 'r') as f:
                data = json.load(f)
                for uni_code in UNIVERSITIES.keys():
                    if uni_code not in data:
                        data[uni_code] = {}
                return data
        return create_initial_progress_data()
    except:
        return create_initial_progress_data()

def save_progress_data(data):
    try:
        with open(PROGRESS_DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except:
        return False

def load_team_attendance():
    try:
        if os.path.exists(TEAM_ATTENDANCE_FILE):
            with open(TEAM_ATTENDANCE_FILE, 'r') as f:
                return json.load(f)
        return create_initial_team_attendance()
    except:
        return create_initial_team_attendance()

def save_team_attendance(data):
    try:
        with open(TEAM_ATTENDANCE_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except:
        return False

def load_mpr_data():
    try:
        if os.path.exists(MPR_DATA_FILE):
            with open(MPR_DATA_FILE, 'r') as f:
                return json.load(f)
        return create_initial_mpr_data()
    except:
        return create_initial_mpr_data()

def save_mpr_data(data):
    try:
        with open(MPR_DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except:
        return False

def get_plan_for_date(date_str):
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
                pending_dates.append({"date": date, "task": plan.get("task", ""), "category": plan.get("task_category", ""), "description": plan.get("description", ""), "deliverables": plan.get("deliverables", ""), "venue": plan.get("venue", "")})
    return pending_dates

def log_daily_entry(university_code, date, task_category, task_name, description, deliverables, status, hours_spent, remarks, swapped, edited, updated_by):
    data = load_progress_data()
    if university_code not in data:
        data[university_code] = {}
    data[university_code][date] = {"date": date, "task_category": task_category, "task_name": task_name, "description": description, "deliverables": deliverables, "status": status, "hours_spent": hours_spent, "remarks": remarks, "swapped_from_default": swapped, "edited_task": edited, "updated_at": datetime.now().isoformat(), "updated_by": updated_by}
    return save_progress_data(data)

def mark_all_tasks_completed(university_code):
    data = load_progress_data()
    if university_code not in data:
        data[university_code] = {}
    for date, plan in DEFAULT_PLAN.items():
        data[university_code][date] = {
            "date": date, "task_category": plan.get("task_category", ""), "task_name": plan.get("task", ""),
            "description": plan.get("description", ""), "deliverables": plan.get("deliverables", ""),
            "status": "completed", "hours_spent": 8.0, "remarks": "Task completed as per plan",
            "swapped_from_default": False, "edited_task": False, "updated_at": datetime.now().isoformat(), "updated_by": "system"
        }
    return save_progress_data(data)

def get_university_entries(university_code):
    data = load_progress_data()
    if university_code not in data:
        return pd.DataFrame()
    records = []
    for date, entry in data[university_code].items():
        plan = get_plan_for_date(date)
        venue = plan.get("venue", "") if plan else ""
        records.append({"Date": date, "Venue": venue, "Task": entry.get("task_name", ""), "Status": entry.get("status", "").upper(), "Hours": entry.get("hours_spent", 0)})
    return pd.DataFrame(records).sort_values("Date")

def get_summary_stats():
    data = load_progress_data()
    stats = []
    for uni_code, uni_info in UNIVERSITIES.items():
        entries = data.get(uni_code, {})
        total_planned = len(get_all_planned_dates())
        completed = sum(1 for e in entries.values() if e.get("status") == "completed")
        stats.append({"University": uni_info["name"], "Completed": completed, "Total": total_planned, "Pending": total_planned - completed})
    return pd.DataFrame(stats)

def reset_all_data():
    for file in [PROGRESS_DATA_FILE, TEAM_ATTENDANCE_FILE, MPR_DATA_FILE]:
        if os.path.exists(file):
            os.remove(file)
    save_progress_data(create_initial_progress_data())
    save_team_attendance(create_initial_team_attendance())
    save_mpr_data(create_initial_mpr_data())
    return True

def initialize_all_data():
    for uni_code in UNIVERSITIES.keys():
        mark_all_tasks_completed(uni_code)
    attendance = load_team_attendance()
    for team_type, members in TEAM_MEMBERS.items():
        if team_type not in attendance:
            attendance[team_type] = {}
        for member in members:
            attendance[team_type][member["name"]] = {"present_days": 19, "absent_days": 0, "holidays": 12}
    save_team_attendance(attendance)
    return True

# ============================================================
# MPR GENERATION - EXACTLY AS PER SOP ANNEXURE C
# ============================================================

def generate_complete_mpr_html(university_code):
    uni_info = UNIVERSITIES[university_code]
    attendance_data = load_team_attendance()
    mpr_data = load_mpr_data()
    
    period_start = datetime.strptime(mpr_data.get("period_start", "2026-05-04"), "%Y-%m-%d")
    period_end = datetime.strptime(mpr_data.get("period_end", "2026-05-29"), "%Y-%m-%d")
    
    # Build Project Team Deployment table
    team_rows = ""
    sr_no = 1
    
    # MITRA LEVEL
    team_rows += '<tr class="sub-header"><td colspan="7"><strong>MITRA LEVEL</strong></td></tr>'
    for member in TEAM_MEMBERS.get("MITRA", []):
        att = attendance_data.get("MITRA", {}).get(member["name"], {})
        present = att.get('present_days', 19)
        absent = att.get('absent_days', 0)
        holidays = att.get('holidays', 12)
        team_rows += f"""
        <tr>
            <td>{sr_no}</td>
            <td>{member['name']}</td>
            <td>{member['profile']}</td>
            <td>{member['location']}</td>
            <td>{present}</div>
     </div>
    </body>
    </html>"""
    return html

def get_html_download_link(html_content, filename):
    b64 = base64.b64encode(html_content.encode()).decode()
    return f'<a href="data:text/html;base64,{b64}" download="{filename}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">📥 Download {filename}</a>'

def show_sangam_info():
    st.markdown('<div class="sangam-card">', unsafe_allow_html=True)
    st.markdown("### 🎉 SANGAM Orientation & Training Program")
    st.markdown("**Dates:** May 4-6, 2026 | **Venue:** Trident Board Room, Mumbai | ✅ **Status:** Completed")
    st.markdown('</div>', unsafe_allow_html=True)

def show_credentials():
    st.markdown("""
    <div class="credentials-box">
        <h4>🔐 Demo Credentials (Password: <strong>Name@2026</strong> for all)</h4>
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

def create_admin_dashboard():
    st.markdown('<div class="admin-card"><h2>📊 Admin Dashboard</h2><p>Complete Project Analytics & Reports</p></div>', unsafe_allow_html=True)
    st.markdown('<span class="storage-status storage-connected">✅ Persistent Storage Active</span>', unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 🗑️ Data Management")
        if st.button("🔄 Reset All Data (Start Fresh)", use_container_width=True):
            if reset_all_data():
                st.success("✅ All data has been reset!")
                st.rerun()
        if st.button("📋 Mark ALL Tasks as COMPLETED", use_container_width=True):
            initialize_all_data()
            st.success("✅ All tasks marked completed with 100% attendance!")
            st.rerun()
    
    show_sangam_info()
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    total_unis = len(UNIVERSITIES)
    total_planned = len(get_all_planned_dates()) * total_unis
    summary_df = get_summary_stats()
    total_completed = summary_df["Completed"].sum() if not summary_df.empty else 0
    
    with col1: st.metric("Working Days", "19 (May 4-29)")
    with col2: st.metric("Universities", f"{total_unis}")
    with col3: st.metric("Total Tasks", total_planned)
    with col4: st.metric("Tasks Completed", total_completed)
    
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["📊 Progress Overview", "🏛️ University Details", "📄 Generate Reports"])
    
    with tab1:
        summary_df = get_summary_stats()
        if not summary_df.empty:
            fig = px.bar(summary_df, x="University", y="Completed", title="University-wise Tasks Completed", color="Completed", text="Completed", height=500)
            fig.update_traces(texttemplate='%{text}', textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
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
        st.markdown("### Individual University Report")
        selected_uni = st.selectbox("Select University", list(UNIVERSITIES.keys()), format_func=lambda x: UNIVERSITIES[x]["name"], key="report_uni")
        if st.button("Generate University MPR", use_container_width=True):
            with st.spinner("Generating MPR..."):
                html_content = generate_complete_mpr_html(selected_uni)
                st.markdown(get_html_download_link(html_content, f"MPR_{UNIVERSITIES[selected_uni]['name'].replace(' ', '_')}_May2026.html"), unsafe_allow_html=True)
                st.success("MPR generated!")
        
        st.markdown("---")
        st.markdown("### Consolidated Report (All Universities)")
        if st.button("Generate Consolidated MPR", use_container_width=True):
            with st.spinner("Generating consolidated MPR..."):
                html_content = generate_consolidated_mpr_html()
                st.markdown(get_html_download_link(html_content, "Consolidated_MPR_All_Universities_May2026.html"), unsafe_allow_html=True)
                st.success("Consolidated MPR generated!")

def create_project_lead_dashboard():
    st.markdown('<div class="projectlead-card"><h2>👨‍💼 Project Lead Dashboard - Dr. Harshal Kotwal</h2><p>Generate Reports</p></div>', unsafe_allow_html=True)
    show_sangam_info()
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["📝 MPR Settings", "📄 Reports"])
    
    with tab1:
        st.subheader("MPR Header Information")
        mpr_data = load_mpr_data()
        col1, col2 = st.columns(2)
        with col1:
            work_order_ref = st.text_input("Work Order Reference", value=mpr_data.get("work_order_ref", "MITRA/Research/MahaSTRIDE/EduRFP/49/2025"))
            period_start = st.date_input("Period Start", value=datetime.strptime(mpr_data.get("period_start", "2026-05-04"), "%Y-%m-%d").date())
        with col2:
            work_order_date = st.text_input("Work Order Date", value=mpr_data.get("work_order_date", "11-05-2026"))
            period_end = st.date_input("Period End", value=datetime.strptime(mpr_data.get("period_end", "2026-05-29"), "%Y-%m-%d").date())
        if st.button("Save MPR Settings", use_container_width=True):
            mpr_data["work_order_ref"] = work_order_ref
            mpr_data["work_order_date"] = work_order_date
            mpr_data["period_start"] = period_start.strftime("%Y-%m-%d")
            mpr_data["period_end"] = period_end.strftime("%Y-%m-%d")
            save_mpr_data(mpr_data)
            st.success("MPR settings saved!")
    
    with tab2:
        st.subheader("📄 Generate Reports")
        col1, col2 = st.columns(2)
        with col1:
            selected_uni = st.selectbox("Select University", list(UNIVERSITIES.keys()), format_func=lambda x: UNIVERSITIES[x]["name"])
            if st.button("Generate University MPR", use_container_width=True):
                html_content = generate_complete_mpr_html(selected_uni)
                st.markdown(get_html_download_link(html_content, f"MPR_{UNIVERSITIES[selected_uni]['name'].replace(' ', '_')}_May2026.html"), unsafe_allow_html=True)
        with col2:
            if st.button("Generate Consolidated MPR", use_container_width=True):
                html_content = generate_consolidated_mpr_html()
                st.markdown(get_html_download_link(html_content, "Consolidated_MPR_All_Universities_May2026.html"), unsafe_allow_html=True)

def create_coordinator_dashboard(university_code, coordinator_name):
    st.markdown('<div class="info-card"><h2>📋 Coordinator Dashboard</h2><p>Log Your Daily Work</p></div>', unsafe_allow_html=True)
    uni_info = UNIVERSITIES[university_code]
    st.markdown(f"**🏛️ University:** {uni_info['name']} | **👤 Coordinator:** {coordinator_name} | **📌 Nodal Officer:** {uni_info['nodal_officer']}")
    st.info(f"⏰ **Working Hours:** {WORKING_HOURS}")
    
    pending_tasks = get_pending_tasks_for_coordinator(university_code)
    completed_entries = get_university_entries(university_code)
    total_planned = len(get_all_planned_dates())
    completed_count = len(completed_entries)
    
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("📋 Total Tasks", total_planned)
    with col2: st.metric("✅ Completed", completed_count)
    with col3: st.metric("⏳ Pending", total_planned - completed_count)
    
    progress_value = completed_count / total_planned if total_planned > 0 else 0
    progress_value = max(0.0, min(1.0, progress_value))
    st.progress(progress_value)
    
    if pending_tasks:
        st.subheader("📋 YOUR PENDING TASKS")
        selected_date_str = st.selectbox("Select Date to Log Work", [task["date"] for task in pending_tasks])
        if selected_date_str:
            selected_task = next((t for t in pending_tasks if t["date"] == selected_date_str), None)
            if selected_task:
                st.markdown(f"""
                <div class="default-task-card">
                    <strong>📋 {selected_task['date']}</strong><br>
                    <strong>📍 Venue:</strong> {selected_task['venue']}<br>
                    <strong>🎯 Task:</strong> {selected_task['task']}<br>
                    <strong>📝 Description:</strong> {selected_task['description']}
                </div>
                """, unsafe_allow_html=True)
                
                with st.form("log_task_form"):
                    use_planned = st.radio("Complete planned task?", ["✅ Yes", "🔄 No"], horizontal=True)
                    if use_planned == "✅ Yes":
                        task_category, task_name, description, deliverables = selected_task['category'], selected_task['task'], selected_task['description'], selected_task['deliverables']
                    else:
                        task_category = st.selectbox("Category", list(TASK_CATEGORIES.keys()))
                        task_name = st.text_input("Task")
                        description = st.text_area("Description")
                        deliverables = st.text_area("Deliverables")
                    
                    hours = st.number_input("Hours Spent", 0.5, 12.0, 8.0)
                    remarks = st.text_area("Remarks")
                    
                    if st.form_submit_button("✅ Submit"):
                        if log_daily_entry(university_code, selected_task['date'], task_category, task_name, description, deliverables, "completed", hours, remarks, use_planned != "✅ Yes", use_planned != "✅ Yes", coordinator_name):
                            st.success("Logged!")
                            st.rerun()
    else:
        st.success("🎉 All tasks completed!")

def generate_consolidated_mpr_html():
    """Generate consolidated MPR for all universities"""
    summary_df = get_summary_stats()
    attendance_data = load_team_attendance()
    mpr_data = load_mpr_data()
    
    total_planned = len(get_all_planned_dates()) * len(UNIVERSITIES)
    total_completed = summary_df["Completed"].sum() if not summary_df.empty else 0
    
    period_start = datetime.strptime(mpr_data.get("period_start", "2026-05-04"), "%Y-%m-%d")
    period_end = datetime.strptime(mpr_data.get("period_end", "2026-05-29"), "%Y-%m-%d")
    
    if total_completed == total_planned:
        overall_status = "✅ Fully Completed"
    elif total_completed >= total_planned * 0.75:
        overall_status = "🟢 Substantially Complete"
    elif total_completed >= total_planned * 0.5:
        overall_status = "🟡 In Progress"
    elif total_completed >= total_planned * 0.25:
        overall_status = "🔵 Initiated"
    else:
        overall_status = "⚪ Not Started"
    
    # Build consolidated team deployment table
    team_rows = ""
    sr_no = 1
    
    # MITRA LEVEL
    team_rows += '<tr class="sub-header"><td colspan="7"><strong>MITRA LEVEL</strong></td></tr>'
    for member in TEAM_MEMBERS.get("MITRA", []):
        att = attendance_data.get("MITRA", {}).get(member["name"], {})
        present = att.get('present_days', 19)
        absent = att.get('absent_days', 0)
        holidays = att.get('holidays', 12)
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
    
    # All Universities
    for uni_code, uni_info in UNIVERSITIES.items():
        if uni_code != "MITRA":
            team_rows += f'<tr class="sub-header"><td colspan="7"><strong>{uni_info["name"]}</strong></td></tr>'
            for member in TEAM_MEMBERS.get(uni_code, []):
                att = attendance_data.get(uni_code, {}).get(member["name"], {})
                present = att.get('present_days', 19)
                absent = att.get('absent_days', 0)
                holidays = att.get('holidays', 12)
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
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Consolidated Monthly Progress Report - All Universities</title>
    <style>
        body {{
            font-family: 'Times New Roman', serif;
            margin: 0.7in;
            font-size: 11pt;
            line-height: 1.2;
        }}
        .header {{
            text-align: center;
            margin-bottom: 20px;
        }}
        .mitra-title {{
            font-size: 12pt;
            font-weight: bold;
        }}
        .confidential {{
            text-align: right;
            font-weight: bold;
            margin-bottom: 20px;
            font-size: 10pt;
        }}
        .report-title {{
            font-size: 14pt;
            font-weight: bold;
            text-align: center;
            margin: 15px 0;
        }}
        .section-title {{
            font-size: 12pt;
            font-weight: bold;
            margin-top: 15px;
            margin-bottom: 8px;
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
        .sub-header {{
            background-color: #d0d0d0;
            font-weight: bold;
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
    <div style="text-align: center;">Reporting Period: {period_start.strftime('%d-%m-%Y')} to {period_end.strftime('%d-%m-%Y')}</div>

    <div class="section-title">Overall Project Progress</div>
    <div style="margin: 10px 0;">
        <strong>Overall Status: {overall_status}</strong><br>
        <strong>Tasks Completed:</strong> {total_completed} / {total_planned}<br>
        <strong>Working Days:</strong> 19 days (May 4-29, 2026, excluding weekends & holidays)
    </div>

    <div class="section-title">Project Team Deployment</div>
    <table>
        <tr>
            <th>Sr. No.</th>
            <th>Name of the Key Professional</th>
            <th>Profile as per contract</th>
            <th>Location</th>
            <th>Present Days</th>
            <th>Absent Days</th>
            <th>Holidays</th>
        </tr>
        {team_rows}
    </table>

    <div class="section-title">University-wise Progress Summary</div>
    <table>
        <tr>
            <th>Sr. No.</th>
            <th>University</th>
            <th>Tasks Completed</th>
            <th>Total Tasks</th>
            <th>Status</th>
        </tr>"""
    
    for i, (_, row) in enumerate(summary_df.iterrows()):
        status = "✅ Completed" if row["Completed"] == row["Total"] else "🟡 In Progress"
        html += f"""
        <tr>
            <td>{i+1}</td>
            <td>{row['University']}</td>
            <td>{row['Completed']}</td>
            <td>{row['Total']}</td>
            <td>{status}</td>
        </tr>"""
    
    html += f"""
    </table>

    <div class="section-title">Training Programs Conducted (May 4-6, 2026 at Trident Board Room, Mumbai)</div>
    <table>
        <tr><th>Date</th><th>Program</th><th>Participants</th><th>Status</th></tr>
        <tr><td>May 4, 2026</div>
     </div>
    </body>
    </html>"""
    return html

def main():
    # Initialize data on first run
    if not os.path.exists(PROGRESS_DATA_FILE):
        initialize_all_data()
    
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    
    if not st.session_state["authenticated"]:
        with st.container():
            st.markdown('<div class="main-header"><h1>🔐 mahaSTRIDE NIRF Data Collection Tracker</h1><p>Phase 1: May 4-29, 2026 (19 Working Days)</p></div>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.markdown("### Login")
                email = st.text_input("Email", placeholder="Enter your registered email")
                password = st.text_input("Password", type="password", placeholder="Enter password")
                
                if st.button("Login", type="primary", use_container_width=True):
                    if email and password:
                        success, role, name, university = authenticate_user(email, password)
                        if success:
                            st.session_state["authenticated"] = True
                            st.session_state["user_role"] = role
                            st.session_state["user_name"] = name
                            if university:
                                st.session_state["user_university"] = university
                            st.rerun()
                        else:
                            st.error("❌ Invalid email or password")
                    else:
                        st.warning("⚠️ Please enter both email and password")
                
                st.markdown("---")
                show_credentials()
        return
    
    # Main app after login
    role = st.session_state["user_role"]
    name = st.session_state["user_name"]
    university = st.session_state.get("user_university")
    
    with st.sidebar:
        st.title("📊 mahaSTRIDE")
        st.markdown(f"**Welcome, {name}**")
        st.markdown(f"**Today:** {datetime.now().strftime('%d-%b-%Y')}")
        st.markdown("**Phase 1:** May 4-29, 2026")
        st.markdown("---")
        
        if role == "admin":
            menu = st.radio("Navigation", ["📊 Admin Dashboard", "ℹ️ About"])
        elif role == "project_lead":
            menu = st.radio("Navigation", ["👨‍💼 Project Lead Dashboard", "ℹ️ About"])
        else:
            menu = st.radio("Navigation", ["📋 My Tasks", "📊 My Progress", "ℹ️ About"])
        
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            for key in ["authenticated", "user_role", "user_name", "user_university"]:
                st.session_state.pop(key, None)
            st.rerun()
    
    if role == "admin":
        if menu == "📊 Admin Dashboard":
            create_admin_dashboard()
        else:
            st.title("ℹ️ About mahaSTRIDE")
            st.markdown("""
            ### Project Overview
            
            **mahaSTRIDE** is Maharashtra's flagship project for improving university rankings.
            
            **May 2026 Working Schedule (19 Days):**
            - May 4-6: SANGAM Training at Trident Board Room, Mumbai
            - May 7-29: Work at respective universities (19 working days)
            
            **Key Deliverables:**
            1. Inception Report (Due: June 6, 2026)
            2. GRDAUs Establishment (Due: July 6, 2026)
            3. Monthly Progress Report (Due: 10th of each month)
            """)
    
    elif role == "project_lead":
        if menu == "👨‍💼 Project Lead Dashboard":
            create_project_lead_dashboard()
        else:
            st.title("ℹ️ Project Lead Dashboard")
            st.markdown("""
            **Your Responsibilities:**
            1. Configure MPR header information
            2. Generate MPR reports for all universities
            
            **The MPR includes:**
            - Project Team Deployment table
            - Major Activities section
            - Minutes of Meetings
            - Major Deliverables status
            - Risk Management
            - Status of Initiatives
            - Approvals and Signatures
            """)
    
    else:
        if university:
            if menu == "📋 My Tasks":
                create_coordinator_dashboard(university, name)
            elif menu == "📊 My Progress":
                st.title("📊 My Progress")
                df = get_university_entries(university)
                if not df.empty:
                    st.dataframe(df, use_container_width=True)
                    completed = len(df[df["Status"] == "COMPLETED"])
                    total = len(get_all_planned_dates())
                    st.metric("Completed Tasks", f"{completed}/{total}")
                else:
                    st.info("No entries logged yet")
            else:
                st.title("ℹ️ Coordinator Dashboard")
                st.markdown("""
                **How to Log Work:**
                1. Select a date from pending tasks
                2. Confirm if you completed the planned task
                3. Add hours spent and submit
                
                **May 2026 Schedule:**
                - May 4-6: SANGAM Training at Trident Board Room, Mumbai
                - May 7-29: Work at respective universities
                """)
        else:
            st.error("University not assigned. Please contact admin.")

if __name__ == "__main__":
    main()
