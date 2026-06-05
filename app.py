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
import time

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
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
        border-left: 4px solid #28a745;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# COMPLETE USER CREDENTIALS
# ============================================================
USERS = {
    "admin@mahastride.com": {
        "password": sha256("Admin@2026".encode()).hexdigest(),
        "role": "admin",
        "name": "Administrator",
        "team": "MITRA"
    },
    "projectlead@mahastride.com": {
        "password": sha256("ProjectLead@2026".encode()).hexdigest(),
        "role": "project_lead",
        "name": "Dr. Harshal Kotwal",
        "team": "ICARE"
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
        "team": "SPPU Pune"
    },
    "vaibhav@coep.edu": {
        "password": sha256("Vaibhav@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Vaibhav Ambekar",
        "team": "COEP Pune"
    },
    "pratham@au.edu": {
        "password": sha256("Pratham@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Prathamesh Babhulkar",
        "team": "Amravati University"
    },
    "anjali@nu.edu": {
        "password": sha256("Anjali@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Anjali Singh",
        "team": "Nagpur University"
    },
    "nitish@kbcnmu.edu": {
        "password": sha256("Nitish@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Nitish Kumbhar",
        "team": "KBCNMU Jalgaon"
    },
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
# DETAILED DAILY TASKS FOR EACH WORKING DAY
# ============================================================

def get_detailed_tasks_for_date(date):
    """Return detailed task for a specific date"""
    date_str = date.strftime("%Y-%m-%d")
    
    # June 2026 Detailed Tasks
    june_tasks = {
        "2026-06-08": {
            "task": "Conduct faculty interviews at assigned university",
            "sub_tasks": ["Schedule interviews with 5 faculty members", "Prepare interview questionnaire", "Document interview responses", "Identify key research areas"],
            "deliverable": "Faculty Interview Summary Report",
            "category": "Data Collection",
            "priority": "High"
        },
        "2026-06-09": {
            "task": "Analyze research output metrics",
            "sub_tasks": ["Collect publication data from last 5 years", "Calculate citation impact", "Identify top research areas", "Benchmark against top universities"],
            "deliverable": "Research Output Analysis Report",
            "category": "Analysis",
            "priority": "High"
        },
        "2026-06-10": {
            "task": "Evaluate infrastructure readiness",
            "sub_tasks": ["Review lab facilities", "Assess library resources", "Check IT infrastructure", "Document infrastructure gaps"],
            "deliverable": "Infrastructure Readiness Report",
            "category": "Assessment",
            "priority": "Medium"
        },
        "2026-06-11": {
            "task": "Assess international collaboration",
            "sub_tasks": ["Identify existing MoUs", "List international research projects", "Document visiting faculty", "Propose new collaborations"],
            "deliverable": "International Collaboration Assessment",
            "category": "Assessment",
            "priority": "Medium"
        },
        "2026-06-12": {
            "task": "Compile assessment findings",
            "sub_tasks": ["Consolidate all assessment data", "Create summary metrics", "Identify patterns and trends", "Prepare presentation"],
            "deliverable": "Comprehensive Assessment Compilation",
            "category": "Analysis",
            "priority": "High"
        },
        "2026-06-15": {
            "task": "GRDAU Training Session for Coordinators",
            "sub_tasks": ["Prepare training materials", "Conduct 3-hour training session", "Answer participant questions", "Collect feedback forms"],
            "deliverable": "Training Session Report",
            "category": "Training",
            "priority": "High"
        },
        "2026-06-16": {
            "task": "Data validation workshop",
            "sub_tasks": ["Review data collection methods", "Identify data inconsistencies", "Standardize data formats", "Create validation checklist"],
            "deliverable": "Data Validation Framework",
            "category": "Training",
            "priority": "High"
        },
        "2026-06-17": {
            "task": "NIRF submission preparation",
            "sub_tasks": ["Complete NIRF data templates", "Verify all metrics", "Prepare supporting documents", "Review with IQAC"],
            "deliverable": "NIRF Submission Package",
            "category": "Reporting",
            "priority": "High"
        },
        "2026-06-18": {
            "task": "Review progress with Vice Chancellor",
            "sub_tasks": ["Prepare progress presentation", "Compile key achievements", "Discuss challenges", "Get VC approval for next steps"],
            "deliverable": "VC Meeting Minutes",
            "category": "Meetings",
            "priority": "High"
        },
        "2026-06-19": {
            "task": "Update data repository",
            "sub_tasks": ["Upload all collected data", "Organize data by category", "Add metadata", "Backup repository"],
            "deliverable": "Updated Data Repository",
            "category": "Data Collection",
            "priority": "Medium"
        },
        "2026-06-22": {
            "task": "Finalize Diagnostic Reports",
            "sub_tasks": ["Review all sections", "Add executive summary", "Include recommendations", "Format as per guidelines"],
            "deliverable": "Diagnostic Report Draft",
            "category": "Reporting",
            "priority": "High"
        },
        "2026-06-23": {
            "task": "Submit Diagnostic Assessment Reports",
            "sub_tasks": ["Get final approval", "Submit to PMU", "Send copy to VC", "Archive submission"],
            "deliverable": "Submitted Diagnostic Reports",
            "category": "Reporting",
            "priority": "High"
        },
        "2026-06-24": {
            "task": "Prepare June MPR",
            "sub_tasks": ["Compile June activities", "Document achievements", "List challenges faced", "Plan for July"],
            "deliverable": "June MPR Draft",
            "category": "Reporting",
            "priority": "High"
        },
        "2026-06-25": {
            "task": "Plan July activities",
            "sub_tasks": ["Review Phase 1 remaining tasks", "Create July work schedule", "Assign responsibilities", "Set deadlines"],
            "deliverable": "July Work Plan",
            "category": "Planning",
            "priority": "Medium"
        },
        "2026-06-26": {
            "task": "Client review meeting",
            "sub_tasks": ["Prepare presentation", "Present June progress", "Receive feedback", "Document action items"],
            "deliverable": "Client Meeting Minutes",
            "category": "Meetings",
            "priority": "High"
        },
        "2026-06-29": {
            "task": "Continue data analysis",
            "sub_tasks": ["Analyze remaining data", "Identify improvement areas", "Prepare analysis charts", "Document findings"],
            "deliverable": "Data Analysis Report",
            "category": "Analysis",
            "priority": "Medium"
        },
        "2026-06-30": {
            "task": "Finalize and submit June MPR",
            "sub_tasks": ["Incorporate feedback", "Finalize report", "Submit to PMU", "Get acknowledgment"],
            "deliverable": "June MPR Final",
            "category": "Reporting",
            "priority": "High"
        }
    }
    
    # July 2026 Detailed Tasks
    july_tasks = {
        "2026-07-01": {
            "task": "Complete gap analysis against NIRF/NAAC/Global Rankings",
            "sub_tasks": ["Compare current vs target metrics", "Identify critical gaps", "Prioritize improvement areas", "Create gap analysis matrix"],
            "deliverable": "Gap Analysis Report",
            "category": "Analysis",
            "priority": "High"
        },
        "2026-07-02": {
            "task": "Prepare SWOT reports for each university",
            "sub_tasks": ["Conduct SWOT workshop", "Document strengths/weaknesses", "Identify opportunities/threats", "Compile university-wise SWOT"],
            "deliverable": "7 SWOT Analysis Reports",
            "category": "Documentation",
            "priority": "High"
        },
        "2026-07-03": {
            "task": "Submit GRDAU establishment plan",
            "sub_tasks": ["Define GRDAU structure", "List required resources", "Set up operational procedures", "Get approval from VC"],
            "deliverable": "GRDAU Establishment Plan",
            "category": "Reporting",
            "priority": "High"
        },
        "2026-07-06": {
            "task": "Finalize GRDAU in all universities",
            "sub_tasks": ["Setup GRDAU office", "Install necessary software", "Create user accounts", "Test systems"],
            "deliverable": "GRDAU Operational Status",
            "category": "Setup",
            "priority": "High"
        },
        "2026-07-07": {
            "task": "Train GRDAU staff",
            "sub_tasks": ["Conduct training session", "Demonstrate data entry", "Explain reporting process", "Assess staff readiness"],
            "deliverable": "GRDAU Training Completion Report",
            "category": "Training",
            "priority": "High"
        },
        "2026-07-08": {
            "task": "Develop SOP for GRDAU",
            "sub_tasks": ["Draft standard procedures", "Define roles and responsibilities", "Create workflow diagrams", "Get approval"],
            "deliverable": "GRDAU SOP Document",
            "category": "Documentation",
            "priority": "High"
        },
        "2026-07-09": {
            "task": "Setup data management systems",
            "sub_tasks": ["Configure database", "Setup backup systems", "Implement security protocols", "Test data integrity"],
            "deliverable": "Data Management System",
            "category": "Technical",
            "priority": "High"
        },
        "2026-07-10": {
            "task": "Review GRDAU readiness",
            "sub_tasks": ["Check all systems", "Verify staff training", "Test data flow", "Document readiness status"],
            "deliverable": "GRDAU Readiness Report",
            "category": "Assessment",
            "priority": "Medium"
        },
        "2026-07-13": {
            "task": "Data quality framework implementation",
            "sub_tasks": ["Define quality metrics", "Create validation rules", "Setup automated checks", "Test framework"],
            "deliverable": "Data Quality Framework",
            "category": "Technical",
            "priority": "High"
        },
        "2026-07-14": {
            "task": "Dashboard requirements gathering",
            "sub_tasks": ["Meet with stakeholders", "List required KPIs", "Define visualization needs", "Document requirements"],
            "deliverable": "Dashboard Requirements Document",
            "category": "Meetings",
            "priority": "High"
        },
        "2026-07-15": {
            "task": "Prepare baseline report",
            "sub_tasks": ["Compile all baseline data", "Create summary statistics", "Document methodology", "Format report"],
            "deliverable": "Baseline Report",
            "category": "Reporting",
            "priority": "High"
        },
        "2026-07-16": {
            "task": "Stakeholder feedback session",
            "sub_tasks": ["Schedule meeting", "Present findings", "Collect feedback", "Document action items"],
            "deliverable": "Stakeholder Feedback Report",
            "category": "Meetings",
            "priority": "Medium"
        },
        "2026-07-17": {
            "task": "Update project plan",
            "sub_tasks": ["Review progress against plan", "Adjust timelines if needed", "Update resource allocation", "Communicate changes"],
            "deliverable": "Updated Project Plan",
            "category": "Planning",
            "priority": "Medium"
        },
        "2026-07-20": {
            "task": "Finalize July MPR",
            "sub_tasks": ["Compile July activities", "Document Phase 1 completion", "Prepare for Phase 2", "Submit to PMU"],
            "deliverable": "July MPR Report",
            "category": "Reporting",
            "priority": "High"
        },
        "2026-07-21": {
            "task": "Phase 1 completion review",
            "sub_tasks": ["Review all Phase 1 deliverables", "Assess quality metrics", "Document lessons learned", "Celebrate achievements"],
            "deliverable": "Phase 1 Completion Report",
            "category": "Meetings",
            "priority": "High"
        },
        "2026-07-22": {
            "task": "Plan Phase 2 activities",
            "sub_tasks": ["Review Phase 2 requirements", "Create detailed work plan", "Assign resources", "Set milestones"],
            "deliverable": "Phase 2 Work Plan",
            "category": "Planning",
            "priority": "High"
        },
        "2026-07-23": {
            "task": "Client presentation - Phase 1 results",
            "sub_tasks": ["Prepare presentation", "Showcase achievements", "Present metrics", "Get client approval"],
            "deliverable": "Client Presentation Deck",
            "category": "Meetings",
            "priority": "High"
        },
        "2026-07-24": {
            "task": "Document lessons learned",
            "sub_tasks": ["Capture successes", "Document challenges", "Recommend improvements", "Share with team"],
            "deliverable": "Lessons Learned Document",
            "category": "Documentation",
            "priority": "Medium"
        },
        "2026-07-27": {
            "task": "Prepare for Phase 2 kickoff",
            "sub_tasks": ["Review Phase 2 objectives", "Prepare kickoff materials", "Schedule team meeting", "Setup tracking systems"],
            "deliverable": "Phase 2 Kickoff Package",
            "category": "Planning",
            "priority": "Medium"
        },
        "2026-07-28": {
            "task": "Team meeting for Phase 2",
            "sub_tasks": ["Present Phase 2 plan", "Clarify roles", "Discuss challenges", "Align on goals"],
            "deliverable": "Phase 2 Team Meeting Minutes",
            "category": "Meetings",
            "priority": "Medium"
        },
        "2026-07-29": {
            "task": "Review project status",
            "sub_tasks": ["Check all trackers", "Verify data completeness", "Update dashboards", "Prepare status report"],
            "deliverable": "Project Status Report",
            "category": "Reporting",
            "priority": "Medium"
        },
        "2026-07-30": {
            "task": "Submit July MPR (final)",
            "sub_tasks": ["Finalize report", "Get approvals", "Submit to PMU", "Confirm receipt"],
            "deliverable": "July MPR Submitted",
            "category": "Reporting",
            "priority": "High"
        },
        "2026-07-31": {
            "task": "Plan August activities",
            "sub_tasks": ["Review August deliverables", "Create daily schedule", "Assign tasks", "Setup deadlines"],
            "deliverable": "August Work Plan",
            "category": "Planning",
            "priority": "Medium"
        }
    }
    
    # Check if date is in specific task dictionaries
    if date_str in june_tasks:
        return june_tasks[date_str]
    elif date_str in july_tasks:
        return july_tasks[date_str]
    else:
        # For dates beyond July 2026, generate detailed tasks based on the month
        return get_generic_detailed_task(date)

def get_generic_detailed_task(date):
    """Generate detailed task for dates beyond July 2026"""
    month = date.month
    year = date.year
    
    if year == 2026 and month == 8:
        return {
            "task": f"Develop Institutional Development Plan (IDP) - Day {date.day}",
            "sub_tasks": ["Review IDP template", "Collect strategic inputs", "Draft IDP sections", "Validate with stakeholders"],
            "deliverable": f"IDP Development Progress",
            "category": "Planning",
            "priority": "High"
        }
    elif year == 2026 and month == 9:
        return {
            "task": f"Dashboard Design and Development - Activity {date.day}",
            "sub_tasks": ["Design dashboard mockups", "Integrate data sources", "Test visualizations", "Gather feedback"],
            "deliverable": f"Dashboard Component",
            "category": "Technical",
            "priority": "High"
        }
    elif year == 2026 and month == 10:
        return {
            "task": f"Milestone 2: Institutional Development Plans - Day {date.day}",
            "sub_tasks": ["Finalize IDPs", "Get institutional sign-off", "Submit milestone report", "Present to client"],
            "deliverable": f"Milestone 2 Deliverable",
            "category": "Reporting",
            "priority": "High"
        }
    elif year == 2026 and month == 11:
        return {
            "task": f"Data Portal Deployment - Activity {date.day}",
            "sub_tasks": ["Deploy portal", "Configure settings", "Test functionality", "Train users"],
            "deliverable": f"Portal Deployment Progress",
            "category": "Technical",
            "priority": "High"
        }
    elif year == 2026 and month == 12:
        return {
            "task": f"Capacity Building Training - Module {date.day}",
            "sub_tasks": ["Prepare training materials", "Conduct sessions", "Assess learning", "Collect feedback"],
            "deliverable": f"Training Completion Report",
            "category": "Training",
            "priority": "High"
        }
    elif year == 2027:
        # For 2027, create specific tasks based on the month
        month_names = ["January", "February", "March", "April", "May", "June", 
                       "July", "August", "September", "October", "November", "December"]
        month_name = month_names[month-1]
        
        if month <= 4:
            category = "Implementation"
            task_prefix = f"Phase 3: {month_name} Implementation Activities"
        elif month <= 8:
            category = "Enhancement"
            task_prefix = f"Phase 4: {month_name} Enhancement Activities"
        else:
            category = "Finalization"
            task_prefix = f"Phase 5: {month_name} Finalization Activities"
        
        return {
            "task": f"{task_prefix} - Day {date.day}",
            "sub_tasks": [
                "Review project progress",
                "Complete assigned deliverables",
                "Document work completed",
                "Coordinate with team members",
                "Update project trackers"
            ],
            "deliverable": "Daily Progress Report",
            "category": category,
            "priority": "Medium"
        }
    else:
        # For 2028 tasks
        month_names = ["January", "February", "March", "April"]
        month_name = month_names[month-1]
        
        if month == 1:
            return {
                "task": f"Global Ranking Submission Preparation - Day {date.day}",
                "sub_tasks": ["Compile ranking data", "Complete submission forms", "Review with experts", "Finalize submissions"],
                "deliverable": "Ranking Submission Package",
                "category": "Reporting",
                "priority": "High"
            }
        elif month == 2:
            return {
                "task": f"Milestone 6: Enhanced Global Rankings - Day {date.day}",
                "sub_tasks": ["Submit rankings for 10 colleges", "Prepare evidence", "Document participation", "Submit milestone report"],
                "deliverable": "Milestone 6 Achievement Report",
                "category": "Milestone",
                "priority": "High"
            }
        elif month == 3:
            return {
                "task": f"Sustainability and Handover Planning - Day {date.day}",
                "sub_tasks": ["Develop sustainability plan", "Document lessons learned", "Prepare handover materials", "Train successor team"],
                "deliverable": "Sustainability Plan",
                "category": "Planning",
                "priority": "High"
            }
        else:
            return {
                "task": f"Final Evaluation and Project Closure - Day {date.day}",
                "sub_tasks": ["Complete final evaluation", "Submit closure report", "Handover all materials", "Project sign-off"],
                "deliverable": "Project Closure Report",
                "category": "Closure",
                "priority": "High"
            }

def get_all_tasks():
    """Generate all daily tasks for all working days"""
    all_tasks = {}
    
    start_date = datetime(2026, 5, 4)
    end_date = datetime(2028, 4, 28)
    
    current = start_date
    while current <= end_date:
        if current.weekday() < 5:  # Monday to Friday
            date_str = current.strftime("%Y-%m-%d")
            task_info = get_detailed_tasks_for_date(current)
            all_tasks[date_str] = task_info
        current += timedelta(days=1)
    
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
    
    for email, user in USERS.items():
        if user.get("role") == "data_analyst":
            if email not in completions:
                completions[email] = {}
            
            for date_str in completed_dates:
                if date_str not in completions[email]:
                    completions[email][date_str] = {
                        "completed_at": datetime(2026, 6, 5, 17, 0, 0).isoformat(),
                        "remarks": "Completed - Initial project setup phase (May 4 to June 5, 2026)"
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
                "sub_tasks": task_info.get("sub_tasks", []),
                "deliverable": task_info.get("deliverable", ""),
                "category": task_info.get("category", ""),
                "priority": task_info.get("priority", "Medium"),
                "status": "Completed" if is_completed else "Pending",
                "completed_at": completion_info.get("completed_at", ""),
                "remarks": completion_info.get("remarks", "")
            })
    
    return sorted(user_tasks, key=lambda x: x["date"])

def mark_task_complete(email, date_str, remarks, work_hours):
    completions = load_completions()
    if email not in completions:
        completions[email] = {}
    
    completions[email][date_str] = {
        "completed_at": datetime.now().isoformat(),
        "remarks": remarks,
        "work_hours": work_hours
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
# DATA ANALYST DASHBOARD
# ============================================================

def data_analyst_dashboard(email, user):
    st.markdown(f"## 📝 My Tasks - {user.get('name')}")
    st.markdown(f"**Team:** {user.get('team', 'N/A')}")
    st.markdown("**Working Hours:** 10:00 AM - 6:00 PM (Monday to Friday)")
    
    user_tasks = get_user_tasks(email)
    
    # Filter tasks
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
    
    # Today's task with complete button
    today = datetime.now().strftime("%Y-%m-%d")
    today_task = next((t for t in user_tasks if t["date"] == today and t["date"] > "2026-06-05"), None)
    
    if today_task:
        st.subheader("📌 Today's Task")
        
        if today_task["status"] == "Completed":
            st.markdown(f"""
            <div class="task-card task-completed">
                ✅ <strong>TASK COMPLETED</strong><br>
                <strong>Task:</strong> {today_task['task']}<br>
                <strong>Deliverable:</strong> {today_task['deliverable']}<br>
                <strong>Remarks:</strong> {today_task.get('remarks', 'No remarks')}
            </div>
            """, unsafe_allow_html=True)
        else:
            with st.form(key=f"complete_today_task"):
                st.markdown(f"""
                <div class="task-card task-pending">
                    <strong>⏳ PENDING - Please complete today's task</strong><br>
                    <strong>Task:</strong> {today_task['task']}<br>
                    <strong>Deliverable:</strong> {today_task['deliverable']}<br>
                    <strong>Priority:</strong> {today_task['priority']}
                </div>
                """, unsafe_allow_html=True)
                
                if today_task.get('sub_tasks'):
                    st.markdown("**📋 Sub-tasks to complete:**")
                    for stask in today_task['sub_tasks']:
                        st.markdown(f"- {stask}")
                    st.markdown("---")
                
                col1, col2 = st.columns(2)
                with col1:
                    start_time = st.time_input("Start Time", value=datetime.strptime("10:00", "%H:%M").time())
                with col2:
                    end_time = st.time_input("End Time", value=datetime.strptime("18:00", "%H:%M").time())
                
                work_hours = f"{start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"
                
                remarks = st.text_area("📝 What did you accomplish today?", height=120)
                
                submitted = st.form_submit_button("✅ MARK AS COMPLETE", use_container_width=True, type="primary")
                
                if submitted:
                    if not remarks:
                        st.error("⚠️ Please describe what you accomplished today")
                    else:
                        if mark_task_complete(email, today_task["date"], remarks, work_hours):
                            st.markdown('<div class="success-message">🎉 Task completed successfully! Great work! 🎉</div>', unsafe_allow_html=True)
                            time.sleep(1)
                            st.rerun()
    
    st.markdown("---")
    
    # Other pending tasks
    if pending_tasks:
        st.subheader("⏳ Other Pending Tasks")
        
        for task in pending_tasks[:5]:
            if task['date'] != today:
                with st.expander(f"📅 {task['date']} - {task['task'][:60]}..."):
                    st.markdown(f"""
                    **Task:** {task['task']}<br>
                    **Deliverable:** {task['deliverable']}<br>
                    **Category:** {task['category']}<br>
                    **Priority:** {task['priority']}
                    """, unsafe_allow_html=True)
                    
                    if task.get('sub_tasks'):
                        st.markdown("**Sub-tasks:**")
                        for stask in task['sub_tasks']:
                            st.markdown(f"- {stask}")
                    
                    with st.form(key=f"complete_task_{task['date']}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            task_start = st.time_input("Start Time", value=datetime.strptime("10:00", "%H:%M").time(), key=f"start_{task['date']}")
                        with col2:
                            task_end = st.time_input("End Time", value=datetime.strptime("18:00", "%H:%M").time(), key=f"end_{task['date']}")
                        
                        task_hours = f"{task_start.strftime('%H:%M')} - {task_end.strftime('%H:%M')}"
                        task_remarks = st.text_area("Work Accomplished", height=80, key=f"remarks_{task['date']}")
                        
                        if st.form_submit_button(f"✅ Complete Task for {task['date']}", use_container_width=True):
                            if task_remarks:
                                if mark_task_complete(email, task["date"], task_remarks, task_hours):
                                    st.success(f"✅ Task for {task['date']} completed!")
                                    st.rerun()
                            else:
                                st.error("Please describe your work accomplishments")
    
    # Recently completed tasks
    if completed_tasks:
        st.subheader("✅ Recently Completed Tasks")
        for task in completed_tasks[-5:]:
            st.markdown(f"""
            <div class="task-card task-completed">
                <strong>✅ {task['date']}</strong><br>
                {task['task'][:80]}...
            </div>
            """, unsafe_allow_html=True)
    
    # Progress visualization
    st.markdown("---")
    st.subheader("📊 My Progress Dashboard")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = go.Figure(data=[go.Pie(
            labels=['Completed (Initial)', 'Completed (My Work)', 'Pending'],
            values=[len(initial_completed), len(completed_tasks), len(pending_tasks)],
            marker_colors=['#28a745', '#20c997', '#ffc107'],
            hole=0.4
        )])
        fig.update_layout(title="Task Breakdown", height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        total_future = len(completed_tasks) + len(pending_tasks)
        progress_pct = (len(completed_tasks) / total_future * 100) if total_future > 0 else 0
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=progress_pct,
            title={'text': "Your Progress (Tasks from June 8 onwards)"},
            gauge={'axis': {'range': [0, 100]},
                   'bar': {'color': "#28a745"},
                   'steps': [
                       {'range': [0, 33], 'color': "#ffcccc"},
                       {'range': [33, 66], 'color': "#ffffcc"},
                       {'range': [66, 100], 'color': "#ccffcc"}]}))
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# ADMIN DASHBOARD
# ============================================================

def admin_dashboard():
    st.markdown("## 📊 Admin Dashboard")
    
    all_tasks = load_tasks()
    completions = load_completions()
    progress_df = get_all_analysts_progress()
    team_summary = get_team_summary()
    
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
    
    st.subheader("👥 Team Progress Dashboard")
    fig = px.bar(progress_df, x="name", y="progress", color="team",
                 title="Team Member Progress (%)", text="progress", height=500)
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader("📊 Team-wise Summary")
    st.dataframe(team_summary, use_container_width=True, hide_index=True)
    st.subheader("📋 Detailed Team Performance")
    st.dataframe(progress_df, use_container_width=True, hide_index=True)

# ============================================================
# PROJECT LEAD DASHBOARD
# ============================================================

def project_lead_dashboard():
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
    
    st.subheader("Team Performance Overview")
    fig = px.bar(progress_df, x="name", y="progress", color="team",
                 title="Team Member Progress (%)", text="progress", height=450)
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Detailed Team Performance")
    st.dataframe(progress_df, use_container_width=True, hide_index=True)

# ============================================================
# MAIN APP
# ============================================================

def main():
    load_tasks()
    initialize_completed_tasks()
    
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
    
    user_info = st.session_state.user_info
    email = st.session_state.user_email
    role = user_info.get("role", "data_analyst")
    
    with st.sidebar:
        st.markdown("## 📋 MahaSTRIDE")
        st.markdown(f"**Welcome, {user_info.get('name')}**")
        if role == "data_analyst":
            st.markdown(f"*Team: {user_info.get('team', 'N/A')}*")
        st.markdown(f"*Role: {role.upper()}*")
        st.markdown("---")
        
        if role == "admin":
            nav_options = ["📊 Dashboard", "👥 Team Performance", "📄 MPR Reports", "📅 Monthly Plan"]
        elif role == "project_lead":
            nav_options = ["📊 Dashboard", "👥 Team Performance", "📄 MPR Reports"]
        else:
            nav_options = ["📝 My Tasks", "📊 My Progress", "📅 Calendar View"]
        
        selected_nav = st.radio("Navigation", nav_options, label_visibility="collapsed")
        
        st.markdown("---")
        st.markdown("### ℹ️ Info")
        st.markdown("**Hours:** 10:00 AM - 6:00 PM")
        st.markdown("**Days:** Monday to Friday")
        st.markdown("**Duration:** 24 months")
        st.markdown("**Status:** ✅ May 4 - June 5, 2026 COMPLETED")
        
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()
    
    if role == "admin":
        if selected_nav == "📊 Dashboard":
            admin_dashboard()
        elif selected_nav == "👥 Team Performance":
            st.markdown("## 👥 Team Performance Analysis")
            progress_df = get_all_analysts_progress()
            fig = px.bar(progress_df, x="team", y="progress", color="team", title="Team-wise Progress", text="progress")
            fig.update_traces(textposition="outside")
            st.plotly_chart(fig, use_container_width=True)
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
            all_tasks = load_tasks()
            for date_str, task in list(all_tasks.items())[:50]:
                st.markdown(f"**{date_str}:** {task['task']}")
    
    elif role == "project_lead":
        if selected_nav == "📊 Dashboard":
            project_lead_dashboard()
        elif selected_nav == "👥 Team Performance":
            st.markdown("## 👥 Team Performance Analysis")
            progress_df = get_all_analysts_progress()
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
    
    else:
        if selected_nav == "📝 My Tasks":
            data_analyst_dashboard(email, user_info)
        elif selected_nav == "📊 My Progress":
            st.markdown(f"## 📊 My Progress - {user_info.get('name')}")
            user_tasks = get_user_tasks(email)
            future_tasks = [t for t in user_tasks if t["date"] > "2026-06-05"]
            completed = sum(1 for t in future_tasks if t["status"] == "Completed")
            total = len(future_tasks)
            st.metric("Progress", f"{(completed/total*100):.1f}%" if total > 0 else "0%")
            st.progress(completed/total if total > 0 else 0)
        elif selected_nav == "📅 Calendar View":
            st.markdown(f"## 📅 Calendar View - {user_info.get('name')}")
            user_tasks = get_user_tasks(email)
            for task in user_tasks:
                if task["date"] > "2026-06-05":
                    status_icon = "✅" if task["status"] == "Completed" else "⏳"
                    st.markdown(f"{status_icon} **{task['date']}** - {task['task'][:80]}")

if __name__ == "__main__":
    main()
