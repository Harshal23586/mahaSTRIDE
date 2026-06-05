import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import calendar
import json
import os
from hashlib import sha256
import base64

# Page configuration
st.set_page_config(
    page_title="MahaSTRIDE - Project Management System",
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
    .dashboard-card {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        margin: 0;
    }
    .metric-label {
        font-size: 0.8rem;
        opacity: 0.9;
        margin: 0;
    }
    .nav-tab {
        padding: 0.5rem 1rem;
        border-radius: 5px;
        margin: 0.2rem 0;
        cursor: pointer;
    }
    .nav-tab-active {
        background-color: #2a5298;
        color: white;
    }
    .task-card {
        background: white;
        border-left: 4px solid #2a5298;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .task-completed {
        border-left-color: #28a745;
        background-color: #d4edda;
    }
    .task-pending {
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
</style>
""", unsafe_allow_html=True)

# ============================================================
# COMPLETE USER CREDENTIALS - ALL DATA ANALYSTS
# ============================================================
USERS = {
    # Admin
    "admin@mahastride.com": {
        "password": sha256("Admin@2026".encode()).hexdigest(),
        "role": "admin",
        "name": "Administrator",
        "team": "MITRA"
    },
    # Project Lead
    "projectlead@mahastride.com": {
        "password": sha256("ProjectLead@2026".encode()).hexdigest(),
        "role": "project_lead",
        "name": "Dr. Harshal Kotwal",
        "team": "ICARE"
    },
    # MITRA Level
    "shubham@mitra.gov.in": {
        "password": sha256("Shubham@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Shubham Singh",
        "team": "MITRA"
    },
    # Mumbai University
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
    # Savitribai Phule Pune University
    "jagan@sspu.edu": {
        "password": sha256("Jagan@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Jagan Sridhar",
        "team": "SPPU Pune"
    },
    # COEP Technological University
    "vaibhav@coep.edu": {
        "password": sha256("Vaibhav@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Vaibhav Ambekar",
        "team": "COEP Pune"
    },
    # Sant Gadge Baba Amravati University
    "pratham@au.edu": {
        "password": sha256("Pratham@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Prathamesh Babhulkar",
        "team": "Amravati University"
    },
    # Rashtrasant Tukadoji Maharaj Nagpur University
    "anjali@nu.edu": {
        "password": sha256("Anjali@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Anjali Singh",
        "team": "Nagpur University"
    },
    # KBCNMU, Jalgaon
    "nitish@kbcnmu.edu": {
        "password": sha256("Nitish@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Nitish Kumbhar",
        "team": "KBCNMU Jalgaon"
    },
    # Dr. Babasaheb Ambedkar Marathwada University
    "atharv@bamu.edu": {
        "password": sha256("Atharv@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Atharav Paturkar",
        "team": "BAMU Aurangabad"
    }
}

# ============================================================
# DATA FILES
# ============================================================
DAILY_TASKS_FILE = "daily_tasks_data.json"
TASK_COMPLETION_FILE = "task_completion_data.json"

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
    
    if month == 12:
        last_day = datetime(year, month, 31)
    else:
        last_day = datetime(year, month + 1, 1) - timedelta(days=1)
    
    current = first_day
    while current <= last_day:
        if current.weekday() < 5:
            working_days.append(current)
        current += timedelta(days=1)
    return working_days

def get_daily_tasks_for_month(year, month):
    """Generate daily tasks for a specific month"""
    working_days = get_working_days_in_month(year, month)
    daily_tasks = {}
    
    # Get monthly plan
    plan = get_24_month_plan()
    month_data = None
    for month_num, data in plan.items():
        if data["year"] == year and data["month"].split()[0].lower() == datetime(year, month, 1).strftime("%B").lower():
            month_data = data
            break
    
    activities = month_data["activities"] if month_data else []
    
    for idx, working_day in enumerate(working_days):
        date_str = working_day.strftime("%Y-%m-%d")
        
        if idx < len(activities):
            activity = activities[idx]
            daily_tasks[date_str] = {
                "task": activity["activity"],
                "deliverable": activity["deliverable"],
                "due_date": activity["due_date"],
                "category": get_category(activity["activity"]),
                "priority": "High" if "MILESTONE" in activity["activity"] else "Medium"
            }
        else:
            daily_tasks[date_str] = {
                "task": "Continue project activities and documentation",
                "deliverable": "Daily Progress Report",
                "due_date": date_str,
                "category": "General",
                "priority": "Medium"
            }
    
    return daily_tasks

def get_category(activity):
    if "Training" in activity:
        return "Training"
    elif "Data" in activity:
        return "Data Collection"
    elif "Report" in activity or "MPR" in activity:
        return "Reporting"
    elif "Meeting" in activity:
        return "Meetings"
    elif "Assessment" in activity:
        return "Assessment"
    elif "MILESTONE" in activity:
        return "Milestone"
    else:
        return "General"

def get_all_tasks():
    """Generate all tasks for all months"""
    all_tasks = {}
    
    for year in [2026, 2027, 2028]:
        for month in range(1, 13):
            if year == 2026 and month < 5:
                continue
            if year == 2028 and month > 4:
                continue
            
            monthly_tasks = get_daily_tasks_for_month(year, month)
            all_tasks.update(monthly_tasks)
    
    return all_tasks

def load_tasks():
    if os.path.exists(DAILY_TASKS_FILE):
        with open(DAILY_TASKS_FILE, 'r') as f:
            return json.load(f)
    tasks = get_all_tasks()
    with open(DAILY_TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)
    return tasks

def load_completions():
    if os.path.exists(TASK_COMPLETION_FILE):
        with open(TASK_COMPLETION_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_completions(completions):
    with open(TASK_COMPLETION_FILE, 'w') as f:
        json.dump(completions, f, indent=2)

def initialize_completed_tasks():
    """Mark May 4 to June 5, 2026 as completed for all data analysts"""
    completions = load_completions()
    all_tasks = load_tasks()
    
    # Get working dates from May 4 to June 5, 2026
    completed_dates = []
    start_date = datetime(2026, 5, 4)
    end_date = datetime(2026, 6, 5)
    current = start_date
    while current <= end_date:
        if current.weekday() < 5:
            date_str = current.strftime("%Y-%m-%d")
            if date_str in all_tasks:
                completed_dates.append(date_str)
        current += timedelta(days=1)
    
    # Mark for all data analysts
    for email, user in USERS.items():
        if user.get("role") == "data_analyst":
            if email not in completions:
                completions[email] = {}
            
            for date_str in completed_dates:
                if date_str not in completions[email]:
                    completions[email][date_str] = {
                        "completed_at": datetime(2026, 6, 5, 17, 0, 0).isoformat(),
                        "remarks": "Completed - Initial project setup phase"
                    }
    
    save_completions(completions)
    return len(completed_dates)

def get_user_tasks(email):
    user = USERS.get(email, {})
    all_tasks = load_tasks()
    completions = load_completions()
    user_completions = completions.get(email, {})
    
    user_tasks = []
    for date_str, task_info in all_tasks.items():
        if user.get("role") == "data_analyst":
            is_completed = date_str in user_completions
            completion_info = user_completions.get(date_str, {})
            
            user_tasks.append({
                "date": date_str,
                "task": task_info.get("task", ""),
                "deliverable": task_info.get("deliverable", ""),
                "due_date": task_info.get("due_date", ""),
                "category": task_info.get("category", ""),
                "priority": task_info.get("priority", "Medium"),
                "status": "Completed" if is_completed else "Pending",
                "completed_at": completion_info.get("completed_at", ""),
                "remarks": completion_info.get("remarks", "")
            })
    
    return sorted(user_tasks, key=lambda x: x["date"])

def mark_task_complete(email, date_str, remarks):
    completions = load_completions()
    if email not in completions:
        completions[email] = {}
    
    completions[email][date_str] = {
        "completed_at": datetime.now().isoformat(),
        "remarks": remarks
    }
    save_completions(completions)
    return True

def get_all_analysts_progress():
    """Get progress for all data analysts"""
    all_tasks = load_tasks()
    completions = load_completions()
    total_tasks = len(all_tasks)
    
    progress_data = []
    for email, user in USERS.items():
        if user.get("role") == "data_analyst":
            user_completions = completions.get(email, {})
            completed = len(user_completions)
            progress_data.append({
                "name": user["name"],
                "team": user.get("team", "N/A"),
                "completed": completed,
                "total": total_tasks,
                "progress": round((completed / total_tasks * 100), 1) if total_tasks > 0 else 0
            })
    
    return pd.DataFrame(progress_data)

def get_team_summary():
    """Get team-wise summary"""
    progress_df = get_all_analysts_progress()
    team_summary = progress_df.groupby("team").agg({
        "completed": "sum",
        "total": "first"
    }).reset_index()
    team_summary["progress"] = round((team_summary["completed"] / team_summary["total"] * 100), 1)
    return team_summary

def generate_mpr_html(year, month):
    """Generate MPR report"""
    month_names = ["January", "February", "March", "April", "May", "June", 
                   "July", "August", "September", "October", "November", "December"]
    month_name = month_names[month-1]
    
    progress_df = get_all_analysts_progress()
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Monthly Progress Report - {month_name} {year}</title>
    <style>
        body {{ font-family: 'Times New Roman', serif; margin: 0.7in; font-size: 11pt; }}
        .header {{ text-align: center; margin-bottom: 20px; }}
        .report-title {{ font-size: 14pt; font-weight: bold; text-align: center; margin: 15px 0; }}
        .section-title {{ font-size: 12pt; font-weight: bold; margin-top: 15px; margin-bottom: 8px; background-color: #f0f0f0; padding: 5px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
        th, td {{ border: 1px solid #000; padding: 6px; vertical-align: top; }}
        th {{ background-color: #e8e8e8; font-weight: bold; text-align: center; }}
        .footer {{ text-align: center; font-size: 9pt; font-style: italic; margin-top: 30px; }}
    </style>
</head>
<body>
<div class="header">
    <h2>Maharashtra Institution for Transformation (MITRA)</h2>
    <h3>Monthly Progress Report - {month_name} {year}</h3>
</div>

<div class="section-title">1. Team Performance Summary</div>
<table>
    <tr><th>Team Member</th><th>Team</th><th>Tasks Completed</th><th>Total Tasks</th><th>Progress (%)</th></tr>
    {''.join([f'<tr><td>{row["name"]}</td><td>{row["team"]}</td><td>{row["completed"]}</td><td>{row["total"]}</td><td>{row["progress"]}%</td></tr>' for _, row in progress_df.iterrows()])}
</table>

<div class="section-title">2. Overall Statistics</div>
<table>
    <tr><td><strong>Total Working Days (24 months)</strong></td><td>{len(load_tasks())}</td></tr>
    <tr><td><strong>Total Task Completions</strong></td><td>{sum(len(c) for c in load_completions().values())}</td></tr>
    <tr><td><strong>Active Team Members</strong></td><td>{len(progress_df)}</td></tr>
</table>

<div class="footer">Generated on {datetime.now().strftime('%d-%b-%Y %H:%M:%S')}</div>
</body>
</html>"""
    
    return html

def get_download_link(html, filename):
    b64 = base64.b64encode(html.encode()).decode()
    return f'<a href="data:text/html;base64,{b64}" download="{filename}" style="background:#28a745;color:white;padding:10px 20px;text-decoration:none;border-radius:5px;">📥 Download {filename}</a>'

def show_credentials():
    st.markdown("""
    <div class="credentials-box">
        <h4>🔐 Login Credentials</h4>
        <p><strong>Password for all accounts:</strong> <code>Name@2026</code> (e.g., Admin@2026, Sneha@2026)</p>
        <table style="width:100%; font-size:12px;">
            <tr><th>Role</th><th>Email</th><th>Password</th></tr>
            <tr><td>🔴 Admin</td><td>admin@mahastride.com</td><td>Admin@2026</td></tr>
            <tr><td>🔵 Project Lead</td><td>projectlead@mahastride.com</td><td>ProjectLead@2026</td></tr>
            <tr><td>🟢 Data Analyst</td><td>sneha@mu.edu</td><td>Sneha@2026</td></tr>
            <tr><td>🟢 Data Analyst</td><td>shubham@mitra.gov.in</td><td>Shubham@2026</td></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# MAIN APP
# ============================================================

def main():
    # Initialize data
    load_tasks()
    initialize_completed_tasks()
    
    # Authentication
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        st.markdown("""
        <div class="main-header">
            <h1>📊 MahaSTRIDE Project Management System</h1>
            <p>Complete 24-Month Task Management | May 2026 - April 2028</p>
            <p>Monday to Friday | 10:00 AM - 6:00 PM</p>
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
    
    # Get user info
    user_info = st.session_state.user_info
    email = st.session_state.user_email
    role = user_info.get("role", "data_analyst")
    
    # Sidebar Navigation
    with st.sidebar:
        st.markdown("## 📋 MahaSTRIDE")
        st.markdown(f"**Welcome, {user_info.get('name')}**")
        if role == "data_analyst":
            st.markdown(f"*Team: {user_info.get('team', 'N/A')}*")
        st.markdown(f"*Role: {role.upper()}*")
        st.markdown("---")
        
        # Navigation Tabs
        if role == "admin":
            nav_options = ["📊 Dashboard", "👥 Team Performance", "📄 MPR Reports", "📅 Monthly Plan"]
        elif role == "project_lead":
            nav_options = ["📊 Dashboard", "👥 Team Performance", "📄 MPR Reports", "📋 Task Overview"]
        else:
            nav_options = ["📝 My Tasks", "📊 My Progress", "📅 Calendar View"]
        
        selected_nav = st.radio("Navigation", nav_options, label_visibility="collapsed")
        
        st.markdown("---")
        st.markdown("### ℹ️ Info")
        st.markdown("**Working Hours:** 10:00 AM - 6:00 PM")
        st.markdown("**Working Days:** Monday to Friday")
        st.markdown("**Project Duration:** 24 months")
        st.markdown("**Status:** ✅ May 4 - June 5, 2026 COMPLETED")
        
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()
    
    # ============================================================
    # ADMIN DASHBOARD
    # ============================================================
    if role == "admin":
        if selected_nav == "📊 Dashboard":
            st.markdown("## 📊 Admin Dashboard")
            
            all_tasks = load_tasks()
            completions = load_completions()
            progress_df = get_all_analysts_progress()
            team_summary = get_team_summary()
            
            # Key Metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="metric-value">{len(all_tasks)}</div>
                    <div class="metric-label">Total Working Days</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="metric-value">{len([d for d in all_tasks.keys() if d <= "2026-06-05"])}</div>
                    <div class="metric-label">Completed (May 4 - June 5)</div>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="metric-value">{len([u for u in USERS.values() if u.get("role") == "data_analyst"])}</div>
                    <div class="metric-label">Team Members</div>
                </div>
                """, unsafe_allow_html=True)
            with col4:
                total_completions = sum(len(c) for c in completions.values())
                st.markdown(f"""
                <div class="stat-card">
                    <div class="metric-value">{total_completions}</div>
                    <div class="metric-label">Total Task Completions</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Team Progress Chart - COMPLETE LIST
            st.subheader("👥 Team Progress Dashboard")
            
            fig = px.bar(progress_df, x="name", y="progress", color="team",
                         title="Team Member Progress (%)",
                         labels={"name": "Team Member", "progress": "Progress (%)"},
                         text="progress", height=500)
            fig.update_traces(textposition="outside")
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("---")
            
            # Team Summary
            st.subheader("📊 Team-wise Summary")
            st.dataframe(team_summary, use_container_width=True, hide_index=True)
            
            # Detailed table
            st.subheader("📋 Detailed Team Performance")
            st.dataframe(progress_df, use_container_width=True, hide_index=True)
        
        elif selected_nav == "👥 Team Performance":
            st.markdown("## 👥 Team Performance Analysis")
            
            progress_df = get_all_analysts_progress()
            
            col1, col2 = st.columns(2)
            with col1:
                fig = px.pie(progress_df, values="completed", names="name", title="Tasks Completed by Team Member")
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                fig = px.bar(progress_df, x="team", y="progress", color="team", 
                             title="Team-wise Progress", text="progress")
                fig.update_traces(textposition="outside")
                st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("---")
            st.subheader("Complete Team Member List")
            st.dataframe(progress_df, use_container_width=True, hide_index=True)
        
        elif selected_nav == "📄 MPR Reports":
            st.markdown("## 📄 Monthly Progress Reports")
            
            col1, col2 = st.columns(2)
            with col1:
                report_year = st.selectbox("Select Year", [2026, 2027, 2028])
            with col2:
                report_month = st.selectbox("Select Month", range(1, 13), 
                                            format_func=lambda x: ["January","February","March","April","May","June",
                                                                  "July","August","September","October","November","December"][x-1])
            
            if st.button("Generate MPR Report", use_container_width=True):
                html = generate_mpr_html(report_year, report_month)
                st.markdown(get_download_link(html, f"MPR_{report_year}_{report_month}.html"), unsafe_allow_html=True)
        
        elif selected_nav == "📅 Monthly Plan":
            st.markdown("## 📅 24-Month Project Plan")
            
            plan = get_24_month_plan()
            for month_num, month_data in plan.items():
                with st.expander(f"{month_data['month']} {month_data['year']}"):
                    for activity in month_data["activities"]:
                        st.markdown(f"• **{activity['activity']}** - {activity['deliverable']} (Due: {activity['due_date']})")
    
    # ============================================================
    # PROJECT LEAD DASHBOARD
    # ============================================================
    elif role == "project_lead":
        if selected_nav == "📊 Dashboard":
            st.markdown("## 👨‍💼 Project Lead Dashboard")
            st.markdown("**Dr. Harshal Kotwal** - ICARE Project Director")
            
            all_tasks = load_tasks()
            progress_df = get_all_analysts_progress()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📅 Total Working Days", len(all_tasks))
            with col2:
                st.metric("👥 Team Members", len(progress_df))
            with col3:
                avg_progress = progress_df["progress"].mean() if not progress_df.empty else 0
                st.metric("📈 Average Team Progress", f"{avg_progress:.1f}%")
            
            st.markdown("---")
            
            # Team Progress Chart
            st.subheader("Team Performance Overview")
            fig = px.bar(progress_df, x="name", y="progress", color="team",
                         title="Team Member Progress (%)",
                         labels={"name": "Team Member", "progress": "Progress (%)"},
                         text="progress", height=450)
            fig.update_traces(textposition="outside")
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("---")
            st.subheader("Detailed Team Performance")
            st.dataframe(progress_df, use_container_width=True, hide_index=True)
        
        elif selected_nav == "👥 Team Performance":
            st.markdown("## 👥 Team Performance Analysis")
            
            progress_df = get_all_analysts_progress()
            
            col1, col2 = st.columns(2)
            with col1:
                fig = px.pie(progress_df, values="completed", names="name", title="Tasks Completed Distribution")
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                fig = px.bar(progress_df, x="team", y="progress", color="team", 
                             title="Team-wise Progress", text="progress")
                fig.update_traces(textposition="outside")
                st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("---")
            st.subheader("Complete Team Member List")
            
            # Display with progress bars
            for _, row in progress_df.iterrows():
                st.markdown(f"**{row['name']}** - {row['team']}")
                st.progress(row['progress']/100)
                st.caption(f"{row['completed']}/{row['total']} tasks completed ({row['progress']}%)")
                st.markdown("---")
        
        elif selected_nav == "📄 MPR Reports":
            st.markdown("## 📄 Monthly Progress Reports")
            
            col1, col2 = st.columns(2)
            with col1:
                report_year = st.selectbox("Select Year", [2026, 2027, 2028])
            with col2:
                report_month = st.selectbox("Select Month", range(1, 13), 
                                            format_func=lambda x: ["January","February","March","April","May","June",
                                                                  "July","August","September","October","November","December"][x-1])
            
            if st.button("Generate MPR Report", use_container_width=True):
                html = generate_mpr_html(report_year, report_month)
                st.markdown(get_download_link(html, f"MPR_{report_year}_{report_month}.html"), unsafe_allow_html=True)
        
        elif selected_nav == "📋 Task Overview":
            st.markdown("## 📋 Task Overview")
            
            all_tasks = load_tasks()
            st.dataframe(pd.DataFrame(list(all_tasks.items()), columns=["Date", "Task Info"]), use_container_width=True)
    
    # ============================================================
    # DATA ANALYST DASHBOARD
    # ============================================================
    else:
        if selected_nav == "📝 My Tasks":
            st.markdown(f"## 📝 My Tasks - {user_info.get('name')}")
            st.markdown(f"**Team:** {user_info.get('team', 'N/A')}")
            st.markdown("**Working Hours:** 10:00 AM - 6:00 PM (Monday to Friday)")
            
            user_tasks = get_user_tasks(email)
            
            # Filter for future tasks (after June 5, 2026)
            pending_tasks = [t for t in user_tasks if t["date"] > "2026-06-05" and t["status"] == "Pending"]
            completed_tasks = [t for t in user_tasks if t["date"] > "2026-06-05" and t["status"] == "Completed"]
            initial_completed = [t for t in user_tasks if t["date"] <= "2026-06-05"]
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📅 Total Tasks", len(user_tasks))
            with col2:
                st.metric("✅ Completed (Initial)", len(initial_completed))
            with col3:
                st.metric("✅ Completed (Your Work)", len(completed_tasks))
            with col4:
                st.metric("⏳ Pending", len(pending_tasks))
            
            st.markdown("---")
            
            # Today's Task
            today = datetime.now().strftime("%Y-%m-%d")
            today_task = next((t for t in user_tasks if t["date"] == today and t["date"] > "2026-06-05"), None)
            
            if today_task and today_task["status"] == "Pending":
                st.subheader("📌 Today's Task")
                with st.form(key="complete_task_form"):
                    st.markdown(f"""
                    <div class="task-card task-pending">
                        <strong>Task:</strong> {today_task['task']}<br>
                        <strong>Deliverable:</strong> {today_task['deliverable']}<br>
                        <strong>Due Date:</strong> {today_task['due_date']}<br>
                        <strong>Priority:</strong> {today_task['priority']}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    remarks = st.text_area("Work Accomplished / Remarks", height=100,
                                          placeholder="Describe what you worked on today...")
                    
                    if st.form_submit_button("✅ Mark as Complete", use_container_width=True):
                        if remarks:
                            if mark_task_complete(email, today_task["date"], remarks):
                                st.success("Task completed! Great work!")
                                st.rerun()
                        else:
                            st.error("Please enter work accomplishments")
            
            elif today_task and today_task["status"] == "Completed":
                st.subheader("📌 Today's Task - Completed")
                st.markdown(f"""
                <div class="task-card task-completed">
                    ✅ <strong>Completed</strong><br>
                    <strong>Task:</strong> {today_task['task']}<br>
                    <strong>Remarks:</strong> {today_task.get('remarks', 'No remarks')}
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # All Pending Tasks
            if pending_tasks:
                st.subheader("⏳ Pending Tasks")
                for task in pending_tasks[:10]:
                    st.markdown(f"""
                    <div class="task-card task-pending">
                        <strong>📅 {task['date']}</strong><br>
                        <strong>Task:</strong> {task['task']}<br>
                        <strong>Deliverable:</strong> {task['deliverable']}<br>
                        <strong>Due:</strong> {task['due_date']}
                    </div>
                    """, unsafe_allow_html=True)
        
        elif selected_nav == "📊 My Progress":
            st.markdown(f"## 📊 My Progress - {user_info.get('name')}")
            
            user_tasks = get_user_tasks(email)
            future_tasks = [t for t in user_tasks if t["date"] > "2026-06-05"]
            completed = sum(1 for t in future_tasks if t["status"] == "Completed")
            total = len(future_tasks)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📊 Total Tasks (June 8 onwards)", total)
            with col2:
                st.metric("✅ Completed", completed)
            with col3:
                st.metric("📈 Progress", f"{(completed/total*100):.1f}%" if total > 0 else "0%")
            
            st.progress(completed/total if total > 0 else 0)
            
            st.markdown("---")
            
            # Monthly progress chart
            st.subheader("Monthly Progress")
            monthly_data = {}
            for task in future_tasks:
                month_key = task["date"][:7]
                if month_key not in monthly_data:
                    monthly_data[month_key] = {"total": 0, "completed": 0}
                monthly_data[month_key]["total"] += 1
                if task["status"] == "Completed":
                    monthly_data[month_key]["completed"] += 1
            
            if monthly_data:
                df_monthly = pd.DataFrame([
                    {"Month": k, "Completed": v["completed"], "Total": v["total"]}
                    for k, v in monthly_data.items()
                ])
                fig = px.bar(df_monthly, x="Month", y="Completed", title="Monthly Task Completion", text="Total")
                st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("---")
            st.subheader("All Tasks")
            st.dataframe(pd.DataFrame(future_tasks), use_container_width=True, hide_index=True)
        
        elif selected_nav == "📅 Calendar View":
            st.markdown(f"## 📅 Calendar View - {user_info.get('name')}")
            
            user_tasks = get_user_tasks(email)
            
            # Create calendar view
            for task in user_tasks:
                if task["date"] > "2026-06-05":
                    status_icon = "✅" if task["status"] == "Completed" else "⏳"
                    st.markdown(f"{status_icon} **{task['date']}** - {task['task'][:80]}")

if __name__ == "__main__":
    main()
