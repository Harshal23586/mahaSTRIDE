import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import calendar

# Page configuration
st.set_page_config(
    page_title="MahaSTRIDE - ICARE Project Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .deliverable-card {
        background-color: white;
        border-left: 4px solid #2a5298;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 5px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .completed-badge {
        background-color: #28a745;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: bold;
    }
    .warning-card {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 5px;
    }
    .success-card {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 5px;
    }
    .info-card {
        background-color: #d1ecf1;
        border-left: 4px solid #17a2b8;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Project Constants
PROJECT_NAME = "MahaSTRIDE - University Ranking Framework Project"
CLIENT = "Maharashtra Institution for Transformation (MITRA)"
CONSULTANT = "Indian Centre for Academic Rankings & Excellence - ICARE Pvt. Ltd."
CONTRACT_START = datetime(2026, 5, 6)
CONTRACT_END = datetime(2028, 5, 6)
CURRENT_DATE = datetime(2026, 6, 4)

UNIVERSITIES = [
    "Mumbai University, Mumbai",
    "Savitribai Phule Pune University, Pune",
    "COEP Technological University, Pune",
    "Kavayitri Bahinabai Chaudhari North Maharashtra University, Jalgaon",
    "Dr. Babasaheb Ambedkar Marathwada University, Chhatrapati Sambhajinagar",
    "Rashtrasant Tukadoji Maharaj Nagpur University, Nagpur",
    "Sant Gadge Baba Amravati University, Amravati"
]

# May 2026 completed activities (from the MPR)
COMPLETED_MAY_ACTIVITIES = [
    {"activity": "SANGAM Orientation & Training (May 4-6 at Trident Board Room)", "date": "May 4-6, 2026", "team": "ICARE Team", "status": "completed"},
    {"activity": "University Onboarding & Data Source Mapping", "date": "May 7-8, 2026", "team": "ICARE Team", "status": "completed"},
    {"activity": "NIRF Data Collection (Student, Faculty, Research, Placement, Finance)", "date": "May 12-20, 2026", "team": "ICARE Team", "status": "completed"},
    {"activity": "Stakeholder Consultation & Review Meetings", "date": "May 18-27, 2026", "team": "ICARE Team", "status": "completed"},
    {"activity": "Inception Report & GRDAU Framework Development", "date": "May 22-26, 2026", "team": "ICARE Team", "status": "completed"},
    {"activity": "May MPR Preparation & Finalization", "date": "May 29, 2026", "team": "ICARE Team", "status": "completed"},
]

# May 2026 meetings completed (from the MPR)
COMPLETED_MAY_MEETINGS = [
    {"date": "May 4-6, 2026", "agenda": "SANGAM Orientation, Training & Workshop", "outcome": "Training completed. GRDAU concept introduced."},
    {"date": "May 7, 2026", "agenda": "Project Kick-off and data source mapping", "outcome": "Data collection initiated"},
    {"date": "May 18, 2026", "agenda": "Data gap review and action plan", "outcome": "Departments to submit pending data"},
    {"date": "May 27, 2026", "agenda": "Review of May progress", "outcome": "MPR preparation initiated"},
]

# Team structure (from MPR)
TEAM_STRUCTURE = {
    "MITRA Level": [
        {"role": "Project Lead", "name": "Dr. Harshal Kotwal", "location": "MITRA, Mumbai", "present_days_may": 19, "absent": 0, "holidays": 12},
        {"role": "Data Analytics and Dashboard Specialist", "name": "Mr. Shubham Singh", "location": "MITRA, Mumbai", "present_days_may": 19, "absent": 0, "holidays": 12},
    ],
    "University Level": [
        {"role": "Statistician & Program Designer", "name": "Mr. Sagar Teli", "university": "Mumbai University", "present_days_may": 19, "absent": 0, "holidays": 12},
        {"role": "Institutional Coordinator cum Research & Innovation Officer", "name": "Ms. Sneha Kashitkar", "university": "Mumbai University", "present_days_may": 19, "absent": 0, "holidays": 12},
        {"role": "Institutional Coordinator cum Research & Innovation Officer", "name": "Mr. Nitish Kumbhar", "university": "Kavayitri Bahinabai Chaudhari North Maharashtra University", "present_days_may": 19, "absent": 0, "holidays": 12},
        {"role": "Institutional Coordinator cum Research & Innovation Officer", "name": "Ms. Anjali Singh", "university": "Rashtrasant Tukadoji Maharaj Nagpur University", "present_days_may": 19, "absent": 0, "holidays": 12},
        {"role": "Institutional Coordinator cum Research & Innovation Officer", "name": "Mr. Vaibhav Ambekar", "university": "COEP Technological University", "present_days_may": 19, "absent": 0, "holidays": 12},
        {"role": "Institutional Coordinator cum Research & Innovation Officer", "name": "Mr. Atharav Paturkar", "university": "Dr. Babasaheb Ambedkar Marathwada University", "present_days_may": 19, "absent": 0, "holidays": 12},
        {"role": "Institutional Coordinator cum Research & Innovation Officer", "name": "Mr. Prathamesh Babhulkar", "university": "Sant Gadge Baba Amravati University", "present_days_may": 19, "absent": 0, "holidays": 12},
        {"role": "Institutional Coordinator cum Research & Innovation Officer", "name": "Mr. Jagan Sridhar", "university": "Savitribai Phule Pune University", "present_days_may": 19, "absent": 0, "holidays": 12},
    ]
}

# Milestones
MILESTONES = [
    {"id": 1, "name": "Establishment of Sustainable Data & Quality Systems", "percentage": 10, "target_date": "2026-09-30", "status": "pending"},
    {"id": 2, "name": "Institutional Development Plans and Execution Monitoring", "percentage": 10, "target_date": "2026-10-31", "status": "pending"},
    {"id": 3, "name": "Capacity Building Participation", "percentage": 10, "target_date": "2026-12-31", "status": "pending"},
    {"id": 4, "name": "Minimum 10% Improvement in Performance Indicators", "percentage": 15, "target_date": "2027-06-30", "status": "pending"},
    {"id": 5, "name": "Minimum 20% Improvement in Performance Indicators", "percentage": 25, "target_date": "2027-12-31", "status": "pending"},
    {"id": 6, "name": "Enhanced Global Rankings Participation of 10 colleges", "percentage": 20, "target_date": "2028-02-29", "status": "pending"},
    {"id": 7, "name": "Final Evaluation and Reporting", "percentage": 10, "target_date": "2028-04-30", "status": "pending"}
]

def create_monthly_plan():
    months = []
    start_date = CONTRACT_START
    
    for i in range(24):
        month_end = start_date.replace(day=calendar.monthrange(start_date.year, start_date.month)[1])
        is_completed = start_date < CURRENT_DATE or (start_date.year == CURRENT_DATE.year and start_date.month < CURRENT_DATE.month)
        is_current = start_date.year == CURRENT_DATE.year and start_date.month == CURRENT_DATE.month
        
        months.append({
            "month_num": i + 1,
            "start_date": start_date,
            "end_date": month_end,
            "year": start_date.year,
            "month_name": start_date.strftime("%B"),
            "short_name": start_date.strftime("%b %Y"),
            "quarter": ((start_date.month - 1) // 3) + 1,
            "is_completed": is_completed,
            "is_current": is_current
        })
        
        if start_date.month == 12:
            start_date = start_date.replace(year=start_date.year + 1, month=1)
        else:
            start_date = start_date.replace(month=start_date.month + 1)
    
    return months

MONTHLY_PLAN = create_monthly_plan()

def create_activities_by_month():
    activities = {
        1: {
            "month": "May 2026",
            "status": "completed",
            "activities": [
                {"activity": "SANGAM Orientation & Training", "deliverable": "Training Completed", "due_date": "May 6, 2026", "status": "completed"},
                {"activity": "University Onboarding & Data Source Mapping", "deliverable": "Data Source Inventory", "due_date": "May 8, 2026", "status": "completed"},
                {"activity": "NIRF Data Collection", "deliverable": "NIRF Data Repository", "due_date": "May 20, 2026", "status": "completed"},
                {"activity": "Stakeholder Consultation Meetings", "deliverable": "Meeting Minutes", "due_date": "May 27, 2026", "status": "completed"},
                {"activity": "Inception Report & GRDAU Framework", "deliverable": "Inception Report", "due_date": "May 26, 2026", "status": "completed"},
                {"activity": "Monthly Progress Report Submission", "deliverable": "MPR May 2026", "due_date": "May 29, 2026", "status": "completed"},
            ]
        },
        2: {
            "month": "June 2026",
            "status": "current",
            "activities": [
                {"activity": "Complete Diagnostic Assessments across all 7 universities", "deliverable": "7 Diagnostic Reports", "due_date": "June 30, 2026", "status": "in_progress"},
                {"activity": "Continue baseline data collection and validation", "deliverable": "Validated Baseline Data", "due_date": "June 25, 2026", "status": "in_progress"},
                {"activity": "Establish GRDAU framework documentation", "deliverable": "GRDAU SOP Document", "due_date": "June 20, 2026", "status": "pending"},
                {"activity": "Conduct initial GRDAU training for university coordinators", "deliverable": "Training Session 1 Completed", "due_date": "June 15, 2026", "status": "in_progress"},
                {"activity": "Submit June MPR", "deliverable": "MPR June 2026", "due_date": "June 30, 2026", "status": "pending"},
            ]
        },
        3: {
            "month": "July 2026",
            "status": "upcoming",
            "activities": [
                {"activity": "Complete gap analysis against NIRF/NAAC/Global Rankings", "deliverable": "Gap Analysis Report", "due_date": "July 15, 2026", "status": "pending"},
                {"activity": "SWOT analysis for each university", "deliverable": "7 SWOT Reports", "due_date": "July 20, 2026", "status": "pending"},
                {"activity": "Finalize GRDAU establishment in all universities", "deliverable": "7 GRDAUs Operational", "due_date": "July 31, 2026", "status": "pending"},
                {"activity": "Submit July MPR", "deliverable": "MPR July 2026", "due_date": "July 31, 2026", "status": "pending"},
            ]
        },
        4: {
            "month": "August 2026",
            "status": "upcoming",
            "activities": [
                {"activity": "Develop Institutional Development Plans (IDPs)", "deliverable": "IDP Drafts", "due_date": "August 15, 2026", "status": "pending"},
                {"activity": "Stakeholder review of IDPs", "deliverable": "Stakeholder Feedback", "due_date": "August 25, 2026", "status": "pending"},
                {"activity": "Design data portal architecture", "deliverable": "Portal Design Document", "due_date": "August 31, 2026", "status": "pending"},
                {"activity": "Submit August MPR", "deliverable": "MPR August 2026", "due_date": "August 31, 2026", "status": "pending"},
            ]
        },
        5: {
            "month": "September 2026",
            "status": "upcoming",
            "activities": [
                {"activity": "Finalize IDPs with university approval", "deliverable": "7 Approved IDPs", "due_date": "September 15, 2026", "status": "pending"},
                {"activity": "Create performance monitoring dashboard mockups", "deliverable": "Dashboard Designs", "due_date": "September 20, 2026", "status": "pending"},
                {"activity": "MILESTONE 1: Establishment of Sustainable Data & Quality Systems", "deliverable": "Milestone Achievement Report", "due_date": "September 30, 2026", "status": "pending"},
                {"activity": "Submit September MPR", "deliverable": "MPR September 2026", "due_date": "September 30, 2026", "status": "pending"},
            ]
        },
        6: {
            "month": "October 2026",
            "status": "upcoming",
            "activities": [
                {"activity": "Complete dashboard development", "deliverable": "Dashboard Beta Version", "due_date": "October 15, 2026", "status": "pending"},
                {"activity": "MILESTONE 2: Institutional Development Plans and Execution Monitoring", "deliverable": "Milestone Achievement Report", "due_date": "October 31, 2026", "status": "pending"},
                {"activity": "Mid-term review preparation", "deliverable": "Mid-term Review Materials", "due_date": "October 25, 2026", "status": "pending"},
                {"activity": "Submit October MPR", "deliverable": "MPR October 2026", "due_date": "October 31, 2026", "status": "pending"},
            ]
        },
        7: {
            "month": "November 2026",
            "status": "upcoming",
            "activities": [
                {"activity": "Deploy data portal MVP", "deliverable": "Data Portal Live", "due_date": "November 15, 2026", "status": "pending"},
                {"activity": "Mid-term Progress Report submission", "deliverable": "Mid-term Report", "due_date": "November 30, 2026", "status": "pending"},
                {"activity": "Training needs assessment completion", "deliverable": "Training Needs Report", "due_date": "November 20, 2026", "status": "pending"},
                {"activity": "Submit November MPR", "deliverable": "MPR November 2026", "due_date": "November 30, 2026", "status": "pending"},
            ]
        },
        8: {
            "month": "December 2026",
            "status": "upcoming",
            "activities": [
                {"activity": "Launch performance dashboards", "deliverable": "Dashboards Deployed", "due_date": "December 10, 2026", "status": "pending"},
                {"activity": "Develop training modules", "deliverable": "Training Curriculum", "due_date": "December 15, 2026", "status": "pending"},
                {"activity": "MILESTONE 3: Capacity Building Participation", "deliverable": "Milestone Achievement Report", "due_date": "December 31, 2026", "status": "pending"},
                {"activity": "Submit December MPR", "deliverable": "MPR December 2026", "due_date": "December 31, 2026", "status": "pending"},
            ]
        },
        9: {
            "month": "January 2027",
            "status": "upcoming",
            "activities": [
                {"activity": "First round of training programs across all universities", "deliverable": "Training Completion Report", "due_date": "January 25, 2027", "status": "pending"},
                {"activity": "Data quality framework implementation", "deliverable": "Data Quality Framework", "due_date": "January 20, 2027", "status": "pending"},
                {"activity": "Submit January MPR", "deliverable": "MPR January 2027", "due_date": "January 31, 2027", "status": "pending"},
            ]
        },
        10: {
            "month": "February 2027",
            "status": "upcoming",
            "activities": [
                {"activity": "Data validation and quality improvement cycles", "deliverable": "Data Quality Report", "due_date": "February 20, 2027", "status": "pending"},
                {"activity": "Research output enhancement initiatives", "deliverable": "Research Enhancement Plan", "due_date": "February 25, 2027", "status": "pending"},
                {"activity": "Submit February MPR", "deliverable": "MPR February 2027", "due_date": "February 28, 2027", "status": "pending"},
            ]
        },
        11: {
            "month": "March 2027",
            "status": "upcoming",
            "activities": [
                {"activity": "International collaboration framework development", "deliverable": "Collaboration Framework", "due_date": "March 15, 2027", "status": "pending"},
                {"activity": "Outcome-based education (OBE) implementation support", "deliverable": "OBE Guidelines", "due_date": "March 20, 2027", "status": "pending"},
                {"activity": "Submit March MPR", "deliverable": "MPR March 2027", "due_date": "March 31, 2027", "status": "pending"},
            ]
        },
        12: {
            "month": "April 2027",
            "status": "upcoming",
            "activities": [
                {"activity": "Accreditation preparedness assessment", "deliverable": "Accreditation Readiness Report", "due_date": "April 15, 2027", "status": "pending"},
                {"activity": "Quality assurance framework implementation", "deliverable": "QA Framework", "due_date": "April 25, 2027", "status": "pending"},
                {"activity": "Submit April MPR", "deliverable": "MPR April 2027", "due_date": "April 30, 2027", "status": "pending"},
            ]
        },
        13: {
            "month": "May 2027",
            "status": "upcoming",
            "activities": [
                {"activity": "Year 1 performance review", "deliverable": "Annual Performance Report", "due_date": "May 15, 2027", "status": "pending"},
                {"activity": "Enhanced data collection and reporting", "deliverable": "Enhanced Data Repository", "due_date": "May 20, 2027", "status": "pending"},
                {"activity": "Submit May MPR", "deliverable": "MPR May 2027", "due_date": "May 31, 2027", "status": "pending"},
            ]
        },
        14: {
            "month": "June 2027",
            "status": "upcoming",
            "activities": [
                {"activity": "MILESTONE 4: Minimum 10% Improvement in Performance Indicators", "deliverable": "Milestone Achievement Report", "due_date": "June 30, 2027", "status": "pending"},
                {"activity": "Mid-year performance assessment", "deliverable": "Mid-year Assessment", "due_date": "June 25, 2027", "status": "pending"},
                {"activity": "Submit June MPR", "deliverable": "MPR June 2027", "due_date": "June 30, 2027", "status": "pending"},
            ]
        },
        15: {
            "month": "July 2027",
            "status": "upcoming",
            "activities": [
                {"activity": "Advanced training programs for GRDAU staff", "deliverable": "Advanced Training Report", "due_date": "July 20, 2027", "status": "pending"},
                {"activity": "Research publication support and tracking", "deliverable": "Publication Report", "due_date": "July 25, 2027", "status": "pending"},
                {"activity": "Submit July MPR", "deliverable": "MPR July 2027", "due_date": "July 31, 2027", "status": "pending"},
            ]
        },
        16: {
            "month": "August 2027",
            "status": "upcoming",
            "activities": [
                {"activity": "International ranking agency engagement", "deliverable": "Engagement Report", "due_date": "August 20, 2027", "status": "pending"},
                {"activity": "Dashboard enhancements based on feedback", "deliverable": "Enhanced Dashboards", "due_date": "August 25, 2027", "status": "pending"},
                {"activity": "Submit August MPR", "deliverable": "MPR August 2027", "due_date": "August 31, 2027", "status": "pending"},
            ]
        },
        17: {
            "month": "September 2027",
            "status": "upcoming",
            "activities": [
                {"activity": "Citation analysis and improvement strategies", "deliverable": "Citation Report", "due_date": "September 15, 2027", "status": "pending"},
                {"activity": "Employer perception enhancement initiatives", "deliverable": "Employer Engagement Report", "due_date": "September 20, 2027", "status": "pending"},
                {"activity": "Submit September MPR", "deliverable": "MPR September 2027", "due_date": "September 30, 2027", "status": "pending"},
            ]
        },
        18: {
            "month": "October 2027",
            "status": "upcoming",
            "activities": [
                {"activity": "Academic reputation building strategies", "deliverable": "Reputation Strategy Document", "due_date": "October 15, 2027", "status": "pending"},
                {"activity": "IPR and patent filing support", "deliverable": "IPR Status Report", "due_date": "October 25, 2027", "status": "pending"},
                {"activity": "Submit October MPR", "deliverable": "MPR October 2027", "due_date": "October 31, 2027", "status": "pending"},
            ]
        },
        19: {
            "month": "November 2027",
            "status": "upcoming",
            "activities": [
                {"activity": "SDG-aligned research promotion", "deliverable": "SDG Research Report", "due_date": "November 15, 2027", "status": "pending"},
                {"activity": "International student enrollment strategies", "deliverable": "Internationalization Plan", "due_date": "November 20, 2027", "status": "pending"},
                {"activity": "Submit November MPR", "deliverable": "MPR November 2027", "due_date": "November 30, 2027", "status": "pending"},
            ]
        },
        20: {
            "month": "December 2027",
            "status": "upcoming",
            "activities": [
                {"activity": "MILESTONE 5: Minimum 20% Improvement in Performance Indicators", "deliverable": "Milestone Achievement Report", "due_date": "December 31, 2027", "status": "pending"},
                {"activity": "Year-end performance review", "deliverable": "Year-end Report", "due_date": "December 20, 2027", "status": "pending"},
                {"activity": "Submit December MPR", "deliverable": "MPR December 2027", "due_date": "December 31, 2027", "status": "pending"},
            ]
        },
        21: {
            "month": "January 2028",
            "status": "upcoming",
            "activities": [
                {"activity": "Global ranking submission preparation", "deliverable": "Ranking Submission Package", "due_date": "January 20, 2028", "status": "pending"},
                {"activity": "Final round of capacity building", "deliverable": "Final Training Report", "due_date": "January 25, 2028", "status": "pending"},
                {"activity": "Submit January MPR", "deliverable": "MPR January 2028", "due_date": "January 31, 2028", "status": "pending"},
            ]
        },
        22: {
            "month": "February 2028",
            "status": "upcoming",
            "activities": [
                {"activity": "MILESTONE 6: Enhanced Global Rankings Participation of 10 colleges", "deliverable": "Milestone Achievement Report", "due_date": "February 29, 2028", "status": "pending"},
                {"activity": "Final dashboard and portal review", "deliverable": "Final System Review", "due_date": "February 25, 2028", "status": "pending"},
                {"activity": "Submit February MPR", "deliverable": "MPR February 2028", "due_date": "February 29, 2028", "status": "pending"},
            ]
        },
        23: {
            "month": "March 2028",
            "status": "upcoming",
            "activities": [
                {"activity": "Sustainability planning and handover documentation", "deliverable": "Sustainability Plan", "due_date": "March 15, 2028", "status": "pending"},
                {"activity": "Lessons learned documentation", "deliverable": "Lessons Learned Report", "due_date": "March 20, 2028", "status": "pending"},
                {"activity": "Submit March MPR", "deliverable": "MPR March 2028", "due_date": "March 31, 2028", "status": "pending"},
            ]
        },
        24: {
            "month": "April 2028",
            "status": "upcoming",
            "activities": [
                {"activity": "MILESTONE 7: Final Evaluation and Reporting", "deliverable": "Final Closure Report", "due_date": "April 30, 2028", "status": "pending"},
                {"activity": "Project closure and knowledge transfer", "deliverable": "Knowledge Transfer Report", "due_date": "April 25, 2028", "status": "pending"},
                {"activity": "Final MPR submission", "deliverable": "Final MPR", "due_date": "April 30, 2028", "status": "pending"},
                {"activity": "Handover of all project materials to MITRA", "deliverable": "Complete Project Documentation", "due_date": "April 30, 2028", "status": "pending"},
            ]
        }
    }
    return activities

ACTIVITIES_BY_MONTH = create_activities_by_month()

# Contract deliverables timeline
CONTRACT_DELIVERABLES = [
    {"deliverable": "Inception Report and Deployment Plan", "due_date": "2026-06-05", "status": "completed", "actual_date": "2026-05-26"},
    {"deliverable": "Diagnostic Assessment Reports (Institution-wise)", "due_date": "2026-07-05", "status": "pending", "actual_date": None},
    {"deliverable": "Institutional Development Plans (IDPs)", "due_date": "2026-08-14", "status": "pending", "actual_date": None},
    {"deliverable": "GRDAUs Established and Operationalized", "due_date": "2026-07-05", "status": "pending", "actual_date": None},
    {"deliverable": "Mid-term Progress Report", "due_date": "2026-11-02", "status": "pending", "actual_date": None},
    {"deliverable": "Training and Capacity Building Reports", "due_date": "Quarterly", "status": "pending", "actual_date": None},
    {"deliverable": "Dashboard Reports and Analytics", "due_date": "Monthly from day 60", "status": "in_progress", "actual_date": None},
    {"deliverable": "Final Closure Report and Recommendations", "due_date": "2028-05-06", "status": "pending", "actual_date": None}
]

# Risk Register
RISK_REGISTER = [
    {"risk": "Data availability and quality issues from universities", "probability": "High", "impact": "High", "mitigation": "Early data audit, continuous validation, escalation mechanism", "owner": "Project Lead"},
    {"risk": "Delay in GRDAU establishment due to university bureaucracy", "probability": "Medium", "impact": "High", "mitigation": "Regular follow-ups, escalation to MITRA, weekly coordination meetings", "owner": "Institutional Coordinators"},
    {"risk": "Resource attrition or unavailability", "probability": "Medium", "impact": "Medium", "mitigation": "Cross-training, backup resources, 15-day replacement notice", "owner": "HR Team"},
    {"risk": "Technology infrastructure limitations", "probability": "Low", "impact": "Medium", "mitigation": "Cloud-based solutions, compatibility assessment, alternative plans", "owner": "Data Analytics Specialist"},
    {"risk": "Non-achievement of performance improvement targets", "probability": "Medium", "impact": "High", "mitigation": "Regular monitoring, corrective action plans, stakeholder engagement", "owner": "Project Lead"},
    {"risk": "World Bank compliance and audit issues", "probability": "Low", "impact": "High", "mitigation": "Strict adherence to guidelines, proper documentation, regular internal audits", "owner": "Compliance Officer"}
]

def render_sidebar():
    with st.sidebar:
        st.markdown("### 📋 MahaSTRIDE")
        st.markdown("---")
        
        menu_options = {
            "🏠 Dashboard": "dashboard",
            "✅ May 2026": "may",
            "📅 24-Month Plan": "plan",
            "👥 Team": "team",
            "🎯 Milestones": "milestones",
            "📋 Deliverables": "deliverables",
            "⚠️ Risks": "risks"
        }
        
        selected = st.radio(
            "Navigation",
            options=list(menu_options.keys()),
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        completed_months = sum(1 for m in MONTHLY_PLAN if m["is_completed"])
        progress_pct = (completed_months / 24) * 100
        
        st.markdown("### 📈 Project Progress")
        st.progress(progress_pct / 100)
        st.caption(f"{completed_months}/24 months completed ({progress_pct:.0f}%)")
        
        st.markdown("---")
        
        st.info(f"""
        **Project Details**
        - 📅 Start Date: 06 May 2026
        - 📅 End Date: 06 May 2028
        - 🏫 Universities: 7
        - 👥 Team Size: 11 members
        - 📊 Duration: 24 months
        """)
        
        upcoming = [m for m in MILESTONES if m["status"] == "pending"][:3]
        st.markdown("### 🎯 Upcoming Milestones")
        for m in upcoming:
            st.caption(f"• {m['name'][:35]}...")
            st.caption(f"  📅 {m['target_date']}")
        
        return menu_options[selected]

def render_dashboard():
    st.header("📊 Project Dashboard")
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        days_remaining = (CONTRACT_END - CURRENT_DATE).days
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin:0; color:#2a5298;">{days_remaining}</h3>
            <p style="margin:0; color:#666;">Days Remaining</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        completed_months = sum(1 for m in MONTHLY_PLAN if m["is_completed"])
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin:0; color:#28a745;">{completed_months}/24</h3>
            <p style="margin:0; color:#666;">Months Completed</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        completed_deliverables = sum(1 for d in CONTRACT_DELIVERABLES if d["status"] == "completed")
        total_deliverables = len(CONTRACT_DELIVERABLES)
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin:0; color:#17a2b8;">{completed_deliverables}/{total_deliverables}</h3>
            <p style="margin:0; color:#666;">Key Deliverables</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin:0; color:#6f42c1;">{len(UNIVERSITIES)}</h3>
            <p style="margin:0; color:#666;">Universities</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Time Progress")
        completed_months = sum(1 for m in MONTHLY_PLAN if m["is_completed"])
        progress_percent = (completed_months / 24) * 100
        st.progress(progress_percent / 100)
        st.caption(f"{progress_percent:.1f}% complete")
    
    with col2:
        st.subheader("🎯 Milestone Progress")
        completed_milestones = sum(1 for m in MILESTONES if m["status"] == "completed")
        milestone_progress = (completed_milestones / len(MILESTONES)) * 100
        st.progress(milestone_progress / 100)
        st.caption(f"{completed_milestones}/{len(MILESTONES)} milestones completed ({milestone_progress:.0f}%)")
    
    st.markdown("---")
    
    st.subheader("🎯 Current Focus - June 2026")
    
    current_activities = ACTIVITIES_BY_MONTH[2]["activities"]
    for activity in current_activities:
        if activity["status"] == "in_progress":
            st.markdown(f"""
            <div class="info-card">
                🔄 <strong>{activity['activity']}</strong><br>
                📦 Deliverable: {activity['deliverable']}<br>
                📅 Due: {activity['due_date']}
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("📊 Weekly Snapshot")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="success-card">
            <strong>✅ Completed This Week</strong><br>
            • Diagnostic assessment framework finalized<br>
            • GRDAU training materials prepared<br>
            • Data collection templates distributed
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="warning-card">
            <strong>⚠️ In Progress</strong><br>
            • Diagnostic assessments at 7 universities<br>
            • Baseline data validation<br>
            • Stakeholder coordination meetings
        </div>
        """, unsafe_allow_html=True)

def render_may_completed():
    st.header("✅ May 2026 - Month 1 Completed")
    st.markdown("---")
    
    st.subheader("👥 Team Attendance - May 2026")
    
    team_data = []
    for level, members in TEAM_STRUCTURE.items():
        for member in members:
            team_data.append({
                "Level": level,
                "Role": member["role"],
                "Name": member["name"],
                "Present Days": member.get("present_days_may", 19),
                "Absent": member.get("absent", 0),
                "Holidays": member.get("holidays", 12),
                "Location": member.get("location", member.get("university", ""))
            })
    
    df_team = pd.DataFrame(team_data)
    st.dataframe(df_team, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    st.subheader("✅ Activities Completed in May 2026")
    
    for activity in COMPLETED_MAY_ACTIVITIES:
        st.markdown(f"""
        <div class="deliverable-card">
            <span class="completed-badge">COMPLETED</span>
            <strong>{activity['activity']}</strong><br>
            📅 {activity['date']} | 👥 {activity['team']}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.subheader("📝 Meetings Conducted in May 2026")
    
    meetings_df = pd.DataFrame(COMPLETED_MAY_MEETINGS)
    st.dataframe(meetings_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    st.subheader("🏆 Key Accomplishments - May 2026")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("""
        **🎓 SANGAM Training Completed**
        - 3-day intensive orientation (May 4-6)
        - All 10 coordinators trained
        - GRDAU concept introduced successfully
        """)
        
        st.success("""
        **🏫 University Onboarding**
        - All 7 universities onboarded
        - Data source mapping completed
        - Nodal officers identified
        """)
    
    with col2:
        st.success("""
        **📊 NIRF Data Collection**
        - Student, Faculty, Research data collected
        - Placement and Finance data gathered
        - Baseline data repository created
        """)
        
        st.success("""
        **📄 Inception Report**
        - Framework developed
        - GRDAU structure defined
        - Submitted as per contract (May 26, 2026)
        """)
    
    st.markdown("---")
    
    st.subheader("📄 Monthly Progress Report (MPR) - May 2026")
    st.info("""
    **MPR submitted on: 29 May 2026**
    - Submitted to: PMU, MahaSTRIDE at pmu.mahastride@mahamitra.org
    - Approved by: Nominated Nodal Officer and Registrar
    - Copy sent to: Hon. Vice Chancellor and Project Director, MahaSTRIDE
    """)

def render_plan():
    st.header("📅 24-Month Project Plan (May 2026 - April 2028)")
    st.markdown("---")
    
    phases = [
        ("Phase 1: Foundation (Months 1-3)", [1, 2, 3]),
        ("Phase 2: Planning (Months 4-6)", [4, 5, 6]),
        ("Phase 3: Implementation (Months 7-12)", [7, 8, 9, 10, 11, 12]),
        ("Phase 4: Enhancement (Months 13-18)", [13, 14, 15, 16, 17, 18]),
        ("Phase 5: Finalization (Months 19-24)", [19, 20, 21, 22, 23, 24])
    ]
    
    selected_phase = st.radio(
        "Select Phase",
        options=[p[0] for p in phases],
        horizontal=True
    )
    
    phase_months = [p[1] for p in phases if p[0] == selected_phase][0]
    
    for month_num in phase_months:
        month_data = ACTIVITIES_BY_MONTH[month_num]
        
        if month_data["status"] == "completed":
            status_icon = "✅"
            status_color = "success-card"
        elif month_data["status"] == "current":
            status_icon = "🔄"
            status_color = "info-card"
        else:
            status_icon = "⏳"
            status_color = "warning-card"
        
        st.markdown(f"""
        <div class="{status_color}">
            <h3>{status_icon} {month_data['month']}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        for activity in month_data["activities"]:
            if activity["status"] == "completed":
                icon = "✅"
            elif activity["status"] == "in_progress":
                icon = "🔄"
            else:
                icon = "📅"
            st.markdown(f"- {icon} **{activity['activity']}** - *{activity['deliverable']}* (Due: {activity['due_date']})")
        
        st.markdown("---")
    
    st.subheader("📊 Monthly Activity Summary")
    
    summary_data = []
    for month_num, month_data in ACTIVITIES_BY_MONTH.items():
        summary_data.append({
            "Month": month_data["month"],
            "Status": month_data["status"].upper(),
            "Total Activities": len(month_data["activities"]),
            "Completed": sum(1 for a in month_data["activities"] if a["status"] == "completed"),
            "In Progress": sum(1 for a in month_data["activities"] if a["status"] == "in_progress")
        })
    
    df_summary = pd.DataFrame(summary_data)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_summary["Month"], y=df_summary["Completed"], name="Completed", marker_color="#28a745"))
    fig.add_trace(go.Bar(x=df_summary["Month"], y=df_summary["In Progress"], name="In Progress", marker_color="#ffc107"))
    fig.update_layout(title="Activities by Month", xaxis_title="Month", yaxis_title="Number of Activities", barmode="stack", height=500)
    st.plotly_chart(fig, use_container_width=True)

def render_team():
    st.header("👥 Team Structure & Resources")
    st.markdown("---")
    
    st.subheader("🏢 MITRA Level Resources")
    mitra_df = pd.DataFrame(TEAM_STRUCTURE["MITRA Level"])
    st.dataframe(mitra_df, use_container_width=True, hide_index=True)
    
    st.subheader("🏫 University Level Resources (GRDAU Coordinators)")
    uni_df = pd.DataFrame(TEAM_STRUCTURE["University Level"])
    st.dataframe(uni_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    st.subheader("📊 Deployment Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Personnel", "11", delta=None)
    with col2:
        st.metric("MITRA Level", "2", delta=None)
    with col3:
        st.metric("University Level", "9", delta="Across 7 universities")
    with col4:
        st.metric("Universities Covered", "7", delta=None)
    
    st.markdown("---")
    
    st.subheader("📋 Resource Requirements (as per contract)")
    
    requirements = pd.DataFrame({
        "Requirement": [
            "Prior written approval for any resource change",
            "15 days advance notice for replacement with CV",
            "MITRA reserves right to reject replacement",
            "Unauthorized substitution may attract penalty",
            "All personnel bound by confidentiality",
            "Monthly attendance and MPR mandatory for payment"
        ]
    })
    st.dataframe(requirements, use_container_width=True, hide_index=True)
    
    st.subheader("📝 Leave Approval Mechanism (as per SOP)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("**University Level Resources**")
        st.write("1. Obtain leave approval on email from Project Head (ICARE)")
        st.write("2. Copy to Nominated Nodal Officer from respective University")
    
    with col2:
        st.info("**MITRA Level Resources**")
        st.write("1. Obtain leave approval on email from Project Head (ICARE)")
        st.write("2. Project Head to copy Sector Expert, HR, MITRA")

def render_milestones():
    st.header("🎯 Milestones Tracker")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Milestone Distribution")
        
        fig = go.Figure(data=[go.Pie(
            labels=[m["name"][:30] + "..." for m in MILESTONES],
            values=[m["percentage"] for m in MILESTONES],
            hole=0.4,
            marker_colors=['#2a5298', '#28a745', '#ffc107', '#dc3545', '#17a2b8', '#6f42c1', '#fd7e14']
        )])
        fig.update_layout(title="Milestone Weightage Distribution", height=450)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📈 Milestone Status")
        
        milestone_df = pd.DataFrame([{
            "Milestone": m["name"][:35] + ("..." if len(m["name"]) > 35 else ""),
            "Target Date": m["target_date"],
            "Status": m["status"].upper(),
            "Weight": f"{m['percentage']}%"
        } for m in MILESTONES])
        
        st.dataframe(milestone_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    st.subheader("📅 Milestone Timeline")
    
    for m in MILESTONES:
        if m["status"] == "completed":
            icon = "✅"
            color = "#d4edda"
        elif m["status"] == "in_progress":
            icon = "🔄"
            color = "#fff3cd"
        else:
            icon = "⏳"
            color = "#f8f9fa"
        
        st.markdown(f"""
        <div style="background-color:{color}; padding:0.75rem; border-left:3px solid #2a5298; margin-bottom:0.5rem; border-radius:5px;">
            <strong>{icon} {m['name']}</strong><br>
            📅 Target: {m['target_date']} | Status: {m['status'].upper()} | Weight: {m['percentage']}%
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.subheader("📋 Expected Outcomes (Performance-Linked)")
    
    outcomes = {
        "Enhanced Global Rankings Participation": "Successful participation of institutions on minimum two global ranking platforms",
        "Minimum 20% Improvement": "Validation of comparative data between baseline and endline diagnostics",
        "Establishment of Sustainable Data & Quality Systems": "Certification of GRDAU readiness and dashboard deployment",
        "Institutional Development Plans": "Finalization and institutional sign-off of all IDPs",
        "Capacity Building Participation": "Minimum 60% participation of IQAC faculty and staff",
        "Final Evaluation": "Approval of final report and satisfactory project closure"
    }
    
    for outcome, metric in outcomes.items():
        st.markdown(f"""
        <div class="info-card">
            <strong>🏆 {outcome}</strong><br>
            📊 {metric}
        </div>
        """, unsafe_allow_html=True)

def render_deliverables():
    st.header("📋 Contract Deliverables Tracker")
    st.markdown("---")
    
    completed = sum(1 for d in CONTRACT_DELIVERABLES if d["status"] == "completed")
    in_progress = sum(1 for d in CONTRACT_DELIVERABLES if d["status"] == "in_progress")
    pending = sum(1 for d in CONTRACT_DELIVERABLES if d["status"] == "pending")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("✅ Completed", completed)
    with col2:
        st.metric("🔄 In Progress", in_progress)
    with col3:
        st.metric("⏳ Pending", pending)
    
    st.markdown("---")
    
    for deliverable in CONTRACT_DELIVERABLES:
        if deliverable["status"] == "completed":
            icon = "✅"
            color = "#d4edda"
        elif deliverable["status"] == "in_progress":
            icon = "🔄"
            color = "#fff3cd"
        else:
            icon = "⏳"
            color = "#f8f9fa"
        
        actual_text = f"<br>✅ Actual Submission: {deliverable['actual_date']}" if deliverable.get('actual_date') else ""
        
        st.markdown(f"""
        <div style="background-color:{color}; padding:1rem; margin:0.5rem 0; border-radius:8px;">
            <strong>{icon} {deliverable['deliverable']}</strong><br>
            📅 Due: {deliverable['due_date']}<br>
            📊 Status: {deliverable['status'].upper()}
            {actual_text}
        </div>
        """, unsafe_allow_html=True)

def render_risks():
    st.header("⚠️ Risk Management & Compliance")
    st.markdown("---")
    
    st.subheader("📋 Risk Register")
    
    risk_df = pd.DataFrame(RISK_REGISTER)
    st.dataframe(risk_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    st.subheader("📊 Risk Matrix")
    
    risk_data = []
    for risk in RISK_REGISTER:
        prob_score = 3 if risk["probability"] == "High" else 2 if risk["probability"] == "Medium" else 1
        impact_score = 3 if risk["impact"] == "High" else 2 if risk["impact"] == "Medium" else 1
        risk_data.append({
            "Risk": risk["risk"][:40],
            "Probability Score": prob_score,
            "Impact Score": impact_score,
            "Risk Score": prob_score * impact_score,
            "Probability": risk["probability"],
            "Impact": risk["impact"]
        })
    
    risk_df2 = pd.DataFrame(risk_data)
    
    fig = px.scatter(risk_df2, x="Probability Score", y="Impact Score", 
                     size="Risk Score", text="Risk", 
                     title="Risk Matrix (Bubble size = Risk Priority)",
                     labels={"Probability Score": "Probability (1=Low, 3=High)", 
                            "Impact Score": "Impact (1=Low, 3=High)"})
    fig.update_traces(textposition="top center")
    st.plotly_chart(fig, use_container_width=True)
    
    # Risk summary
    col1, col2, col3 = st.columns(3)
    high_risks = [r for r in RISK_REGISTER if r["probability"] == "High" and r["impact"] == "High"]
    medium_risks = [r for r in RISK_REGISTER if r["probability"] == "Medium" or r["impact"] == "Medium"]
    low_risks = [r for r in RISK_REGISTER if r["probability"] == "Low" and r["impact"] == "Low"]
    
    with col1:
        st.metric("🔴 High Priority Risks", len(high_risks))
    with col2:
        st.metric("🟡 Medium Priority Risks", len(medium_risks))
    with col3:
        st.metric("🟢 Low Priority Risks", len(low_risks))
    
    st.markdown("---")
    
    st.subheader("⚖️ Penalty Provisions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="warning-card">
            <strong>⚠️ Milestone Penalty</strong><br>
            • Fine up to applicable percentage of milestone value for non-completion<br>
            • Applicable if compliance report not submitted as described
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="warning-card">
            <strong>⚠️ Overall Penalty</strong><br>
            • Maximum penalty as per contract terms<br>
            • For breach of contract conditions<br>
            • For unsatisfactory performance<br>
            • For delay in prescribed timelines
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.subheader("🔴 Termination Conditions")
    
    termination_reasons = [
        "Failure to remedy breach within 30 days of notice",
        "Insolvency or bankruptcy",
        "False or misleading information during bid submission",
        "Force Majeure Event lasting 60+ continuous days",
        "Defect, inadequacy, or incompetence in performance",
        "MITRA's sole discretion (with 30 days written notice)"
    ]
    
    for reason in termination_reasons:
        st.markdown(f"- {reason}")
    
    st.markdown("---")
    
    st.subheader("🔒 Fraud and Corruption Compliance")
    st.info("""
    **World Bank Guidelines on Preventing and Combating Fraud and Corruption**
    - Program-for-Results Financing guidelines
    - Anti-Corruption Guidelines shall prevail in case of conflict
    - MITRA as nodal agency ensures compliance
    """)
    
    st.markdown("---")
    
    st.subheader("⚖️ Jurisdiction")
    st.warning("""
    - **Governing Law:** Laws in force in India
    - **Exclusive Jurisdiction:** Courts at Mumbai, India
    - **Arbitration:** As per Arbitration and Conciliation Act
    """)
    
    st.markdown("---")
    
    st.subheader("🔐 Confidentiality Obligations")
    st.write("""
    - All plans, data, reports, and specifications are property of MITRA
    - No publication or speech without prior written consent
    - All materials to be handed over upon request/termination/completion
    - Confidentiality survives termination of contract
    """)

# Main execution
selected = render_sidebar()

if selected == "dashboard":
    render_dashboard()
elif selected == "may":
    render_may_completed()
elif selected == "plan":
    render_plan()
elif selected == "team":
    render_team()
elif selected == "milestones":
    render_milestones()
elif selected == "deliverables":
    render_deliverables()
elif selected == "risks":
    render_risks()

# Footer
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #666; font-size: 0.8rem;">
    <p>© 2026 Maharashtra Institution for Transformation (MITRA) | MahaSTRIDE Project | World Bank Loan No: IBRD 9737-IN</p>
    <p>Last Updated: {datetime.now().strftime('%d %B %Y, %H:%M:%S')}</p>
    <p>ICARE Pvt. Ltd. - Consultant | Duration: 24 months (May 2026 - April 2028)</p>
</div>
""", unsafe_allow_html=True)
