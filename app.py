import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import calendar
from streamlit_option_menu import option_menu

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
    .status-completed {
        background-color: #28a745;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        display: inline-block;
    }
    .status-in-progress {
        background-color: #ffc107;
        color: #333;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        display: inline-block;
    }
    .status-pending {
        background-color: #dc3545;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        display: inline-block;
    }
    .status-upcoming {
        background-color: #17a2b8;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        display: inline-block;
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
    .month-header-completed {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 0.5rem 1rem;
        margin: 0.5rem 0;
        border-radius: 5px;
    }
    .month-header-current {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 0.5rem 1rem;
        margin: 0.5rem 0;
        border-radius: 5px;
    }
    .month-header-upcoming {
        background-color: #e7f3ff;
        border-left: 4px solid #17a2b8;
        padding: 0.5rem 1rem;
        margin: 0.5rem 0;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Project Constants
PROJECT_NAME = "MahaSTRIDE - University Ranking Framework Project"
CLIENT = "Maharashtra Institution for Transformation (MITRA)"
CONSULTANT = "Indian Centre for Academic Rankings & Excellence - ICARE Pvt. Ltd."
CONTRACT_VALUE = 44841888  # Rs.
CONTRACT_START = datetime(2026, 5, 6)
CONTRACT_END = datetime(2028, 5, 6)
CURRENT_DATE = datetime(2026, 6, 4)  # Today's date

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

# Milestone payments (30% of contract)
MILESTONES = [
    {"id": 1, "name": "Establishment of Sustainable Data & Quality Systems", "percentage": 10, "target_date": "2026-09-30", "status": "pending"},
    {"id": 2, "name": "Institutional Development Plans and Execution Monitoring", "percentage": 10, "target_date": "2026-10-31", "status": "pending"},
    {"id": 3, "name": "Capacity Building Participation", "percentage": 10, "target_date": "2026-12-31", "status": "pending"},
    {"id": 4, "name": "Minimum 10% Improvement in Performance Indicators in 5% of colleges across 7 Universities", "percentage": 15, "target_date": "2027-06-30", "status": "pending"},
    {"id": 5, "name": "Minimum 20% Improvement in Performance Indicators in 20% of colleges across 7 Universities", "percentage": 25, "target_date": "2027-12-31", "status": "pending"},
    {"id": 6, "name": "Enhanced Global Rankings Participation of 10 colleges", "percentage": 20, "target_date": "2028-02-29", "status": "pending"},
    {"id": 7, "name": "Final Evaluation and Reporting", "percentage": 10, "target_date": "2028-04-30", "status": "pending"}
]

# Create comprehensive 24-month activity plan (including May 2026)
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
        
        # Move to next month
        if start_date.month == 12:
            start_date = start_date.replace(year=start_date.year + 1, month=1)
        else:
            start_date = start_date.replace(month=start_date.month + 1)
    
    return months

MONTHLY_PLAN = create_monthly_plan()

# Comprehensive activities for entire 24 months
def create_activities_by_month():
    activities = {
        # Month 1: May 2026 - COMPLETED
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
        # Month 2: June 2026
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
        # Month 3: July 2026
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
        # Month 4: August 2026
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
        # Month 5: September 2026
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
        # Month 6: October 2026
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
        # Month 7: November 2026
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
        # Month 8: December 2026
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
        # Month 9: January 2027
        9: {
            "month": "January 2027",
            "status": "upcoming",
            "activities": [
                {"activity": "First round of training programs across all universities", "deliverable": "Training Completion Report", "due_date": "January 25, 2027", "status": "pending"},
                {"activity": "Data quality framework implementation", "deliverable": "Data Quality Framework", "due_date": "January 20, 2027", "status": "pending"},
                {"activity": "Submit January MPR", "deliverable": "MPR January 2027", "due_date": "January 31, 2027", "status": "pending"},
            ]
        },
        # Month 10: February 2027
        10: {
            "month": "February 2027",
            "status": "upcoming",
            "activities": [
                {"activity": "Data validation and quality improvement cycles", "deliverable": "Data Quality Report", "due_date": "February 20, 2027", "status": "pending"},
                {"activity": "Research output enhancement initiatives", "deliverable": "Research Enhancement Plan", "due_date": "February 25, 2027", "status": "pending"},
                {"activity": "Submit February MPR", "deliverable": "MPR February 2027", "due_date": "February 28, 2027", "status": "pending"},
            ]
        },
        # Month 11: March 2027
        11: {
            "month": "March 2027",
            "status": "upcoming",
            "activities": [
                {"activity": "International collaboration framework development", "deliverable": "Collaboration Framework", "due_date": "March 15, 2027", "status": "pending"},
                {"activity": "Outcome-based education (OBE) implementation support", "deliverable": "OBE Guidelines", "due_date": "March 20, 2027", "status": "pending"},
                {"activity": "Submit March MPR", "deliverable": "MPR March 2027", "due_date": "March 31, 2027", "status": "pending"},
            ]
        },
        # Month 12: April 2027
        12: {
            "month": "April 2027",
            "status": "upcoming",
            "activities": [
                {"activity": "Accreditation preparedness assessment", "deliverable": "Accreditation Readiness Report", "due_date": "April 15, 2027", "status": "pending"},
                {"activity": "Quality assurance framework implementation", "deliverable": "QA Framework", "due_date": "April 25, 2027", "status": "pending"},
                {"activity": "Submit April MPR", "deliverable": "MPR April 2027", "due_date": "April 30, 2027", "status": "pending"},
            ]
        },
        # Month 13: May 2027 - Year 2 begins
        13: {
            "month": "May 2027",
            "status": "upcoming",
            "activities": [
                {"activity": "Year 1 performance review", "deliverable": "Annual Performance Report", "due_date": "May 15, 2027", "status": "pending"},
                {"activity": "Enhanced data collection and reporting", "deliverable": "Enhanced Data Repository", "due_date": "May 20, 2027", "status": "pending"},
                {"activity": "Submit May MPR", "deliverable": "MPR May 2027", "due_date": "May 31, 2027", "status": "pending"},
            ]
        },
        # Month 14: June 2027
        14: {
            "month": "June 2027",
            "status": "upcoming",
            "activities": [
                {"activity": "MILESTONE 4: Minimum 10% Improvement in Performance Indicators", "deliverable": "Milestone Achievement Report", "due_date": "June 30, 2027", "status": "pending"},
                {"activity": "Mid-year performance assessment", "deliverable": "Mid-year Assessment", "due_date": "June 25, 2027", "status": "pending"},
                {"activity": "Submit June MPR", "deliverable": "MPR June 2027", "due_date": "June 30, 2027", "status": "pending"},
            ]
        },
        # Month 15: July 2027
        15: {
            "month": "July 2027",
            "status": "upcoming",
            "activities": [
                {"activity": "Advanced training programs for GRDAU staff", "deliverable": "Advanced Training Report", "due_date": "July 20, 2027", "status": "pending"},
                {"activity": "Research publication support and tracking", "deliverable": "Publication Report", "due_date": "July 25, 2027", "status": "pending"},
                {"activity": "Submit July MPR", "deliverable": "MPR July 2027", "due_date": "July 31, 2027", "status": "pending"},
            ]
        },
        # Month 16: August 2027
        16: {
            "month": "August 2027",
            "status": "upcoming",
            "activities": [
                {"activity": "International ranking agency engagement", "deliverable": "Engagement Report", "due_date": "August 20, 2027", "status": "pending"},
                {"activity": "Dashboard enhancements based on feedback", "deliverable": "Enhanced Dashboards", "due_date": "August 25, 2027", "status": "pending"},
                {"activity": "Submit August MPR", "deliverable": "MPR August 2027", "due_date": "August 31, 2027", "status": "pending"},
            ]
        },
        # Month 17: September 2027
        17: {
            "month": "September 2027",
            "status": "upcoming",
            "activities": [
                {"activity": "Citation analysis and improvement strategies", "deliverable": "Citation Report", "due_date": "September 15, 2027", "status": "pending"},
                {"activity": "Employer perception enhancement initiatives", "deliverable": "Employer Engagement Report", "due_date": "September 20, 2027", "status": "pending"},
                {"activity": "Submit September MPR", "deliverable": "MPR September 2027", "due_date": "September 30, 2027", "status": "pending"},
            ]
        },
        # Month 18: October 2027
        18: {
            "month": "October 2027",
            "status": "upcoming",
            "activities": [
                {"activity": "Academic reputation building strategies", "deliverable": "Reputation Strategy Document", "due_date": "October 15, 2027", "status": "pending"},
                {"activity": "IPR and patent filing support", "deliverable": "IPR Status Report", "due_date": "October 25, 2027", "status": "pending"},
                {"activity": "Submit October MPR", "deliverable": "MPR October 2027", "due_date": "October 31, 2027", "status": "pending"},
            ]
        },
        # Month 19: November 2027
        19: {
            "month": "November 2027",
            "status": "upcoming",
            "activities": [
                {"activity": "SDG-aligned research promotion", "deliverable": "SDG Research Report", "due_date": "November 15, 2027", "status": "pending"},
                {"activity": "International student enrollment strategies", "deliverable": "Internationalization Plan", "due_date": "November 20, 2027", "status": "pending"},
                {"activity": "Submit November MPR", "deliverable": "MPR November 2027", "due_date": "November 30, 2027", "status": "pending"},
            ]
        },
        # Month 20: December 2027
        20: {
            "month": "December 2027",
            "status": "upcoming",
            "activities": [
                {"activity": "MILESTONE 5: Minimum 20% Improvement in Performance Indicators", "deliverable": "Milestone Achievement Report", "due_date": "December 31, 2027", "status": "pending"},
                {"activity": "Year-end performance review", "deliverable": "Year-end Report", "due_date": "December 20, 2027", "status": "pending"},
                {"activity": "Submit December MPR", "deliverable": "MPR December 2027", "due_date": "December 31, 2027", "status": "pending"},
            ]
        },
        # Month 21: January 2028
        21: {
            "month": "January 2028",
            "status": "upcoming",
            "activities": [
                {"activity": "Global ranking submission preparation", "deliverable": "Ranking Submission Package", "due_date": "January 20, 2028", "status": "pending"},
                {"activity": "Final round of capacity building", "deliverable": "Final Training Report", "due_date": "January 25, 2028", "status": "pending"},
                {"activity": "Submit January MPR", "deliverable": "MPR January 2028", "due_date": "January 31, 2028", "status": "pending"},
            ]
        },
        # Month 22: February 2028
        22: {
            "month": "February 2028",
            "status": "upcoming",
            "activities": [
                {"activity": "MILESTONE 6: Enhanced Global Rankings Participation of 10 colleges", "deliverable": "Milestone Achievement Report", "due_date": "February 29, 2028", "status": "pending"},
                {"activity": "Final dashboard and portal review", "deliverable": "Final System Review", "due_date": "February 25, 2028", "status": "pending"},
                {"activity": "Submit February MPR", "deliverable": "MPR February 2028", "due_date": "February 29, 2028", "status": "pending"},
            ]
        },
        # Month 23: March 2028
        23: {
            "month": "March 2028",
            "status": "upcoming",
            "activities": [
                {"activity": "Sustainability planning and handover documentation", "deliverable": "Sustainability Plan", "due_date": "March 15, 2028", "status": "pending"},
                {"activity": "Lessons learned documentation", "deliverable": "Lessons Learned Report", "due_date": "March 20, 2028", "status": "pending"},
                {"activity": "Submit March MPR", "deliverable": "MPR March 2028", "due_date": "March 31, 2028", "status": "pending"},
            ]
        },
        # Month 24: April 2028
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

# Contract deliverables timeline (from contract document)
CONTRACT_DELIVERABLES = [
    {"deliverable": "Inception Report and Deployment Plan", "due_days": 30, "due_date": "2026-06-05", "status": "completed", "actual_date": "2026-05-26"},
    {"deliverable": "Diagnostic Assessment Reports (Institution-wise)", "due_days": 60, "due_date": "2026-07-05", "status": "pending", "actual_date": None},
    {"deliverable": "Institutional Development Plans (IDPs)", "due_days": 100, "due_date": "2026-08-14", "status": "pending", "actual_date": None},
    {"deliverable": "GRDAUs Established and Operationalized", "due_days": 60, "due_date": "2026-07-05", "status": "pending", "actual_date": None},
    {"deliverable": "Mid-term Progress Report", "due_days": 180, "due_date": "2026-11-02", "status": "pending", "actual_date": None},
    {"deliverable": "Training and Capacity Building Reports", "due_days": "Quarterly", "due_date": "Quarterly", "status": "pending", "actual_date": None},
    {"deliverable": "Dashboard Reports and Analytics", "due_days": "Monthly", "due_date": "Monthly from day 60", "status": "in_progress", "actual_date": None},
    {"deliverable": "Final Closure Report and Recommendations", "due_days": "End of 24 months", "due_date": "2028-05-06", "status": "pending", "actual_date": None}
]

# Sidebar Navigation
with st.sidebar:
    st.markdown("### 📋 MahaSTRIDE")
    st.markdown("---")
    
    selected = option_menu(
        menu_title=None,
        options=["Dashboard", "May 2026 - Completed", "24-Month Plan", "Team & Resources", "Milestones & Payments", "Deliverables Tracker", "Risk & Compliance"],
        icons=["house", "check-circle", "calendar-month", "people", "currency-dollar", "list-check", "shield"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "#2a5298", "font-size": "1.2rem"},
            "nav-link": {"font-size": "0.9rem", "text-align": "left", "margin": "0.1rem 0"},
            "nav-link-selected": {"background-color": "#2a5298"},
        }
    )
    
    st.divider()
    st.info(f"""
    **Project Details**
    - Contract Value: ₹{CONTRACT_VALUE:,.0f}
    - Start Date: 06 May 2026
    - End Date: 06 May 2028
    - Duration: 24 months
    """)

# Main Content
st.markdown(f"""
<div class="main-header">
    <h1>📊 {PROJECT_NAME}</h1>
    <p><strong>Client:</strong> {CLIENT} | <strong>Consultant:</strong> {CONSULTANT}</p>
    <p>World Bank Loan No: IBRD 9737-IN | RFP Ref: IN-MITRA(PMU)-PforR-Edu-QCBS</p>
</div>
""", unsafe_allow_html=True)

# Dashboard View
if selected == "Dashboard":
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        days_remaining = (CONTRACT_END - CURRENT_DATE).days
        st.markdown(f"""
        <div class="metric-card">
            <h3>📅 {days_remaining}</h3>
            <p>Days Remaining</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        completed_months = sum(1 for m in MONTHLY_PLAN if m["is_completed"])
        st.markdown(f"""
        <div class="metric-card">
            <h3>✅ {completed_months}/24</h3>
            <p>Months Completed</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        completed_deliverables = sum(1 for d in CONTRACT_DELIVERABLES if d["status"] == "completed")
        total_deliverables = len(CONTRACT_DELIVERABLES)
        st.markdown(f"""
        <div class="metric-card">
            <h3>📋 {completed_deliverables}/{total_deliverables}</h3>
            <p>Key Deliverables</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🏫 {len(UNIVERSITIES)}</h3>
            <p>Universities</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Progress Bars
    st.subheader("📈 Overall Project Progress")
    
    col1, col2 = st.columns(2)
    
    with col1:
        completed_months = sum(1 for m in MONTHLY_PLAN if m["is_completed"])
        progress_percent = (completed_months / 24) * 100
        st.progress(progress_percent / 100)
        st.caption(f"Time Progress: {progress_percent:.1f}%")
    
    with col2:
        milestone_progress = 0  # No milestones completed yet
        st.progress(milestone_progress / 100)
        st.caption(f"Milestone Progress: {milestone_progress:.1f}%")
    
    # Quick Stats
    st.subheader("📊 Quick Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Team Members", "11", delta=None)
    with col2:
        st.metric("Hours Logged (May)", "209", delta="11 people x 19 days")
    with col3:
        st.metric("Meetings Completed (May)", "4", delta=None)
    with col4:
        st.metric("Milestones Achieved", "0/7", delta=None)
    
    # Current Focus
    st.subheader("🎯 Current Focus (June 2026)")
    
    current_activities = ACTIVITIES_BY_MONTH[2]["activities"]
    for activity in current_activities:
        if activity["status"] == "in_progress":
            st.info(f"🔄 **{activity['activity']}** - Due: {activity['due_date']}")
        else:
            st.warning(f"⏳ **{activity['activity']}** - Due: {activity['due_date']}")

# May 2026 - Completed View
elif selected == "May 2026 - Completed":
    st.header("✅ May 2026 - Month 1 Completed")
    st.markdown("---")
    
    # Team attendance for May
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
    
    # Completed Activities
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
    
    # Meetings Conducted
    st.subheader("📝 Meetings Conducted in May 2026")
    
    meetings_df = pd.DataFrame(COMPLETED_MAY_MEETINGS)
    st.dataframe(meetings_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Key Accomplishments
    st.subheader("🏆 Key Accomplishments - May 2026")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("""
        **SANGAM Training Completed**
        - 3-day intensive orientation (May 4-6)
        - All 10 coordinators trained
        - GRDAU concept introduced successfully
        """)
        
        st.success("""
        **University Onboarding**
        - All 7 universities onboarded
        - Data source mapping completed
        - Nodal officers identified
        """)
    
    with col2:
        st.success("""
        **NIRF Data Collection**
        - Student, Faculty, Research data collected
        - Placement and Finance data gathered
        - Baseline data repository created
        """)
        
        st.success("""
        **Inception Report**
        - Framework developed
        - GRDAU structure defined
        - Submitted as per contract
        """)
    
    st.markdown("---")
    
    # MPR Submission
    st.subheader("📄 Monthly Progress Report (MPR) - May 2026")
    st.info("""
    **MPR submitted on: 29 May 2026**
    - Submitted to: PMU, MahaSTRIDE at pmu.mahastride@mahamitra.org
    - Approved by: Nominated Nodal Officer and Registrar
    - Copy sent to: Hon. Vice Chancellor and Project Director, MahaSTRIDE
    """)

# 24-Month Plan View
elif selected == "24-Month Plan":
    st.header("📅 24-Month Project Plan (May 2026 - April 2028)")
    st.markdown("---")
    
    # Phase-wise view
    phase_tabs = st.tabs([
        "Phase 1: Foundation (Months 1-3)", 
        "Phase 2: Planning (Months 4-6)", 
        "Phase 3: Implementation (Months 7-12)",
        "Phase 4: Enhancement (Months 13-18)",
        "Phase 5: Finalization (Months 19-24)"
    ])
    
    # Phase 1
    with phase_tabs[0]:
        st.subheader("Phase 1: Foundation & Assessment (May 2026 - July 2026)")
        
        for month_num in [1, 2, 3]:
            month_data = ACTIVITIES_BY_MONTH[month_num]
            status_icon = "✅" if month_data["status"] == "completed" else "🔄" if month_data["status"] == "current" else "⏳"
            st.markdown(f"### {status_icon} {month_data['month']}")
            
            for activity in month_data["activities"]:
                status_icon_act = "✅" if activity["status"] == "completed" else "🔄" if activity["status"] == "in_progress" else "📅"
                st.markdown(f"- {status_icon_act} **{activity['activity']}** - *Deliverable: {activity['deliverable']}* (Due: {activity['due_date']})")
            st.markdown("---")
    
    # Phase 2
    with phase_tabs[1]:
        st.subheader("Phase 2: Planning & Development (August 2026 - October 2026)")
        
        for month_num in [4, 5, 6]:
            month_data = ACTIVITIES_BY_MONTH[month_num]
            st.markdown(f"### ⏳ {month_data['month']}")
            
            for activity in month_data["activities"]:
                status_icon_act = "🔄" if activity["status"] == "in_progress" else "📅"
                st.markdown(f"- {status_icon_act} **{activity['activity']}** - *Deliverable: {activity['deliverable']}* (Due: {activity['due_date']})")
            st.markdown("---")
    
    # Phase 3
    with phase_tabs[2]:
        st.subheader("Phase 3: Implementation & Capacity Building (November 2026 - April 2027)")
        
        for month_num in [7, 8, 9, 10, 11, 12]:
            month_data = ACTIVITIES_BY_MONTH[month_num]
            st.markdown(f"### ⏳ {month_data['month']}")
            
            for activity in month_data["activities"]:
                status_icon_act = "📅"
                st.markdown(f"- {status_icon_act} **{activity['activity']}** - *Deliverable: {activity['deliverable']}* (Due: {activity['due_date']})")
            st.markdown("---")
    
    # Phase 4
    with phase_tabs[3]:
        st.subheader("Phase 4: Enhancement & Global Engagement (May 2027 - October 2027)")
        
        for month_num in [13, 14, 15, 16, 17, 18]:
            month_data = ACTIVITIES_BY_MONTH[month_num]
            st.markdown(f"### ⏳ {month_data['month']}")
            
            for activity in month_data["activities"]:
                status_icon_act = "📅"
                st.markdown(f"- {status_icon_act} **{activity['activity']}** - *Deliverable: {activity['deliverable']}* (Due: {activity['due_date']})")
            st.markdown("---")
    
    # Phase 5
    with phase_tabs[4]:
        st.subheader("Phase 5: Finalization & Handover (November 2027 - April 2028)")
        
        for month_num in [19, 20, 21, 22, 23, 24]:
            month_data = ACTIVITIES_BY_MONTH[month_num]
            st.markdown(f"### ⏳ {month_data['month']}")
            
            for activity in month_data["activities"]:
                status_icon_act = "📅"
                st.markdown(f"- {status_icon_act} **{activity['activity']}** - *Deliverable: {activity['deliverable']}* (Due: {activity['due_date']})")
            st.markdown("---")
    
    # Summary table
    st.subheader("📊 Monthly Summary")
    summary_data = []
    for month_num, month_data in ACTIVITIES_BY_MONTH.items():
        summary_data.append({
            "Month": month_data["month"],
            "Status": month_data["status"].upper(),
            "Activities Count": len(month_data["activities"]),
            "Completed": sum(1 for a in month_data["activities"] if a["status"] == "completed"),
            "In Progress": sum(1 for a in month_data["activities"] if a["status"] == "in_progress")
        })
    
    df_summary = pd.DataFrame(summary_data)
    st.dataframe(df_summary, use_container_width=True, hide_index=True)

# Team & Resources View
elif selected == "Team & Resources":
    st.header("👥 Team Structure & Resources")
    st.markdown("---")
    
    # MITRA Level
    st.subheader("🏢 MITRA Level Resources")
    mitra_df = pd.DataFrame(TEAM_STRUCTURE["MITRA Level"])
    st.dataframe(mitra_df, use_container_width=True, hide_index=True)
    
    # University Level
    st.subheader("🏫 University Level Resources (GRDAU Coordinators)")
    uni_df = pd.DataFrame(TEAM_STRUCTURE["University Level"])
    st.dataframe(uni_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Deployment Summary
    st.subheader("📊 Deployment Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Personnel", "11", delta=None)
    with col2:
        st.metric("MITRA Level", "2", delta=None)
    with col3:
        st.metric("University Level", "9", delta="Across 7 universities")
    
    # Resource Requirements
    st.subheader("📋 Resource Requirements (as per contract)")
    
    requirements = {
        "Requirement": [
            "Prior written approval for any resource change",
            "15 days advance notice for replacement with CV",
            "MITRA reserves right to reject replacement",
            "Unauthorized substitution may attract penalty",
            "All personnel bound by confidentiality"
        ]
    }
    
    st.dataframe(pd.DataFrame(requirements), use_container_width=True, hide_index=True)
    
    # Leave mechanism
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

# Milestones & Payments View
elif selected == "Milestones & Payments":
    st.header("💰 Milestones & Payment Structure")
    st.markdown("---")
    
    # Payment structure
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Payment Distribution")
        
        fig = go.Figure(data=[go.Pie(
            labels=['Monthly Fee (70%)', 'Milestone-Based (30%)'],
            values=[70, 30],
            hole=0.4,
            marker_colors=['#2a5298', '#28a745']
        )])
        fig.update_layout(title="Payment Structure", height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📈 Milestone Breakdown (30% of Contract)")
        
        milestone_df = pd.DataFrame([
            {"Milestone": m["name"][:40], "Percentage": m["percentage"], "Target Date": m["target_date"], "Status": m["status"]}
            for m in MILESTONES
        ])
        st.dataframe(milestone_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Payment terms
    st.subheader("💰 Payment Terms (as per contract)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.warning("**Monthly Payment (70%)**")
        st.write("- Based on attendance and MPR approval")
        st.write("- Distributed across 24 months")
        st.write("- No advance payment")
        st.write("- TDS deducted as applicable")
    
    with col2:
        st.success("**Milestone Payment (30%)**")
        st.write("- Payable on achievement of milestones")
        st.write("- Documentary evidence required")
        st.write("- PMU confirmation before release")
        st.write("- Payment within 60 days of valid invoice")
    
    st.markdown("---")
    
    # Performance Bank Guarantee
    st.subheader("🔒 Performance Bank Guarantee")
    st.info(f"""
    - **Amount:** 5% of Contract Value = ₹{CONTRACT_VALUE * 0.05:,.0f}
    - **Submission:** Within 15 days of LoA or prior to contract signing
    - **Validity:** 90 days after expiration of all contractual obligations
    - **Bank:** Scheduled or Nationalized bank
    - **Format:** As per Annexure X of RFP
    """)

# Deliverables Tracker View
elif selected == "Deliverables Tracker":
    st.header("📋 Contract Deliverables Tracker")
    st.markdown("---")
    
    deliverables_df = pd.DataFrame(CONTRACT_DELIVERABLES)
    
    # Display deliverables
    for idx, row in deliverables_df.iterrows():
        status_icon = "✅" if row["status"] == "completed" else "🔄" if row["status"] == "in_progress" else "⏳"
        with st.expander(f"{status_icon} **{row['deliverable']}**"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Due Date:** {row['due_date']}")
                st.write(f"**Status:** {row['status'].upper()}")
            with col2:
                if row.get('actual_date'):
                    st.write(f"**Actual Submission:** {row['actual_date']}")
                else:
                    st.write("**Actual Submission:** Not yet submitted")
    
    st.markdown("---")
    
    # Expected Outcomes
    st.subheader("🎯 Expected Outcomes (Performance-Linked)")
    
    outcomes = [
        ("Enhanced Global Rankings Participation", "Successful participation of institutions on minimum two global ranking platforms"),
        ("Minimum 20% Improvement", "Validation of comparative data between baseline and endline diagnostics"),
        ("Establishment of Sustainable Data & Quality Systems", "Certification of GRDAU readiness and dashboard deployment"),
        ("Institutional Development Plans", "Finalization and institutional sign-off of all IDPs"),
        ("Capacity Building Participation", "Submission of training completion report with attendance records"),
        ("Final Evaluation", "Approval of final report and satisfactory project closure")
    ]
    
    for outcome, metric in outcomes:
        st.markdown(f"- **{outcome}:** {metric}")

# Risk & Compliance View
elif selected == "Risk & Compliance":
    st.header("⚠️ Risk Management & Compliance")
    st.markdown("---")
    
    # Penalties
    st.subheader("⚖️ Penalty Provisions (as per contract)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.error("**Milestone Penalty**")
        st.write("- Fine up to 10% of milestone value for non-completion")
        st.write("- Applicable if compliance report not submitted as described")
    
    with col2:
        st.error("**Overall Penalty**")
        st.write("- Maximum 10% of total contract value")
        st.write("- For breach of contract conditions")
        st.write("- For unsatisfactory performance")
        st.write("- For delay in prescribed timelines")
    
    st.markdown("---")
    
    # Termination conditions
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
    
    # Fraud and Corruption
    st.subheader("🔒 Fraud and Corruption Compliance")
    st.info("""
    **World Bank Guidelines on Preventing and Combating Fraud and Corruption**
    - Program-for-Results Financing guidelines dated 1 Feb 2012 (revised 10 July 2015)
    - Anti-Corruption Guidelines shall prevail in case of conflict
    - MITRA as nodal agency ensures compliance
    """)
    
    st.markdown("---")
    
    # Jurisdiction
    st.subheader("⚖️ Jurisdiction")
    st.warning("""
    - **Governing Law:** Laws in force in India
    - **Exclusive Jurisdiction:** Courts at Mumbai, India
    - **Arbitration:** Mumbai Centre for Arbitration (as per Arbitration and Conciliation Act, 2015)
    """)
    
    st.markdown("---")
    
    # Confidentiality
    st.subheader("🔐 Confidentiality Obligations")
    st.write("""
    - All plans, data, reports, and specifications are property of MITRA
    - No publication or speech without prior written consent
    - All materials to be handed over upon request/termination/completion
    - Confidentiality survives termination of contract
    """)

# Footer
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #666; font-size: 0.8rem;">
    <p>© 2026 Maharashtra Institution for Transformation (MITRA) | MahaSTRIDE Project | World Bank Loan No: IBRD 9737-IN</p>
    <p>Last Updated: {datetime.now().strftime('%d %B %Y, %H:%M:%S')}</p>
</div>
""", unsafe_allow_html=True)
