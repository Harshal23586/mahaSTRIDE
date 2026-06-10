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
# COMPLETE 24-MONTH PLAN (May 2026 - April 2028)
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
    """Get specific task for a date based on the 24-month plan"""
    date = datetime.strptime(date_str, "%Y-%m-%d")
    month = date.month
    year = date.year
    day = date.day
    
    # ============================================================
    # PHASE 1: FOUNDATION (May - July 2026)
    # ============================================================
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
            "2026-06-08": "Conduct Faculty Interviews at Mumbai University (10 faculty members)",
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
            "2026-07-17": "Develop Dashboard Requirements Document with Stakeholder Inputs",
            "2026-07-20": "Design Baseline Report Template for Phase 1 Completion",
            "2026-07-21": "Compile All Phase 1 Deliverables and Prepare Completion Report",
            "2026-07-22": "Present Phase 1 Findings to MITRA Steering Committee",
            "2026-07-23": "Document Lessons Learned and Best Practices from Phase 1",
            "2026-07-24": "Plan Phase 2 Activities with Detailed Work Breakdown Structure",
            "2026-07-27": "Prepare July Monthly Progress Report with Phase 1 Summary",
            "2026-07-28": "Submit July MPR and Phase 1 Completion Report to PMU",
            "2026-07-29": "Review and Incorporate Client Feedback on Phase 1 Deliverables",
            "2026-07-30": "Finalize Phase 2 Work Plan and Resource Allocation",
            "2026-07-31": "Conduct Phase 2 Kickoff Meeting with All University Coordinators"
        }
        return july_tasks.get(date_str, "Continue July 2026 Phase 1 completion activities")
    
    # ============================================================
    # PHASE 2: PLANNING (August - October 2026)
    # ============================================================
    elif year == 2026 and month == 8:
        aug_tasks = {
            "2026-08-03": "Develop IDP Framework Template Aligned with NIRF Metrics",
            "2026-08-04": "Collect Strategic Plans from Mumbai University Leadership",
            "2026-08-05": "Collect Strategic Plans from Pune University VC Office",
            "2026-08-06": "Collect Strategic Plans from Nagpur University Administration",
            "2026-08-07": "Collect Strategic Plans from Amravati University",
            "2026-08-10": "Collect Strategic Plans from COEP University Director",
            "2026-08-11": "Collect Strategic Plans from KBCNMU Jalgaon",
            "2026-08-12": "Collect Strategic Plans from BAMU Aurangabad",
            "2026-08-13": "Analyze Collected Strategic Plans and Identify Common Themes",
            "2026-08-14": "Draft Institutional Development Plan for Mumbai University",
            "2026-08-17": "Draft IDP for Pune University with Specific KPIs",
            "2026-08-18": "Draft IDP for Nagpur University Focusing on Research Excellence",
            "2026-08-19": "Draft IDP for Amravati University with Timeline",
            "2026-08-20": "Draft IDP for COEP University Emphasizing Industry Connect",
            "2026-08-21": "Draft IDP for KBCNMU Jalgaon with Internationalization Goals",
            "2026-08-24": "Draft IDP for BAMU Aurangabad Focusing on Infrastructure",
            "2026-08-25": "Present IDP Drafts to Respective Vice Chancellors for Feedback",
            "2026-08-26": "Incorporate VC Feedback and Finalize IDPs for All Universities",
            "2026-08-27": "Get Formal Institutional Sign-off on Approved IDPs",
            "2026-08-28": "Prepare August MPR Documenting IDP Development Progress",
            "2026-08-31": "Submit August MPR to PMU with IDP Status Report"
        }
        return aug_tasks.get(date_str, "Continue August 2026 IDP development activities")
    
    elif year == 2026 and month == 9:
        sep_tasks = {
            "2026-09-01": "Design Data Portal Architecture and Database Schema",
            "2026-09-02": "Create High-Fidelity Dashboard Wireframes and Mockups",
            "2026-09-03": "Setup Development Environment and Version Control System",
            "2026-09-04": "Develop Backend APIs for Data Integration",
            "2026-09-07": "Implement User Authentication and Role-Based Access Control",
            "2026-09-08": "Build KPI Dashboard with Metric Cards for NIRF Parameters",
            "2026-09-09": "Integrate Research Output Visualization Charts",
            "2026-09-10": "Add Faculty-Student Ratio Analytics Dashboard",
            "2026-09-11": "Implement Financial Resource Utilization Tracking",
            "2026-09-14": "Develop Placement and Graduate Outcomes Dashboard",
            "2026-09-15": "Create International Collaboration Metrics Visualization",
            "2026-09-16": "Add Citation Analysis and Publication Impact Charts",
            "2026-09-17": "Implement Infrastructure Assessment Dashboard",
            "2026-09-18": "Prepare Milestone 1 Report: Sustainable Data Systems",
            "2026-09-21": "Submit Milestone 1 Report to PMU for Review",
            "2026-09-22": "Present Milestone 1 Achievements to Client",
            "2026-09-23": "Incorporate Client Feedback into Dashboard Design",
            "2026-09-24": "Conduct User Acceptance Testing with University Coordinators",
            "2026-09-25": "Fix Bugs and Optimize Dashboard Performance",
            "2026-09-28": "Deploy Dashboard Beta Version to Staging Server",
            "2026-09-29": "Prepare September MPR with Dashboard Development Status",
            "2026-09-30": "Submit September MPR to PMU"
        }
        return sep_tasks.get(date_str, "Continue September 2026 dashboard development")
    
    elif year == 2026 and month == 10:
        oct_tasks = {
            "2026-10-01": "Complete Dashboard Beta Testing with All Universities",
            "2026-10-02": "Finalize Dashboard Based on User Feedback",
            "2026-10-05": "Prepare Milestone 2 Report: IDP Execution Monitoring",
            "2026-10-06": "Submit Milestone 2 Report to PMU with Evidence",
            "2026-10-07": "Present IDP Monitoring Framework to Client",
            "2026-10-08": "Conduct Dashboard Training for University Administrators",
            "2026-10-09": "Create Comprehensive User Manual and Video Tutorials",
            "2026-10-12": "Compile 6-Month Achievements for Mid-Term Review",
            "2026-10-13": "Prepare Mid-Term Review Presentation for MITRA",
            "2026-10-14": "Conduct Internal Review with ICARE Leadership",
            "2026-10-15": "Present Mid-Term Report to World Bank and MITRA",
            "2026-10-16": "Incorporate Mid-Term Feedback into Project Plan",
            "2026-10-19": "Prepare October MPR with Milestone Achievements",
            "2026-10-20": "Deploy Data Portal to Production Environment",
            "2026-10-21": "Monitor Portal Performance and Fix Issues",
            "2026-10-22": "Setup Analytics Tracking for Portal Usage",
            "2026-10-23": "Create Backup and Disaster Recovery Procedures",
            "2026-10-26": "Plan Phase 3 Implementation Activities",
            "2026-10-27": "Develop Detailed Phase 3 Work Schedule",
            "2026-10-28": "Assign Phase 3 Responsibilities to Team Members",
            "2026-10-29": "Conduct Phase 3 Team Coordination Meeting",
            "2026-10-30": "Submit October MPR to PMU"
        }
        return oct_tasks.get(date_str, "Continue October 2026 Phase 2 completion")
    
    # ============================================================
    # PHASE 3: IMPLEMENTATION (November 2026 - April 2027)
    # ============================================================
    elif year == 2026 and month == 11:
        nov_tasks = {
            "2026-11-02": "Deploy Data Portal MVP with Core Features",
            "2026-11-03": "Conduct Portal Training for GRDAU Coordinators",
            "2026-11-04": "Upload Baseline Data for All 7 Universities",
            "2026-11-05": "Verify Data Accuracy in Portal with Source Documents",
            "2026-11-06": "Collect User Feedback on Portal Usability",
            "2026-11-09": "Implement Priority Fixes Based on User Feedback",
            "2026-11-10": "Add Data Export Functionality to Portal",
            "2026-11-11": "Setup Automated Data Validation Rules",
            "2026-11-12": "Create Custom Reports Generation Feature",
            "2026-11-13": "Train University Staff on Report Generation",
            "2026-11-16": "Develop Training Module for NIRF Data Submission",
            "2026-11-17": "Conduct Research Metrics Analysis Workshop",
            "2026-11-18": "Provide Citation Analysis Training to Faculty",
            "2026-11-19": "Prepare Training Needs Assessment Report",
            "2026-11-20": "Schedule Capacity Building Programs for All Universities",
            "2026-11-23": "Conduct Online Training for Remote Coordinators",
            "2026-11-24": "Prepare Training Materials and Handouts",
            "2026-11-25": "Assess Training Effectiveness with Feedback Forms",
            "2026-11-26": "Plan Advanced Training Modules for Phase 3",
            "2026-11-27": "Prepare November MPR with Training Status",
            "2026-11-30": "Submit November MPR to PMU"
        }
        return nov_tasks.get(date_str, "Continue November 2026 portal deployment")
    
    elif year == 2026 and month == 12:
        dec_tasks = {
            "2026-12-01": "Complete First Round of Training Programs",
            "2026-12-02": "Analyze Training Feedback and Effectiveness",
            "2026-12-03": "Prepare Training Completion Report",
            "2026-12-04": "Launch Performance Dashboards to All Users",
            "2026-12-07": "Develop Advanced Training Modules for GRDAU Staff",
            "2026-12-08": "Conduct Hands-On Data Analytics Workshop",
            "2026-12-09": "Provide One-on-One Coaching for Coordinators",
            "2026-12-10": "Create Certification Program for GRDAU Staff",
            "2026-12-11": "Prepare Milestone 3 Report: Capacity Building",
            "2026-12-14": "Submit Milestone 3 Report with Evidence",
            "2026-12-15": "Present Capacity Building Achievements to Client",
            "2026-12-16": "Compile Year-End Performance Data",
            "2026-12-17": "Prepare Annual Report for 2026",
            "2026-12-18": "Review Project Progress Against Annual Targets",
            "2026-12-21": "Plan 2027 Activities and Resource Requirements",
            "2026-12-22": "Conduct Team Performance Appraisal",
            "2026-12-23": "Document Success Stories and Case Studies",
            "2026-12-24": "Prepare December MPR with Annual Summary",
            "2026-12-28": "Submit December MPR and Annual Report",
            "2026-12-29": "Conduct Client Year-End Review Meeting",
            "2026-12-30": "Plan for Phase 3 Enhancement Activities",
            "2026-12-31": "Celebrate Project Achievements with Team"
        }
        return dec_tasks.get(date_str, "Continue December 2026 year-end activities")
    
    elif year == 2027 and month == 1:
        jan_tasks = {
            "2027-01-04": "Implement Automated Data Quality Checks in Portal",
            "2027-01-05": "Conduct Data Audit for All 7 Universities",
            "2027-01-06": "Clean and Standardize Research Publication Data",
            "2027-01-07": "Validate Faculty Credentials and Qualifications",
            "2027-01-08": "Cross-Verify Student Enrollment Data",
            "2027-01-11": "Identify and Correct Data Inconsistencies",
            "2027-01-12": "Create Data Quality Scorecard for Each University",
            "2027-01-13": "Prepare Data Quality Improvement Plan",
            "2027-01-14": "Implement Research Output Tracking System",
            "2027-01-15": "Analyze Publication Trends and Patterns",
            "2027-01-18": "Identify High-Impact Research Areas",
            "2027-01-19": "Develop Research Enhancement Strategy",
            "2027-01-20": "Create Faculty Research Profiles",
            "2027-01-21": "Setup Citation Tracking Mechanism",
            "2027-01-22": "Prepare Research Enhancement Plan Document",
            "2027-01-25": "Conduct Research Writing Workshop for Faculty",
            "2027-01-26": "Provide Grant Proposal Writing Training",
            "2027-01-27": "Establish Research Collaboration Framework",
            "2027-01-28": "Prepare January MPR with Research Progress",
            "2027-01-29": "Submit January MPR to PMU"
        }
        return jan_tasks.get(date_str, "Continue January 2027 data quality activities")
    
    elif year == 2027 and month == 2:
        feb_tasks = {
            "2027-02-01": "Review Existing International MoUs and Collaborations",
            "2027-02-02": "Identify Potential International Partners for Collaboration",
            "2027-02-03": "Develop Internationalization Strategy Document",
            "2027-02-04": "Create MoU Template for New Partnerships",
            "2027-02-05": "Initiate Discussions with Foreign Universities",
            "2027-02-08": "Develop Outcome-Based Education (OBE) Framework",
            "2027-02-09": "Create OBE Implementation Guidelines",
            "2027-02-10": "Train Faculty on OBE Curriculum Design",
            "2027-02-11": "Develop Program Outcomes and Course Outcomes",
            "2027-02-12": "Create Assessment Rubrics for OBE",
            "2027-02-15": "Implement OBE Tracking Dashboard",
            "2027-02-16": "Conduct OBE Readiness Assessment",
            "2027-02-17": "Prepare OBE Implementation Report",
            "2027-02-18": "Plan International Faculty Exchange Program",
            "2027-02-19": "Create Student Exchange Program Framework",
            "2027-02-22": "Develop International Admission Process",
            "2027-02-23": "Prepare International Student Support System",
            "2027-02-24": "Conduct International Webinar Series",
            "2027-02-25": "Prepare February MPR with OBE Progress",
            "2027-02-26": "Submit February MPR to PMU"
        }
        return feb_tasks.get(date_str, "Continue February 2027 international collaboration")
    
    elif year == 2027 and month == 3:
        mar_tasks = {
            "2027-03-01": "Conduct NAAC Accreditation Readiness Assessment",
            "2027-03-02": "Review NBA Accreditation Criteria for Programs",
            "2027-03-03": "Identify Gaps for Accreditation Requirements",
            "2027-03-04": "Prepare Accreditation Action Plan",
            "2027-03-05": "Create Accreditation Documentation Template",
            "2027-03-08": "Train IQAC on Accreditation Process",
            "2027-03-09": "Develop Quality Assurance Framework",
            "2027-03-10": "Create Internal Audit Checklist",
            "2027-03-11": "Conduct Mock Accreditation Visit",
            "2027-03-12": "Prepare Quality Improvement Plan",
            "2027-03-15": "Implement QA Dashboard for Monitoring",
            "2027-03-16": "Develop Student Feedback System",
            "2027-03-17": "Create Faculty Evaluation Framework",
            "2027-03-18": "Implement Continuous Quality Improvement Cycle",
            "2027-03-19": "Prepare QA Implementation Report",
            "2027-03-22": "Conduct Stakeholder Satisfaction Survey",
            "2027-03-23": "Analyze Survey Results and Identify Improvements",
            "2027-03-24": "Prepare March MPR with QA Progress",
            "2027-03-25": "Submit March MPR to PMU",
            "2027-03-26": "Plan Phase 4 Enhancement Activities"
        }
        return mar_tasks.get(date_str, "Continue March 2027 accreditation activities")
    
    elif year == 2027 and month == 4:
        apr_tasks = {
            "2027-04-01": "Collect Performance Data for First 6 Months",
            "2027-04-02": "Calculate Improvement Percentages for All Indicators",
            "2027-04-05": "Analyze Research Output Increase Metrics",
            "2027-04-06": "Measure Placement Rate Improvement",
            "2027-04-07": "Calculate Faculty-Student Ratio Enhancement",
            "2027-04-08": "Measure International Collaboration Growth",
            "2027-04-09": "Prepare Milestone 4 Report: 10% Improvement",
            "2027-04-12": "Compile Evidence Documents for Improvement",
            "2027-04-13": "Submit Milestone 4 Report to PMU",
            "2027-04-14": "Present Improvement Achievements to Client",
            "2027-04-15": "Prepare Year 1 Annual Performance Report",
            "2027-04-16": "Compile Annual Achievements and Metrics",
            "2027-04-19": "Create Annual Report Presentation",
            "2027-04-20": "Present Year 1 Results to MITRA Board",
            "2027-04-21": "Plan Year 2 Enhancement Activities",
            "2027-04-22": "Conduct Team Annual Performance Review",
            "2027-04-23": "Prepare April MPR with Annual Summary",
            "2027-04-26": "Submit April MPR and Annual Report",
            "2027-04-27": "Conduct Client Annual Review Meeting",
            "2027-04-28": "Finalize Year 2 Work Plan and Budget",
            "2027-04-29": "Celebrate Year 1 Achievements with Team",
            "2027-04-30": "Plan Phase 4 Kickoff Activities"
        }
        return apr_tasks.get(date_str, "Continue April 2027 milestone 4 activities")
    
    # ============================================================
    # PHASE 4: ENHANCEMENT (May - October 2027)
    # ============================================================
    elif year == 2027 and 5 <= month <= 10:
        phase = "Phase 4: Enhancement"
        enhancement_tasks = {
            5: "Year 2 Kickoff and Advanced Analytics Implementation",
            6: "Global Ranking Preparation and QS/THE/US News Submissions",
            7: "Advanced Training Programs and Research Support",
            8: "Employer Perception Enhancement and Industry Connect",
            9: "Milestone 5: 20% Improvement Achievement",
            10: "Academic Reputation Building and Final Ranking Prep"
        }
        return f"{phase} - {enhancement_tasks.get(month, 'Continue enhancement activities')} - Day {day}"
    
    # ============================================================
    # PHASE 5: FINALIZATION (November 2027 - April 2028)
    # ============================================================
    elif year == 2027 and month >= 11:
        phase = "Phase 5: Finalization"
        final_tasks = {
            11: "Final Ranking Submissions and Milestone 6",
            12: "Sustainability Planning and Knowledge Transfer"
        }
        return f"{phase} - {final_tasks.get(month, 'Continue finalization activities')} - Day {day}"
    
    elif year == 2028 and month <= 4:
        phase = "Phase 5: Finalization"
        final_2028_tasks = {
            1: "Final Evaluation Preparation",
            2: "Final Client Presentation and Milestone 7",
            3: "Project Closure and Knowledge Transfer",
            4: "Contract Completion and Final Submission"
        }
        return f"{phase} - {final_2028_tasks.get(month, 'Continue finalization activities')} - Day {day}"
    
    else:
        return "Continue project activities as per plan"


# Generate DEFAULT_PLAN for all working days
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
        </table>"""
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
        summary_rows += f"<tr><td>{i+1}</div><td>{row['University']}</div><td>{row['Completed']}</div><td>{row['Total']}</div><td>{status}</div></table>"
    
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
    <strong>Total Working Days:</strong> {len(DEFAULT_PLAN)} days
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
    main()
