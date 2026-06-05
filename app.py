import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import calendar
import json
import os
from hashlib import sha256

# Page configuration
st.set_page_config(
    page_title="MahaSTRIDE - Daily Activity Planner",
    page_icon="📋",
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
    .daily-task-card {
        background: white;
        border-left: 4px solid #2a5298;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .daily-task-completed {
        border-left-color: #28a745;
        background-color: #d4edda;
    }
    .daily-task-pending {
        border-left-color: #ffc107;
        background-color: #fff3cd;
    }
    .credentials-box {
        background-color: #f8f9fa;
        border: 2px solid #2a5298;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .role-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    .admin-badge { background-color: #dc3545; color: white; }
    .lead-badge { background-color: #17a2b8; color: white; }
    .analyst-badge { background-color: #28a745; color: white; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# USER CREDENTIALS
# ============================================================
USERS = {
    "admin@mahastride.com": {
        "password": sha256("Admin@2026".encode()).hexdigest(),
        "role": "admin",
        "name": "Administrator"
    },
    "projectlead@mahastride.com": {
        "password": sha256("ProjectLead@2026".encode()).hexdigest(),
        "role": "project_lead",
        "name": "Dr. Harshal Kotwal"
    },
    "sneha@mu.edu": {
        "password": sha256("Sneha@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Sneha Kashitkar",
        "team": "Mumbai University"
    },
    "shubham@mitra.gov.in": {
        "password": sha256("Shubham@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Shubham Singh",
        "team": "MITRA"
    }
}

# ============================================================
# DATA FILES
# ============================================================
DAILY_TASKS_FILE = "daily_tasks_breakdown.json"
TASK_COMPLETION_FILE = "task_completion.json"

# ============================================================
# COMPLETE 24-MONTH PLAN
# ============================================================

def get_24_month_plan():
    """Return the complete 24-month plan"""
    return {
        1: {"month": "May 2026", "year": 2026, "status": "completed", "activities": [
            {"activity": "SANGAM Orientation & Training", "deliverable": "Training Completed", "due_date": "May 6, 2026"},
            {"activity": "University Onboarding & Data Source Mapping", "deliverable": "Data Source Inventory", "due_date": "May 8, 2026"},
            {"activity": "NIRF Data Collection", "deliverable": "NIRF Data Repository", "due_date": "May 20, 2026"},
            {"activity": "Stakeholder Consultation Meetings", "deliverable": "Meeting Minutes", "due_date": "May 27, 2026"},
            {"activity": "Inception Report & GRDAU Framework", "deliverable": "Inception Report", "due_date": "May 26, 2026"},
            {"activity": "Monthly Progress Report Submission", "deliverable": "MPR May 2026", "due_date": "May 29, 2026"},
        ]},
        2: {"month": "June 2026", "year": 2026, "status": "current", "activities": [
            {"activity": "Complete Diagnostic Assessments across all 7 universities", "deliverable": "7 Diagnostic Reports", "due_date": "June 30, 2026"},
            {"activity": "Continue baseline data collection and validation", "deliverable": "Validated Baseline Data", "due_date": "June 25, 2026"},
            {"activity": "Establish GRDAU framework documentation", "deliverable": "GRDAU SOP Document", "due_date": "June 20, 2026"},
            {"activity": "Conduct initial GRDAU training for university coordinators", "deliverable": "Training Session 1 Completed", "due_date": "June 15, 2026"},
            {"activity": "Submit June MPR", "deliverable": "MPR June 2026", "due_date": "June 30, 2026"},
        ]},
        3: {"month": "July 2026", "year": 2026, "status": "upcoming", "activities": [
            {"activity": "Complete gap analysis against NIRF/NAAC/Global Rankings", "deliverable": "Gap Analysis Report", "due_date": "July 15, 2026"},
            {"activity": "SWOT analysis for each university", "deliverable": "7 SWOT Reports", "due_date": "July 20, 2026"},
            {"activity": "Finalize GRDAU establishment in all universities", "deliverable": "7 GRDAUs Operational", "due_date": "July 31, 2026"},
            {"activity": "Submit July MPR", "deliverable": "MPR July 2026", "due_date": "July 31, 2026"},
        ]},
        4: {"month": "August 2026", "year": 2026, "status": "upcoming", "activities": [
            {"activity": "Develop Institutional Development Plans (IDPs)", "deliverable": "IDP Drafts", "due_date": "August 15, 2026"},
            {"activity": "Stakeholder review of IDPs", "deliverable": "Stakeholder Feedback", "due_date": "August 25, 2026"},
            {"activity": "Design data portal architecture", "deliverable": "Portal Design Document", "due_date": "August 31, 2026"},
            {"activity": "Submit August MPR", "deliverable": "MPR August 2026", "due_date": "August 31, 2026"},
        ]},
        5: {"month": "September 2026", "year": 2026, "status": "upcoming", "activities": [
            {"activity": "Finalize IDPs with university approval", "deliverable": "7 Approved IDPs", "due_date": "September 15, 2026"},
            {"activity": "Create performance monitoring dashboard mockups", "deliverable": "Dashboard Designs", "due_date": "September 20, 2026"},
            {"activity": "MILESTONE 1: Establishment of Sustainable Data & Quality Systems", "deliverable": "Milestone Achievement Report", "due_date": "September 30, 2026"},
            {"activity": "Submit September MPR", "deliverable": "MPR September 2026", "due_date": "September 30, 2026"},
        ]},
        6: {"month": "October 2026", "year": 2026, "status": "upcoming", "activities": [
            {"activity": "Complete dashboard development", "deliverable": "Dashboard Beta Version", "due_date": "October 15, 2026"},
            {"activity": "MILESTONE 2: Institutional Development Plans and Execution Monitoring", "deliverable": "Milestone Achievement Report", "due_date": "October 31, 2026"},
            {"activity": "Mid-term review preparation", "deliverable": "Mid-term Review Materials", "due_date": "October 25, 2026"},
            {"activity": "Submit October MPR", "deliverable": "MPR October 2026", "due_date": "October 31, 2026"},
        ]},
        7: {"month": "November 2026", "year": 2026, "status": "upcoming", "activities": [
            {"activity": "Deploy data portal MVP", "deliverable": "Data Portal Live", "due_date": "November 15, 2026"},
            {"activity": "Mid-term Progress Report submission", "deliverable": "Mid-term Report", "due_date": "November 30, 2026"},
            {"activity": "Training needs assessment completion", "deliverable": "Training Needs Report", "due_date": "November 20, 2026"},
            {"activity": "Submit November MPR", "deliverable": "MPR November 2026", "due_date": "November 30, 2026"},
        ]},
        8: {"month": "December 2026", "year": 2026, "status": "upcoming", "activities": [
            {"activity": "Launch performance dashboards", "deliverable": "Dashboards Deployed", "due_date": "December 10, 2026"},
            {"activity": "Develop training modules", "deliverable": "Training Curriculum", "due_date": "December 15, 2026"},
            {"activity": "MILESTONE 3: Capacity Building Participation", "deliverable": "Milestone Achievement Report", "due_date": "December 31, 2026"},
            {"activity": "Submit December MPR", "deliverable": "MPR December 2026", "due_date": "December 31, 2026"},
        ]},
        9: {"month": "January 2027", "year": 2027, "status": "upcoming", "activities": [
            {"activity": "First round of training programs across all universities", "deliverable": "Training Completion Report", "due_date": "January 25, 2027"},
            {"activity": "Data quality framework implementation", "deliverable": "Data Quality Framework", "due_date": "January 20, 2027"},
            {"activity": "Submit January MPR", "deliverable": "MPR January 2027", "due_date": "January 31, 2027"},
        ]},
        10: {"month": "February 2027", "year": 2027, "status": "upcoming", "activities": [
            {"activity": "Data validation and quality improvement cycles", "deliverable": "Data Quality Report", "due_date": "February 20, 2027"},
            {"activity": "Research output enhancement initiatives", "deliverable": "Research Enhancement Plan", "due_date": "February 25, 2027"},
            {"activity": "Submit February MPR", "deliverable": "MPR February 2027", "due_date": "February 28, 2027"},
        ]},
        11: {"month": "March 2027", "year": 2027, "status": "upcoming", "activities": [
            {"activity": "International collaboration framework development", "deliverable": "Collaboration Framework", "due_date": "March 15, 2027"},
            {"activity": "Outcome-based education (OBE) implementation support", "deliverable": "OBE Guidelines", "due_date": "March 20, 2027"},
            {"activity": "Submit March MPR", "deliverable": "MPR March 2027", "due_date": "March 31, 2027"},
        ]},
        12: {"month": "April 2027", "year": 2027, "status": "upcoming", "activities": [
            {"activity": "Accreditation preparedness assessment", "deliverable": "Accreditation Readiness Report", "due_date": "April 15, 2027"},
            {"activity": "Quality assurance framework implementation", "deliverable": "QA Framework", "due_date": "April 25, 2027"},
            {"activity": "Submit April MPR", "deliverable": "MPR April 2027", "due_date": "April 30, 2027"},
        ]},
        13: {"month": "May 2027", "year": 2027, "status": "upcoming", "activities": [
            {"activity": "Year 1 performance review", "deliverable": "Annual Performance Report", "due_date": "May 15, 2027"},
            {"activity": "Enhanced data collection and reporting", "deliverable": "Enhanced Data Repository", "due_date": "May 20, 2027"},
            {"activity": "Submit May MPR", "deliverable": "MPR May 2027", "due_date": "May 31, 2027"},
        ]},
        14: {"month": "June 2027", "year": 2027, "status": "upcoming", "activities": [
            {"activity": "MILESTONE 4: Minimum 10% Improvement in Performance Indicators", "deliverable": "Milestone Achievement Report", "due_date": "June 30, 2027"},
            {"activity": "Mid-year performance assessment", "deliverable": "Mid-year Assessment", "due_date": "June 25, 2027"},
            {"activity": "Submit June MPR", "deliverable": "MPR June 2027", "due_date": "June 30, 2027"},
        ]},
        15: {"month": "July 2027", "year": 2027, "status": "upcoming", "activities": [
            {"activity": "Advanced training programs for GRDAU staff", "deliverable": "Advanced Training Report", "due_date": "July 20, 2027"},
            {"activity": "Research publication support and tracking", "deliverable": "Publication Report", "due_date": "July 25, 2027"},
            {"activity": "Submit July MPR", "deliverable": "MPR July 2027", "due_date": "July 31, 2027"},
        ]},
        16: {"month": "August 2027", "year": 2027, "status": "upcoming", "activities": [
            {"activity": "International ranking agency engagement", "deliverable": "Engagement Report", "due_date": "August 20, 2027"},
            {"activity": "Dashboard enhancements based on feedback", "deliverable": "Enhanced Dashboards", "due_date": "August 25, 2027"},
            {"activity": "Submit August MPR", "deliverable": "MPR August 2027", "due_date": "August 31, 2027"},
        ]},
        17: {"month": "September 2027", "year": 2027, "status": "upcoming", "activities": [
            {"activity": "Citation analysis and improvement strategies", "deliverable": "Citation Report", "due_date": "September 15, 2027"},
            {"activity": "Employer perception enhancement initiatives", "deliverable": "Employer Engagement Report", "due_date": "September 20, 2027"},
            {"activity": "Submit September MPR", "deliverable": "MPR September 2027", "due_date": "September 30, 2027"},
        ]},
        18: {"month": "October 2027", "year": 2027, "status": "upcoming", "activities": [
            {"activity": "Academic reputation building strategies", "deliverable": "Reputation Strategy Document", "due_date": "October 15, 2027"},
            {"activity": "IPR and patent filing support", "deliverable": "IPR Status Report", "due_date": "October 25, 2027"},
            {"activity": "Submit October MPR", "deliverable": "MPR October 2027", "due_date": "October 31, 2027"},
        ]},
        19: {"month": "November 2027", "year": 2027, "status": "upcoming", "activities": [
            {"activity": "SDG-aligned research promotion", "deliverable": "SDG Research Report", "due_date": "November 15, 2027"},
            {"activity": "International student enrollment strategies", "deliverable": "Internationalization Plan", "due_date": "November 20, 2027"},
            {"activity": "Submit November MPR", "deliverable": "MPR November 2027", "due_date": "November 30, 2027"},
        ]},
        20: {"month": "December 2027", "year": 2027, "status": "upcoming", "activities": [
            {"activity": "MILESTONE 5: Minimum 20% Improvement in Performance Indicators", "deliverable": "Milestone Achievement Report", "due_date": "December 31, 2027"},
            {"activity": "Year-end performance review", "deliverable": "Year-end Report", "due_date": "December 20, 2027"},
            {"activity": "Submit December MPR", "deliverable": "MPR December 2027", "due_date": "December 31, 2027"},
        ]},
        21: {"month": "January 2028", "year": 2028, "status": "upcoming", "activities": [
            {"activity": "Global ranking submission preparation", "deliverable": "Ranking Submission Package", "due_date": "January 20, 2028"},
            {"activity": "Final round of capacity building", "deliverable": "Final Training Report", "due_date": "January 25, 2028"},
            {"activity": "Submit January MPR", "deliverable": "MPR January 2028", "due_date": "January 31, 2028"},
        ]},
        22: {"month": "February 2028", "year": 2028, "status": "upcoming", "activities": [
            {"activity": "MILESTONE 6: Enhanced Global Rankings Participation of 10 colleges", "deliverable": "Milestone Achievement Report", "due_date": "February 29, 2028"},
            {"activity": "Final dashboard and portal review", "deliverable": "Final System Review", "due_date": "February 25, 2028"},
            {"activity": "Submit February MPR", "deliverable": "MPR February 2028", "due_date": "February 29, 2028"},
        ]},
        23: {"month": "March 2028", "year": 2028, "status": "upcoming", "activities": [
            {"activity": "Sustainability planning and handover documentation", "deliverable": "Sustainability Plan", "due_date": "March 15, 2028"},
            {"activity": "Lessons learned documentation", "deliverable": "Lessons Learned Report", "due_date": "March 20, 2028"},
            {"activity": "Submit March MPR", "deliverable": "MPR March 2028", "due_date": "March 31, 2028"},
        ]},
        24: {"month": "April 2028", "year": 2028, "status": "upcoming", "activities": [
            {"activity": "MILESTONE 7: Final Evaluation and Reporting", "deliverable": "Final Closure Report", "due_date": "April 30, 2028"},
            {"activity": "Project closure and knowledge transfer", "deliverable": "Knowledge Transfer Report", "due_date": "April 25, 2028"},
            {"activity": "Final MPR submission", "deliverable": "Final MPR", "due_date": "April 30, 2028"},
            {"activity": "Handover of all project materials to MITRA", "deliverable": "Complete Project Documentation", "due_date": "April 30, 2028"},
        ]},
    }

def get_working_days_in_month(year, month):
    """Get all working days (Monday to Friday) in a given month"""
    working_days = []
    first_day = datetime(year, month, 1)
    
    # Get last day of month
    if month == 12:
        last_day = datetime(year, month, 31)
    else:
        last_day = datetime(year, month + 1, 1) - timedelta(days=1)
    
    current = first_day
    while current <= last_day:
        if current.weekday() < 5:  # Monday to Friday
            working_days.append(current)
        current += timedelta(days=1)
    return working_days

def get_daily_breakdown_february_2028():
    """Daily breakdown for February 2028"""
    return {
        "2028-02-01": {
            "task": "Review ranking submission requirements for 10 colleges",
            "sub_tasks": [
                "Identify 10 target colleges for ranking submission",
                "Review QS/THE/US News submission guidelines",
                "Create ranking data checklist"
            ],
            "deliverable": "Ranking Requirements Document",
            "category": "Planning",
            "priority": "High"
        },
        "2028-02-02": {
            "task": "Collect ranking data for first 5 colleges",
            "sub_tasks": [
                "Gather research publication data",
                "Collect citation metrics",
                "Compile faculty credentials"
            ],
            "deliverable": "Ranking Data Set - Batch 1",
            "category": "Data Collection",
            "priority": "High"
        },
        "2028-02-03": {
            "task": "Collect ranking data for remaining 5 colleges",
            "sub_tasks": [
                "Complete data collection for all 10 colleges",
                "Validate collected data",
                "Identify data gaps"
            ],
            "deliverable": "Ranking Data Set - Complete",
            "category": "Data Collection",
            "priority": "High"
        },
        "2028-02-04": {
            "task": "Data validation and quality check",
            "sub_tasks": [
                "Cross-verify all ranking data",
                "Check for inconsistencies",
                "Prepare validation report"
            ],
            "deliverable": "Data Validation Report",
            "category": "Analysis",
            "priority": "High"
        },
        "2028-02-07": {
            "task": "Prepare ranking submission for QS",
            "sub_tasks": [
                "Fill QS ranking templates",
                "Upload supporting documents",
                "Review submission completeness"
            ],
            "deliverable": "QS Ranking Submission",
            "category": "Reporting",
            "priority": "High"
        },
        "2028-02-08": {
            "task": "Prepare ranking submission for THE",
            "sub_tasks": [
                "Complete THE ranking forms",
                "Submit research impact data",
                "Verify international metrics"
            ],
            "deliverable": "THE Ranking Submission",
            "category": "Reporting",
            "priority": "High"
        },
        "2028-02-09": {
            "task": "Prepare ranking submission for US News",
            "sub_tasks": [
                "Complete US News submission",
                "Submit global reputation data",
                "Finalize all submissions"
            ],
            "deliverable": "US News Ranking Submission",
            "category": "Reporting",
            "priority": "High"
        },
        "2028-02-10": {
            "task": "Compile Milestone 6 Achievement Report",
            "sub_tasks": [
                "Document all ranking submissions",
                "Prepare evidence package",
                "Draft milestone report"
            ],
            "deliverable": "Milestone 6 Report Draft",
            "category": "Reporting",
            "priority": "High"
        },
        "2028-02-11": {
            "task": "Finalize and submit Milestone 6 Report",
            "sub_tasks": [
                "Review milestone report",
                "Get client approval",
                "Submit to PMU"
            ],
            "deliverable": "Milestone Achievement Report",
            "category": "Reporting",
            "priority": "High"
        },
        "2028-02-14": {
            "task": "Begin final dashboard review",
            "sub_tasks": [
                "Check all dashboard modules",
                "Verify data accuracy",
                "Test all visualizations"
            ],
            "deliverable": "Dashboard Review Checklist",
            "category": "Technical",
            "priority": "High"
        },
        "2028-02-15": {
            "task": "Dashboard performance testing",
            "sub_tasks": [
                "Load testing",
                "Response time analysis",
                "Identify bottlenecks"
            ],
            "deliverable": "Performance Test Report",
            "category": "Technical",
            "priority": "High"
        },
        "2028-02-16": {
            "task": "Portal functionality review",
            "sub_tasks": [
                "Test all portal features",
                "Verify user access controls",
                "Check data export functionality"
            ],
            "deliverable": "Portal Review Report",
            "category": "Technical",
            "priority": "Medium"
        },
        "2028-02-17": {
            "task": "Incorporate feedback and fixes",
            "sub_tasks": [
                "Address review comments",
                "Fix identified issues",
                "Update documentation"
            ],
            "deliverable": "Updated Dashboard/Portal",
            "category": "Technical",
            "priority": "High"
        },
        "2028-02-18": {
            "task": "Final System Review completion",
            "sub_tasks": [
                "Conduct final acceptance test",
                "Prepare system review report",
                "Get client sign-off"
            ],
            "deliverable": "Final System Review Report",
            "category": "Reporting",
            "priority": "High"
        },
        "2028-02-21": {
            "task": "Prepare February MPR draft",
            "sub_tasks": [
                "Compile monthly achievements",
                "Document milestone progress",
                "List deliverables completed"
            ],
            "deliverable": "February MPR Draft",
            "category": "Reporting",
            "priority": "High"
        },
        "2028-02-22": {
            "task": "Review February activities",
            "sub_tasks": [
                "Verify all activities logged",
                "Check attendance records",
                "Review team contributions"
            ],
            "deliverable": "Activity Verification Report",
            "category": "Reporting",
            "priority": "Medium"
        },
        "2028-02-23": {
            "task": "Finalize February MPR",
            "sub_tasks": [
                "Incorporate feedback",
                "Format report as per SOP",
                "Prepare for submission"
            ],
            "deliverable": "Final February MPR",
            "category": "Reporting",
            "priority": "High"
        },
        "2028-02-24": {
            "task": "Submit February MPR to PMU",
            "sub_tasks": [
                "Send to pmu.mahastride@mahamitra.org",
                "Get acknowledgment",
                "Archive submission"
            ],
            "deliverable": "MPR Submission Confirmation",
            "category": "Reporting",
            "priority": "High"
        },
        "2028-02-25": {
            "task": "Plan March 2028 activities",
            "sub_tasks": [
                "Review remaining deliverables",
                "Create March work plan",
                "Assign responsibilities"
            ],
            "deliverable": "March 2028 Work Plan",
            "category": "Planning",
            "priority": "Medium"
        },
        "2028-02-28": {
            "task": "Month-end reconciliation",
            "sub_tasks": [
                "Complete pending tasks",
                "Update all trackers",
                "Prepare for final phase"
            ],
            "deliverable": "Month-end Status Report",
            "category": "Reporting",
            "priority": "Medium"
        },
        "2028-02-29": {
            "task": "Leap day - Final milestone review",
            "sub_tasks": [
                "Review Milestone 6 achievement",
                "Prepare for Phase 5 completion",
                "Team coordination meeting"
            ],
            "deliverable": "Milestone Review Document",
            "category": "Meetings",
            "priority": "High"
        }
    }

def get_daily_breakdown_january_2028():
    """Daily breakdown for January 2028"""
    return {
        "2028-01-03": {
            "task": "Final ranking submission preparation",
            "sub_tasks": ["Review ranking requirements", "Collect final data", "Validate all metrics"],
            "deliverable": "Ranking Preparation Checklist",
            "category": "Planning",
            "priority": "High"
        },
        "2028-01-04": {
            "task": "Global ranking data compilation",
            "sub_tasks": ["Compile QS data", "Compile THE data", "Compile US News data"],
            "deliverable": "Complete Ranking Data Package",
            "category": "Data Collection",
            "priority": "High"
        },
        "2028-01-05": {
            "task": "Final round of capacity building",
            "sub_tasks": ["Schedule training sessions", "Prepare materials", "Conduct training"],
            "deliverable": "Final Training Report",
            "category": "Training",
            "priority": "High"
        },
        "2028-01-06": {
            "task": "Prepare January MPR",
            "sub_tasks": ["Compile monthly data", "Draft report", "Get approvals"],
            "deliverable": "MPR January 2028",
            "category": "Reporting",
            "priority": "High"
        },
        "2028-01-07": {
            "task": "Ranking submission review",
            "sub_tasks": ["Quality check", "Peer review", "Final corrections"],
            "deliverable": "Ranking Submission Review",
            "category": "Reporting",
            "priority": "High"
        },
        "2028-01-10": {
            "task": "Submit January MPR",
            "sub_tasks": ["Send to PMU", "Get acknowledgment", "Archive"],
            "deliverable": "MPR Submission",
            "category": "Reporting",
            "priority": "High"
        },
        "2028-01-11": {
            "task": "Continue ranking preparations",
            "sub_tasks": ["Update missing data", "Refine metrics", "Prepare narratives"],
            "deliverable": "Updated Ranking Data",
            "category": "Data Collection",
            "priority": "Medium"
        },
        "2028-01-12": {
            "task": "Coordinate with ranking agencies",
            "sub_tasks": ["Schedule calls", "Clarify requirements", "Submit queries"],
            "deliverable": "Agency Communication Log",
            "category": "Coordination",
            "priority": "High"
        },
        "2028-01-13": {
            "task": "Finalize all ranking submissions",
            "sub_tasks": ["Complete QS", "Complete THE", "Complete US News"],
            "deliverable": "All Submissions Complete",
            "category": "Reporting",
            "priority": "High"
        },
        "2028-01-14": {
            "task": "Prepare for milestone 6",
            "sub_tasks": ["Compile evidence", "Draft report", "Review with team"],
            "deliverable": "Milestone 6 Draft",
            "category": "Reporting",
            "priority": "High"
        },
        "2028-01-17": {
            "task": "Continue milestone preparation",
            "sub_tasks": ["Format report", "Add supporting docs", "Final review"],
            "deliverable": "Milestone 6 Report",
            "category": "Reporting",
            "priority": "High"
        },
        "2028-01-18": {
            "task": "Submit milestone 6 for approval",
            "sub_tasks": ["Send to Project Lead", "Address feedback", "Finalize"],
            "deliverable": "Approved Milestone Report",
            "category": "Reporting",
            "priority": "High"
        },
        "2028-01-19": {
            "task": "Plan February activities",
            "sub_tasks": ["Create work plan", "Set priorities", "Assign tasks"],
            "deliverable": "February Work Plan",
            "category": "Planning",
            "priority": "Medium"
        },
        "2028-01-20": {
            "task": "Team meeting for final phase",
            "sub_tasks": ["Review progress", "Discuss challenges", "Align on goals"],
            "deliverable": "Meeting Minutes",
            "category": "Meetings",
            "priority": "Medium"
        },
        "2028-01-21": {
            "task": "Continue daily operations",
            "sub_tasks": ["Monitor dashboards", "Update data", "Respond to queries"],
            "deliverable": "Daily Activity Log",
            "category": "Operations",
            "priority": "Medium"
        },
        "2028-01-24": {
            "task": "Prepare for final evaluation",
            "sub_tasks": ["Review project goals", "Compile achievements", "Identify gaps"],
            "deliverable": "Evaluation Preparation Document",
            "category": "Planning",
            "priority": "High"
        },
        "2028-01-25": {
            "task": "Final dashboard review",
            "sub_tasks": ["Check all features", "Verify data", "Test performance"],
            "deliverable": "Dashboard Review Report",
            "category": "Technical",
            "priority": "High"
        },
        "2028-01-26": {
            "task": "Portal final review",
            "sub_tasks": ["Check functionality", "Verify security", "Test usability"],
            "deliverable": "Portal Review Report",
            "category": "Technical",
            "priority": "High"
        },
        "2028-01-27": {
            "task": "Final system review",
            "sub_tasks": ["Integrate feedback", "Make improvements", "Document changes"],
            "deliverable": "System Review Complete",
            "category": "Technical",
            "priority": "High"
        },
        "2028-01-28": {
            "task": "Month-end planning",
            "sub_tasks": ["Review January progress", "Plan February", "Update trackers"],
            "deliverable": "Monthly Planning Document",
            "category": "Planning",
            "priority": "Medium"
        },
        "2028-01-31": {
            "task": "Submit January MPR (if not done)",
            "sub_tasks": ["Final submission", "Confirm receipt", "Archive"],
            "deliverable": "MPR January 2028 Complete",
            "category": "Reporting",
            "priority": "High"
        }
    }

def get_daily_breakdown_for_month(month_num, year, month):
    """Get daily breakdown for a specific month"""
    
    # February 2028
    if year == 2028 and month == 2:
        return get_daily_breakdown_february_2028()
    
    # January 2028
    if year == 2028 and month == 1:
        return get_daily_breakdown_january_2028()
    
    # For other months, generate generic daily breakdown
    plan = get_24_month_plan()
    month_data = plan.get(month_num, {})
    activities = month_data.get("activities", [])
    
    working_days = get_working_days_in_month(year, month)
    daily_breakdown = {}
    
    for idx, working_day in enumerate(working_days):
        date_str = working_day.strftime("%Y-%m-%d")
        
        # Assign activities to working days
        if idx < len(activities):
            activity = activities[idx]
            daily_breakdown[date_str] = {
                "task": activity["activity"],
                "sub_tasks": [
                    f"Plan and prepare for {activity['activity'].lower()}",
                    f"Execute {activity['activity'].lower()}",
                    f"Document progress and challenges",
                    f"Prepare {activity['deliverable']}",
                    f"Review and submit deliverables"
                ],
                "deliverable": activity["deliverable"],
                "category": get_category_from_activity(activity["activity"]),
                "priority": "High" if "MILESTONE" in activity["activity"] else "Medium"
            }
        else:
            # Generic tasks for remaining days
            daily_breakdown[date_str] = {
                "task": "Continue project activities and documentation",
                "sub_tasks": [
                    "Review progress against plan",
                    "Update project documentation",
                    "Coordinate with team members",
                    "Plan next day's activities",
                    "Log daily work in system"
                ],
                "deliverable": "Daily Progress Report",
                "category": "General",
                "priority": "Medium"
            }
    
    return daily_breakdown

def get_category_from_activity(activity):
    if "Training" in activity or "SANGAM" in activity:
        return "Training"
    elif "Data" in activity or "Collection" in activity:
        return "Data Collection"
    elif "Report" in activity or "MPR" in activity:
        return "Reporting"
    elif "Meeting" in activity or "Review" in activity:
        return "Meetings"
    elif "Assessment" in activity or "Analysis" in activity:
        return "Assessment"
    elif "Development" in activity or "Planning" in activity:
        return "Planning"
    elif "Dashboard" in activity or "Portal" in activity:
        return "Technical"
    elif "MILESTONE" in activity:
        return "Milestone"
    else:
        return "General"

# ============================================================
# DATA MANAGEMENT FUNCTIONS
# ============================================================

def load_daily_tasks():
    if os.path.exists(DAILY_TASKS_FILE):
        with open(DAILY_TASKS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_daily_tasks(tasks):
    with open(DAILY_TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)

def load_completions():
    if os.path.exists(TASK_COMPLETION_FILE):
        with open(TASK_COMPLETION_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_completions(completions):
    with open(TASK_COMPLETION_FILE, 'w') as f:
        json.dump(completions, f, indent=2)

def get_all_daily_tasks():
    """Get all daily tasks for all months"""
    all_tasks = load_daily_tasks()
    
    if not all_tasks:
        # Generate tasks for all months
        plan = get_24_month_plan()
        
        for month_num, month_data in plan.items():
            year = month_data["year"]
            month_name = month_data["month"].split()[0]
            
            # Convert month name to number
            month_map = {
                "January": 1, "February": 2, "March": 3, "April": 4,
                "May": 5, "June": 6, "July": 7, "August": 8,
                "September": 9, "October": 10, "November": 11, "December": 12
            }
            month = month_map[month_name]
            
            daily_breakdown = get_daily_breakdown_for_month(month_num, year, month)
            for date_str, task_info in daily_breakdown.items():
                all_tasks[date_str] = task_info
        
        save_daily_tasks(all_tasks)
    
    return all_tasks

def get_user_tasks(email, year=None, month=None):
    user = USERS.get(email, {})
    user_role = user.get("role", "")
    
    all_tasks = get_all_daily_tasks()
    completions = load_completions()
    user_completions = completions.get(email, {})
    
    user_tasks = []
    
    for date_str, task_info in all_tasks.items():
        task_date = datetime.strptime(date_str, "%Y-%m-%d")
        
        if year and task_date.year != year:
            continue
        if month and task_date.month != month:
            continue
        
        if user_role == "data_analyst":
            is_completed = date_str in user_completions
            completion_info = user_completions.get(date_str, {})
            
            # Tasks before June 8, 2026 are auto-completed
            if date_str <= "2026-06-05":
                status = "Completed"
            else:
                status = "Completed" if is_completed else "Pending"
            
            user_tasks.append({
                "date": date_str,
                "day": task_date.strftime("%A"),
                "task": task_info.get("task", ""),
                "sub_tasks": task_info.get("sub_tasks", []),
                "deliverable": task_info.get("deliverable", ""),
                "category": task_info.get("category", ""),
                "priority": task_info.get("priority", "Medium"),
                "status": status,
                "completed_at": completion_info.get("completed_at", ""),
                "remarks": completion_info.get("remarks", "")
            })
    
    return sorted(user_tasks, key=lambda x: x["date"])

def mark_task_complete(email, date_str, remarks=""):
    completions = load_completions()
    if email not in completions:
        completions[email] = {}
    
    completions[email][date_str] = {
        "completed_at": datetime.now().isoformat(),
        "remarks": remarks
    }
    save_completions(completions)
    return True

def show_credentials():
    st.markdown("""
    <div class="credentials-box">
        <h4>🔐 Default Login Credentials</h4>
        <p><strong>Password format:</strong> <code>FirstName@2026</code></p>
        <table style="width:100%">
            <tr><th>Role</th><th>Email</th><th>Password</th></tr>
            <tr><td style="background:#dc3545;color:white;padding:2px 8px;border-radius:5px;">Admin</div>
                <td>admin@mahastride.com</div><td>Admin@2026</div></tr>
            <tr><td style="background:#17a2b8;color:white;padding:2px 8px;border-radius:5px;">Project Lead</div>
                <td>projectlead@mahastride.com</div><td>ProjectLead@2026</div></tr>
            <tr><td style="background:#28a745;color:white;padding:2px 8px;border-radius:5px;">Data Analyst</div>
                <td>sneha@mu.edu</div><td>Sneha@2026</div></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# DASHBOARD FUNCTIONS
# ============================================================

def admin_dashboard():
    st.markdown("## 📊 Administrator Dashboard")
    
    all_tasks = get_all_daily_tasks()
    
    total_days = len(all_tasks)
    completed_initial = len([d for d in all_tasks.keys() if d <= "2026-06-05"])
    
    col1, col2, col3 = st.columns(3)
    col1.metric("📅 Total Working Days (24 months)", total_days)
    col2.metric("✅ Auto-Completed (May 4 - June 5)", completed_initial)
    col3.metric("👥 Data Analysts", sum(1 for u in USERS.values() if u.get("role") == "data_analyst"))
    
    st.markdown("---")
    
    st.subheader("📅 24-Month Plan Overview")
    plan = get_24_month_plan()
    
    for month_num, month_data in plan.items():
        status_icon = "✅" if month_data["status"] == "completed" else "🔄" if month_data["status"] == "current" else "📅"
        with st.expander(f"{status_icon} {month_data['month']} - {month_data['year']}"):
            for activity in month_data["activities"]:
                st.markdown(f"• **{activity['activity']}** - *{activity['deliverable']}* (Due: {activity['due_date']})")

def project_lead_dashboard():
    st.markdown("## 👨‍💼 Project Lead Dashboard")
    st.markdown("**Dr. Harshal Kotwal** - ICARE Project Director")
    
    # Month selector
    years = [2026, 2027, 2028]
    selected_year = st.selectbox("Select Year", years, index=0)
    
    months = list(range(1, 13))
    month_names = ["January", "February", "March", "April", "May", "June", 
                   "July", "August", "September", "October", "November", "December"]
    selected_month = st.selectbox("Select Month", months, format_func=lambda x: month_names[x-1])
    
    st.markdown("---")
    
    # Get daily tasks for the selected month
    daily_tasks = get_user_tasks("sneha@mu.edu", selected_year, selected_month)
    
    if daily_tasks:
        st.subheader(f"Daily Activity Plan - {month_names[selected_month-1]} {selected_year}")
        
        for task in daily_tasks:
            if task["status"] == "Completed":
                status_class = "daily-task-completed"
                status_icon = "✅"
            else:
                status_class = "daily-task-pending"
                status_icon = "⏳"
            
            st.markdown(f"""
            <div class="daily-task-card {status_class}">
                <strong>{status_icon} {task['date']} ({task['day']})</strong><br>
                <strong>📌 Task:</strong> {task['task']}<br>
                <strong>📦 Deliverable:</strong> {task['deliverable']}<br>
                <strong>📂 Category:</strong> {task['category']} | <strong>Priority:</strong> {task['priority']}<br>
                <strong>📋 Sub-tasks:</strong>
                <ul>
                    {''.join([f'<li>{st}</li>' for st in task['sub_tasks'][:3]])}
                </ul>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info(f"No tasks found for {month_names[selected_month-1]} {selected_year}")

def data_analyst_dashboard(email, user):
    st.markdown(f"## 📋 Daily Task Dashboard")
    st.markdown(f"**Welcome, {user['name']}**")
    st.markdown(f"**Team:** {user.get('team', 'N/A')}")
    st.markdown(f"**Working Hours:** 10:00 AM - 6:00 PM (Monday to Friday)")
    
    # Month selector
    col1, col2 = st.columns(2)
    with col1:
        selected_year = st.selectbox("Select Year", [2026, 2027, 2028], index=0)
    with col2:
        month_names = ["January", "February", "March", "April", "May", "June", 
                       "July", "August", "September", "October", "November", "December"]
        selected_month = st.selectbox("Select Month", range(1, 13), format_func=lambda x: month_names[x-1], index=5)
    
    st.markdown("---")
    
    # Get tasks for selected month
    daily_tasks = get_user_tasks(email, selected_year, selected_month)
    
    if daily_tasks:
        total = len(daily_tasks)
        completed = sum(1 for t in daily_tasks if t["status"] == "Completed")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("📅 Working Days", total)
        col2.metric("✅ Completed", completed)
        col3.metric("⏳ Pending", total - completed)
        
        st.progress(completed/total if total > 0 else 0)
        
        st.markdown("---")
        
        # Today's task
        today = datetime.now().strftime("%Y-%m-%d")
        today_task = next((t for t in daily_tasks if t["date"] == today), None)
        
        if today_task and today_task["date"] > "2026-06-05":
            st.subheader("📌 Today's Task")
            if today_task["status"] == "Completed":
                st.markdown(f"""
                <div class="daily-task-card daily-task-completed">
                    ✅ <strong>COMPLETED - {today_task['date']} ({today_task['day']})</strong><br>
                    <strong>Task:</strong> {today_task['task']}<br>
                    <strong>Deliverable:</strong> {today_task['deliverable']}<br>
                    <strong>Category:</strong> {today_task['category']}<br>
                    <strong>Priority:</strong> {today_task['priority']}<br>
                    <strong>Remarks:</strong> {today_task.get('remarks', 'No remarks')}
                </div>
                """, unsafe_allow_html=True)
            else:
                with st.form(key=f"task_{today_task['date']}"):
                    st.markdown(f"""
                    <div class="daily-task-card daily-task-pending">
                        ⏳ <strong>PENDING - {today_task['date']} ({today_task['day']})</strong><br>
                        <strong>Task:</strong> {today_task['task']}<br>
                        <strong>Deliverable:</strong> {today_task['deliverable']}<br>
                        <strong>Category:</strong> {today_task['category']}<br>
                        <strong>Priority:</strong> {today_task['priority']}<br>
                        <strong>Sub-tasks to complete:</strong>
                        <ul>
                            {''.join([f'<li>{st}</li>' for st in today_task['sub_tasks']])}
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("**Work Log (10:00 AM - 6:00 PM)**")
                    col1, col2 = st.columns(2)
                    with col1:
                        start_time = st.time_input("Start Time", value=datetime.strptime("10:00", "%H:%M").time())
                    with col2:
                        end_time = st.time_input("End Time", value=datetime.strptime("18:00", "%H:%M").time())
                    
                    remarks = st.text_area("Work Accomplished / Remarks", height=100)
                    
                    if st.form_submit_button("✅ Mark as Complete", use_container_width=True):
                        work_log = f"Worked from {start_time} to {end_time}. {remarks}"
                        if mark_task_complete(email, today_task["date"], work_log):
                            st.success("Task completed! Great work!")
                            st.rerun()
        
        st.markdown("---")
        st.subheader(f"📅 All Tasks for {month_names[selected_month-1]} {selected_year}")
        
        for task in daily_tasks:
            status_icon = "✅" if task["status"] == "Completed" else "⏳"
            st.markdown(f"""
            <div class="daily-task-card">
                <strong>{status_icon} {task['date']} ({task['day']})</strong><br>
                <strong>Task:</strong> {task['task']}<br>
                <strong>Deliverable:</strong> {task['deliverable']}<br>
                <strong>Status:</strong> {task['status']}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info(f"No tasks available for {month_names[selected_month-1]} {selected_year}")

# ============================================================
# MAIN APP
# ============================================================

def main():
    # Initialize
    get_all_daily_tasks()
    
    # Authentication
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        st.markdown("""
        <div class="main-header">
            <h1>📋 MahaSTRIDE Daily Activity Planner</h1>
            <p>Complete 24-Month Daily Task Breakdown | May 2026 - April 2028</p>
            <p>Monday to Friday | 10:00 AM - 6:00 PM</p>
            <p>✅ May 4 to June 5, 2026: Auto-Completed | June 8, 2026 onwards: Pending</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("### 🔐 Login")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            
            if st.button("Login", use_container_width=True):
                if email in USERS:
                    hashed_input = sha256(password.encode()).hexdigest()
                    if USERS[email]["password"] == hashed_input:
                        st.session_state.authenticated = True
                        st.session_state.user_email = email
                        st.session_state.user_info = USERS[email]
                        st.rerun()
                    else:
                        st.error("Invalid password")
                else:
                    st.error("Email not found")
            
            show_credentials()
        
        return
    
    # Logged in view
    user_info = st.session_state.user_info
    email = st.session_state.user_email
    role = user_info.get("role", "data_analyst")
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 📋 MahaSTRIDE")
        st.markdown(f"**Welcome, {user_info.get('name')}**")
        if role == "data_analyst":
            st.markdown(f"*Team: {user_info.get('team', 'N/A')}*")
        st.markdown(f"*Role: {role.upper()}*")
        st.markdown("---")
        
        if role == "admin":
            menu = st.radio("Navigation", ["📊 Admin Dashboard", "📅 Monthly Plans"])
        elif role == "project_lead":
            menu = st.radio("Navigation", ["👨‍💼 Lead Dashboard"])
        else:
            menu = st.radio("Navigation", ["📝 My Daily Tasks"])
        
        st.markdown("---")
        st.markdown("**Working Hours**")
        st.markdown("🕐 10:00 AM - 6:00 PM")
        st.markdown("📅 Monday to Friday")
        
        st.markdown("---")
        st.markdown("**Status**")
        st.markdown("✅ May 4 - June 5, 2026: COMPLETED")
        st.markdown("📅 June 8, 2026 onwards: PENDING")
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()
    
    # Main content
    if role == "admin":
        if menu == "📊 Admin Dashboard":
            admin_dashboard()
        else:
            st.markdown("## 📅 24-Month Activity Plan")
            plan = get_24_month_plan()
            for month_num, month_data in plan.items():
                with st.expander(f"{month_data['month']} {month_data['year']}"):
                    for activity in month_data["activities"]:
                        st.markdown(f"• **{activity['activity']}** - {activity['deliverable']} (Due: {activity['due_date']})")
    
    elif role == "project_lead":
        project_lead_dashboard()
    
    else:
        data_analyst_dashboard(email, user_info)
    
    # Footer
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: #666; font-size: 0.8rem;">
        <p>© 2026-2028 MahaSTRIDE Project | World Bank Loan No: IBRD 9737-IN | ICARE Pvt. Ltd.</p>
        <p>24-Month Daily Activity Plan: May 2026 - April 2028 | Working Days: Monday to Friday | Hours: 10:00 - 18:00</p>
        <p>Last Updated: {datetime.now().strftime('%d %B %Y, %H:%M:%S')}</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
