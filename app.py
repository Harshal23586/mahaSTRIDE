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
    .default-task-card {
        background: linear-gradient(135deg, #e8f8f5 0%, #d4efdf 100%);
        border-left: 4px solid #27ae60;
        padding: 1.2rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .training-badge {
        background-color: #17a2b8;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        display: inline-block;
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

MITRA_OFFICIALS = {"project_director": "Dr. Harshal Kotwal, Project Director, MahaSTRIDE", "jt_ceo": "Jt. CEO, MITRA"}
ICARE_OFFICIALS = {"project_head": "Shri Karthick Sridhar, Project Head, ICARE Pvt. Ltd."}

WORKING_HOURS = "10:00 AM - 6:00 PM"

# ============================================================
# DEFAULT PLAN - 19 WORKING DAYS (May 4-29, 2026)
# May 4,5,6: SANGAM at Trident Board Room, Mumbai (ALL TOGETHER)
# May 7,8,11,12,13,14,15,18,19,20,21,22,25,26,27,29: University work
# ============================================================

DEFAULT_PLAN = {
    # SANGAM at Trident Board Room (May 4-6)
    "2026-05-04": {"task_category": "Training", "task": "SANGAM Orientation Day 1", "description": "Joint session at Trident Board Room. Project overview, MahaSTRIDE introduction, roles & responsibilities.", "deliverables": "Orientation completion certificate", "venue": "Trident Board Room, Mumbai"},
    "2026-05-05": {"task_category": "Training", "task": "SANGAM Training Day 2", "description": "Joint session at Trident Board Room. NIRF framework deep dive: TLR, RP, GO, OI parameters.", "deliverables": "Training materials", "venue": "Trident Board Room, Mumbai"},
    "2026-05-06": {"task_category": "Training", "task": "SANGAM Workshop Day 3", "description": "Joint session at Trident Board Room. GRDAU concept, hands-on data collection templates.", "deliverables": "GRDAU framework draft", "venue": "Trident Board Room, Mumbai"},
    # University Reporting (May 7-29)
    "2026-05-07": {"task_category": "Setup", "task": "University Reporting & Onboarding", "description": "Report to university. Meet VC, Registrar, Nodal Officer. Confirm workspace and data access.", "deliverables": "Onboarding report", "venue": "Respective University"},
    "2026-05-08": {"task_category": "Setup", "task": "NIRF Data Source Mapping", "description": "Map all NIRF-related data sources across university departments.", "deliverables": "Data source map", "venue": "Respective University"},
    "2026-05-11": {"task_category": "Documentation", "task": "Data Gap Template & Request Letters", "description": "Create NIRF Data Gap Template. Prepare department-wise data request letters.", "deliverables": "Gap template", "venue": "Respective University"},
    "2026-05-12": {"task_category": "Data Collection", "task": "Student & Faculty Data Collection", "description": "Collect student enrollment, graduation data and faculty details.", "deliverables": "Student and faculty data files", "venue": "Respective University"},
    "2026-05-13": {"task_category": "Data Collection", "task": "Research & Placement Data Collection", "description": "Collect research publications, citations, patents and placement statistics.", "deliverables": "Research and placement data", "venue": "Respective University"},
    "2026-05-14": {"task_category": "Data Collection", "task": "Financial & Infrastructure Data", "description": "Collect financial records, library resources, IT infrastructure.", "deliverables": "Financial and infrastructure data", "venue": "Respective University"},
    "2026-05-15": {"task_category": "Analysis", "task": "Data Consolidation & Validation", "description": "Consolidate collected data. Cross-verify with source documents.", "deliverables": "Consolidated dataset v1", "venue": "Respective University"},
    "2026-05-18": {"task_category": "Meetings", "task": "Stakeholder Consultation Meeting", "description": "Conduct meeting with department heads to discuss data gaps.", "deliverables": "Meeting minutes", "venue": "Respective University"},
    "2026-05-19": {"task_category": "Data Collection", "task": "Missing Data Follow-up", "description": "Follow up with departments for missing data.", "deliverables": "Updated data files", "venue": "Respective University"},
    "2026-05-20": {"task_category": "Analysis", "task": "NIRF Data Template Preparation", "description": "Prepare first draft of NIRF data template as per NIRF 2026 format.", "deliverables": "Draft NIRF submission", "venue": "Respective University"},
    "2026-05-21": {"task_category": "Documentation", "task": "SWOT Analysis & Gap Report", "description": "Prepare university-specific SWOT analysis and gap report.", "deliverables": "SWOT analysis report", "venue": "Respective University"},
    "2026-05-22": {"task_category": "WFH", "task": "Inception Report Drafting", "description": "Draft Inception Report: deployment structure, methodology, timelines.", "deliverables": "Inception Report draft", "venue": "Work From Home"},
    "2026-05-25": {"task_category": "Documentation", "task": "GRDAU Planning - Team Identification", "description": "Identify GRDAU team members. Define roles and responsibilities.", "deliverables": "GRDAU team structure", "venue": "Respective University"},
    "2026-05-26": {"task_category": "Documentation", "task": "GRDAU Operational Framework", "description": "Finalize GRDAU operational framework and KPIs.", "deliverables": "GRDAU framework", "venue": "Respective University"},
    "2026-05-27": {"task_category": "Meetings", "task": "Review Meeting with ICARE Team", "description": "Review May progress, data collection status, GRDAU readiness.", "deliverables": "Meeting minutes", "venue": "Respective University"},
    "2026-05-29": {"task_category": "Reporting", "task": "May MPR Finalization", "description": "Finalize May MPR as per SOP Annexure C. Compile deliverables.", "deliverables": "May MPR", "venue": "Respective University"}
}

TASK_CATEGORIES = {
    "Setup": ["University onboarding", "NIRF data source mapping"],
    "Training": ["SANGAM Orientation", "NIRF Framework training"],
    "Data Collection": ["Student data", "Faculty data", "Research data", "Placement data", "Financial data"],
    "Analysis": ["Data consolidation", "Data validation", "Gap analysis", "SWOT analysis"],
    "Reporting": ["NIRF template", "MPR preparation", "Inception Report", "GRDAU framework"],
    "Meetings": ["Stakeholder consultation", "Review meeting"],
    "WFH": ["Report compilation"],
    "Coordination": ["Department follow-up"]
}

TEAM_MEMBERS = {
    "MITRA": [
        {"name": "Dr. Harshal Kotwal", "profile": "Project Director", "location": "MITRA"},
        {"name": "Shubham", "profile": "Coordinator, MITRA", "location": "MITRA"},
        {"name": "Shri Karthick Sridhar", "profile": "Project Head, ICARE", "location": "MITRA"}
    ],
    "MU": [{"name": "Ms Sneha", "profile": "Coordinator", "location": "Mumbai University"}, {"name": "Mr Sagar", "profile": "Coordinator", "location": "Mumbai University"}],
    "SSPU": [{"name": "Mr Jagan", "profile": "Coordinator", "location": "SPPU"}],
    "COEP": [{"name": "Mr Vaibhav", "profile": "Coordinator", "location": "COEP"}],
    "AU": [{"name": "Mr Pratham", "profile": "Coordinator", "location": "Amravati University"}],
    "NU": [{"name": "Ms Anjali", "profile": "Coordinator", "location": "Nagpur University"}],
    "KBCNMU": [{"name": "Mr Nitish", "profile": "Coordinator", "location": "KBCNMU"}],
    "BAMU": [{"name": "Mr Atharv", "profile": "Coordinator", "location": "BAMU"}]
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

PROGRESS_FILE = "progress_data.json"

def load_data():
    try:
        if os.path.exists(PROGRESS_FILE):
            with open(PROGRESS_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return {}

def save_data(data):
    try:
        with open(PROGRESS_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except:
        return False

def get_plan_for_date(date):
    return DEFAULT_PLAN.get(date)

def get_all_dates():
    return list(DEFAULT_PLAN.keys())

def get_pending_tasks(university):
    data = load_data()
    completed = set(data.get(university, {}).keys())
    pending = []
    for date in get_all_dates():
        if date not in completed:
            plan = get_plan_for_date(date)
            if plan:
                pending.append({"date": date, "task": plan["task"], "category": plan["task_category"], 
                               "description": plan["description"], "deliverables": plan["deliverables"], "venue": plan.get("venue", "")})
    return pending

def log_task(university, date, category, task, desc, deliverables, status, hours, remarks, updated_by):
    data = load_data()
    if university not in data:
        data[university] = {}
    data[university][date] = {"category": category, "task": task, "description": desc, "deliverables": deliverables,
                              "status": status, "hours": hours, "remarks": remarks, "updated_by": updated_by, 
                              "updated_at": datetime.now().isoformat()}
    return save_data(data)

def mark_all_completed(university):
    data = load_data()
    if university not in data:
        data[university] = {}
    for date, plan in DEFAULT_PLAN.items():
        data[university][date] = {"category": plan["task_category"], "task": plan["task"], 
                                  "description": plan["description"], "deliverables": plan["deliverables"],
                                  "status": "completed", "hours": 8.0, "remarks": "Completed as per plan",
                                  "updated_by": "system", "updated_at": datetime.now().isoformat()}
    return save_data(data)

def get_entries(university):
    data = load_data()
    if university not in data:
        return pd.DataFrame()
    records = []
    for date, entry in data[university].items():
        plan = get_plan_for_date(date)
        venue = plan.get("venue", "") if plan else ""
        records.append({"Date": date, "Venue": venue, "Task": entry.get("task", ""), "Category": entry.get("category", ""),
                       "Status": entry.get("status", "").upper(), "Hours": entry.get("hours", 0), "Updated By": entry.get("updated_by", "")})
    return pd.DataFrame(records).sort_values("Date")

def get_summary():
    data = load_data()
    stats = []
    for code, info in UNIVERSITIES.items():
        entries = data.get(code, {})
        total = len(DEFAULT_PLAN)
        completed = sum(1 for e in entries.values() if e.get("status") == "completed")
        stats.append({"University": info["name"], "Completed": completed, "Total": total, 
                     "Pending": total - completed, "Status": "✅ Completed" if completed == total else "🟡 In Progress"})
    return pd.DataFrame(stats)

def generate_mpr_html(university):
    info = UNIVERSITIES[university]
    entries = get_entries(university)
    period_start = datetime(2026, 5, 4)
    period_end = datetime(2026, 5, 29)
    completed = len(entries) if not entries.empty else 0
    total = len(DEFAULT_PLAN)
    
    html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>MPR - {info['name']}</title>
<style>body {{ font-family: 'Times New Roman', margin: 0.7in; }} .header {{ text-align: center; }} .report-title {{ font-size: 14pt; font-weight: bold; text-align: center; }} table {{ width: 100%; border-collapse: collapse; }} th, td {{ border: 1px solid #000; padding: 5px; }} th {{ background: #e8e8e8; }}</style></head>
<body>
<div class="header"><h2>Maharashtra Institution for Transformation (MITRA)</h2><p>5th Floor, Nirmal, Nariman Point, Mumbai-400021</p></div>
<div class="report-title">MONTHLY PROGRESS REPORT</div>
<p style="text-align:center">From {period_start.strftime('%d-%m-%Y')} to {period_end.strftime('%d-%m-%Y')}</p>
<table><tr><td><strong>Work Order:</strong> MITRA/Research/MahaSTRIDE/EduRFP/49/2025</td><td><strong>University:</strong> {info['name']}</td></tr></table>
<h3>Project Team Deployment</h3>
<table><tr><th>Name</th><th>Profile</th><th>Present</th><th>Absent</th><th>Holidays</th></tr>"""
    for m in TEAM_MEMBERS.get(university, []) + TEAM_MEMBERS.get("MITRA", []):
        html += f"<tr><td>{m['name']}</td><td>{m['profile']}</td><td>19</td><td>0</td><td>12</td></tr>"
    html += f"""</table>
<h3>A. Major Activities</h3><table><tr><th>Activity</th><th>Status</th></tr>
<tr><td>SANGAM Orientation & Training</td><td>✅ Completed</td></tr>
<tr><td>University Onboarding</td><td>✅ Completed</td></tr>
<tr><td>NIRF Data Collection</td><td>{'✅ Completed' if completed == total else '🟡 In Progress'}</td></tr>
<tr><td>GRDAU Planning</td><td>🟡 In Progress</td></tr>
<tr><td>Inception Report</td><td>🟡 In Progress</td></tr>
<tr><td>May MPR</td><td>✅ Completed</td></tr></table>
<h3>B. Minutes of Meetings</h3><table><tr><th>Date</th><th>Agenda</th><th>Outcome</th></tr>
<tr><td>May 4-6, 2026</td><td>SANGAM Orientation & Training</td><td>Training completed for all coordinators</td></tr>
<tr><td>May 18, 2026</td><td>Stakeholder Consultation</td><td>Data gaps identified</td></tr>
<tr><td>May 27, 2026</td><td>Review Meeting with ICARE</td><td>May progress reviewed</td></tr></table>
<h3>C. Major Deliverables</h3><table><tr><th>Deliverable</th><th>Status</th><th>Due Date</th></tr>
<tr><td>Inception Report</td><td>{'✅ Completed' if completed == total else '🟡 In Progress'}</td><td>June 6, 2026</td></tr>
<tr><td>GRDAU Establishment</td><td>🟡 Planning Phase</td><td>July 6, 2026</td></tr>
<tr><td>May MPR</td><td>✅ Completed</td><td>June 10, 2026</td></tr></table>
<h3>Approvals</h3>
<table><tr><td><strong>Prepared by:</strong></td><td>{', '.join(info['coordinators'])}</td></tr>
<tr><td><strong>Verified by:</strong></td><td>{info['nodal_officer']}</td></tr>
<tr><td><strong>Approved by:</strong></td><td>{MITRA_OFFICIALS['project_director']}</td></tr></table>
<p class="footer">Report generated on {datetime.now().strftime('%d-%b-%Y %H:%M:%S')}</p>
</body></html>"""
    return html

def generate_consolidated_html():
    summary = get_summary()
    period_start = datetime(2026, 5, 4)
    period_end = datetime(2026, 5, 29)
    total_completed = summary["Completed"].sum() if not summary.empty else 0
    total_planned = len(DEFAULT_PLAN) * len(UNIVERSITIES)
    
    html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Consolidated MPR - All Universities</title>
<style>body {{ font-family: 'Times New Roman', margin: 0.7in; }} .header {{ text-align: center; }} .report-title {{ font-size: 14pt; font-weight: bold; text-align: center; }} table {{ width: 100%; border-collapse: collapse; }} th, td {{ border: 1px solid #000; padding: 5px; }} th {{ background: #e8e8e8; }}</style></head>
<body>
<div class="header"><h2>Maharashtra Institution for Transformation (MITRA)</h2><p>5th Floor, Nirmal, Nariman Point, Mumbai-400021</p></div>
<div class="report-title">CONSOLIDATED MONTHLY PROGRESS REPORT</div>
<p style="text-align:center">All Maharashtra State Universities | {period_start.strftime('%d-%m-%Y')} to {period_end.strftime('%d-%m-%Y')}</p>
<h3>Overall Progress</h3>
<p><strong>Overall Status:</strong> {'✅ Completed' if total_completed == total_planned else '🟡 Substantially Complete'}<br>
<strong>Tasks Completed:</strong> {total_completed} / {total_planned}<br>
<strong>Working Days:</strong> 19 days (May 4-29, excluding weekends & holidays)</p>
<h3>University-wise Progress</h3>
<table><tr><th>University</th><th>Completed</th><th>Total</th><th>Status</th></tr>"""
    for _, row in summary.iterrows():
        html += f"<tr><td>{row['University']}</td><td>{row['Completed']}</td><td>{row['Total']}</td><td>{row['Status']}</td></tr>"
    html += f"""</table>
<h3>Training Programs (May 4-6, 2026 at Trident Board Room, Mumbai)</h3>
<table><tr><th>Date</th><th>Program</th><th>Status</th></tr>
<tr><td>May 4, 2026</td><td>SANGAM Orientation - Project Overview</td><td>✅ Completed</td></tr>
<tr><td>May 5, 2026</td><td>SANGAM Training - NIRF Framework</td><td>✅ Completed</td></tr>
<tr><td>May 6, 2026</td><td>SANGAM Workshop - GRDAU & Data Templates</td><td>✅ Completed</td></tr></table>
<h3>Major Deliverables Status</h3>
<table><tr><th>Deliverable</th><th>Status</th><th>Due Date</th></tr>
<tr><td>Inception Report</td><td>🟡 In Progress</td><td>June 6, 2026</td></tr>
<tr><td>GRDAUs Establishment</td><td>🟡 Planning Phase</td><td>July 6, 2026</td></tr>
<tr><td>Monthly Progress Report (May)</td><td>✅ Completed</td><td>June 10, 2026</td></tr></table>
<h3>Plan for June 2026</h3>
<table><tr><th>Activity</th><th>Target Date</th></tr>
<tr><td>Complete NIRF data collection</td><td>June 15, 2026</td></tr>
<tr><td>Submit Diagnostic Assessment Reports</td><td>June 30, 2026</td></tr>
<tr><td>Finalize GRDAU team compositions</td><td>June 30, 2026</td></tr></table>
<h3>Approvals</h3>
<table><tr><td><strong>Prepared by:</strong></td><td>All Coordinators</td></tr>
<tr><td><strong>Verified by:</strong></td><td>Nodal Officers</td></tr>
<tr><td><strong>Approved by:</strong></td><td>{MITRA_OFFICIALS['project_director']}</td></tr></table>
<p>Report generated on {datetime.now().strftime('%d-%b-%Y %H:%M:%S')}</p>
</body></html>"""
    return html

def get_download_link(html, filename):
    b64 = base64.b64encode(html.encode()).decode()
    return f'<a href="data:text/html;base64,{b64}" download="{filename}" style="background:#4CAF50;color:white;padding:10px 20px;text-decoration:none;border-radius:5px;">📥 Download {filename}</a>'

def show_sangam_info():
    st.markdown("""
    <div style="background:linear-gradient(135deg,#f093fb 0%,#f5576c 100%);color:white;padding:1rem;border-radius:10px;margin:1rem 0">
    <h3>🎉 SANGAM Orientation & Training Program</h3>
    <p><strong>Dates:</strong> May 4-6, 2026 | <strong>Venue:</strong> Trident Board Room, Mumbai<br>
    <strong>Participants:</strong> All Coordinators | <strong>Status:</strong> ✅ Completed successfully</p>
    </div>
    """, unsafe_allow_html=True)

def main():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    
    if not st.session_state["authenticated"]:
        with st.container():
            st.markdown('<div class="main-header"><h1>🔐 mahaSTRIDE Project Tracker</h1><p>Phase 1: May 4-29, 2026 (19 Working Days)</p></div>', unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.markdown("### Login")
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                if st.button("Login", use_container_width=True):
                    if email and password:
                        success, role, name, university = authenticate_user(email, password)
                        if success:
                            st.session_state.update({"authenticated": True, "user_email": email, "user_role": role, "user_name": name, "user_university": university})
                            st.rerun()
                        else:
                            st.error("Invalid credentials")
                st.markdown("---")
                st.markdown("""
                **Demo Credentials** (Password: Name@2026)<br>
                Admin: admin@mahastride.com<br>
                Project Lead: projectlead@mahastride.com<br>
                Coordinators: sneha@mu.edu, sagar@mu.edu, shubham@mitra.gov.in, jagan@sspu.edu, vaibhav@coep.edu, pratham@au.edu, anjali@nu.edu, nitish@kbcnmu.edu, atharv@bamu.edu
                """, unsafe_allow_html=True)
        return
    
    role, name, university = st.session_state["user_role"], st.session_state["user_name"], st.session_state.get("user_university")
    
    with st.sidebar:
        st.title("📊 mahaSTRIDE")
        st.markdown(f"**Welcome, {name}**")
        st.markdown(f"**Today:** {datetime.now().strftime('%d-%b-%Y')}")
        st.markdown("**May 2026:** 19 Working Days")
        st.markdown("---")
        if role == "admin":
            menu = st.radio("Navigation", ["📊 Admin Dashboard", "ℹ️ About"])
        elif role == "project_lead":
            menu = st.radio("Navigation", ["👨‍💼 Project Lead Dashboard", "ℹ️ About"])
        else:
            menu = st.radio("Navigation", ["📋 My Tasks", "📊 My Progress", "ℹ️ About"])
        if st.button("🚪 Logout", use_container_width=True):
            for key in ["authenticated", "user_email", "user_role", "user_name", "user_university"]:
                st.session_state.pop(key, None)
            st.rerun()
    
    if role == "admin":
        if menu == "📊 Admin Dashboard":
            st.markdown('<div class="admin-card"><h2>📊 Admin Dashboard</h2></div>', unsafe_allow_html=True)
            if st.button("📋 Mark ALL Tasks as Completed for ALL Universities", use_container_width=True):
                for code in UNIVERSITIES:
                    mark_all_completed(code)
                st.success("✅ All tasks marked completed!")
                st.rerun()
            show_sangam_info()
            col1, col2, col3, col4 = st.columns(4)
            total_planned = len(DEFAULT_PLAN) * len(UNIVERSITIES)
            summary = get_summary()
            total_completed = summary["Completed"].sum() if not summary.empty else 0
            col1.metric("Working Days", "19")
            col2.metric("Universities", len(UNIVERSITIES))
            col3.metric("Total Tasks", total_planned)
            col4.metric("Completed", total_completed, delta=f"{total_planned - total_completed} pending")
            st.dataframe(summary, use_container_width=True)
            with st.expander("📄 Generate Reports"):
                st.markdown("### Individual University Report")
                sel_uni = st.selectbox("Select University", list(UNIVERSITIES.keys()), format_func=lambda x: UNIVERSITIES[x]["name"])
                if st.button("Generate MPR"):
                    html = generate_mpr_html(sel_uni)
                    st.markdown(get_download_link(html, f"MPR_{UNIVERSITIES[sel_uni]['name'].replace(' ', '_')}_May2026.html"), unsafe_allow_html=True)
                st.markdown("### Consolidated Report")
                if st.button("Generate Consolidated MPR"):
                    html = generate_consolidated_html()
                    st.markdown(get_download_link(html, "Consolidated_MPR_May2026.html"), unsafe_allow_html=True)
    
    elif role == "project_lead":
        if menu == "👨‍💼 Project Lead Dashboard":
            st.markdown('<div class="projectlead-card"><h2>👨‍💼 Project Lead Dashboard</h2></div>', unsafe_allow_html=True)
            show_sangam_info()
            with st.expander("📄 Generate Reports"):
                st.markdown("### Individual University Report")
                sel_uni = st.selectbox("Select University", list(UNIVERSITIES.keys()), format_func=lambda x: UNIVERSITIES[x]["name"])
                if st.button("Generate MPR"):
                    html = generate_mpr_html(sel_uni)
                    st.markdown(get_download_link(html, f"MPR_{UNIVERSITIES[sel_uni]['name'].replace(' ', '_')}_May2026.html"), unsafe_allow_html=True)
                st.markdown("### Consolidated Report")
                if st.button("Generate Consolidated MPR"):
                    html = generate_consolidated_html()
                    st.markdown(get_download_link(html, "Consolidated_MPR_May2026.html"), unsafe_allow_html=True)
    
    else:
        if menu == "📋 My Tasks" and university:
            st.markdown(f'<div class="info-card"><h2>📋 Coordinator Dashboard</h2><p>{UNIVERSITIES[university]["name"]} | {name}</p></div>', unsafe_allow_html=True)
            show_sangam_info()
            pending = get_pending_tasks(university)
            entries = get_entries(university)
            total, completed = len(DEFAULT_PLAN), len(entries)
            col1, col2, col3 = st.columns(3)
            col1.metric("📋 Total Tasks", total)
            col2.metric("✅ Completed", completed)
            col3.metric("⏳ Pending", total - completed)
            st.progress(completed/total if total else 0)
            if pending:
                sel_date = st.selectbox("Select Date", [t["date"] for t in pending])
                task = next(t for t in pending if t["date"] == sel_date)
                st.markdown(f"""
                <div class="default-task-card">
                    <strong>📋 {task['date']}</strong><br>
                    <strong>🎯 Task:</strong> {task['task']}<br>
                    <strong>📍 Venue:</strong> {task['venue']}<br>
                    <strong>📝 Description:</strong> {task['description']}
                </div>
                """, unsafe_allow_html=True)
                with st.form("log_form"):
                    status = st.selectbox("Status", ["completed"])
                    hours = st.number_input("Hours Spent", 0.5, 12.0, 8.0)
                    remarks = st.text_area("Remarks")
                    if st.form_submit_button("✅ Submit"):
                        if log_task(university, sel_date, task["category"], task["task"], task["description"], 
                                   task["deliverables"], status, hours, remarks, name):
                            st.success("Logged!")
                            st.rerun()
            else:
                st.success("🎉 All tasks completed!")
            with st.expander("📋 Completed Tasks"):
                if not entries.empty:
                    st.dataframe(entries, use_container_width=True)

if __name__ == "__main__":
    # Initialize data on first run
    for code in UNIVERSITIES:
        if code not in load_data():
            mark_all_completed(code)
    main()
