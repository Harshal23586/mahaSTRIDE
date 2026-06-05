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
    page_title="MahaSTRIDE - Complete 24-Month Task Management System",
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
    .task-card {
        background: linear-gradient(135deg, #e8f8f5 0%, #d4efdf 100%);
        border-left: 4px solid #27ae60;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .task-card-pending {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        border-left: 4px solid #ffc107;
    }
    .task-card-completed {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border-left: 4px solid #28a745;
    }
    .stat-card {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem;
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
    .weekday-header {
        background-color: #2a5298;
        color: white;
        padding: 0.5rem;
        text-align: center;
        border-radius: 5px;
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
        "name": "Administrator"
    },
    "projectlead@mahastride.com": {
        "password": sha256("ProjectLead@2026".encode()).hexdigest(),
        "role": "project_lead",
        "name": "Dr. Harshal Kotwal"
    },
    "shubham@mitra.gov.in": {
        "password": sha256("Shubham@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Shubham Singh",
        "team": "MITRA"
    },
    "sneha@mu.edu": {
        "password": sha256("Sneha@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Sneha Kashitkar",
        "team": "Mumbai University"
    },
    "sagar@mu.edu": {
        "password": sha256("Sagar@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Sagar Teli",
        "team": "Mumbai University"
    },
    "jagan@sspu.edu": {
        "password": sha256("Jagan@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Jagan Sridhar",
        "team": "Savitribai Phule Pune University"
    },
    "vaibhav@coep.edu": {
        "password": sha256("Vaibhav@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Vaibhav Ambekar",
        "team": "COEP Technological University"
    },
    "pratham@au.edu": {
        "password": sha256("Pratham@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Prathamesh Babhulkar",
        "team": "Sant Gadge Baba Amravati University"
    },
    "anjali@nu.edu": {
        "password": sha256("Anjali@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Anjali Singh",
        "team": "Rashtrasant Tukadoji Maharaj Nagpur University"
    },
    "nitish@kbcnmu.edu": {
        "password": sha256("Nitish@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Nitish Kumbhar",
        "team": "KBCNMU, Jalgaon"
    },
    "atharv@bamu.edu": {
        "password": sha256("Atharv@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Atharav Paturkar",
        "team": "Dr. Babasaheb Ambedkar Marathwada University"
    }
}

# ============================================================
# TEAMS DETAILS
# ============================================================
TEAMS = {
    "ICARE": {"members": ["Dr. Harshal Kotwal"], "type": "leadership"},
    "MITRA": {"members": ["Shubham Singh"], "type": "coordination"},
    "Mumbai University": {"members": ["Sneha Kashitkar", "Sagar Teli"], "type": "university"},
    "Savitribai Phule Pune University": {"members": ["Jagan Sridhar"], "type": "university"},
    "COEP Technological University": {"members": ["Vaibhav Ambekar"], "type": "university"},
    "Sant Gadge Baba Amravati University": {"members": ["Prathamesh Babhulkar"], "type": "university"},
    "Rashtrasant Tukadoji Maharaj Nagpur University": {"members": ["Anjali Singh"], "type": "university"},
    "KBCNMU, Jalgaon": {"members": ["Nitish Kumbhar"], "type": "university"},
    "Dr. Babasaheb Ambedkar Marathwada University": {"members": ["Atharav Paturkar"], "type": "university"}
}

# ============================================================
# DATA FILES
# ============================================================
TASKS_FILE = "complete_24month_tasks.json"
TASK_COMPLETION_FILE = "task_completion.json"
ASSIGNMENTS_FILE = "assignments.json"

# ============================================================
# WORKING HOURS
# ============================================================
WORKING_HOURS = {
    "start": "10:00",
    "end": "18:00",
    "total_hours": 8,
    "working_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
}

# ============================================================
# 24-MONTH DAILY TASK GENERATION
# ============================================================

def get_working_dates(start_date, end_date):
    """Get all working dates (Monday to Friday) between start and end dates"""
    working_dates = []
    current = start_date
    while current <= end_date:
        if current.weekday() < 5:  # Monday=0 to Friday=4
            working_dates.append(current)
        current += timedelta(days=1)
    return working_dates

def generate_phase_1_tasks(date, week_num, day_num):
    """Phase 1: Foundation (Months 1-3) - May to July 2026"""
    month = date.month
    
    if month == 5:  # May 2026 - Initial Setup
        tasks_by_week = {
            1: [  # Week 1: May 4-8
                {"task": "SANGAM Orientation Day 1 - Project Overview", "category": "Training", "priority": "High", "target": "all"},
                {"task": "SANGAM Training Day 2 - NIRF Framework", "category": "Training", "priority": "High", "target": "all"},
                {"task": "SANGAM Workshop Day 3 - GRDAU Concept", "category": "Training", "priority": "High", "target": "all"},
                {"task": "University Reporting & Onboarding", "category": "Setup", "priority": "High", "target": "coordinator"},
                {"task": "NIRF Data Source Mapping", "category": "Setup", "priority": "High", "target": "coordinator"}
            ],
            2: [  # Week 2: May 11-15
                {"task": "Create Data Gap Template", "category": "Documentation", "priority": "Medium", "target": "coordinator"},
                {"task": "Collect Student & Faculty Data", "category": "Data Collection", "priority": "High", "target": "coordinator"},
                {"task": "Collect Research & Placement Data", "category": "Data Collection", "priority": "High", "target": "coordinator"},
                {"task": "Collect Financial & Infrastructure Data", "category": "Data Collection", "priority": "Medium", "target": "coordinator"},
                {"task": "Data Consolidation & Validation", "category": "Analysis", "priority": "High", "target": "coordinator"}
            ],
            3: [  # Week 3: May 18-22
                {"task": "Stakeholder Consultation Meeting", "category": "Meetings", "priority": "High", "target": "coordinator"},
                {"task": "Missing Data Follow-up", "category": "Data Collection", "priority": "Medium", "target": "coordinator"},
                {"task": "NIRF Template Preparation", "category": "Analysis", "priority": "High", "target": "coordinator"},
                {"task": "SWOT Analysis & Gap Report", "category": "Documentation", "priority": "High", "target": "coordinator"},
                {"task": "Inception Report Drafting", "category": "Reporting", "priority": "High", "target": "coordinator"}
            ],
            4: [  # Week 4: May 25-29
                {"task": "GRDAU Team Identification", "category": "Documentation", "priority": "Medium", "target": "coordinator"},
                {"task": "GRDAU Operational Framework", "category": "Documentation", "priority": "High", "target": "coordinator"},
                {"task": "Review Meeting with ICARE", "category": "Meetings", "priority": "High", "target": "all"},
                {"task": "May MPR Finalization", "category": "Reporting", "priority": "High", "target": "coordinator"},
                {"task": "Plan for June Activities", "category": "Planning", "priority": "Medium", "target": "coordinator"}
            ]
        }
        week_key = week_num if week_num <= 4 else 4
        tasks = tasks_by_week.get(week_key, [{"task": "Data validation and reporting", "category": "Analysis", "priority": "Medium", "target": "coordinator"}])
        idx = min(day_num - 1, len(tasks) - 1)
        return tasks[idx] if tasks else {"task": "Continue data collection", "category": "Data Collection", "priority": "Medium", "target": "coordinator"}
    
    elif month == 6:  # June 2026 - Diagnostic Assessments
        tasks_by_week = {
            1: [  # Week 1: June 1-5
                {"task": "Complete Diagnostic Assessment Framework", "category": "Assessment", "priority": "High", "target": "coordinator"},
                {"task": "Begin University-wise Assessments", "category": "Assessment", "priority": "High", "target": "coordinator"},
                {"task": "Review existing data quality", "category": "Analysis", "priority": "High", "target": "coordinator"},
                {"task": "Identify data gaps per university", "category": "Assessment", "priority": "High", "target": "coordinator"},
                {"task": "Prepare assessment templates", "category": "Documentation", "priority": "Medium", "target": "coordinator"}
            ],
            2: [  # Week 2: June 8-12
                {"task": "Conduct faculty interviews", "category": "Assessment", "priority": "High", "target": "coordinator"},
                {"task": "Analyze research output metrics", "category": "Analysis", "priority": "High", "target": "coordinator"},
                {"task": "Evaluate infrastructure readiness", "category": "Assessment", "priority": "Medium", "target": "coordinator"},
                {"task": "Assess international collaboration", "category": "Assessment", "priority": "Medium", "target": "coordinator"},
                {"task": "Compile assessment findings", "category": "Analysis", "priority": "High", "target": "coordinator"}
            ],
            3: [  # Week 3: June 15-19
                {"task": "GRDAU Training Session for Coordinators", "category": "Training", "priority": "High", "target": "coordinator"},
                {"task": "Data validation workshop", "category": "Training", "priority": "High", "target": "coordinator"},
                {"task": "NIRF submission preparation", "category": "Reporting", "priority": "High", "target": "coordinator"},
                {"task": "Review progress with VC", "category": "Meetings", "priority": "High", "target": "coordinator"},
                {"task": "Update data repository", "category": "Data Collection", "priority": "Medium", "target": "coordinator"}
            ],
            4: [  # Week 4: June 22-26
                {"task": "Finalize Diagnostic Reports", "category": "Reporting", "priority": "High", "target": "coordinator"},
                {"task": "Submit Diagnostic Assessment Reports", "category": "Reporting", "priority": "High", "target": "coordinator"},
                {"task": "Prepare June MPR", "category": "Reporting", "priority": "High", "target": "coordinator"},
                {"task": "Plan July activities", "category": "Planning", "priority": "Medium", "target": "coordinator"},
                {"task": "Client review meeting", "category": "Meetings", "priority": "High", "target": "all"}
            ]
        }
        week_key = week_num if week_num <= 4 else 4
        tasks = tasks_by_week.get(week_key, [{"task": "Continue assessments", "category": "Assessment", "priority": "Medium", "target": "coordinator"}])
        idx = min(day_num - 1, len(tasks) - 1)
        return tasks[idx]
    
    else:  # July 2026 - Gap Analysis and GRDAU Setup
        tasks_by_week = {
            1: [  # Week 1: July 1-3
                {"task": "Complete gap analysis", "category": "Analysis", "priority": "High", "target": "coordinator"},
                {"task": "Prepare SWOT reports", "category": "Documentation", "priority": "High", "target": "coordinator"},
                {"task": "Submit GRDAU establishment plan", "category": "Reporting", "priority": "High", "target": "coordinator"},
            ],
            2: [  # Week 2: July 6-10
                {"task": "Finalize GRDAU in all universities", "category": "Setup", "priority": "High", "target": "coordinator"},
                {"task": "Train GRDAU staff", "category": "Training", "priority": "High", "target": "coordinator"},
                {"task": "Develop SOP for GRDAU", "category": "Documentation", "priority": "High", "target": "coordinator"},
                {"task": "Setup data management systems", "category": "Technical", "priority": "High", "target": "coordinator"},
                {"task": "Review GRDAU readiness", "category": "Assessment", "priority": "Medium", "target": "coordinator"}
            ],
            3: [  # Week 3: July 13-17
                {"task": "Data quality framework implementation", "category": "Technical", "priority": "High", "target": "coordinator"},
                {"task": "Dashboard requirements gathering", "category": "Meetings", "priority": "High", "target": "coordinator"},
                {"task": "Prepare baseline report", "category": "Reporting", "priority": "High", "target": "coordinator"},
                {"task": "Stakeholder feedback session", "category": "Meetings", "priority": "Medium", "target": "coordinator"},
                {"task": "Update project plan", "category": "Planning", "priority": "Medium", "target": "lead"}
            ],
            4: [  # Week 4: July 20-24
                {"task": "Finalize July MPR", "category": "Reporting", "priority": "High", "target": "coordinator"},
                {"task": "Phase 1 completion review", "category": "Meetings", "priority": "High", "target": "all"},
                {"task": "Plan Phase 2 activities", "category": "Planning", "priority": "High", "target": "lead"},
                {"task": "Client presentation", "category": "Meetings", "priority": "High", "target": "all"},
                {"task": "Document lessons learned", "category": "Documentation", "priority": "Medium", "target": "coordinator"}
            ]
        }
        week_key = week_num if week_num <= 4 else 4
        tasks = tasks_by_week.get(week_key, [{"task": "Continue GRDAU setup", "category": "Setup", "priority": "Medium", "target": "coordinator"}])
        idx = min(day_num - 1, len(tasks) - 1)
        return tasks[idx]

def generate_phase_2_tasks(date, week_num, day_num):
    """Phase 2: Planning (Months 4-6) - August to October 2026"""
    
    if date.month == 8:  # August 2026 - IDP Development
        tasks_by_week = {
            1: [  # Week 1: Aug 3-7
                {"task": "IDP framework development", "category": "Planning", "priority": "High", "target": "coordinator"},
                {"task": "Collect university strategic plans", "category": "Data Collection", "priority": "High", "target": "coordinator"},
                {"task": "Analyze existing plans", "category": "Analysis", "priority": "High", "target": "coordinator"},
                {"task": "Draft IDP template", "category": "Documentation", "priority": "High", "target": "coordinator"},
                {"task": "Review with stakeholders", "category": "Meetings", "priority": "Medium", "target": "coordinator"}
            ],
            2: [  # Week 2: Aug 10-14
                {"task": "Develop university-specific IDPs", "category": "Planning", "priority": "High", "target": "coordinator"},
                {"task": "Set KPIs for each university", "category": "Planning", "priority": "High", "target": "coordinator"},
                {"task": "Define timelines for IDP implementation", "category": "Planning", "priority": "High", "target": "coordinator"},
                {"task": "Review IDPs with VCs", "category": "Meetings", "priority": "High", "target": "coordinator"},
                {"task": "Incorporate feedback", "category": "Documentation", "priority": "Medium", "target": "coordinator"}
            ],
            3: [  # Week 3: Aug 17-21
                {"task": "Finalize IDPs", "category": "Reporting", "priority": "High", "target": "coordinator"},
                {"task": "Get institutional sign-off", "category": "Meetings", "priority": "High", "target": "coordinator"},
                {"task": "Data portal architecture design", "category": "Technical", "priority": "High", "target": "analyst"},
                {"task": "Technical requirements gathering", "category": "Meetings", "priority": "High", "target": "analyst"},
                {"task": "Portal wireframing", "category": "Technical", "priority": "Medium", "target": "analyst"}
            ],
            4: [  # Week 4: Aug 24-28
                {"task": "Dashboard requirements specification", "category": "Technical", "priority": "High", "target": "analyst"},
                {"task": "Technology stack selection", "category": "Technical", "priority": "High", "target": "analyst"},
                {"task": "Prepare August MPR", "category": "Reporting", "priority": "High", "target": "coordinator"},
                {"task": "Client review meeting", "category": "Meetings", "priority": "High", "target": "all"},
                {"task": "Plan September activities", "category": "Planning", "priority": "Medium", "target": "lead"}
            ]
        }
        week_key = week_num if week_num <= 4 else 4
        tasks = tasks_by_week.get(week_key, [{"task": "Continue IDP development", "category": "Planning", "priority": "Medium", "target": "coordinator"}])
        idx = min(day_num - 1, len(tasks) - 1)
        return tasks[idx]
    
    elif date.month == 9:  # September 2026 - Dashboard Design
        tasks_by_week = {
            1: [  # Week 1: Aug 31-Sep 4
                {"task": "Dashboard prototype design", "category": "Technical", "priority": "High", "target": "analyst"},
                {"task": "Data visualization mockups", "category": "Technical", "priority": "High", "target": "analyst"},
                {"task": "User interface design", "category": "Technical", "priority": "High", "target": "analyst"},
                {"task": "Review with project lead", "category": "Meetings", "priority": "High", "target": "analyst"},
                {"task": "Incorporate design feedback", "category": "Technical", "priority": "Medium", "target": "analyst"}
            ],
            2: [  # Week 2: Sep 7-11
                {"task": "Database schema design", "category": "Technical", "priority": "High", "target": "analyst"},
                {"task": "API development planning", "category": "Technical", "priority": "High", "target": "analyst"},
                {"task": "Data integration strategy", "category": "Technical", "priority": "High", "target": "analyst"},
                {"task": "Security framework design", "category": "Technical", "priority": "High", "target": "analyst"},
                {"task": "Technical documentation", "category": "Documentation", "priority": "Medium", "target": "analyst"}
            ],
            3: [  # Week 3: Sep 14-18
                {"task": "Milestone 1 achievement preparation", "category": "Reporting", "priority": "High", "target": "coordinator"},
                {"task": "Sustainable Data Systems documentation", "category": "Documentation", "priority": "High", "target": "coordinator"},
                {"task": "Quality framework finalization", "category": "Documentation", "priority": "High", "target": "coordinator"},
                {"task": "Submit Milestone 1 report", "category": "Reporting", "priority": "High", "target": "coordinator"},
                {"task": "Client presentation", "category": "Meetings", "priority": "High", "target": "all"}
            ],
            4: [  # Week 4: Sep 21-25
                {"task": "Prepare September MPR", "category": "Reporting", "priority": "High", "target": "coordinator"},
                {"task": "Data validation protocols", "category": "Documentation", "priority": "High", "target": "coordinator"},
                {"task": "Training material preparation", "category": "Training", "priority": "High", "target": "coordinator"},
                {"task": "Stakeholder update meeting", "category": "Meetings", "priority": "Medium", "target": "coordinator"},
                {"task": "Plan October activities", "category": "Planning", "priority": "Medium", "target": "lead"}
            ]
        }
        week_key = week_num if week_num <= 4 else 4
        tasks = tasks_by_week.get(week_key, [{"task": "Continue dashboard development", "category": "Technical", "priority": "Medium", "target": "analyst"}])
        idx = min(day_num - 1, len(tasks) - 1)
        return tasks[idx]
    
    else:  # October 2026 - Dashboard Completion
        tasks_by_week = {
            1: [  # Week 1: Sep 28-Oct 2
                {"task": "Complete dashboard development", "category": "Technical", "priority": "High", "target": "analyst"},
                {"task": "Beta version deployment", "category": "Technical", "priority": "High", "target": "analyst"},
                {"task": "Testing and QA", "category": "Technical", "priority": "High", "target": "analyst"},
                {"task": "Bug fixing", "category": "Technical", "priority": "High", "target": "analyst"},
                {"task": "Performance optimization", "category": "Technical", "priority": "Medium", "target": "analyst"}
            ],
            2: [  # Week 2: Oct 5-9
                {"task": "Milestone 2 preparation", "category": "Reporting", "priority": "High", "target": "coordinator"},
                {"task": "IDP execution monitoring framework", "category": "Documentation", "priority": "High", "target": "coordinator"},
                {"task": "Submit Milestone 2 report", "category": "Reporting", "priority": "High", "target": "coordinator"},
                {"task": "Dashboard user training", "category": "Training", "priority": "High", "target": "coordinator"},
                {"task": "User feedback collection", "category": "Meetings", "priority": "Medium", "target": "coordinator"}
            ],
            3: [  # Week 3: Oct 12-16
                {"task": "Mid-term review preparation", "category": "Reporting", "priority": "High", "target": "coordinator"},
                {"task": "Compile mid-term achievements", "category": "Documentation", "priority": "High", "target": "coordinator"},
                {"task": "Prepare presentation", "category": "Reporting", "priority": "High", "target": "lead"},
                {"task": "Review with ICARE leadership", "category": "Meetings", "priority": "High", "target": "lead"},
                {"task": "Finalize mid-term report", "category": "Reporting", "priority": "High", "target": "coordinator"}
            ],
            4: [  # Week 4: Oct 19-23
                {"task": "Submit Mid-term Progress Report", "category": "Reporting", "priority": "High", "target": "coordinator"},
                {"task": "Prepare October MPR", "category": "Reporting", "priority": "High", "target": "coordinator"},
                {"task": "Client review meeting", "category": "Meetings", "priority": "High", "target": "all"},
                {"task": "Phase 2 completion review", "category": "Meetings", "priority": "High", "target": "all"},
                {"task": "Plan Phase 3 activities", "category": "Planning", "priority": "High", "target": "lead"}
            ]
        }
        week_key = week_num if week_num <= 4 else 4
        tasks = tasks_by_week.get(week_key, [{"task": "Continue dashboard deployment", "category": "Technical", "priority": "Medium", "target": "analyst"}])
        idx = min(day_num - 1, len(tasks) - 1)
        return tasks[idx]

def generate_phase_3_tasks(date, week_num, day_num):
    """Phase 3: Implementation (Months 7-12) - November 2026 to April 2027"""
    
    if date.month == 11:  # November 2026 - Portal Deployment
        tasks_by_week = {
            1: [  # Week 1: Nov 2-6
                {"task": "Data portal deployment", "category": "Technical", "priority": "High", "target": "analyst"},
                {"task": "User acceptance testing", "category": "Technical", "priority": "High", "target": "analyst"},
                {"task": "Portal launch preparation", "category": "Technical", "priority": "High", "target": "analyst"},
                {"task": "Go-live checklist", "category": "Documentation", "priority": "High", "target": "analyst"},
                {"task": "Launch announcement", "category": "Communication", "priority": "Medium", "target": "lead"}
            ],
            2: [  # Week 2: Nov 9-13
                {"task": "Portal monitoring and support", "category": "Technical", "priority": "High", "target": "analyst"},
                {"task": "Data upload and migration", "category": "Data Collection", "priority": "High", "target": "coordinator"},
                {"task": "User training sessions", "category": "Training", "priority": "High", "target": "coordinator"},
                {"task": "Feedback collection", "category": "Meetings", "priority": "Medium", "target": "coordinator"},
                {"task": "Bug fixes and enhancements", "category": "Technical", "priority": "High", "target": "analyst"}
            ],
            3: [  # Week 3: Nov 16-20
                {"task": "Dashboard rollout", "category": "Technical", "priority": "High", "target": "analyst"},
                {"task": "Dashboard training", "category": "Training", "priority": "High", "target": "coordinator"},
                {"task": "Performance monitoring setup", "category": "Technical", "priority": "High", "target": "analyst"},
                {"task": "KPI tracking implementation", "category": "Technical", "priority": "High", "target": "analyst"},
                {"task": "Dashboard documentation", "category": "Documentation", "priority": "Medium", "target": "analyst"}
            ],
            4: [  # Week 4: Nov 23-27
                {"task": "Training needs assessment", "category": "Assessment", "priority": "High", "target": "coordinator"},
                {"task": "Prepare training modules", "category": "Training", "priority": "High", "target": "coordinator"},
                {"task": "Schedule training programs", "category": "Planning", "priority": "Medium", "target": "coordinator"},
                {"task": "Prepare November MPR", "category": "Reporting", "priority": "High", "target": "coordinator"},
                {"task": "Client review meeting", "category": "Meetings", "priority": "High", "target": "all"}
            ]
        }
        week_key = week_num if week_num <= 4 else 4
        tasks = tasks_by_week.get(week_key, [{"task": "Continue portal deployment", "category": "Technical", "priority": "Medium", "target": "analyst"}])
        idx = min(day_num - 1, len(tasks) - 1)
        return tasks[idx]
    
    elif date.month == 12:  # December 2026 - Training Programs
        tasks_by_week = {
            1: [  # Week 1: Nov 30-Dec 4
                {"task": "Launch performance dashboards", "category": "Technical", "priority": "High", "target": "analyst"},
                {"task": "Dashboard analytics setup", "category": "Technical", "priority": "High", "target": "analyst"},
                {"task": "Real-time data integration", "category": "Technical", "priority": "High", "target": "analyst"},
                {"task": "Dashboard training for admins", "category": "Training", "priority": "High", "target": "coordinator"},
                {"task": "User guide creation", "category": "Documentation", "priority": "Medium", "target": "coordinator"}
            ],
            2: [  # Week 2: Dec 7-11
                {"task": "Training Module 1: NIRF Data Management", "category": "Training", "priority": "High", "target": "coordinator"},
                {"task": "Training Module 2: Research Metrics", "category": "Training", "priority": "High", "target": "coordinator"},
                {"task": "Training Module 3: Dashboard Usage", "category": "Training", "priority": "High", "target": "coordinator"},
                {"task": "Assessment of training effectiveness", "category": "Assessment", "priority": "Medium", "target": "coordinator"},
                {"task": "Training feedback collection", "category": "Data Collection", "priority": "Medium", "target": "coordinator"}
            ],
            3: [  # Week 3: Dec 14-18
                {"task": "Milestone 3 achievement preparation", "category": "Reporting", "priority": "High", "target": "coordinator"},
                {"task": "Capacity Building documentation", "category": "Documentation", "priority": "High", "target": "coordinator"},
                {"task": "Submit Milestone 3 report", "category": "Reporting", "priority": "High", "target": "coordinator"},
                {"task": "Review training outcomes", "category": "Assessment", "priority": "High", "target": "coordinator"},
                {"task": "Plan advanced training", "category": "Planning", "priority": "Medium", "target": "coordinator"}
            ],
            4: [  # Week 4: Dec 21-25, 28-31
                {"task": "Prepare December MPR", "category": "Reporting", "priority": "High", "target": "coordinator"},
                {"task": "Year-end performance review", "category": "Meetings", "priority": "High", "target": "all"},
                {"task": "Annual report preparation", "category": "Reporting", "priority": "High", "target": "coordinator"},
                {"task": "Plan January 2027 activities", "category": "Planning", "priority": "High", "target": "lead"},
                {"task": "Client year-end presentation", "category": "Meetings", "priority": "High", "target": "all"}
            ]
        }
        week_key = week_num if week_num <= 4 else 4
        tasks = tasks_by_week.get(week_key, [{"task": "Continue training programs", "category": "Training", "priority": "Medium", "target": "coordinator"}])
        idx = min(day_num - 1, len(tasks) - 1)
        return tasks[idx]
    
    elif date.month == 1:  # January 2027 - Data Quality
        tasks_by_week = {
            1: [  # Week 1: Jan 4-8
                {"task": "Data quality framework implementation", "category": "Technical", "priority": "High", "target": "analyst"},
                {"task": "Data validation rules setup", "category": "Technical", "priority": "High", "target": "analyst"},
                {"task": "Automated data checks", "category": "Technical", "priority": "High", "target": "analyst"},
                {"task": "Data cleaning procedures", "category": "Data Collection", "priority": "High", "target": "coordinator"},
                {"task": "Data quality dashboard", "category": "Technical", "priority": "Medium", "target": "analyst"}
            ],
            2: [  # Week 2: Jan 11-15
                {"task": "Data audit and validation", "category": "Data Collection", "priority": "High", "target": "coordinator"},
                {"task": "Identify data inconsistencies", "category": "Analysis", "priority": "High", "target": "coordinator"},
                {"task": "Correct data errors", "category": "Data Collection", "priority": "High", "target": "coordinator"},
                {"task": "Data completeness check", "category": "Analysis", "priority": "High", "target": "coordinator"},
                {"task": "Update data repository", "category": "Data Collection", "priority": "Medium", "target": "coordinator"}
            ],
            3: [  # Week 3: Jan 18-22
                {"task": "Research output enhancement planning", "category": "Planning", "priority": "High", "target": "coordinator"},
                {"task": "Identify research strengths", "category": "Analysis", "priority": "High", "target": "coordinator"},
                {"task": "Develop research strategy", "category": "Planning", "priority": "High", "target": "coordinator"},
                {"task": "Publication support framework", "category": "Documentation", "priority": "High", "target": "coordinator"},
                {"task": "Research collaboration mapping", "category": "Analysis", "priority": "Medium", "target": "coordinator"}
            ],
            4: [  # Week 4: Jan 25-29
                {"task": "Prepare January MPR", "category": "Reporting", "priority": "High", "target": "coordinator"},
                {"task": "Data quality report", "category": "Reporting", "priority": "High", "target": "coordinator"},
                {"task": "Research enhancement plan", "category": "Documentation", "priority": "High", "target": "coordinator"},
                {"task": "Client review meeting", "category": "Meetings", "priority": "High", "target": "all"},
                {"task": "Plan February activities", "category": "Planning", "priority": "Medium", "target": "lead"}
            ]
        }
        week_key = week_num if week_num <= 4 else 4
        tasks = tasks_by_week.get(week_key, [{"task": "Continue data quality work", "category": "Data Collection", "priority": "Medium", "target": "coordinator"}])
        idx = min(day_num - 1, len(tasks) - 1)
        return tasks[idx]
    
    elif date.month == 2:  # February 2027 - Research Enhancement
        tasks_by_week = {
            1: [  # Week 1: Feb 1-5
                {"task": "Research output tracking system", "category": "Technical", "priority": "High", "target": "analyst"},
                {"task": "Citation analysis setup", "category": "Analysis", "priority": "High", "target": "coordinator"},
                {"task": "Research publication database", "category": "Data Collection", "priority": "High", "target": "coordinator"},
                {"task": "Faculty research profiles", "category": "Data Collection", "priority": "Medium", "target": "coordinator"},
                {"task": "Research impact metrics", "category": "Analysis", "priority": "High", "target": "coordinator"}
            ],
            2: [  # Week 2: Feb 8-12
                {"task": "International collaboration development", "category": "Outreach", "priority": "High", "target": "coordinator"},
                {"task": "MoU templates preparation", "category": "Documentation", "priority": "High", "target": "coordinator"},
                {"task": "Partner university identification", "category": "Research", "priority": "High", "target": "coordinator"},
                {"task": "Collaboration framework", "category": "Documentation", "priority": "High", "target": "coordinator"},
                {"task": "International visibility plan", "category": "Planning", "priority": "Medium", "target": "coordinator"}
            ],
            3: [  # Week 3: Feb 15-19
                {"task": "Outcome-based education (OBE) implementation", "category": "Training", "priority": "High", "target": "coordinator"},
                {"task": "OBE framework development", "category": "Documentation", "priority": "High", "target": "coordinator"},
                {"task": "Faculty OBE training", "category": "Training", "priority": "High", "target": "coordinator"},
                {"task": "Curriculum alignment", "category": "Planning", "priority": "High", "target": "coordinator"},
                {"task": "OBE assessment tools", "category": "Technical", "priority": "Medium", "target": "analyst"}
            ],
            4: [  # Week 4: Feb 22-26
                {"task": "Prepare February MPR", "category": "Reporting", "priority": "High", "target": "coordinator"},
                {"task": "Research enhancement report", "category": "Reporting", "priority": "High", "target": "coordinator"},
                {"task": "Collaboration status update", "category": "Reporting", "priority": "Medium", "target": "coordinator"},
                {"task": "Client review meeting", "category": "Meetings", "priority": "High", "target": "all"},
                {"task": "Plan March activities", "category": "Planning", "priority": "Medium", "target": "lead"}
            ]
        }
        week_key = week_num if week_num <= 4 else 4
        tasks = tasks_by_week.get(week_key, [{"task": "Continue research enhancement", "category": "Research", "priority": "Medium", "target": "coordinator"}])
        idx = min(day_num - 1, len(tasks) - 1)
        return tasks[idx]
    
    else:  # March-April 2027 - Accreditation and QA
        if date.month == 3:
            tasks_by_week = {
                1: [  # Week 1: Mar 1-5
                    {"task": "Accreditation preparedness assessment", "category": "Assessment", "priority": "High", "target": "coordinator"},
                    {"task": "NAAC/NBA criteria review", "category": "Analysis", "priority": "High", "target": "coordinator"},
                    {"task": "Gap analysis for accreditation", "category": "Assessment", "priority": "High", "target": "coordinator"},
                    {"task": "Accreditation action plan", "category": "Planning", "priority": "High", "target": "coordinator"},
                    {"task": "Documentation preparation", "category": "Documentation", "priority": "High", "target": "coordinator"}
                ],
                2: [  # Week 2: Mar 8-12
                    {"task": "Quality assurance framework implementation", "category": "Technical", "priority": "High", "target": "analyst"},
                    {"task": "QA metrics definition", "category": "Planning", "priority": "High", "target": "coordinator"},
                    {"task": "Internal audit preparation", "category": "Assessment", "priority": "High", "target": "coordinator"},
                    {"task": "QA dashboard development", "category": "Technical", "priority": "High", "target": "analyst"},
                    {"task": "Quality improvement plan", "category": "Documentation", "priority": "Medium", "target": "coordinator"}
                ],
                3: [  # Week 3: Mar 15-19
                    {"task": "Milestone 4 preparation (10% improvement)", "category": "Reporting", "priority": "High", "target": "coordinator"},
                    {"task": "Performance data analysis", "category": "Analysis", "priority": "High", "target": "coordinator"},
                    {"task": "Improvement metrics calculation", "category": "Analysis", "priority": "High", "target": "coordinator"},
                    {"task": "Submit Milestone 4 report", "category": "Reporting", "priority": "High", "target": "coordinator"},
                    {"task": "Client presentation", "category": "Meetings", "priority": "High", "target": "all"}
                ],
                4: [  # Week 4: Mar 22-26, 29-31
                    {"task": "Prepare March MPR", "category": "Reporting", "priority": "High", "target": "coordinator"},
                    {"task": "Quarterly performance review", "category": "Meetings", "priority": "High", "target": "all"},
                    {"task": "Phase 3 progress review", "category": "Meetings", "priority": "High", "target": "all"},
                    {"task": "Plan Phase 4 activities", "category": "Planning", "priority": "High", "target": "lead"},
                    {"task": "Stakeholder update", "category": "Meetings", "priority": "Medium", "target": "coordinator"}
                ]
            }
        else:  # April 2027
            tasks_by_week = {
                1: [  # Week 1: Apr 1-2, 5-9
                    {"task": "Phase 3 completion review", "category": "Meetings", "priority": "High", "target": "all"},
                    {"task": "Year 1 achievements documentation", "category": "Documentation", "priority": "High", "target": "coordinator"},
                    {"task": "Annual report drafting", "category": "Reporting", "priority": "High", "target": "coordinator"},
                    {"task": "Prepare April MPR", "category": "Reporting", "priority": "High", "target": "coordinator"},
                    {"task": "Client annual review meeting", "category": "Meetings", "priority": "High", "target": "all"}
                ],
                2: [  # Week 2: Apr 12-16
                    {"task": "Plan Year 2 activities", "category": "Planning", "priority": "High", "target": "lead"},
                    {"task": "Update project plan", "category": "Planning", "priority": "High", "target": "lead"},
                    {"task": "Resource planning for Year 2", "category": "Planning", "priority": "High", "target": "lead"},
                    {"task": "Budget review", "category": "Meetings", "priority": "Medium", "target": "lead"},
                    {"task": "Team meeting for Year 2", "category": "Meetings", "priority": "High", "target": "all"}
                ],
                3: [  # Week 3: Apr 19-23
                    {"task": "Lessons learned documentation", "category": "Documentation", "priority": "High", "target": "coordinator"},
                    {"task": "Best practices compilation", "category": "Documentation", "priority": "High", "target": "coordinator"},
                    {"task": "Success stories collection", "category": "Documentation", "priority": "Medium", "target": "coordinator"},
                    {"task": "Knowledge management system", "category": "Technical", "priority": "High", "target": "analyst"},
                    {"task": "Case study development", "category": "Documentation", "priority": "Medium", "target": "coordinator"}
                ],
                4: [  # Week 4: Apr 26-30
                    {"task": "Finalize Year 1 Annual Report", "category": "Reporting", "priority": "High", "target": "coordinator"},
                    {"task": "Submit Annual Report to MITRA", "category": "Reporting", "priority": "High", "target": "lead"},
                    {"task": "Phase 4 kick-off planning", "category": "Planning", "priority": "High", "target": "lead"},
                    {"task": "Client presentation - Year 1 results", "category": "Meetings", "priority": "High", "target": "all"},
                    {"task": "May 2027 planning", "category": "Planning", "priority": "Medium", "target": "lead"}
                ]
            }
        week_key = week_num if week_num <= 4 else 4
        tasks = tasks_by_week.get(week_key, [{"task": "Continue Phase 3 activities", "category": "Implementation", "priority": "Medium", "target": "coordinator"}])
        idx = min(day_num - 1, len(tasks) - 1)
        return tasks[idx]

def generate_phase_4_tasks(date, week_num, day_num):
    """Phase 4: Enhancement (Months 13-18) - May to October 2027"""
    
    if date.month == 5:  # May 2027 - Year 2 Kick-off
        tasks_by_week = {
            1: [  # Week 1: May 3-7
                {"task": "Year 2 kick-off meeting", "category": "Meetings", "priority": "High", "target": "all"},
                {"task": "Review Year 1 performance", "category": "Analysis", "priority": "High", "target": "coordinator"},
                {"task": "Set Year 2 targets", "category": "Planning", "priority": "High", "target": "lead"},
                {"task": "Team goal alignment", "category": "Meetings", "priority": "High", "target": "all"},
                {"task": "Year 2 action plan finalization", "category": "Planning", "priority": "High", "target": "lead"}
            ],
            2: [  # Week 2: May 10-14
                {"task": "Enhanced data collection protocols", "category": "Data Collection", "priority": "High", "target": "coordinator"},
                {"task": "Advanced analytics setup", "category": "Technical", "priority": "High", "target": "analyst"},
                {"task": "Predictive modeling planning", "category": "Analysis", "priority": "High", "target": "analyst"},
                {"task": "Data visualization enhancements", "category": "Technical", "priority": "High", "target": "analyst"},
                {"task": "Dashboard upgrades", "category": "Technical", "priority": "Medium", "target": "analyst"}
            ],
            3: [  # Week 3: May 17-21
                {"task": "International ranking agency engagement", "category": "Outreach", "priority": "High", "target": "coordinator"},
                {"task": "QS ranking submission preparation", "category": "Reporting", "priority": "High", "target": "coordinator"},
                {"task": "THE ranking data compilation", "category": "Data Collection", "priority": "High", "target": "coordinator"},
                {"task": "US News ranking readiness", "category": "Assessment", "priority": "High", "target": "coordinator"},
                {"task": "Ranking improvement strategies", "category": "Planning", "priority": "High", "target": "coordinator"}
            ],
            4: [  # Week 4: May 24-28
                {"task": "Prepare May MPR", "category": "Reporting", "priority": "High", "target": "coordinator"},
                {"task": "Client review meeting", "category": "Meetings", "priority": "High", "target": "all"},
                {"task": "Ranking submission progress report", "category": "Reporting", "priority": "High", "target": "coordinator"},
                {"task": "Plan June activities", "category": "Planning", "priority": "Medium", "target": "lead"},
                {"task": "Team performance review", "category": "Meetings", "priority": "Medium", "target": "lead"}
            ]
        }
        week_key = week_num if week_num <= 4 else 4
        tasks = tasks_by_week.get(week_key, [{"task": "Continue Year 2 activities", "category": "Implementation", "priority": "Medium", "target": "coordinator"}])
        idx = min(day_num - 1, len(tasks) - 1)
        return tasks[idx]
    
    elif date.month == 6:  # June 2027 - Milestone 4 (10% Improvement)
        tasks_by_week = {
            1: [  # Week 1: May 31-Jun 4
                {"task": "Milestone 4 data collection", "category": "Data Collection", "priority": "High", "target": "coordinator"},
                {"task": "Performance improvement calculation", "category": "Analysis", "priority": "High", "target": "coordinator"},
                {"task": "Baseline vs current comparison", "category": "Analysis", "priority": "High", "target": "coordinator"},
                {"task": "Improvement validation", "category": "Assessment", "priority": "High", "target": "coordinator"},
                {"task": "Prepare evidence documentation", "category": "Documentation", "priority": "High", "target": "coordinator"}
            ],
            2: [  # Week 2: Jun 7-11
                {"task": "Submit Milestone 4 report", "category": "Reporting", "priority": "High", "target": "coordinator"},
                {"task": "Client presentation - 10% improvement", "category": "Meetings", "priority": "High", "target": "all"},
                {"task": "Mid-year performance assessment", "category": "Assessment", "priority": "High", "target": "coordinator"},
                {"task": "Identify areas for further improvement", "category": "Analysis", "priority": "High", "target": "coordinator"},
                {"task": "Action plan for remaining year", "category": "Planning", "priority": "High", "target": "coordinator"}
            ],
            3: [  # Week 3: Jun 14-18
                {"task": "Advanced training programs", "category": "Training", "priority": "High", "target": "coordinator"},
                {"task": "GRDAU advanced training", "category": "Training", "priority": "High", "target": "coordinator"},
                {"task": "Data analytics advanced workshop", "category": "Training", "priority": "High", "target": "analyst"},
                {"task": "Research publication workshop", "category": "Training", "priority": "High", "target": "coordinator"},
                {"task": "Training effectiveness assessment", "category": "Assessment", "priority": "Medium", "target": "coordinator"}
            ],
            4: [  # Week 4: Jun 21-25, 28-30
                {"task": "Prepare June MPR", "category": "Reporting", "priority": "High", "target": "coordinator"},
                {"task": "Research publication tracking", "category": "Data Collection", "priority": "High", "target": "coordinator"},
                {"task": "Citation analysis report", "category": "Analysis", "priority": "High", "target": "coordinator"},
                {"task": "Client review meeting", "category": "Meetings", "priority": "High", "target": "all"},
                {"task": "Plan July activities", "category": "Planning", "priority": "Medium", "target": "lead"}
            ]
        }
        week_key = week_num if week_num <= 4 else 4
        tasks = tasks_by_week.get(week_key, [{"task": "Continue Milestone 4 activities", "category": "Reporting", "priority": "Medium", "target": "coordinator"}])
        idx = min(day_num - 1, len(tasks) - 1)
        return tasks[idx]
    
    else:  # July-October 2027 - Enhancement and Global Engagement
        if date.month == 7:
            tasks_by_week = {
                1: [  # July 1-2, 5-9
                    {"task": "Publication support program", "category": "Research", "priority": "High", "target": "coordinator"},
                    {"task": "Research writing workshop", "category": "Training", "priority": "High", "target": "coordinator"},
                    {"task": "Journal submission support", "category": "Research", "priority": "High", "target": "coordinator"},
                    {"task": "Research collaboration facilitation", "category": "Outreach", "priority": "High", "target": "coordinator"},
                    {"task": "Research impact measurement", "category": "Analysis", "priority": "Medium", "target": "coordinator"}
                ],
                2: [  # July 12-16
                    {"task": "IPR and patent filing support", "category": "Research", "priority": "High", "target": "coordinator"},
                    {"task": "Patent filing process training", "category": "Training", "priority": "High", "target": "coordinator"},
                    {"task": "IPR policy development", "category": "Documentation", "priority": "High", "target": "coordinator"},
                    {"task": "Patent search and analysis", "category": "Analysis", "priority": "High", "target": "coordinator"},
                    {"task": "Technology transfer office setup", "category": "Setup", "priority": "Medium", "target": "coordinator"}
                ],
                3: [  # July 19-23
                    {"task": "International student enrollment strategy", "category": "Outreach", "priority": "High", "target": "coordinator"},
                    {"task": "International marketing plan", "category": "Planning", "priority": "High", "target": "coordinator"},
                    {"task": "Student exchange programs", "category": "Outreach", "priority": "High", "target": "coordinator"},
                    {"task": "International admission process", "category": "Documentation", "priority": "Medium", "target": "coordinator"},
                    {"task": "International student support", "category": "Planning", "priority": "Medium", "target": "coordinator"}
                ],
                4: [  # July 26-30
                    {"task": "Prepare July MPR", "category": "Reporting", "priority": "High", "target": "coordinator"},
                    {"task": "SDG research alignment", "category": "Research", "priority": "High", "target": "coordinator"},
                    {"task": "SDG impact assessment", "category": "Analysis", "priority": "High", "target": "coordinator"},
                    {"task": "Client review meeting", "category": "Meetings", "priority": "High", "target": "all"},
                    {"task": "Plan August activities", "category": "Planning", "priority": "Medium", "target": "lead"}
                ]
            }
        elif date.month == 8:
            tasks_by_week = {
                1: [  # Aug 2-6
                    {"task": "Academic reputation building", "category": "Outreach", "priority": "High", "target": "coordinator"},
                    {"task": "Faculty recognition program", "category": "Planning", "priority": "High", "target": "coordinator"},
                    {"task": "Award nominations", "category": "Outreach", "priority": "High", "target": "coordinator"},
                    {"task": "Media engagement strategy", "category": "Planning", "priority": "Medium", "target": "coordinator"},
                    {"task": "University branding", "category": "Communication", "priority": "Medium", "target": "coordinator"}
                ],
                2: [  # Aug 9-13
                    {"task": "Employer perception enhancement", "category": "Outreach", "priority": "High", "target": "coordinator"},
                    {"task": "Industry advisory board formation", "category": "Setup", "priority": "High", "target": "coordinator"},
                    {"task": "Corporate connect program", "category": "Outreach", "priority": "High", "target": "coordinator"},
                    {"task": "Placement enhancement strategies", "category": "Planning", "priority": "High", "target": "coordinator"},
                    {"task": "Alumni engagement program", "category": "Outreach", "priority": "Medium", "target": "coordinator"}
                ],
                3: [  # Aug 16-20
                    {"task": "Dashboard enhancements", "category": "Technical", "priority": "High", "target": "analyst"},
                    {"task": "New analytics features", "category": "Technical", "priority": "High", "target": "analyst"},
                    {"task": "Predictive analytics module", "category": "Technical", "priority": "High", "target": "analyst"},
                    {"task": "User feedback implementation", "category": "Technical", "priority": "High", "target": "analyst"},
                    {"task": "Performance optimization", "category": "Technical", "priority": "Medium", "target": "analyst"}
                ],
                4: [  # Aug 23-27
                    {"task": "Prepare August MPR", "category": "Reporting", "priority": "High", "target": "coordinator"},
                    {"task": "Employer perception survey", "category": "Data Collection", "priority": "High", "target": "coordinator"},
                    {"task": "Survey analysis", "category": "Analysis", "priority": "High", "target": "coordinator"},
                    {"task": "Client review meeting", "category": "Meetings", "priority": "High", "target": "all"},
                    {"task": "Plan September activities", "category": "Planning", "priority": "Medium", "target": "lead"}
                ]
            }
        elif date.month == 9:
            tasks_by_week = {
                1: [  # Aug 30-Sep 3
                    {"task": "Citation analysis and improvement", "category": "Analysis", "priority": "High", "target": "coordinator"},
                    {"task": "Citation tracking system", "category": "Technical", "priority": "High", "target": "analyst"},
                    {"task": "Research impact report", "category": "Reporting", "priority": "High", "target": "coordinator"},
                    {"task": "High-impact journal targeting", "category": "Research", "priority": "High", "target": "coordinator"},
                    {"task": "Citation enhancement workshop", "category": "Training", "priority": "Medium", "target": "coordinator"}
                ],
                2: [  # Sep 6-10
                    {"task": "Global ranking submission preparation", "category": "Reporting", "priority": "High", "target": "coordinator"},
                    {"task": "QS ranking data finalization", "category": "Data Collection", "priority": "High", "target": "coordinator"},
                    {"task": "THE ranking submission", "category": "Reporting", "priority": "High", "target": "coordinator"},
                    {"task": "Ranking data validation", "category": "Data Collection", "priority": "High", "target": "coordinator"},
                    {"task": "Ranking improvement analysis", "category": "Analysis", "priority": "High", "target": "coordinator"}
                ],
                3: [  # Sep 13-17
                    {"task": "Milestone 5 preparation (20% improvement)", "category": "Reporting", "priority": "High", "target": "coordinator"},
                    {"task": "Performance data compilation", "category": "Data Collection", "priority": "High", "target": "coordinator"},
                    {"task": "20% improvement calculation", "category": "Analysis", "priority": "High", "target": "coordinator"},
                    {"task": "Evidence collection", "category": "Documentation", "priority": "High", "target": "coordinator"},
                    {"task": "Submit Milestone 5 report", "category": "Reporting", "priority": "High", "target": "coordinator"}
                ],
                4: [  # Sep 20-24, 27-30
                    {"task": "Prepare September MPR", "category": "Reporting", "priority": "High", "target": "coordinator"},
                    {"task": "Client milestone presentation", "category": "Meetings", "priority": "High", "target": "all"},
                    {"task": "Phase 4 progress review", "category": "Meetings", "priority": "High", "target": "all"},
                    {"task": "Plan Phase 5 activities", "category": "Planning", "priority": "High", "target": "lead"},
                    {"task": "Team performance review", "category": "Meetings", "priority": "Medium", "target": "lead"}
                ]
            }
        else:  # October 2027
            tasks_by_week = {
                1: [  # Oct 1, 4-8
                    {"task": "Final ranking submission review", "category": "Reporting", "priority": "High", "target": "coordinator"},
                    {"task": "Complete all ranking submissions", "category": "Reporting", "priority": "High", "target": "coordinator"},
                    {"task": "Ranking outcome tracking", "category": "Analysis", "priority": "High", "target": "coordinator"},
                    {"task": "Prepare ranking reports", "category": "Reporting", "priority": "High", "target": "coordinator"},
                    {"task": "Client ranking update", "category": "Meetings", "priority": "High", "target": "all"}
                ],
                2: [  # Oct 11-15
                    {"task": "Phase 4 completion review", "category": "Meetings", "priority": "High", "target": "all"},
                    {"task": "Documentation consolidation", "category": "Documentation", "priority": "High", "target": "coordinator"},
                    {"task": "Knowledge transfer preparation", "category": "Planning", "priority": "High", "target": "coordinator"},
                    {"task": "Sustainability planning", "category": "Planning", "priority": "High", "target": "lead"},
                    {"task": "Handover documentation", "category": "Documentation", "priority": "High", "target": "coordinator"}
                ],
                3: [  # Oct 18-22
                    {"task": "Prepare October MPR", "category": "Reporting", "priority": "High", "target": "coordinator"},
                    {"task": "Phase 4 achievements report", "category": "Reporting", "priority": "High", "target": "coordinator"},
                    {"task": "Lessons learned Phase 4", "category": "Documentation", "priority": "Medium", "target": "coordinator"},
                    {"task": "Client review meeting", "category": "Meetings", "priority": "High", "target": "all"},
                    {"task": "Plan Phase 5 activities", "category": "Planning", "priority": "High", "target": "lead"}
                ],
                4: [  # Oct 25-29
                    {"task": "Phase 5 kick-off planning", "category": "Planning", "priority": "High", "target": "lead"},
                    {"task": "Final evaluation framework", "category": "Planning", "priority": "High", "target": "coordinator"},
                    {"task": "Sustainability plan finalization", "category": "Documentation", "priority": "High", "target": "lead"},
                    {"task": "Team meeting for Phase 5", "category": "Meetings", "priority": "High", "target": "all"},
                    {"task": "November 2027 planning", "category": "Planning", "priority": "Medium", "target": "lead"}
                ]
            }
        week_key = week_num if week_num <= 4 else 4
        tasks = tasks_by_week.get(week_key, [{"task": "Continue Phase 4 activities", "category": "Implementation", "priority": "Medium", "target": "coordinator"}])
        idx = min(day_num - 1, len(tasks) - 1)
        return tasks[idx]

def generate_phase_5_tasks(date, week_num, day_num):
    """Phase 5: Finalization (Months 19-24) - November 2027 to April 2028"""
    
    if date.month == 11:  # November 2027
        tasks_by_week = {
            1: [  # Nov 1-5
                {"task": "Phase 5 kick-off", "category": "Meetings", "priority": "High", "target": "all"},
                {"task": "Final ranking submission timeline", "category": "Planning", "priority": "High", "target": "coordinator"},
                {"task": "Data finalization for rankings", "category": "Data Collection", "priority": "High", "target": "coordinator"},
                {"task": "Final data validation", "category": "Analysis", "priority": "High", "target": "coordinator"},
                {"task": "Ranking submission preparation", "category": "Reporting", "priority": "High", "target": "coordinator"}
            ],
            2: [  # Nov 8-12
                {"task": "Global ranking final submissions", "category": "Reporting", "priority": "High", "target": "coordinator"},
                {"task": "QS final submission", "category": "Reporting", "priority": "High", "target": "coordinator"},
                {"task": "THE final submission", "category": "Reporting", "priority": "High", "target": "coordinator"},
                {"task": "US News final submission", "category": "Reporting", "priority": "High", "target": "coordinator"},
                {"task": "Submission confirmation tracking", "category": "Documentation", "priority": "Medium", "target": "coordinator"}
            ],
            3: [  # Nov 15-19
                {"task": "Milestone 6 preparation", "category": "Reporting", "priority": "High", "target": "coordinator"},
                {"task": "Global rankings participation evidence", "category": "Documentation", "priority": "High", "target": "coordinator"},
                {"task": "10 colleges ranking confirmation", "category": "Data Collection", "priority": "High", "target": "coordinator"},
                {"task": "Submit Milestone 6 report", "category": "Reporting", "priority": "High", "target": "coordinator"},
                {"task": "Client presentation", "category": "Meetings", "priority": "High", "target": "all"}
            ],
            4: [  # Nov 22-26, 29-30
                {"task": "Prepare November MPR", "category": "Reporting", "priority": "High", "target": "coordinator"},
                {"task": "Final project evaluation framework", "category": "Planning", "priority": "High", "target": "lead"},
                {"task": "Sustainability plan development", "category": "Planning", "priority": "High", "target": "lead"},
                {"task": "Client review meeting", "category": "Meetings", "priority": "High", "target": "all"},
                {"task": "Plan December activities", "category": "Planning", "priority": "Medium", "target": "lead"}
            ]
        }
        week_key = week_num if week_num <= 4 else 4
        tasks = tasks_by_week.get(week_key, [{"task": "Continue Phase 5 activities", "category": "Finalization", "priority": "Medium", "target": "coordinator"}])
        idx = min(day_num - 1, len(tasks) - 1)
        return tasks[idx]
    
    elif date.month == 12:  # December 2027
        tasks_by_week = {
            1: [  # Nov 29-Dec 3
                {"task": "Final performance review", "category": "Analysis", "priority": "High", "target": "coordinator"},
                {"task": "Year-end data compilation", "category": "Data Collection", "priority": "High", "target": "coordinator"},
                {"task": "Final improvement calculation", "category": "Analysis", "priority": "High", "target": "coordinator"},
                {"task": "Performance report preparation", "category": "Reporting", "priority": "High", "target": "coordinator"},
                {"task": "Baseline to endline comparison", "category": "Analysis", "priority": "High", "target": "coordinator"}
            ],
            2: [  # Dec 6-10
                {"task": "Milestone 5 final submission (20% improvement)", "category": "Reporting", "priority": "High", "target": "coordinator"},
                {"task": "Submit Milestone 5 report", "category": "Reporting", "priority": "High", "target": "coordinator"},
                {"task": "Client presentation - 20% improvement", "category": "Meetings", "priority": "High", "target": "all"},
                {"task": "Final outcomes documentation", "category": "Documentation", "priority": "High", "target": "coordinator"},
                {"task": "Success stories compilation", "category": "Documentation", "priority": "Medium", "target": "coordinator"}
            ],
            3: [  # Dec 13-17
                {"task": "Sustainability planning workshop", "category": "Meetings", "priority": "High", "target": "all"},
                {"task": "GRDAU sustainability plan", "category": "Planning", "priority": "High", "target": "coordinator"},
                {"task": "Dashboard handover plan", "category": "Planning", "priority": "High", "target": "analyst"},
                {"task": "Training sustainability", "category": "Planning", "priority": "High", "target": "coordinator"},
                {"task": "Knowledge transfer strategy", "category": "Planning", "priority": "High", "target": "lead"}
            ],
            4: [  # Dec 20-24, 27-31
                {"task": "Prepare December MPR", "category": "Reporting", "priority": "High", "target": "coordinator"},
                {"task": "Final project documentation", "category": "Documentation", "priority": "High", "target": "coordinator"},
                {"task": "Year-end report", "category": "Reporting", "priority": "High", "target": "coordinator"},
                {"task": "Client year-end review", "category": "Meetings", "priority": "High", "target": "all"},
                {"task": "Plan January 2028 activities", "category": "Planning", "priority": "Medium", "target": "lead"}
            ]
        }
        week_key = week_num if week_num <= 4 else 4
        tasks = tasks_by_week.get(week_key, [{"task": "Continue finalization", "category": "Finalization", "priority": "Medium", "target": "coordinator"}])
        idx = min(day_num - 1, len(tasks) - 1)
        return tasks[idx]
    
    elif date.month == 1:  # January 2028
        tasks_by_week = {
            1: [  # Jan 3-7
                {"task": "Final dashboard review", "category": "Technical", "priority": "High", "target": "analyst"},
                {"task": "System optimization", "category": "Technical", "priority": "High", "target": "analyst"},
                {"task": "Final bug fixes", "category": "Technical", "priority": "High", "target": "analyst"},
                {"task": "Performance testing", "category": "Technical", "priority": "High", "target": "analyst"},
                {"task": "Security audit", "category": "Assessment", "priority": "High", "target": "analyst"}
            ],
            2: [  # Jan 10-14
                {"task": "Knowledge transfer sessions", "category": "Training", "priority": "High", "target": "coordinator"},
                {"task": "GRDAU staff final training", "category": "Training", "priority": "High", "target": "coordinator"},
                {"task": "System administrator training", "category": "Training", "priority": "High", "target": "analyst"},
                {"task": "Documentation handover", "category": "Documentation", "priority": "High", "target": "coordinator"},
                {"task": "User manual finalization", "category": "Documentation", "priority": "Medium", "target": "coordinator"}
            ],
            3: [  # Jan 17-21
                {"task": "Milestone 7 preparation (Final Evaluation)", "category": "Reporting", "priority": "High", "target": "coordinator"},
                {"task": "Final project evaluation", "category": "Assessment", "priority": "High", "target": "lead"},
                {"task": "Lessons learned documentation", "category": "Documentation", "priority": "High", "target": "coordinator"},
                {"task": "Recommendations report", "category": "Reporting", "priority": "High", "target": "lead"},
                {"task": "Submit Milestone 7 draft", "category": "Reporting", "priority": "High", "target": "coordinator"}
            ],
            4: [  # Jan 24-28, 31
                {"task": "Prepare January MPR", "category": "Reporting", "priority": "High", "target": "coordinator"},
                {"task": "Final report review with client", "category": "Meetings", "priority": "High", "target": "all"},
                {"task": "Incorporate client feedback", "category": "Documentation", "priority": "High", "target": "coordinator"},
                {"task": "Final report finalization", "category": "Reporting", "priority": "High", "target": "coordinator"},
                {"task": "Plan February activities", "category": "Planning", "priority": "Medium", "target": "lead"}
            ]
        }
        week_key = week_num if week_num <= 4 else 4
        tasks = tasks_by_week.get(week_key, [{"task": "Continue finalization", "category": "Finalization", "priority": "Medium", "target": "coordinator"}])
        idx = min(day_num - 1, len(tasks) - 1)
        return tasks[idx]
    
    elif date.month == 2:  # February 2028
        tasks_by_week = {
            1: [  # Feb 1-4
                {"task": "Final evaluation report submission", "category": "Reporting", "priority": "High", "target": "coordinator"},
                {"task": "Submit Milestone 7 report", "category": "Reporting", "priority": "High", "target": "coordinator"},
                {"task": "Client presentation - final results", "category": "Meetings", "priority": "High", "target": "all"},
                {"task": "Final approval process", "category": "Reporting", "priority": "High", "target": "lead"},
                {"task": "Project closure documentation", "category": "Documentation", "priority": "High", "target": "coordinator"}
            ],
            2: [  # Feb 7-11
                {"task": "Complete project handover", "category": "Documentation", "priority": "High", "target": "all"},
                {"task": "Handover all deliverables", "category": "Documentation", "priority": "High", "target": "coordinator"},
                {"task": "Final data export", "category": "Technical", "priority": "High", "target": "analyst"},
                {"task": "Archive project materials", "category": "Documentation", "priority": "High", "target": "coordinator"},
                {"task": "Handover sign-off", "category": "Meetings", "priority": "High", "target": "lead"}
            ],
            3: [  # Feb 14-18
                {"task": "Final financial reconciliation", "category": "Documentation", "priority": "High", "target": "lead"},
                {"task": "Team performance review", "category": "Meetings", "priority": "High", "target": "lead"},
                {"task": "Project success celebration", "category": "Meetings", "priority": "Medium", "target": "all"},
                {"task": "Prepare final MPR", "category": "Reporting", "priority": "High", "target": "coordinator"},
                {"task": "Client satisfaction survey", "category": "Data Collection", "priority": "Medium", "target": "lead"}
            ],
            4: [  # Feb 21-25, 28-29
                {"task": "Prepare February MPR", "category": "Reporting", "priority": "High", "target": "coordinator"},
                {"task": "Final project closure report", "category": "Reporting", "priority": "High", "target": "coordinator"},
                {"task": "Submit final deliverables to MITRA", "category": "Reporting", "priority": "High", "target": "lead"},
                {"task": "Project closure meeting", "category": "Meetings", "priority": "High", "target": "all"},
                {"task": "Plan March activities (wrap-up)", "category": "Planning", "priority": "Medium", "target": "lead"}
            ]
        }
        week_key = week_num if week_num <= 4 else 4
        tasks = tasks_by_week.get(week_key, [{"task": "Continue handover", "category": "Handover", "priority": "Medium", "target": "coordinator"}])
        idx = min(day_num - 1, len(tasks) - 1)
        return tasks[idx]
    
    else:  # March-April 2028 - Final Wrap-up
        if date.month == 3:
            tasks_by_week = {
                1: [  # Mar 1-3, 6-10
                    {"task": "Final report submission to World Bank", "category": "Reporting", "priority": "High", "target": "lead"},
                    {"task": "Project success documentation", "category": "Documentation", "priority": "High", "target": "coordinator"},
                    {"task": "Impact assessment report", "category": "Reporting", "priority": "High", "target": "coordinator"},
                    {"task": "Policy recommendations", "category": "Documentation", "priority": "High", "target": "lead"},
                    {"task": "Final client presentation", "category": "Meetings", "priority": "High", "target": "all"}
                ],
                2: [  # Mar 13-17
                    {"task": "Complete all pending documentation", "category": "Documentation", "priority": "High", "target": "coordinator"},
                    {"task": "Finalize all reports", "category": "Reporting", "priority": "High", "target": "coordinator"},
                    {"task": "Archive all project data", "category": "Documentation", "priority": "High", "target": "analyst"},
                    {"task": "Knowledge management system handover", "category": "Technical", "priority": "High", "target": "analyst"},
                    {"task": "Final system backup", "category": "Technical", "priority": "Medium", "target": "analyst"}
                ],
                3: [  # Mar 20-24
                    {"task": "Prepare March MPR", "category": "Reporting", "priority": "High", "target": "coordinator"},
                    {"task": "Final project evaluation", "category": "Assessment", "priority": "High", "target": "lead"},
                    {"task": "Team debrief session", "category": "Meetings", "priority": "High", "target": "all"},
                    {"task": "Lessons learned workshop", "category": "Meetings", "priority": "High", "target": "all"},
                    {"task": "Project completion certificate", "category": "Documentation", "priority": "Medium", "target": "lead"}
                ],
                4: [  # Mar 27-31
                    {"task": "Final client sign-off", "category": "Meetings", "priority": "High", "target": "lead"},
                    {"task": "Contract closure", "category": "Documentation", "priority": "High", "target": "lead"},
                    {"task": "Final financial closure", "category": "Documentation", "priority": "High", "target": "lead"},
                    {"task": "Release of Bank Guarantee", "category": "Documentation", "priority": "High", "target": "lead"},
                    {"task": "Project closure party", "category": "Meetings", "priority": "Medium", "target": "all"}
                ]
            }
        else:  # April 2028
            tasks_by_week = {
                1: [  # Apr 3-7
                    {"task": "Final project completion report", "category": "Reporting", "priority": "High", "target": "coordinator"},
                    {"task": "Submit final deliverables", "category": "Reporting", "priority": "High", "target": "lead"},
                    {"task": "Project closure documentation", "category": "Documentation", "priority": "High", "target": "coordinator"},
                    {"task": "Final MPR submission", "category": "Reporting", "priority": "High", "target": "coordinator"},
                    {"task": "Client acknowledgment", "category": "Meetings", "priority": "High", "target": "lead"}
                ],
                2: [  # Apr 10-14
                    {"task": "Final team meeting", "category": "Meetings", "priority": "High", "target": "all"},
                    {"task": "Project success celebration", "category": "Meetings", "priority": "High", "target": "all"},
                    {"task": "Individual performance reviews", "category": "Meetings", "priority": "High", "target": "lead"},
                    {"task": "Future recommendations", "category": "Documentation", "priority": "Medium", "target": "lead"},
                    {"task": "Project archive finalization", "category": "Documentation", "priority": "Medium", "target": "coordinator"}
                ],
                3: [  # Apr 17-21
                    {"task": "Final report submission to MITRA", "category": "Reporting", "priority": "High", "target": "lead"},
                    {"task": "Project completion presentation", "category": "Meetings", "priority": "High", "target": "all"},
                    {"task": "Contract completion certificate", "category": "Documentation", "priority": "High", "target": "lead"},
                    {"task": "Team appreciation", "category": "Meetings", "priority": "Medium", "target": "lead"},
                    {"task": "Project close-out", "category": "Meetings", "priority": "High", "target": "all"}
                ],
                4: [  # Apr 24-28
                    {"task": "Final project closure", "category": "Meetings", "priority": "High", "target": "all"},
                    {"task": "Handover completion", "category": "Documentation", "priority": "High", "target": "lead"},
                    {"task": "Project success metrics", "category": "Reporting", "priority": "High", "target": "coordinator"},
                    {"task": "Lessons learned final compilation", "category": "Documentation", "priority": "Medium", "target": "coordinator"},
                    {"task": "CONTRACT COMPLETION - May 6, 2028", "category": "Milestone", "priority": "High", "target": "all"}
                ]
            }
        week_key = week_num if week_num <= 4 else 4
        tasks = tasks_by_week.get(week_key, [{"task": "Complete project closure", "category": "Closure", "priority": "High", "target": "all"}])
        idx = min(day_num - 1, len(tasks) - 1)
        return tasks[idx]

def generate_all_tasks():
    """Generate complete 24-month daily tasks"""
    all_tasks = {}
    
    start_date = datetime(2026, 5, 4)
    end_date = datetime(2028, 4, 28)
    working_dates = get_working_dates(start_date, end_date)
    
    for date in working_dates:
        # Calculate month number from start
        month_diff = (date.year - start_date.year) * 12 + (date.month - start_date.month)
        month_num = month_diff + 1
        
        # Calculate week of month
        week_num = (date.day - 1) // 7 + 1
        day_num = date.day
        
        # Determine which phase
        if month_num <= 3:
            task_info = generate_phase_1_tasks(date, week_num, day_num)
        elif month_num <= 6:
            task_info = generate_phase_2_tasks(date, week_num, day_num)
        elif month_num <= 12:
            task_info = generate_phase_3_tasks(date, week_num, day_num)
        elif month_num <= 18:
            task_info = generate_phase_4_tasks(date, week_num, day_num)
        else:
            task_info = generate_phase_5_tasks(date, week_num, day_num)
        
        date_str = date.strftime("%Y-%m-%d")
        all_tasks[date_str] = {
            "task": task_info["task"],
            "category": task_info["category"],
            "priority": task_info["priority"],
            "target": task_info["target"],
            "phase": get_phase_name(month_num),
            "month_num": month_num,
            "day_of_week": date.strftime("%A")
        }
    
    return all_tasks

def get_phase_name(month_num):
    if month_num <= 3:
        return "Phase 1: Foundation"
    elif month_num <= 6:
        return "Phase 2: Planning"
    elif month_num <= 12:
        return "Phase 3: Implementation"
    elif month_num <= 18:
        return "Phase 4: Enhancement"
    else:
        return "Phase 5: Finalization"

# ============================================================
# DATA MANAGEMENT FUNCTIONS
# ============================================================

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as f:
            return json.load(f)
    tasks = generate_all_tasks()
    save_tasks(tasks)
    return tasks

def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)

def load_completions():
    if os.path.exists(TASK_COMPLETION_FILE):
        with open(TASK_COMPLETION_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_completions(completions):
    with open(TASK_COMPLETION_FILE, 'w') as f:
        json.dump(completions, f, indent=2)

def load_assignments():
    if os.path.exists(ASSIGNMENTS_FILE):
        with open(ASSIGNMENTS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_assignments(assignments):
    with open(ASSIGNMENTS_FILE, 'w') as f:
        json.dump(assignments, f, indent=2)

def get_user_tasks(email, target_date=None):
    user = USERS.get(email, {})
    user_role = user.get("role", "")
    user_team = user.get("team", "")
    
    all_tasks = load_tasks()
    completions = load_completions()
    user_completions = completions.get(email, {})
    
    user_tasks = []
    
    for date_str, task_info in all_tasks.items():
        if target_date and date_str != target_date:
            continue
        
        # Check if task is assigned to this user
        target = task_info.get("target", "")
        is_assigned = (
            target == "all" or
            (user_role == "project_lead" and target in ["lead", "all"]) or
            (user_role == "data_analyst" and target in ["coordinator", "analyst", "all"])
        )
        
        if is_assigned:
            is_completed = date_str in user_completions
            completion_info = user_completions.get(date_str, {})
            
            user_tasks.append({
                "date": date_str,
                "day": datetime.strptime(date_str, "%Y-%m-%d").strftime("%A"),
                "task": task_info["task"],
                "category": task_info["category"],
                "priority": task_info["priority"],
                "phase": task_info["phase"],
                "status": "Completed" if is_completed else "Pending",
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

def get_team_summary():
    completions = load_completions()
    all_tasks = load_tasks()
    total_tasks = len(all_tasks)
    
    summary = []
    for email, user in USERS.items():
        if user.get("role") == "data_analyst":
            user_completions = len(completions.get(email, {}))
            summary.append({
                "Name": user["name"],
                "Team": user.get("team", "N/A"),
                "Completed": user_completions,
                "Total": total_tasks,
                "Progress %": round((user_completions / total_tasks * 100), 1) if total_tasks > 0 else 0
            })
    
    return pd.DataFrame(summary)

def show_credentials():
    st.markdown("""
    <div class="credentials-box">
        <h4>🔐 Default Login Credentials</h4>
        <p><strong>Password format:</strong> <code>FirstName@2026</code> (e.g., Admin@2026, Sneha@2026)</p>
        <table style="width:100%">
            <tr><th>Role</th><th>Email</th><th>Password</th></tr>
            <tr><td><span class="role-badge admin-badge">Admin</span></td><td>admin@mahastride.com</td><td>Admin@2026</td></tr>
            <tr><td><span class="role-badge lead-badge">Project Lead</span></td><td>projectlead@mahastride.com</td><td>ProjectLead@2026</td></tr>
            <tr><td rowspan="2"><span class="role-badge analyst-badge">Data Analyst</span></td><td>sneha@mu.edu</td><td>Sneha@2026</td></tr>
            <tr><td>shubham@mitra.gov.in</td><td>Shubham@2026</td></tr>
        </table>
        <p style="margin-top:10px; font-size:12px;">Use any email from the credentials above with password: <strong>FirstName@2026</strong></p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# DASHBOARD FUNCTIONS
# ============================================================

def admin_dashboard():
    st.markdown("## 📊 Administrator Dashboard")
    
    all_tasks = load_tasks()
    completions = load_completions()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📅 Total Working Days", len(all_tasks))
    col2.metric("👥 Total Users", len(USERS))
    col3.metric("📊 Data Analysts", sum(1 for u in USERS.values() if u.get("role") == "data_analyst"))
    col4.metric("✅ Total Completions", sum(len(c) for c in completions.values()))
    
    st.markdown("---")
    
    # Phase breakdown
    st.subheader("📈 Project Phases Breakdown")
    phase_counts = {}
    for task in all_tasks.values():
        phase = task["phase"]
        phase_counts[phase] = phase_counts.get(phase, 0) + 1
    
    fig = px.pie(values=list(phase_counts.values()), names=list(phase_counts.keys()), title="Tasks by Phase")
    st.plotly_chart(fig, use_container_width=True)
    
    # Team performance
    st.subheader("👥 Team Performance")
    df_summary = get_team_summary()
    st.dataframe(df_summary, use_container_width=True, hide_index=True)
    
    fig = px.bar(df_summary, x="Name", y="Progress %", color="Team", title="Team Progress (%)")
    st.plotly_chart(fig, use_container_width=True)

def project_lead_dashboard():
    st.markdown("## 👨‍💼 Project Lead Dashboard")
    st.markdown("**Dr. Harshal Kotwal** - ICARE Project Director")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Progress Overview", "📅 Today's Plan", "👥 Team Tasks", "📈 Analytics"])
    
    all_tasks = load_tasks()
    completions = load_completions()
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Overall progress
            total_tasks = len(all_tasks)
            total_completions = sum(len(c) for c in completions.values())
            st.metric("📊 Total Task Completions", f"{total_completions}/{total_tasks * len([u for u in USERS.values() if u.get('role') == 'data_analyst'])}")
        
        with col2:
            # Completion rate
            df_summary = get_team_summary()
            avg_progress = df_summary["Progress %"].mean() if not df_summary.empty else 0
            st.metric("📈 Average Team Progress", f"{avg_progress:.1f}%")
        
        st.markdown("---")
        
        # Phase progress
        st.subheader("Phase-wise Progress")
        phase_data = []
        for phase in ["Phase 1: Foundation", "Phase 2: Planning", "Phase 3: Implementation", "Phase 4: Enhancement", "Phase 5: Finalization"]:
            phase_tasks = [t for t in all_tasks.values() if t["phase"] == phase]
            phase_data.append({
                "Phase": phase,
                "Total Tasks": len(phase_tasks)
            })
        
        df_phase = pd.DataFrame(phase_data)
        fig = px.bar(df_phase, x="Phase", y="Total Tasks", title="Tasks Distribution by Phase")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        today = datetime.now().strftime("%Y-%m-%d")
        if today in all_tasks:
            task = all_tasks[today]
            st.markdown(f"""
            <div class="task-card">
                <strong>📅 {today} ({datetime.now().strftime('%A')})</strong><br>
                <strong>🎯 Task:</strong> {task['task']}<br>
                <strong>📂 Category:</strong> {task['category']}<br>
                <strong>🏷️ Priority:</strong> {task['priority']}<br>
                <strong>📍 Phase:</strong> {task['phase']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("No task scheduled for today (weekend or holiday)")
    
    with tab3:
        st.subheader("Team Member Task Status")
        
        for email, user in USERS.items():
            if user.get("role") == "data_analyst":
                with st.expander(f"👤 {user['name']} - {user.get('team', 'N/A')}"):
                    user_tasks = get_user_tasks(email)
                    completed = sum(1 for t in user_tasks if t["status"] == "Completed")
                    total = len(user_tasks)
                    st.progress(completed/total if total > 0 else 0)
                    st.caption(f"Progress: {completed}/{total} tasks completed")
                    
                    # Show recent tasks
                    recent = user_tasks[-5:] if len(user_tasks) > 5 else user_tasks
                    for task in recent:
                        status_icon = "✅" if task["status"] == "Completed" else "⏳"
                        st.markdown(f"{status_icon} {task['date']}: {task['task'][:60]}...")
    
    with tab4:
        st.subheader("Analytics Dashboard")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Task category distribution
            category_counts = {}
            for task in all_tasks.values():
                cat = task["category"]
                category_counts[cat] = category_counts.get(cat, 0) + 1
            
            fig = px.pie(values=list(category_counts.values()), names=list(category_counts.keys()), title="Task Categories")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Priority distribution
            priority_counts = {}
            for task in all_tasks.values():
                pri = task["priority"]
                priority_counts[pri] = priority_counts.get(pri, 0) + 1
            
            fig = px.bar(x=list(priority_counts.keys()), y=list(priority_counts.values()), title="Task Priorities", color=list(priority_counts.keys()))
            st.plotly_chart(fig, use_container_width=True)

def data_analyst_dashboard(email, user):
    st.markdown(f"## 📋 Task Dashboard")
    st.markdown(f"**Welcome, {user['name']}**")
    st.markdown(f"**Team:** {user.get('team', 'N/A')}")
    st.markdown(f"**Working Hours:** 10:00 AM - 6:00 PM (Monday to Friday)")
    
    tab1, tab2, tab3 = st.tabs(["📝 Today's Tasks", "📊 My Progress", "📅 All Tasks"])
    
    today = datetime.now().strftime("%Y-%m-%d")
    today_tasks = get_user_tasks(email, today)
    
    with tab1:
        if today_tasks:
            for task in today_tasks:
                if task["status"] == "Completed":
                    st.markdown(f"""
                    <div class="task-card task-card-completed">
                        ✅ <strong>COMPLETED</strong><br>
                        📅 {task['date']} ({task['day']})<br>
                        🎯 {task['task']}<br>
                        📂 Category: {task['category']}<br>
                        🏷️ Priority: {task['priority']}<br>
                        📍 Phase: {task['phase']}<br>
                        💬 Remarks: {task.get('remarks', 'No remarks')}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    with st.form(key=f"task_{task['date']}"):
                        st.markdown(f"""
                        <div class="task-card task-card-pending">
                            ⏳ <strong>PENDING</strong><br>
                            🎯 {task['task']}<br>
                            📂 Category: {task['category']}<br>
                            🏷️ Priority: {task['priority']}<br>
                            📍 Phase: {task['phase']}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("**Work Log (10:00 AM - 6:00 PM)**")
                        col1, col2 = st.columns(2)
                        with col1:
                            start_time = st.time_input("Start Time", value=datetime.strptime("10:00", "%H:%M").time())
                        with col2:
                            end_time = st.time_input("End Time", value=datetime.strptime("18:00", "%H:%M").time())
                        
                        remarks = st.text_area("Work Accomplished / Remarks", height=100, 
                                              placeholder="Describe what you worked on today...")
                        
                        if st.form_submit_button("✅ Mark as Complete", use_container_width=True):
                            work_log = f"Worked from {start_time} to {end_time}. {remarks}"
                            if mark_task_complete(email, task["date"], work_log):
                                st.success("Task completed! Great work!")
                                st.rerun()
        else:
            st.info("No tasks assigned for today. This may be a weekend or holiday.")
            st.markdown("**Working Days:** Monday to Friday only")
    
    with tab2:
        all_user_tasks = get_user_tasks(email)
        completed = sum(1 for t in all_user_tasks if t["status"] == "Completed")
        total = len(all_user_tasks)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("📊 Total Tasks", total)
        col2.metric("✅ Completed", completed)
        col3.metric("⏳ Remaining", total - completed)
        
        st.progress(completed/total if total > 0 else 0)
        
        # Phase-wise progress
        st.subheader("Phase-wise Progress")
        phase_data = []
        phases = ["Phase 1: Foundation", "Phase 2: Planning", "Phase 3: Implementation", "Phase 4: Enhancement", "Phase 5: Finalization"]
        
        for phase in phases:
            phase_tasks = [t for t in all_user_tasks if t["phase"] == phase]
            phase_completed = sum(1 for t in phase_tasks if t["status"] == "Completed")
            phase_data.append({
                "Phase": phase.split(":")[0],
                "Completed": phase_completed,
                "Total": len(phase_tasks)
            })
        
        df_phase = pd.DataFrame(phase_data)
        fig = px.bar(df_phase, x="Phase", y="Completed", title="Phase-wise Completion", 
                     text="Total", hover_data=["Total"])
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        all_user_tasks = get_user_tasks(email)
        
        # Filter options
        col1, col2 = st.columns(2)
        with col1:
            filter_phase = st.selectbox("Filter by Phase", ["All"] + list(set(t["phase"] for t in all_user_tasks)))
        with col2:
            filter_status = st.selectbox("Filter by Status", ["All", "Pending", "Completed"])
        
        filtered_tasks = all_user_tasks
        if filter_phase != "All":
            filtered_tasks = [t for t in filtered_tasks if t["phase"] == filter_phase]
        if filter_status != "All":
            filtered_tasks = [t for t in filtered_tasks if t["status"] == filter_status]
        
        df_tasks = pd.DataFrame(filtered_tasks)
        st.dataframe(df_tasks, use_container_width=True, hide_index=True)
        
        # Export option
        csv = df_tasks.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Tasks as CSV", csv, f"my_tasks_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")

# ============================================================
# MAIN APP
# ============================================================

def main():
    # Initialize tasks if needed
    if not os.path.exists(TASKS_FILE):
        tasks = generate_all_tasks()
        save_tasks(tasks)
    
    # Authentication
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        st.markdown("""
        <div class="main-header">
            <h1>📋 MahaSTRIDE 24-Month Task Management System</h1>
            <p>May 2026 - April 2028 | Monday to Friday | 10:00 AM - 6:00 PM</p>
            <p>Complete daily task assignment and progress tracking for all 24 months</p>
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
        st.markdown(f"**Welcome,**")
        st.markdown(f"**{user_info.get('name')}**")
        
        if role == "data_analyst":
            st.markdown(f"*Team: {user_info.get('team', 'N/A')}*")
        
        st.markdown(f"*Role: {role.upper()}*")
        st.markdown("---")
        
        if role == "admin":
            menu = st.radio("Navigation", ["📊 Dashboard", "👥 Team Management"])
        elif role == "project_lead":
            menu = st.radio("Navigation", ["👨‍💼 Lead Dashboard"])
        else:
            menu = st.radio("Navigation", ["📝 My Tasks"])
        
        st.markdown("---")
        st.markdown("**Working Hours**")
        st.markdown("🕐 10:00 AM - 6:00 PM")
        st.markdown("📅 Monday to Friday")
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()
    
    # Main content based on role
    if role == "admin":
        if menu == "📊 Dashboard":
            admin_dashboard()
        else:
            st.markdown("## 👥 Team Management")
            df_users = pd.DataFrame([{
                "Name": u["name"],
                "Role": u["role"],
                "Team": u.get("team", "N/A")
            } for u in USERS.values()])
            st.dataframe(df_users, use_container_width=True, hide_index=True)
    
    elif role == "project_lead":
        project_lead_dashboard()
    
    else:
        data_analyst_dashboard(email, user_info)
    
    # Footer
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: #666; font-size: 0.8rem;">
        <p>© 2026-2028 MahaSTRIDE Project | World Bank Loan No: IBRD 9737-IN | ICARE Pvt. Ltd.</p>
        <p>24-Month Project: May 2026 - April 2028 | Working Days: Monday to Friday | Hours: 10:00 - 18:00</p>
        <p>Last Updated: {datetime.now().strftime('%d %B %Y, %H:%M:%S')}</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
