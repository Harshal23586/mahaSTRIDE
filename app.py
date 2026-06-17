import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import calendar
import io
import base64

# Page configuration
st.set_page_config(
    page_title="MahaSTRIDE - Project Plan Dashboard",
    page_icon="🎯",
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
    .assignment-title {
        font-size: 1.1rem;
        font-weight: 500;
        margin: 0.5rem 0;
        padding: 0.5rem;
        background-color: rgba(255,255,255,0.1);
        border-radius: 8px;
        text-align: center;
    }
    .parties-info {
        background: linear-gradient(135deg, #2a5298 0%, #1e3c72 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-top: 1rem;
        font-size: 0.9rem;
        border: 1px solid rgba(255,255,255,0.2);
    }
    .quarter-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        transition: transform 0.3s;
    }
    .quarter-card:hover {
        transform: translateY(-5px);
    }
    .milestone-completed {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
    }
    .milestone-achieved {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
    }
    .milestone-upcoming {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
    }
    .stat-card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
    .status-ongoing {
        background-color: #fff3cd;
        color: #856404;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        display: inline-block;
    }
    .status-completed {
        background-color: #d4edda;
        color: #155724;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        display: inline-block;
    }
    .war-room-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .party-box {
        background: rgba(255,255,255,0.15);
        border-radius: 8px;
        padding: 0.75rem;
        margin: 0.5rem 0;
    }
    .daily-task-card {
        background: white;
        border-left: 4px solid #2a5298;
        padding: 0.75rem;
        margin: 0.3rem 0;
        border-radius: 5px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .daily-task-completed {
        border-left-color: #28a745;
        background-color: #d4edda;
    }
    .daily-task-pending {
        border-left-color: #ffc107;
        background-color: #fff3cd;
    }
    .coordinator-tag {
        display: inline-block;
        background-color: #e9ecef;
        padding: 0.1rem 0.5rem;
        border-radius: 12px;
        font-size: 0.7rem;
        margin: 0.1rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# PROJECT DATA
# ============================================================

PROJECT_NAME = "MahaSTRIDE - Maharashtra Strengthening Institutional Capabilities in Districts for Enabling Growth"
ASSIGNMENT_TITLE = "Engagement of a Consultancy Firm for Comprehensive Data Collection, Advanced Analytics, and Development of Performance Improvement Framework for Maharashtra State Universities under MahaSTRIDE Operations"

CLIENT_NAME = "Maharashtra Institute for Transformation (MITRA), State Data Authority, Government of Maharashtra"
CONSULTANT_NAME = "Indian Centre for Academic Rankings & Excellence - ICARE Pvt. Ltd."

START_DATE = datetime(2026, 5, 5)
END_DATE = datetime(2028, 5, 6)

# Achieved Milestones
ACHIEVED_MILESTONES = [
    {"milestone": "SANGAM Orientation & Training Completed", "date": "May 4-6, 2026", "status": "achieved"},
    {"milestone": "Inception Report & GRDAU Framework Submitted", "date": "May 26, 2026", "status": "achieved"}
]

# Universities Data with GRDAU Status
UNIVERSITIES = {
    "MU": {
        "name": "Mumbai University",
        "location": "Mumbai",
        "vice_chancellor": "Dr. Ravindra Kulkarni",
        "nodal_officer": "Dr. Varsha Kelkar Mane",
        "contact": "+91-22-26543000",
        "coordinators": ["Sneha Kashitkar", "Sagar Teli"],
        "grdau_status": "Completed",
        "grdau_completion_date": "July 5, 2026"
    },
    "SSPU": {
        "name": "Savitribai Phule Pune University",
        "location": "Pune",
        "vice_chancellor": "Dr. Suresh Gosavi",
        "nodal_officer": "Prof. Vinayak Joshi",
        "contact": "+91-20-25696061",
        "coordinators": ["Jagan Sridhar"],
        "grdau_status": "Completed",
        "grdau_completion_date": "July 5, 2026"
    },
    "COEP": {
        "name": "COEP Technological University",
        "location": "Pune",
        "vice_chancellor": "Dr. B. K. Mishra",
        "nodal_officer": "Dr. Uttam Chaskar",
        "contact": "+91-20-25507000",
        "coordinators": ["Vaibhav Ambekar"],
        "grdau_status": "Completed",
        "grdau_completion_date": "July 5, 2026"
    },
    "KBCNMU": {
        "name": "Kavayitri Bahinabai Chaudhari North Maharashtra University",
        "location": "Jalgaon",
        "vice_chancellor": "Dr. R. P. Swami",
        "nodal_officer": "Prof. Sameer Narkhede",
        "contact": "+91-257-2257457",
        "coordinators": ["Nitish Kumbhar"],
        "grdau_status": "Completed",
        "grdau_completion_date": "July 5, 2026"
    },
    "BAMU": {
        "name": "Dr. Babasaheb Ambedkar Marathwada University",
        "location": "Chhatrapati Sambhajinagar",
        "vice_chancellor": "Dr. Pramod Yeole",
        "nodal_officer": "Prof. G. D. Khedkar",
        "contact": "+91-240-2403111",
        "coordinators": ["Atharav Paturkar"],
        "grdau_status": "Completed",
        "grdau_completion_date": "July 5, 2026"
    },
    "NU": {
        "name": "Rashtrasant Tukadoji Maharaj Nagpur University",
        "location": "Nagpur",
        "vice_chancellor": "Dr. Subhash Chaudhari",
        "nodal_officer": "Prof. Nandkishor Karade",
        "contact": "+91-712-2500511",
        "coordinators": ["Anjali Singh"],
        "grdau_status": "Completed",
        "grdau_completion_date": "July 5, 2026"
    },
    "AU": {
        "name": "Sant Gadge Baba Amravati University",
        "location": "Amravati",
        "vice_chancellor": "Dr. Milind Baride",
        "nodal_officer": "Dr. A. B. Naik",
        "contact": "+91-721-2662379",
        "coordinators": ["Prathamesh Babhulkar"],
        "grdau_status": "Completed",
        "grdau_completion_date": "July 5, 2026"
    },
    "MITRA": {
        "name": "MITRA - State Data Authority",
        "location": "Mumbai",
        "ceo": "Shri. Aman Mittal",
        "nodal_officer": "Dr. Harshal Kotwal",
        "contact": "+91-22-69979440",
        "coordinators": ["Shubham Singh"],
        "grdau_status": "Completed",
        "grdau_completion_date": "July 5, 2026"
    }
}

# ============================================================
# DAILY PLAN OF ACTION FOR COORDINATORS
# ============================================================

def get_daily_plan(year, month):
    """Generate daily plan of action for coordinators based on month and year"""
    
    # Get all working days for the selected month
    first_day = datetime(year, month, 1)
    if month == 12:
        last_day = datetime(year, month, 31)
    else:
        last_day = datetime(year, month + 1, 1) - timedelta(days=1)
    
    working_days = []
    current = first_day
    while current <= last_day:
        if current.weekday() < 5:  # Monday to Friday
            working_days.append(current)
        current += timedelta(days=1)
    
    daily_plan = {}
    
    # ============================================================
    # PHASE 1: FOUNDATION (May - July 2026)
    # ============================================================
    
    if year == 2026 and month == 5:
        tasks = {
            "2026-05-04": {"task": "SANGAM Orientation Day 1 - Project Overview & MahaSTRIDE Introduction", "venue": "Trident Board Room, Mumbai", "coordinators": ["All"]},
            "2026-05-05": {"task": "SANGAM Training Day 2 - NIRF Framework Deep Dive", "venue": "Trident Board Room, Mumbai", "coordinators": ["All"]},
            "2026-05-06": {"task": "SANGAM Workshop Day 3 - GRDAU Concept & Data Templates", "venue": "Trident Board Room, Mumbai", "coordinators": ["All"]},
            "2026-05-07": {"task": "University Reporting & Onboarding - Meet VC & Registrar", "venue": "Respective University", "coordinators": ["All"]},
            "2026-05-08": {"task": "NIRF Data Source Mapping - Map data sources across departments", "venue": "Respective University", "coordinators": ["All"]},
            "2026-05-11": {"task": "Create Data Gap Template and Request Letters", "venue": "Respective University", "coordinators": ["All"]},
            "2026-05-12": {"task": "Collect Student Enrollment & Faculty Data from all departments", "venue": "Respective University", "coordinators": ["All"]},
            "2026-05-13": {"task": "Collect Research Publications & Placement Data", "venue": "Respective University", "coordinators": ["All"]},
            "2026-05-14": {"task": "Collect Financial & Infrastructure Data", "venue": "Respective University", "coordinators": ["All"]},
            "2026-05-15": {"task": "Data Consolidation & Validation - First Pass", "venue": "Respective University", "coordinators": ["All"]},
            "2026-05-18": {"task": "Stakeholder Consultation Meeting with Department Heads", "venue": "Respective University", "coordinators": ["All"]},
            "2026-05-19": {"task": "Missing Data Follow-up and Verification", "venue": "Respective University", "coordinators": ["All"]},
            "2026-05-20": {"task": "NIRF Template Preparation and Draft Submission", "venue": "Respective University", "coordinators": ["All"]},
            "2026-05-21": {"task": "SWOT Analysis & Gap Report Preparation", "venue": "Respective University", "coordinators": ["All"]},
            "2026-05-22": {"task": "Inception Report Drafting", "venue": "Respective University", "coordinators": ["All"]},
            "2026-05-25": {"task": "GRDAU Team Identification and Nomination", "venue": "Respective University", "coordinators": ["All"]},
            "2026-05-26": {"task": "GRDAU Operational Framework Finalization", "venue": "Respective University", "coordinators": ["All"]},
            "2026-05-27": {"task": "Review Meeting with ICARE Leadership", "venue": "Respective University", "coordinators": ["All"]},
            "2026-05-29": {"task": "May MPR Finalization and Submission", "venue": "Respective University", "coordinators": ["All"]}
        }
        
        for date in working_days:
            date_str = date.strftime("%Y-%m-%d")
            if date_str in tasks:
                daily_plan[date_str] = tasks[date_str]
            else:
                daily_plan[date_str] = {"task": "Continue project activities", "venue": "Respective University", "coordinators": ["All"]}
    
    elif year == 2026 and month == 6:
        tasks = {
            "2026-06-01": {"task": "Complete Diagnostic Assessment Framework", "venue": "Respective University", "coordinators": ["All"]},
            "2026-06-02": {"task": "Begin University-wise Assessments", "venue": "Respective University", "coordinators": ["All"]},
            "2026-06-03": {"task": "Review Existing Data Quality Across Departments", "venue": "Respective University", "coordinators": ["All"]},
            "2026-06-04": {"task": "Identify Data Gaps per University", "venue": "Respective University", "coordinators": ["All"]},
            "2026-06-05": {"task": "Prepare Assessment Templates", "venue": "Respective University", "coordinators": ["All"]},
            "2026-06-08": {"task": "Conduct Faculty Interviews - Round 1", "venue": "Respective University", "coordinators": ["All"]},
            "2026-06-09": {"task": "Analyze Research Output Metrics", "venue": "Respective University", "coordinators": ["All"]},
            "2026-06-10": {"task": "Evaluate Infrastructure Readiness", "venue": "Respective University", "coordinators": ["All"]},
            "2026-06-11": {"task": "Assess International Collaboration", "venue": "Respective University", "coordinators": ["All"]},
            "2026-06-12": {"task": "Compile Assessment Findings", "venue": "Respective University", "coordinators": ["All"]},
            "2026-06-15": {"task": "GRDAU Training - Module 1: Data Management", "venue": "Respective University", "coordinators": ["All"]},
            "2026-06-16": {"task": "Data Validation Workshop", "venue": "Respective University", "coordinators": ["All"]},
            "2026-06-17": {"task": "NIRF Submission Preparation", "venue": "Respective University", "coordinators": ["All"]},
            "2026-06-18": {"task": "Review Progress with Vice Chancellor", "venue": "Respective University", "coordinators": ["All"]},
            "2026-06-19": {"task": "Update Central Data Repository", "venue": "Respective University", "coordinators": ["All"]},
            "2026-06-22": {"task": "Finalize Diagnostic Reports", "venue": "Respective University", "coordinators": ["All"]},
            "2026-06-23": {"task": "Submit Diagnostic Reports to PMU", "venue": "Respective University", "coordinators": ["All"]},
            "2026-06-24": {"task": "Prepare June MPR", "venue": "Respective University", "coordinators": ["All"]},
            "2026-06-25": {"task": "Plan July Activities", "venue": "Respective University", "coordinators": ["All"]},
            "2026-06-26": {"task": "Client Review Meeting", "venue": "Respective University", "coordinators": ["All"]},
            "2026-06-29": {"task": "Continue Data Analysis", "venue": "Respective University", "coordinators": ["All"]},
            "2026-06-30": {"task": "Finalize and Submit June MPR", "venue": "Respective University", "coordinators": ["All"]}
        }
        
        for date in working_days:
            date_str = date.strftime("%Y-%m-%d")
            if date_str in tasks:
                daily_plan[date_str] = tasks[date_str]
            else:
                daily_plan[date_str] = {"task": "Continue diagnostic assessments", "venue": "Respective University", "coordinators": ["All"]}
    
    elif year == 2026 and month == 7:
        tasks = {
            "2026-07-01": {"task": "Complete Gap Analysis Against NIRF", "venue": "Respective University", "coordinators": ["All"]},
            "2026-07-02": {"task": "Prepare SWOT Analysis - Mumbai University", "venue": "Mumbai University", "coordinators": ["Sneha", "Sagar"]},
            "2026-07-03": {"task": "Prepare SWOT Analysis - Pune University", "venue": "SPPU Pune", "coordinators": ["Jagan"]},
            "2026-07-06": {"task": "Prepare SWOT Analysis - Nagpur University", "venue": "Nagpur University", "coordinators": ["Anjali"]},
            "2026-07-07": {"task": "Prepare SWOT Analysis - Amravati University", "venue": "Amravati University", "coordinators": ["Prathamesh"]},
            "2026-07-08": {"task": "Prepare SWOT Analysis - COEP University", "venue": "COEP Pune", "coordinators": ["Vaibhav"]},
            "2026-07-09": {"task": "Prepare SWOT Analysis - Jalgaon University", "venue": "KBCNMU Jalgaon", "coordinators": ["Nitish"]},
            "2026-07-10": {"task": "Prepare SWOT Analysis - Aurangabad University", "venue": "BAMU Aurangabad", "coordinators": ["Atharav"]},
            "2026-07-13": {"task": "Finalize GRDAU Establishment Plan", "venue": "Respective University", "coordinators": ["All"]},
            "2026-07-14": {"task": "Setup GRDAU Office Infrastructure", "venue": "Respective University", "coordinators": ["All"]},
            "2026-07-15": {"task": "Conduct Data Entry Training for GRDAU Staff", "venue": "Respective University", "coordinators": ["All"]},
            "2026-07-16": {"task": "Create Data Validation Protocols", "venue": "Respective University", "coordinators": ["All"]},
            "2026-07-17": {"task": "Develop Dashboard Requirements Document", "venue": "Respective University", "coordinators": ["All"]},
            "2026-07-20": {"task": "Design Baseline Report Template", "venue": "Respective University", "coordinators": ["All"]},
            "2026-07-21": {"task": "Compile Phase 1 Deliverables", "venue": "Respective University", "coordinators": ["All"]},
            "2026-07-22": {"task": "Present Phase 1 Findings to MITRA", "venue": "Respective University", "coordinators": ["All"]},
            "2026-07-23": {"task": "Document Lessons Learned - Phase 1", "venue": "Respective University", "coordinators": ["All"]},
            "2026-07-24": {"task": "Plan Phase 2 Activities", "venue": "Respective University", "coordinators": ["All"]},
            "2026-07-27": {"task": "Prepare July MPR", "venue": "Respective University", "coordinators": ["All"]},
            "2026-07-28": {"task": "Submit July MPR and Phase 1 Report", "venue": "Respective University", "coordinators": ["All"]},
            "2026-07-29": {"task": "Incorporate Client Feedback", "venue": "Respective University", "coordinators": ["All"]},
            "2026-07-30": {"task": "Finalize Phase 2 Work Plan", "venue": "Respective University", "coordinators": ["All"]},
            "2026-07-31": {"task": "Conduct Phase 2 Kickoff Meeting", "venue": "Respective University", "coordinators": ["All"]}
        }
        
        for date in working_days:
            date_str = date.strftime("%Y-%m-%d")
            if date_str in tasks:
                daily_plan[date_str] = tasks[date_str]
            else:
                daily_plan[date_str] = {"task": "Continue Phase 1 wrap-up", "venue": "Respective University", "coordinators": ["All"]}
    
    # ============================================================
    # PHASE 2: PLANNING (August - October 2026)
    # ============================================================
    
    elif year == 2026 and month == 8:
        tasks = {
            "2026-08-03": {"task": "Develop IDP Framework Template", "venue": "Respective University", "coordinators": ["All"]},
            "2026-08-04": {"task": "Collect Strategic Plans - Mumbai University", "venue": "Mumbai University", "coordinators": ["Sneha", "Sagar"]},
            "2026-08-05": {"task": "Collect Strategic Plans - Pune University", "venue": "SPPU Pune", "coordinators": ["Jagan"]},
            "2026-08-06": {"task": "Collect Strategic Plans - Nagpur University", "venue": "Nagpur University", "coordinators": ["Anjali"]},
            "2026-08-07": {"task": "Collect Strategic Plans - Amravati University", "venue": "Amravati University", "coordinators": ["Prathamesh"]},
            "2026-08-10": {"task": "Collect Strategic Plans - COEP University", "venue": "COEP Pune", "coordinators": ["Vaibhav"]},
            "2026-08-11": {"task": "Collect Strategic Plans - Jalgaon University", "venue": "KBCNMU Jalgaon", "coordinators": ["Nitish"]},
            "2026-08-12": {"task": "Collect Strategic Plans - Aurangabad University", "venue": "BAMU Aurangabad", "coordinators": ["Atharav"]},
            "2026-08-13": {"task": "Analyze Collected Strategic Plans", "venue": "Respective University", "coordinators": ["All"]},
            "2026-08-14": {"task": "Draft IDP - Mumbai University", "venue": "Mumbai University", "coordinators": ["Sneha", "Sagar"]},
            "2026-08-17": {"task": "Draft IDP - Pune University", "venue": "SPPU Pune", "coordinators": ["Jagan"]},
            "2026-08-18": {"task": "Draft IDP - Nagpur University", "venue": "Nagpur University", "coordinators": ["Anjali"]},
            "2026-08-19": {"task": "Draft IDP - Amravati University", "venue": "Amravati University", "coordinators": ["Prathamesh"]},
            "2026-08-20": {"task": "Draft IDP - COEP University", "venue": "COEP Pune", "coordinators": ["Vaibhav"]},
            "2026-08-21": {"task": "Draft IDP - Jalgaon University", "venue": "KBCNMU Jalgaon", "coordinators": ["Nitish"]},
            "2026-08-24": {"task": "Draft IDP - Aurangabad University", "venue": "BAMU Aurangabad", "coordinators": ["Atharav"]},
            "2026-08-25": {"task": "Present IDPs to VCs for Feedback", "venue": "Respective University", "coordinators": ["All"]},
            "2026-08-26": {"task": "Incorporate VC Feedback - Finalize IDPs", "venue": "Respective University", "coordinators": ["All"]},
            "2026-08-27": {"task": "Get Institutional Sign-off on IDPs", "venue": "Respective University", "coordinators": ["All"]},
            "2026-08-28": {"task": "Prepare August MPR", "venue": "Respective University", "coordinators": ["All"]},
            "2026-08-31": {"task": "Submit August MPR to PMU", "venue": "Respective University", "coordinators": ["All"]}
        }
        
        for date in working_days:
            date_str = date.strftime("%Y-%m-%d")
            if date_str in tasks:
                daily_plan[date_str] = tasks[date_str]
            else:
                daily_plan[date_str] = {"task": "Continue IDP development", "venue": "Respective University", "coordinators": ["All"]}
    
    elif year == 2026 and month == 9:
        tasks = {
            "2026-09-01": {"task": "Design Data Portal Architecture", "venue": "Respective University", "coordinators": ["All"]},
            "2026-09-02": {"task": "Create Dashboard Wireframes and Mockups", "venue": "Respective University", "coordinators": ["All"]},
            "2026-09-03": {"task": "Setup Development Environment", "venue": "Respective University", "coordinators": ["All"]},
            "2026-09-04": {"task": "Develop Backend APIs for Data Integration", "venue": "Respective University", "coordinators": ["All"]},
            "2026-09-07": {"task": "Implement User Authentication & RBAC", "venue": "Respective University", "coordinators": ["All"]},
            "2026-09-08": {"task": "Build KPI Dashboard with Metric Cards", "venue": "Respective University", "coordinators": ["All"]},
            "2026-09-09": {"task": "Integrate Research Output Charts", "venue": "Respective University", "coordinators": ["All"]},
            "2026-09-10": {"task": "Add Faculty-Student Ratio Analytics", "venue": "Respective University", "coordinators": ["All"]},
            "2026-09-11": {"task": "Implement Financial Resource Tracking", "venue": "Respective University", "coordinators": ["All"]},
            "2026-09-14": {"task": "Develop Placement Outcomes Dashboard", "venue": "Respective University", "coordinators": ["All"]},
            "2026-09-15": {"task": "Create International Collaboration Metrics", "venue": "Respective University", "coordinators": ["All"]},
            "2026-09-16": {"task": "Add Citation Analysis Charts", "venue": "Respective University", "coordinators": ["All"]},
            "2026-09-17": {"task": "Implement Infrastructure Dashboard", "venue": "Respective University", "coordinators": ["All"]},
            "2026-09-18": {"task": "Prepare Milestone 1 Report", "venue": "Respective University", "coordinators": ["All"]},
            "2026-09-21": {"task": "Submit Milestone 1 Report to PMU", "venue": "Respective University", "coordinators": ["All"]},
            "2026-09-22": {"task": "Present Milestone 1 to Client", "venue": "Respective University", "coordinators": ["All"]},
            "2026-09-23": {"task": "Incorporate Client Feedback into Dashboard", "venue": "Respective University", "coordinators": ["All"]},
            "2026-09-24": {"task": "Conduct User Acceptance Testing", "venue": "Respective University", "coordinators": ["All"]},
            "2026-09-25": {"task": "Fix Bugs and Optimize Performance", "venue": "Respective University", "coordinators": ["All"]},
            "2026-09-28": {"task": "Deploy Dashboard Beta to Staging", "venue": "Respective University", "coordinators": ["All"]},
            "2026-09-29": {"task": "Prepare September MPR", "venue": "Respective University", "coordinators": ["All"]},
            "2026-09-30": {"task": "Submit September MPR to PMU", "venue": "Respective University", "coordinators": ["All"]}
        }
        
        for date in working_days:
            date_str = date.strftime("%Y-%m-%d")
            if date_str in tasks:
                daily_plan[date_str] = tasks[date_str]
            else:
                daily_plan[date_str] = {"task": "Continue dashboard development", "venue": "Respective University", "coordinators": ["All"]}
    
    elif year == 2026 and month == 10:
        tasks = {
            "2026-10-01": {"task": "Complete Dashboard Beta Testing", "venue": "Respective University", "coordinators": ["All"]},
            "2026-10-02": {"task": "Finalize Dashboard Based on Feedback", "venue": "Respective University", "coordinators": ["All"]},
            "2026-10-05": {"task": "Prepare Milestone 2 Report", "venue": "Respective University", "coordinators": ["All"]},
            "2026-10-06": {"task": "Submit Milestone 2 Report to PMU", "venue": "Respective University", "coordinators": ["All"]},
            "2026-10-07": {"task": "Present IDP Monitoring Framework to Client", "venue": "Respective University", "coordinators": ["All"]},
            "2026-10-08": {"task": "Conduct Dashboard Training for Administrators", "venue": "Respective University", "coordinators": ["All"]},
            "2026-10-09": {"task": "Create User Manual and Video Tutorials", "venue": "Respective University", "coordinators": ["All"]},
            "2026-10-12": {"task": "Compile 6-Month Achievements", "venue": "Respective University", "coordinators": ["All"]},
            "2026-10-13": {"task": "Prepare Mid-Term Review Presentation", "venue": "Respective University", "coordinators": ["All"]},
            "2026-10-14": {"task": "Conduct Internal Review with ICARE", "venue": "Respective University", "coordinators": ["All"]},
            "2026-10-15": {"task": "Present Mid-Term Report to World Bank", "venue": "Respective University", "coordinators": ["All"]},
            "2026-10-16": {"task": "Incorporate Mid-Term Feedback", "venue": "Respective University", "coordinators": ["All"]},
            "2026-10-19": {"task": "Prepare October MPR", "venue": "Respective University", "coordinators": ["All"]},
            "2026-10-20": {"task": "Deploy Data Portal to Production", "venue": "Respective University", "coordinators": ["All"]},
            "2026-10-21": {"task": "Monitor Portal Performance", "venue": "Respective University", "coordinators": ["All"]},
            "2026-10-22": {"task": "Setup Analytics Tracking", "venue": "Respective University", "coordinators": ["All"]},
            "2026-10-23": {"task": "Create Backup and Recovery Procedures", "venue": "Respective University", "coordinators": ["All"]},
            "2026-10-26": {"task": "Plan Phase 3 Implementation Activities", "venue": "Respective University", "coordinators": ["All"]},
            "2026-10-27": {"task": "Develop Phase 3 Work Schedule", "venue": "Respective University", "coordinators": ["All"]},
            "2026-10-28": {"task": "Assign Phase 3 Responsibilities", "venue": "Respective University", "coordinators": ["All"]},
            "2026-10-29": {"task": "Conduct Phase 3 Coordination Meeting", "venue": "Respective University", "coordinators": ["All"]},
            "2026-10-30": {"task": "Submit October MPR to PMU", "venue": "Respective University", "coordinators": ["All"]}
        }
        
        for date in working_days:
            date_str = date.strftime("%Y-%m-%d")
            if date_str in tasks:
                daily_plan[date_str] = tasks[date_str]
            else:
                daily_plan[date_str] = {"task": "Continue Phase 2 completion", "venue": "Respective University", "coordinators": ["All"]}
    
    # ============================================================
    # PHASE 3: IMPLEMENTATION (November 2026 - April 2027)
    # ============================================================
    
    elif year == 2026 and month == 11:
        tasks = {
            "2026-11-02": {"task": "Deploy Data Portal MVP", "venue": "Respective University", "coordinators": ["All"]},
            "2026-11-03": {"task": "Conduct Portal Training for GRDAU", "venue": "Respective University", "coordinators": ["All"]},
            "2026-11-04": {"task": "Upload Baseline Data for All Universities", "venue": "Respective University", "coordinators": ["All"]},
            "2026-11-05": {"task": "Verify Data Accuracy in Portal", "venue": "Respective University", "coordinators": ["All"]},
            "2026-11-06": {"task": "Collect User Feedback on Portal", "venue": "Respective University", "coordinators": ["All"]},
            "2026-11-09": {"task": "Implement Priority Fixes Based on Feedback", "venue": "Respective University", "coordinators": ["All"]},
            "2026-11-10": {"task": "Add Data Export Functionality", "venue": "Respective University", "coordinators": ["All"]},
            "2026-11-11": {"task": "Setup Automated Data Validation", "venue": "Respective University", "coordinators": ["All"]},
            "2026-11-12": {"task": "Create Custom Reports Feature", "venue": "Respective University", "coordinators": ["All"]},
            "2026-11-13": {"task": "Train Staff on Report Generation", "venue": "Respective University", "coordinators": ["All"]},
            "2026-11-16": {"task": "Develop NIRF Data Submission Training", "venue": "Respective University", "coordinators": ["All"]},
            "2026-11-17": {"task": "Conduct Research Metrics Workshop", "venue": "Respective University", "coordinators": ["All"]},
            "2026-11-18": {"task": "Provide Citation Analysis Training", "venue": "Respective University", "coordinators": ["All"]},
            "2026-11-19": {"task": "Prepare Training Needs Assessment", "venue": "Respective University", "coordinators": ["All"]},
            "2026-11-20": {"task": "Schedule Capacity Building Programs", "venue": "Respective University", "coordinators": ["All"]},
            "2026-11-23": {"task": "Conduct Online Training for Remote Coordinators", "venue": "Respective University", "coordinators": ["All"]},
            "2026-11-24": {"task": "Prepare Training Materials and Handouts", "venue": "Respective University", "coordinators": ["All"]},
            "2026-11-25": {"task": "Assess Training Effectiveness", "venue": "Respective University", "coordinators": ["All"]},
            "2026-11-26": {"task": "Plan Advanced Training Modules", "venue": "Respective University", "coordinators": ["All"]},
            "2026-11-27": {"task": "Prepare November MPR", "venue": "Respective University", "coordinators": ["All"]},
            "2026-11-30": {"task": "Submit November MPR to PMU", "venue": "Respective University", "coordinators": ["All"]}
        }
        
        for date in working_days:
            date_str = date.strftime("%Y-%m-%d")
            if date_str in tasks:
                daily_plan[date_str] = tasks[date_str]
            else:
                daily_plan[date_str] = {"task": "Continue portal deployment", "venue": "Respective University", "coordinators": ["All"]}
    
    elif year == 2026 and month == 12:
        tasks = {
            "2026-12-01": {"task": "Complete First Round of Training Programs", "venue": "Respective University", "coordinators": ["All"]},
            "2026-12-02": {"task": "Analyze Training Feedback", "venue": "Respective University", "coordinators": ["All"]},
            "2026-12-03": {"task": "Prepare Training Completion Report", "venue": "Respective University", "coordinators": ["All"]},
            "2026-12-04": {"task": "Launch Performance Dashboards", "venue": "Respective University", "coordinators": ["All"]},
            "2026-12-07": {"task": "Develop Advanced Training Modules", "venue": "Respective University", "coordinators": ["All"]},
            "2026-12-08": {"task": "Conduct Hands-on Analytics Workshop", "venue": "Respective University", "coordinators": ["All"]},
            "2026-12-09": {"task": "Provide One-on-One Coaching", "venue": "Respective University", "coordinators": ["All"]},
            "2026-12-10": {"task": "Create GRDAU Certification Program", "venue": "Respective University", "coordinators": ["All"]},
            "2026-12-11": {"task": "Prepare Milestone 3 Report", "venue": "Respective University", "coordinators": ["All"]},
            "2026-12-14": {"task": "Submit Milestone 3 Report", "venue": "Respective University", "coordinators": ["All"]},
            "2026-12-15": {"task": "Present Capacity Building Achievements", "venue": "Respective University", "coordinators": ["All"]},
            "2026-12-16": {"task": "Compile Year-End Performance Data", "venue": "Respective University", "coordinators": ["All"]},
            "2026-12-17": {"task": "Prepare Annual Report 2026", "venue": "Respective University", "coordinators": ["All"]},
            "2026-12-18": {"task": "Review Progress Against Targets", "venue": "Respective University", "coordinators": ["All"]},
            "2026-12-21": {"task": "Plan 2027 Activities", "venue": "Respective University", "coordinators": ["All"]},
            "2026-12-22": {"task": "Conduct Team Performance Appraisal", "venue": "Respective University", "coordinators": ["All"]},
            "2026-12-23": {"task": "Document Success Stories", "venue": "Respective University", "coordinators": ["All"]},
            "2026-12-24": {"task": "Prepare December MPR", "venue": "Respective University", "coordinators": ["All"]},
            "2026-12-28": {"task": "Submit December MPR and Annual Report", "venue": "Respective University", "coordinators": ["All"]},
            "2026-12-29": {"task": "Conduct Client Year-End Review", "venue": "Respective University", "coordinators": ["All"]},
            "2026-12-30": {"task": "Plan Enhancement Activities", "venue": "Respective University", "coordinators": ["All"]},
            "2026-12-31": {"task": "Celebrate Project Achievements", "venue": "Respective University", "coordinators": ["All"]}
        }
        
        for date in working_days:
            date_str = date.strftime("%Y-%m-%d")
            if date_str in tasks:
                daily_plan[date_str] = tasks[date_str]
            else:
                daily_plan[date_str] = {"task": "Continue year-end activities", "venue": "Respective University", "coordinators": ["All"]}
    
    # ============================================================
    # PHASE 4 & 5: ENHANCEMENT & FINALIZATION (2027-2028)
    # ============================================================
    
    elif year == 2027 or year == 2028:
        # Generic tasks for 2027-2028 based on month
        month_names = {
            1: "Data Quality and Research Enhancement",
            2: "International Collaboration and OBE",
            3: "Accreditation and Quality Assurance",
            4: "Milestone 4: 10% Improvement",
            5: "Year 2 Kickoff and Advanced Analytics",
            6: "Global Ranking Preparation (QS, THE, US News)",
            7: "Advanced Training and Research Support",
            8: "Employer Perception and Industry Connect",
            9: "Milestone 5: 20% Improvement",
            10: "Academic Reputation Building",
            11: "Final Ranking Submissions",
            12: "Sustainability and Knowledge Transfer"
        }
        
        if year == 2028:
            month_names.update({
                1: "Final Evaluation Preparation",
                2: "Final Client Presentation and Milestone 7",
                3: "Project Closure and Knowledge Transfer",
                4: "Contract Completion and Final Submission"
            })
        
        day = 1
        for date in working_days:
            date_str = date.strftime("%Y-%m-%d")
            day_num = date.day
            month_focus = month_names.get(month, "Continue project activities")
            
            # Specific tasks for Q1 2028
            if year == 2028 and month == 1:
                tasks_jan = {
                    3: "Prepare Final Evaluation Framework",
                    4: "Compile All Project Achievements",
                    5: "Collect 24-Month Performance Metrics",
                    6: "Analyze Baseline vs Endline Data",
                    7: "Calculate Overall Improvement",
                    10: "Prepare Success Stories Document",
                    11: "Create Case Studies Library",
                    12: "Develop Lessons Learned Report",
                    13: "Prepare Best Practices Guide",
                    14: "Create Future Recommendations",
                    17: "Prepare Final Evaluation Report Draft",
                    18: "Review with ICARE Leadership",
                    19: "Incorporate Feedback",
                    20: "Prepare Final Presentation",
                    21: "Conduct Internal Review",
                    24: "Finalize Evaluation Report",
                    25: "Prepare January MPR",
                    26: "Submit January MPR",
                    27: "Schedule Final Client Presentation",
                    28: "Prepare Client Presentation Materials"
                }
                if day_num in tasks_jan:
                    daily_plan[date_str] = {"task": tasks_jan[day_num], "venue": "Respective University", "coordinators": ["All"]}
                else:
                    daily_plan[date_str] = {"task": f"{month_focus} - Day {day_num}", "venue": "Respective University", "coordinators": ["All"]}
            
            elif year == 2028 and month == 2:
                tasks_feb = {
                    1: "Prepare Milestone 7 Report",
                    2: "Compile Evidence for Milestone",
                    3: "Submit Milestone 7 Report",
                    4: "Prepare Final Client Presentation",
                    7: "Conduct Final Client Presentation",
                    8: "Incorporate Final Client Feedback",
                    9: "Finalize All Project Deliverables",
                    10: "Prepare Project Closure Report",
                    11: "Complete Pending Documentation",
                    14: "Prepare Handover Packages",
                    15: "Conduct Handover Training",
                    16: "Transfer All Credentials",
                    17: "Archive Project Data",
                    18: "Prepare Final Financial Report",
                    21: "Complete Bank Guarantee Release",
                    22: "Prepare Contract Closure Documents",
                    23: "Conduct Final Team Meeting",
                    24: "Prepare February MPR",
                    25: "Submit February MPR",
                    28: "Plan Project Celebration",
                    29: "Final Milestone Review"
                }
                if day_num in tasks_feb:
                    daily_plan[date_str] = {"task": tasks_feb[day_num], "venue": "Respective University", "coordinators": ["All"]}
                else:
                    daily_plan[date_str] = {"task": f"{month_focus} - Day {day_num}", "venue": "Respective University", "coordinators": ["All"]}
            
            elif year == 2028 and month == 3:
                tasks_mar = {
                    1: "Complete Knowledge Transfer",
                    2: "Provide Final GRDAU Training",
                    3: "Handover System Credentials",
                    6: "Transfer Source Code",
                    7: "Provide Database Backup Guide",
                    8: "Conduct Final User Acceptance Test",
                    9: "Get Client Sign-off",
                    10: "Prepare Project Completion Certificate",
                    13: "Conduct Final Project Review",
                    14: "Present Overall Achievements",
                    15: "Discuss Sustainability Support",
                    16: "Get Formal Project Closure Letter",
                    17: "Prepare Celebration Event",
                    20: "Organize Project Completion Celebration",
                    21: "Release Final Payments",
                    22: "Prepare Team Appreciation Letters",
                    23: "Document Impact Assessment",
                    24: "Prepare March MPR",
                    27: "Submit March MPR",
                    28: "Finalize All Reports",
                    29: "Archive Documentation",
                    30: "Complete Financial Reconciliation",
                    31: "Prepare for Contract Completion"
                }
                if day_num in tasks_mar:
                    daily_plan[date_str] = {"task": tasks_mar[day_num], "venue": "Respective University", "coordinators": ["All"]}
                else:
                    daily_plan[date_str] = {"task": f"{month_focus} - Day {day_num}", "venue": "Respective University", "coordinators": ["All"]}
            
            elif year == 2028 and month == 4:
                tasks_apr = {
                    3: "Finalize Pending Deliverables",
                    4: "Complete Final Project Report",
                    5: "Prepare World Bank Executive Summary",
                    6: "Compile Supporting Documents",
                    7: "Review Deliverables Completeness",
                    10: "Get Internal Approval on Final Package",
                    11: "Submit Final Deliverables to PMU",
                    12: "Present Final Outcomes to MITRA",
                    13: "Get Final Acceptance Certificate",
                    14: "Complete Contract Closure",
                    17: "Release Bank Guarantee",
                    18: "Submit Final Invoice",
                    19: "Prepare Project Completion Report",
                    20: "Conduct Final Team Debrief",
                    21: "Prepare Lessons Learned for World Bank",
                    24: "Complete Knowledge Repository Handover",
                    25: "Submit Final Documentation to ICARE",
                    26: "Prepare April MPR",
                    27: "Submit April MPR",
                    28: "CONTRACT COMPLETION - Project Success!"
                }
                if day_num in tasks_apr:
                    daily_plan[date_str] = {"task": tasks_apr[day_num], "venue": "Respective University", "coordinators": ["All"]}
                else:
                    daily_plan[date_str] = {"task": f"{month_focus} - Day {day_num}", "venue": "Respective University", "coordinators": ["All"]}
            
            else:
                daily_plan[date_str] = {"task": f"{month_focus} - Day {day_num}", "venue": "Respective University", "coordinators": ["All"]}
    
    return daily_plan

# ============================================================
# QUARTERLY PLAN
# ============================================================

QUARTERS = {
    "Q1: May - July 2026": {
        "number": 1,
        "months": ["May 2026", "June 2026", "July 2026"],
        "status": "ongoing",
        "key_activities": [
            "✅ SANGAM Orientation & Training (May 4-6 at Trident Board Room)",
            "✅ University Onboarding & Data Source Mapping",
            "✅ NIRF Data Collection (Student, Faculty, Research, Placement, Finance)",
            "✅ Inception Report & GRDAU Framework Development",
            "✅ GRDAU Establishment in all universities (Completed July 5, 2026)",
            "🔄 Diagnostic Assessments across all 7 universities",
            "🔄 Gap Analysis against NIRF/NAAC/Global Rankings",
            "🔄 SWOT Analysis for each university"
        ],
        "deliverables": [
            "✅ Inception Report and Deployment Plan (Submitted May 26, 2026)",
            "✅ GRDAUs Established and Operationalized (Completed July 5, 2026)",
            "🔄 Diagnostic Assessment Reports (7 universities) - Due July 31, 2026",
            "🔄 SWOT Analysis Reports - Due July 31, 2026"
        ],
        "milestones": [
            {"name": "SANGAM Training Completed", "status": "achieved", "date": "May 6, 2026"},
            {"name": "Inception Report Submitted", "status": "achieved", "date": "May 26, 2026"},
            {"name": "GRDAU Establishment Completed", "status": "achieved", "date": "July 5, 2026"},
            {"name": "Diagnostic Reports", "status": "in_progress", "date": "July 31, 2026"},
            {"name": "SWOT Analysis Reports", "status": "in_progress", "date": "July 31, 2026"},
            {"name": "Gap Analysis Report", "status": "in_progress", "date": "July 31, 2026"}
        ],
        "data_collection": "NIRF baseline data collection completed. Diagnostic assessments in progress.",
        "stakeholder_engagement": "VC meetings conducted. IQAC coordination established.",
        "review_mechanism": "Weekly GRDAU meetings. Monthly progress review with MITRA PMU."
    },
    "Q2: August - October 2026": {
        "number": 2,
        "months": ["August 2026", "September 2026", "October 2026"],
        "status": "upcoming",
        "key_activities": [
            "Institutional Development Plans (IDPs) development",
            "Stakeholder review and feedback incorporation",
            "Data portal architecture design",
            "Dashboard requirements gathering",
            "Dashboard prototype development",
            "Milestone 1: Sustainable Data Systems establishment"
        ],
        "deliverables": [
            "Institutional Development Plans (IDPs) - 7",
            "Portal Design Document",
            "Dashboard Mockups",
            "Milestone 1 Report"
        ],
        "milestones": [
            {"name": "IDPs Draft Completed", "status": "pending", "date": "Aug 31, 2026"},
            {"name": "Portal Design Approved", "status": "pending", "date": "Sep 15, 2026"},
            {"name": "Milestone 1: Sustainable Data & Quality Systems", "status": "pending", "date": "Sep 30, 2026"},
            {"name": "Milestone 2: IDP Execution Monitoring", "status": "pending", "date": "Oct 31, 2026"}
        ],
        "data_collection": "IDP data collection. Dashboard requirements gathering.",
        "stakeholder_engagement": "IDP review meetings with VCs. Dashboard workshops.",
        "review_mechanism": "Bi-weekly IDP review. Monthly progress review."
    },
    "Q3: November 2026 - January 2027": {
        "number": 3,
        "months": ["November 2026", "December 2026", "January 2027"],
        "status": "upcoming",
        "key_activities": [
            "Data Portal MVP Deployment",
            "Training Needs Assessment",
            "Capacity Building Programs (First round)",
            "Performance Dashboards Launch",
            "Data Validation and Quality Improvement",
            "Milestone 3: Capacity Building Participation"
        ],
        "deliverables": [
            "Data Portal Live",
            "Training Completion Report",
            "Dashboard Deployment Report"
        ],
        "milestones": [
            {"name": "Portal MVP Launch", "status": "pending", "date": "Nov 15, 2026"},
            {"name": "Mid-term Progress Report", "status": "pending", "date": "Nov 30, 2026"},
            {"name": "First Training Program", "status": "pending", "date": "Dec 15, 2026"},
            {"name": "Milestone 3: Capacity Building", "status": "pending", "date": "Dec 31, 2026"}
        ],
        "data_collection": "Portal data upload. Training feedback collection.",
        "stakeholder_engagement": "Portal training sessions. Capacity building workshops.",
        "review_mechanism": "Portal usage analytics. Training effectiveness assessment."
    },
    "Q4: February - April 2027": {
        "number": 4,
        "months": ["February 2027", "March 2027", "April 2027"],
        "status": "upcoming",
        "key_activities": [
            "Research Output Enhancement Initiatives",
            "International Collaboration Development",
            "Accreditation Preparedness Assessment",
            "Quality Assurance Framework Implementation"
        ],
        "deliverables": [
            "Research Enhancement Plan",
            "Collaboration Framework",
            "QA Framework Report"
        ],
        "milestones": [
            {"name": "Research Enhancement Plan", "status": "pending", "date": "Feb 28, 2027"},
            {"name": "Year 1 Annual Report", "status": "pending", "date": "Apr 30, 2027"}
        ],
        "data_collection": "Research output data. Collaboration metrics.",
        "stakeholder_engagement": "Research committee meetings. Industry collaboration.",
        "review_mechanism": "Research output tracking. QA dashboard monitoring."
    },
    "Q5: May - July 2027": {
        "number": 5,
        "months": ["May 2027", "June 2027", "July 2027"],
        "status": "upcoming",
        "key_activities": [
            "Year 2 Kickoff and Advanced Analytics",
            "Global Ranking Preparation (QS, THE, US News)",
            "Advanced Training Programs",
            "Milestone 4: 10% Improvement Achievement"
        ],
        "deliverables": [
            "Year 2 Work Plan",
            "Ranking Submission Packages",
            "Advanced Training Report",
            "Milestone 4 Report"
        ],
        "milestones": [
            {"name": "QS Ranking Submission", "status": "pending", "date": "Jun 15, 2027"},
            {"name": "Milestone 4: 10% Improvement", "status": "pending", "date": "Jun 30, 2027"}
        ],
        "data_collection": "Ranking data compilation. Improvement metrics.",
        "stakeholder_engagement": "Ranking preparation workshops. Industry advisory board.",
        "review_mechanism": "Quarterly performance review. Ranking submission tracking."
    },
    "Q6: August - October 2027": {
        "number": 6,
        "months": ["August 2027", "September 2027", "October 2027"],
        "status": "upcoming",
        "key_activities": [
            "Employer Perception Enhancement",
            "Academic Reputation Building",
            "Industry Connect Programs",
            "International Student Enrollment Strategies"
        ],
        "deliverables": [
            "Employer Perception Report",
            "Reputation Strategy Document",
            "Industry Connect Report",
            "Internationalization Plan"
        ],
        "milestones": [
            {"name": "Employer Survey Completion", "status": "pending", "date": "Aug 31, 2027"},
            {"name": "International MoUs Signed", "status": "pending", "date": "Sep 30, 2027"}
        ],
        "data_collection": "Employer survey data. Reputation metrics.",
        "stakeholder_engagement": "Employer meets. International partner meetings.",
        "review_mechanism": "Monthly reputation tracking. Employer feedback analysis."
    },
    "Q7: November 2027 - January 2028": {
        "number": 7,
        "months": ["November 2027", "December 2027", "January 2028"],
        "status": "upcoming",
        "key_activities": [
            "Final Global Ranking Submissions",
            "Sustainability Planning",
            "Knowledge Transfer Preparation",
            "Milestone 5: 20% Improvement",
            "Milestone 6: Global Rankings Participation"
        ],
        "deliverables": [
            "Final Ranking Submissions",
            "Sustainability Plan",
            "Knowledge Transfer Report",
            "Milestone 5 & 6 Reports"
        ],
        "milestones": [
            {"name": "Milestone 5: 20% Improvement", "status": "pending", "date": "Dec 31, 2027"},
            {"name": "Milestone 6: Global Rankings", "status": "pending", "date": "Feb 29, 2028"},
            {"name": "Sustainability Plan", "status": "pending", "date": "Dec 15, 2027"}
        ],
        "data_collection": "20% improvement evidence. Ranking participation data.",
        "stakeholder_engagement": "Sustainability workshop. Handover planning.",
        "review_mechanism": "Final evaluation framework. Sustainability assessment."
    },
    "Q8: February - April 2028": {
        "number": 8,
        "months": ["February 2028", "March 2028", "April 2028"],
        "status": "upcoming",
        "key_activities": [
            "Final Evaluation and Reporting",
            "Project Closure and Knowledge Transfer",
            "Milestone 7: Final Evaluation",
            "Contract Completion"
        ],
        "deliverables": [
            "Final Closure Report",
            "Lessons Learned Report",
            "Knowledge Transfer Documentation",
            "Milestone 7 Report"
        ],
        "milestones": [
            {"name": "Milestone 7: Final Evaluation", "status": "pending", "date": "Apr 30, 2028"},
            {"name": "Project Closure", "status": "pending", "date": "May 6, 2028"}
        ],
        "data_collection": "Final performance metrics. Lessons learned.",
        "stakeholder_engagement": "Final client presentation. Project closure meeting.",
        "review_mechanism": "Final evaluation. Client satisfaction survey."
    }
}

# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

if 'nav_selection' not in st.session_state:
    st.session_state.nav_selection = "summary"

with st.sidebar:
    st.markdown("## 🎯 MahaSTRIDE")
    st.markdown("---")
    
    nav_options = {
        "🏠 Executive Summary": "summary",
        "📊 Quarterly Plan": "quarterly",
        "📋 Daily Plan of Action": "dailyplan",
        "🏫 Universities & Team": "universities",
        "🏛️ War Room & GRDAU": "warroom",
        "🎯 Milestones Tracker": "milestones",
        "📋 Deliverables": "deliverables",
        "🔄 Review Mechanisms": "review",
        "📁 Documents": "documents"
    }
    
    selected_nav = st.radio(
        "Navigation", 
        list(nav_options.keys()), 
        label_visibility="collapsed",
        key="nav_radio"
    )
    
    st.session_state.nav_selection = nav_options[selected_nav]
    
    st.markdown("---")
    st.markdown("### ℹ️ Project Info")
    st.markdown(f"**Start Date:** {START_DATE.strftime('%d %b %Y')}")
    st.markdown(f"**End Date:** {END_DATE.strftime('%d %b %Y')}")
    st.markdown(f"**Duration:** 24 months (8 Quarters)")
    st.markdown(f"**Universities:** 7")
    st.markdown(f"**Data Analysts:** 10")
    
    st.markdown("---")
    st.markdown("### ✅ Achievements")
    for achievement in ACHIEVED_MILESTONES:
        st.markdown(f"- ✅ {achievement['milestone']}")
    
    st.markdown("---")
    st.markdown("### 📞 Contact")
    st.markdown("**PMU MahaSTRIDE**")
    st.markdown("📧 pmu.mahastride@mahamitra.org")
    st.markdown("📞 022-69979440")
    st.markdown("📍 5th Floor, Nirmal Building, Nariman Point, Mumbai-400021")

# ============================================================
# MAIN HEADER
# ============================================================

st.markdown(f"""
<div class="main-header">
    <h1>🎯 {PROJECT_NAME}</h1>
    <div class="assignment-title">
        📋 {ASSIGNMENT_TITLE}
    </div>
    <div class="parties-info">
        <div class="party-box">
            <strong>🏛️ Client:</strong> {CLIENT_NAME}
        </div>
        <div class="party-box">
            <strong>🤝 Consultant:</strong> {CONSULTANT_NAME}
        </div>
        <p style="margin-top:0.5rem; font-size:0.85rem;">World Bank Loan No: IBRD 9737-IN | RFP Ref: IN-MITRA(PMU)-PforR-Edu-QCBS</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# CONTENT RENDERING
# ============================================================

selected_key = st.session_state.nav_selection

# 1. EXECUTIVE SUMMARY
if selected_key == "summary":
    st.header("📋 Executive Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <h2>Q1</h2>
            <p>Phase 1 - Ongoing</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <h2>2</h2>
            <p>Milestones Achieved</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <h2>7</h2>
            <p>GRDAUs Established</p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <h2>10</h2>
            <p>Team Members</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.subheader("🎯 Current Status")
    st.markdown("""
    <div class="status-ongoing">Q1: May - July 2026 - ONGOING</div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.subheader("✅ Achievements So Far")
    
    for achievement in ACHIEVED_MILESTONES:
        st.markdown(f"""
        <div class="milestone-achieved">
            ✅ <strong>{achievement['milestone']}</strong><br>
            📅 Completed: {achievement['date']}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.subheader("🏆 GRDAU Establishment Status")
    st.markdown("""
    <div class="milestone-completed">
        ✅ <strong>GRDAUs Established and Operationalized in all 7 universities</strong><br>
        📅 Completed: July 5, 2026
    </div>
    """, unsafe_allow_html=True)

# 2. QUARTERLY PLAN
elif selected_key == "quarterly":
    st.header("📅 8-Quarter Project Plan (May 2026 - April 2028)")
    st.markdown("Working Days: Monday to Friday | Hours: 10:00 AM - 6:00 PM")
    st.markdown("---")
    
    quarter_tabs = st.tabs(list(QUARTERS.keys()))
    
    for tab, (quarter_name, quarter_info) in zip(quarter_tabs, QUARTERS.items()):
        with tab:
            status_display = "🟡 ONGOING" if quarter_info["status"] == "ongoing" else "⚪ UPCOMING"
            st.markdown(f"""
            <div class="quarter-card">
                <h2>{quarter_name}</h2>
                <p><strong>Months:</strong> {', '.join(quarter_info['months'])}</p>
                <p><strong>Status:</strong> {status_display}</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🎯 Key Activities")
                for activity in quarter_info["key_activities"]:
                    st.markdown(f"- {activity}")
                
                st.markdown("---")
                st.markdown("### 📊 Data Collection Processes")
                st.markdown(quarter_info["data_collection"])
                
                st.markdown("---")
                st.markdown("### 🤝 Stakeholder Engagement")
                st.markdown(quarter_info["stakeholder_engagement"])
            
            with col2:
                st.markdown("### 📦 Deliverables")
                for deliverable in quarter_info["deliverables"]:
                    st.markdown(f"- {deliverable}")
                
                st.markdown("---")
                st.markdown("### 🎯 Milestones")
                for milestone in quarter_info["milestones"]:
                    if milestone["status"] == "achieved":
                        icon = "✅"
                        color = "#d4edda"
                    elif milestone["status"] == "in_progress":
                        icon = "🔄"
                        color = "#fff3cd"
                    else:
                        icon = "⏳"
                        color = "#f8f9fa"
                    st.markdown(f"""
                    <div style="background-color:{color}; padding:0.5rem; margin:0.3rem 0; border-radius:5px;">
                        {icon} <strong>{milestone['name']}</strong><br>
                        📅 Target: {milestone['date']}
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("---")
                st.markdown("### 🔄 Review Mechanism")
                st.markdown(quarter_info["review_mechanism"])
            
            st.markdown("---")

# 3. DAILY PLAN OF ACTION
elif selected_key == "dailyplan":
    st.header("📋 Daily Plan of Action - Coordinators")
    st.markdown("Day-wise activities assigned to coordinators (Monday to Friday | 10:00 AM - 6:00 PM)")
    st.markdown("---")
    
    # Year and Month Selector
    col1, col2 = st.columns(2)
    with col1:
        selected_year = st.selectbox("Select Year", [2026, 2027, 2028], index=0)
    with col2:
        month_names = ["January", "February", "March", "April", "May", "June", 
                       "July", "August", "September", "October", "November", "December"]
        selected_month = st.selectbox("Select Month", range(1, 13), format_func=lambda x: month_names[x-1], index=4)
    
    # Get daily plan for selected month
    daily_plan = get_daily_plan(selected_year, selected_month)
    
    if daily_plan:
        # Show summary statistics
        total_days = len(daily_plan)
        st.markdown(f"**Total Working Days in {month_names[selected_month-1]} {selected_year}: {total_days}**")
        
        # Coordinator filter
        all_coordinators = ["All"] + sorted(list(set([coord for plan in daily_plan.values() for coord in plan.get("coordinators", ["All"])])))
        filter_coordinator = st.selectbox("Filter by Coordinator", all_coordinators)
        
        # Display daily tasks
        for date_str, plan in sorted(daily_plan.items()):
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            day_name = date_obj.strftime("%A")
            
            # Filter by coordinator
            if filter_coordinator != "All" and filter_coordinator not in plan.get("coordinators", []):
                continue
            
            # Determine if this date is in the past (completed) or future (pending)
            if date_str <= datetime.now().strftime("%Y-%m-%d"):
                status_class = "daily-task-completed"
                status_icon = "✅"
                status_text = "COMPLETED"
            else:
                status_class = "daily-task-pending"
                status_icon = "⏳"
                status_text = "PENDING"
            
            coordinators = ", ".join(plan.get("coordinators", ["All"]))
            
            st.markdown(f"""
            <div class="daily-task-card {status_class}">
                <strong>{status_icon} {date_str} ({day_name})</strong><br>
                <strong>Task:</strong> {plan.get('task', 'No task assigned')}<br>
                <strong>Venue:</strong> {plan.get('venue', 'N/A')}<br>
                <strong>Coordinators:</strong> <span class="coordinator-tag">{coordinators}</span><br>
                <strong>Status:</strong> {status_text}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info(f"No working days found for {month_names[selected_month-1]} {selected_year}")

# 4. UNIVERSITIES & TEAM
elif selected_key == "universities":
    st.header("🏫 Universities & Team Structure")
    
    st.subheader("📋 Participating Universities with GRDAU Status")
    
    for code, uni in UNIVERSITIES.items():
        with st.expander(f"🏛️ {uni['name']} ({code})"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                **📍 Location:** {uni['location']}<br>
                **👨‍🎓 Vice Chancellor:** {uni.get('vice_chancellor', uni.get('ceo', 'N/A'))}<br>
                **👤 Nodal Officer:** {uni.get('nodal_officer', 'N/A')}<br>
                **📞 Contact:** {uni.get('contact', 'N/A')}
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                **👥 Coordinators:** {', '.join(uni.get('coordinators', []))}<br>
                **🏛️ GRDAU Status:** <span class="status-completed">✅ {uni['grdau_status']}</span><br>
                **📅 Completion Date:** {uni.get('grdau_completion_date', 'N/A')}
                """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.subheader("👥 Project Team (May 2026 Attendance)")
    
    team_data = {
        "Name": ["Dr. Harshal Kotwal", "Shubham Singh", "Sagar Teli", "Sneha Kashitkar", "Nitish Kumbhar",
                "Anjali Singh", "Vaibhav Ambekar", "Atharav Paturkar", "Prathamesh Babhulkar", "Jagan Sridhar"],
        "Role": ["Project Lead", "Data Analytics Specialist", "Statistician & Program Designer", 
                "Institutional Coordinator", "Institutional Coordinator", "Institutional Coordinator",
                "Institutional Coordinator", "Institutional Coordinator", "Institutional Coordinator", "Institutional Coordinator"],
        "University": ["ICARE", "MITRA", "Mumbai University", "Mumbai University", "KBCNMU Jalgaon",
                      "Nagpur University", "COEP Pune", "BAMU Aurangabad", "Amravati University", "SPPU Pune"]
    }
    
    df_team = pd.DataFrame(team_data)
    st.dataframe(df_team, use_container_width=True, hide_index=True)

# 5. WAR ROOM & GRDAU
elif selected_key == "warroom":
    st.header("🏛️ War Room & GRDAU Setup")
    
    st.markdown("""
    <div class="war-room-card">
        <h2>🎯 Project War Room - MITRA, Mumbai</h2>
        <p><strong>Location:</strong> 5th Floor, Nirmal Building, Nariman Point, Mumbai-400021</p>
        <p><strong>Purpose:</strong> Central command center for project monitoring, coordination, and decision-making</p>
        <p><strong>Facilities:</strong> Real-time dashboards, video conferencing, data visualization tools</p>
        <p><strong>Weekly Meetings:</strong> Every Monday at 11:00 AM</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.subheader("🏫 Global Ranking Data Analytics Units (GRDAUs)")
    
    st.markdown("""
    ### ✅ GRDAU Establishment Status - COMPLETED (July 5, 2026)
    
    All 7 universities have successfully established their GRDAUs.
    """)
    
    st.markdown("---")
    
    st.subheader("📍 GRDAU Establishment Status - ALL COMPLETED")
    
    grdau_data = []
    for code, uni in UNIVERSITIES.items():
        if code != "MITRA":
            grdau_data.append({
                "University": uni["name"],
                "Location": uni["location"],
                "Coordinator": ", ".join(uni["coordinators"]),
                "Status": "✅ Completed",
                "Completion Date": "July 5, 2026"
            })
    
    st.dataframe(pd.DataFrame(grdau_data), use_container_width=True, hide_index=True)

# 6. MILESTONES TRACKER
elif selected_key == "milestones":
    st.header("🎯 Project Milestones Tracker")
    
    st.subheader("✅ Achieved Milestones (2)")
    for achievement in ACHIEVED_MILESTONES:
        st.markdown(f"""
        <div class="milestone-achieved">
            ✅ <strong>{achievement['milestone']}</strong><br>
            📅 Completed: {achievement['date']}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.subheader("✅ GRDAU Establishment - COMPLETED")
    st.markdown("""
    <div class="milestone-completed">
        ✅ <strong>GRDAUs Established and Operationalized in all 7 universities</strong><br>
        📅 Completed: July 5, 2026
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.subheader("🔄 In Progress Milestones (Q1)")
    
    current_milestones = [
        {"name": "Diagnostic Assessment Reports", "target": "July 31, 2026", "progress": 60},
        {"name": "SWOT Analysis Reports", "target": "July 31, 2026", "progress": 50},
        {"name": "Gap Analysis against NIRF/Global Rankings", "target": "July 31, 2026", "progress": 40}
    ]
    
    for milestone in current_milestones:
        st.markdown(f"**{milestone['name']}** - Target: {milestone['target']}")
        st.progress(milestone['progress']/100)
        st.caption(f"Progress: {milestone['progress']}%")
        st.markdown("---")
    
    st.markdown("---")
    
    st.subheader("⏳ Upcoming Milestones")
    
    upcoming = [
        {"milestone": "Institutional Development Plans (IDPs)", "date": "August 14, 2026", "quarter": "Q2"},
        {"milestone": "Milestone 1: Sustainable Data & Quality Systems", "date": "September 30, 2026", "quarter": "Q2"},
        {"milestone": "Milestone 2: IDP Execution Monitoring", "date": "October 31, 2026", "quarter": "Q2"},
        {"milestone": "Data Portal MVP Deployment", "date": "November 15, 2026", "quarter": "Q3"},
        {"milestone": "Milestone 3: Capacity Building (60% participation)", "date": "December 31, 2026", "quarter": "Q3"}
    ]
    
    for milestone in upcoming:
        st.markdown(f"""
        <div class="milestone-upcoming">
            ⏳ <strong>{milestone['milestone']}</strong><br>
            📅 Target: {milestone['date']} | 📍 Quarter: {milestone['quarter']}
        </div>
        """, unsafe_allow_html=True)

# 7. DELIVERABLES
elif selected_key == "deliverables":
    st.header("📋 Contract Deliverables Status")
    
    deliverables = [
        {"deliverable": "Inception Report and Deployment Plan", "due_date": "Jun 5, 2026", "status": "completed", "actual": "May 26, 2026"},
        {"deliverable": "GRDAUs Established and Operationalized", "due_date": "Jul 5, 2026", "status": "completed", "actual": "July 5, 2026"},
        {"deliverable": "Diagnostic Assessment Reports", "due_date": "Jul 31, 2026", "status": "in_progress", "actual": None},
        {"deliverable": "SWOT Analysis Reports", "due_date": "Jul 31, 2026", "status": "in_progress", "actual": None},
        {"deliverable": "Institutional Development Plans (IDPs)", "due_date": "Aug 14, 2026", "status": "pending", "actual": None},
        {"deliverable": "Mid-term Progress Report", "due_date": "Nov 30, 2026", "status": "pending", "actual": None},
        {"deliverable": "Final Closure Report", "due_date": "May 6, 2028", "status": "pending", "actual": None}
    ]
    
    for deliverable in deliverables:
        if deliverable["status"] == "completed":
            icon = "✅"
            color = "#d4edda"
        elif deliverable["status"] == "in_progress":
            icon = "🔄"
            color = "#fff3cd"
        else:
            icon = "⏳"
            color = "#f8f9fa"
        
        actual_text = f"<br>✅ Actual Submission: {deliverable['actual']}" if deliverable.get('actual') else ""
        
        st.markdown(f"""
        <div style="background-color:{color}; padding:1rem; margin:0.5rem 0; border-radius:8px;">
            <strong>{icon} {deliverable['deliverable']}</strong><br>
            📅 Due: {deliverable['due_date']}<br>
            📊 Status: {deliverable['status'].upper()}
            {actual_text}
        </div>
        """, unsafe_allow_html=True)

# 8. REVIEW MECHANISMS
elif selected_key == "review":
    st.header("🔄 Review & Monitoring Mechanisms")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### Weekly Reviews
        - **GRDAU Weekly Meetings:** Every Monday, 11:00 AM
        - **Data Validation Sessions:** Every Wednesday
        - **Progress Tracking:** Daily dashboard updates
        
        ### Monthly Reviews
        - **Monthly Progress Report (MPR)** submission by 10th
        - **PMU Review Meeting:** Second week of each month
        - **Attendance Verification:** By 9th of each month
        """)
    
    with col2:
        st.markdown("""
        ### Quarterly Reviews
        - **Quarterly Performance Assessment**
        - **Steering Committee Meeting**
        - **Milestone Achievement Evaluation**
        
        ### Annual Reviews
        - **Annual Performance Report**
        - **World Bank Progress Review**
        - **Strategic Planning Session**
        """)
    
    st.markdown("---")
    
    st.subheader("📋 Reporting Structure")
    
    st.markdown("""
    | Level | Responsible | Reports To | Frequency |
    |-------|-------------|------------|-----------|
    | University Level | Institutional Coordinator | Nodal Officer | Daily |
    | University Level | Nodal Officer | VC + PMU | Weekly |
    | PMU Level | Project Director | MITRA CEO | Weekly |
    | Steering Committee | Chairperson | Government | Quarterly |
    | World Bank | MITRA | World Bank | Bi-annually |
    """)

# 9. DOCUMENTS
elif selected_key == "documents":
    st.header("📁 Reference Documents")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📄 Contract Documents
        - Draft Contract with ICARE
        - Terms & Conditions of Contract
        - Terms of Reference (ToR)
        - Consultant's Technical Proposal
        
        ### 📋 SOP Documents
        - SOP for Payment Processing
        - Attendance Tracking Guidelines
        - MPR Submission Guidelines
        """)
    
    with col2:
        st.markdown("""
        ### 📊 Submitted Reports
        - ✅ Consolidated MPR - May 2026
        - ✅ Inception Report
        - ✅ Work Order (ICARE)
        
        ### 🏛️ Government Orders
        - Planning Department GRs
        - State Steering Committee Minutes
        - Administrative Approvals
        """)
    
    st.markdown("---")
    
    st.subheader("📎 Key Document Status")
    
    doc_status = {
        "Document": ["Contract Agreement", "Work Order", "Performance Bank Guarantee", "Inception Report", "May MPR", "GRDAU Establishment", "Diagnostic Reports"],
        "Status": ["✅ Executed", "✅ Issued", "⏳ Pending", "✅ Submitted", "✅ Submitted", "✅ Completed", "🔄 In Progress"],
        "Due Date": ["Signed", "Mar 25, 2026", "Within 15 days", "May 26, 2026", "May 29, 2026", "July 5, 2026", "July 31, 2026"]
    }
    
    st.dataframe(pd.DataFrame(doc_status), use_container_width=True, hide_index=True)

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #666; font-size: 0.8rem;">
    <p>© 2026-2028 {CLIENT_NAME} | MahaSTRIDE Project | World Bank Loan No: IBRD 9737-IN</p>
    <p>Consultant: {CONSULTANT_NAME} | Duration: 24 months (8 Quarters) | Working Days: Monday to Friday | Hours: 10:00 - 18:00</p>
    <p>Last Updated: {datetime.now().strftime('%d %B %Y, %H:%M:%S')}</p>
</div>
""", unsafe_allow_html=True)
